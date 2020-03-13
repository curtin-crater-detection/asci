import arcpy
from test import hello

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "CDA Tools"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [SecondaryCraterRemovalTool]


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


        # @TODO: output params?
        # param2 = arcpy.Parameter(
        #     displayName="Output Features",
        #     name="out_features",
        #     datatype="GPFeatureLayer",
        #     parameterType="Derived",
        #     direction="Output")

        # param2.parameterDependencies = [param0.name]
        # param2.schema.clone = True

        params = [param0, param1]

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
        arcpy.AddMessage("Name is: {0}".format(hello()))
        crater_detection_layer = parameters[0].value

        thiessen_fc = "./thiessen_temp.shp"
        arcpy.Delete_management(thiessen_fc)

        # thiessen_fc = arcpy.CreateFeatureclass_management( ".", "thiessen_tmp.shp", "POLYGON", None, 
        #                             "DISABLED", "DISABLED", None)

        result = arcpy.CreateThiessenPolygons_analysis(in_features=crater_detection_layer,out_feature_class=thiessen_fc,fields_to_copy="ALL")
        arcpy.AddField_management(thiessen_fc, "area", "FLOAT")

        mxd = arcpy.mapping.MapDocument("CURRENT")  
        df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  
        addLayer = arcpy.mapping.Layer(thiessen_fc)
        arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")  
        arcpy.RefreshActiveView()  
        arcpy.RefreshTOC()

        # arcpy.AddGeometryAttributes_management(thiessen_fc,"AREA_GEODESIC", Area_Unit="SQUARE_KILOMETERS")
        arcpy.CalculateField_management(thiessen_fc,"area", "!shape.area@squarekilometers!", "PYTHON_9.3")
        # arcpy.CalculateAreas_stats(thiessen_fc,"AREA_GEODESIC", Area_Unit="SQUARE_KILOMETERS")

        arcpy.AddMessage("thiessen layer: {0}".format(type(result)))



        return
