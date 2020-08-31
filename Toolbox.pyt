import arcpy
import pandas as pd
import scia_utils
import os

# uncomment for testing
reload(scia_utils)

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "CDA Tools"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [SecondaryCraterRemovalTool]


def arcgis_table_to_dataframe(in_fc, input_fields=None, query="", skip_nulls=False, null_values=None):
    """Function will convert an arcgis table into a pandas dataframe with an object ID index, and the selected
    input fields. Uses TableToNumPyArray to get initial data.
    :param - in_fc - input feature class or table to convert
    :param - input_fields - fields to input into a da numpy converter function
    :param - query - sql like query to filter out records returned
    :param - skip_nulls - skip rows with null values
    :param - null_values - values to replace null values with.
    :returns - pandas dataframe"""
    OIDFieldName = arcpy.Describe(in_fc).OIDFieldName
    if input_fields:
        final_fields = [OIDFieldName] + input_fields
    else:
        final_fields = [field.name for field in arcpy.ListFields(in_fc)]
    np_array = arcpy.da.TableToNumPyArray(in_fc, final_fields, query, skip_nulls, null_values)
    object_id_index = np_array[OIDFieldName]
    fc_dataframe = pd.DataFrame(np_array, index=object_id_index, columns=input_fields)
    return fc_dataframe

def add_layer_to_view(layer, order="BOTTOM"):
    mxd = arcpy.mapping.MapDocument("CURRENT")  
    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  
    addLayer = arcpy.mapping.Layer(layer)
    arcpy.mapping.AddLayer(df, addLayer, order)
    arcpy.RefreshActiveView()  
    arcpy.RefreshTOC()

def get_counting_area_size(counting_area_layer, area_feature_name):
    cursor = arcpy.SearchCursor(counting_area_layer)
    row = next(cursor)
    area = row.getValue(area_feature_name)
    return area

def get_pairs(my_list):
    """
    Returns a set of pairs from a list

    eg if the list is [1, 2, 3] returns [(1, 2), (2, 3)]
    """
    return  [(current, my_list[idx + 1] if  - 1 else None) for idx, current in enumerate(my_list) if idx < len(my_list) - 1]


def get_diam_comparison_statement(min_diam, max_diam):
    """
    Returns a formatted ArcMap SQL statement to select area based on a min and a max.
    Handles the case where max_diam == float("inf").
    """
    if max_diam < float("inf"):
        return '"diameter" >= {} AND "diameter" < {}'.format(min_diam, max_diam)
    else:
        return '"diameter" >= {}'.format(min_diam)

class SecondaryCraterRemovalTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Secondary Crater Removal"
        self.description = "Removes Secondary Craters from a CDA analysis"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        param0 = arcpy.Parameter(
            displayName="Crater detection layer",
            name="crater_detection_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Counting area layer",
            name="counting_area_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="Output folder",
            name="output_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        param3 = arcpy.Parameter(
            displayName="Crater detection layer latitude feature name",
            name="lat_feature_name",
            datatype="GPString",
            direction="Input"
        )

        param3.value = "latitude"

        param4 = arcpy.Parameter(
            displayName="Crater detection layer longitude feature name",
            name="lon_feature_name",
            datatype="GPString",
            direction="Input"
        )

        param4.value = "longitude"

        param5 = arcpy.Parameter(
            displayName="Counting area layer area feature name",
            name="area_feature_name",
            datatype="GPString",
            direction="Input"
        )

        param5.value = "Area"

        param6 = arcpy.Parameter(
            displayName="Number of simulation iterations",
            name="simulation_iterations",
            datatype="GPLong",
            direction="Input"
        )

        # 300 simulation iterations by default
        param6.value = 300

        param7 = arcpy.Parameter(
            displayName="Use diameter binning",
            name="use_diam_binning",
            datatype="GPBoolean",
            direction="Input"
        )

        param7.value = True

        param8 = arcpy.Parameter(
            displayName="Show debug output",
            name="debug",
            datatype="GPBoolean",
            direction="Input"
        )

        param8.value = False

        param2.filter.list = ["File System"]


        params = [param0, param1, param2, param3, param4, param5, param6, param7, param8]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        crater_detection_layer = parameters[0].value
        counting_area_layer = parameters[1].value
        lat_feature_name = parameters[3].valueAsText
        lon_feature_name = parameters[4].valueAsText
        area_feature_name = parameters[5].valueAsText
        simulation_iterations = parameters[6].value
        BASE_FOLDER = parameters[2].valueAsText
        use_diam_binning = parameters[7].value
        debug = parameters[8].value

        arcpy.AddMessage("BASE_FOLDER: {0}".format(BASE_FOLDER))

        if(use_diam_binning):
            diameter_bins = [0, 88, 125, 177, 250, 354, 500, 707, 1000, 1410, 2000, float("inf")]
        else:
            diameter_bins = [0, float("inf")]

        # clear any existing selections
        arcpy.SelectLayerByAttribute_management(crater_detection_layer, "CLEAR_SELECTION") 

        for min_diam, max_diam in get_pairs(diameter_bins):

            thiessen_fc = os.path.join(BASE_FOLDER, "thiessen_temp_{}.shp".format(min_diam))
            arcpy.Delete_management(thiessen_fc)

            craters_within_diam_range = os.path.join(BASE_FOLDER, "input_craters_{}.shp".format(min_diam))
            arcpy.Delete_management(craters_within_diam_range)

            # select craters within the diameter range
            arcpy.Select_analysis(crater_detection_layer, craters_within_diam_range, get_diam_comparison_statement(min_diam, max_diam))

            crater_count = int(str(arcpy.GetCount_management(craters_within_diam_range)))

            arcpy.AddMessage("{} craters in the range [{}, {}]".format(crater_count, min_diam, max_diam))

            # if there are 10 or less craters, all of them are primary
            if crater_count <= 10 and crater_count > 0:
                primary_craters = os.path.join(BASE_FOLDER, "output_primary_craters_{}.shp".format(min_diam))
                arcpy.Delete_management(primary_craters)
                arcpy.CopyFeatures_management(craters_within_diam_range, primary_craters)

                add_layer_to_view(primary_craters, order="TOP")
            elif crater_count > 10:
                result = arcpy.CreateThiessenPolygons_analysis(in_features=craters_within_diam_range,out_feature_class=thiessen_fc,fields_to_copy="ALL")
                arcpy.AddField_management(thiessen_fc, "area", "FLOAT")

                add_layer_to_view(thiessen_fc)
                add_layer_to_view(craters_within_diam_range)

                arcpy.CalculateField_management(thiessen_fc,"area", "!shape.area@squarekilometers!", "PYTHON_9.3")

                arcpy.AddMessage("thiessen layer: {0}".format(type(result)))

                df = arcgis_table_to_dataframe(thiessen_fc, [lat_feature_name, lon_feature_name, 'area'])
                arcpy.AddMessage(str(df))

                counting_area_size = get_counting_area_size(counting_area_layer, area_feature_name)

                arcpy.AddMessage("counting area size: {}".format(counting_area_size))

                threshold_area = scia_utils.simulate_crater_populations(df, counting_area_size, simulation_iterations, debug)

                arcpy.AddMessage("threshold_area: {}".format(threshold_area))

                primary_area = os.path.join(BASE_FOLDER, "output_primary_area_{}.shp".format(min_diam))
                secondary_area = os.path.join(BASE_FOLDER, "output_secondary_area_{}.shp".format(min_diam))
                arcpy.Delete_management(primary_area)
                arcpy.Delete_management(secondary_area)

                arcpy.Select_analysis(thiessen_fc, primary_area, '"area" > {}'.format(threshold_area))
                arcpy.Select_analysis(thiessen_fc, secondary_area, '"area" <= {}'.format(threshold_area))

                add_layer_to_view(primary_area)
                add_layer_to_view(secondary_area)

                primary_craters = os.path.join(BASE_FOLDER, "output_primary_craters_{}.shp".format(min_diam))
                arcpy.Delete_management(primary_craters)
                selection = arcpy.SelectLayerByLocation_management(craters_within_diam_range, "WITHIN", primary_area)
                arcpy.CopyFeatures_management(selection, primary_craters)

                add_layer_to_view(primary_craters, order="TOP")

                secondary_craters = os.path.join(BASE_FOLDER, "output_secondary_craters_{}.shp".format(min_diam))
                arcpy.Delete_management(secondary_craters)
                secondary_selection = arcpy.SelectLayerByLocation_management(craters_within_diam_range, "WITHIN", secondary_area)
                arcpy.CopyFeatures_management(secondary_selection, secondary_craters)

                add_layer_to_view(secondary_craters, order="TOP")
