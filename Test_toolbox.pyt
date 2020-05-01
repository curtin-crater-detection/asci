import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Test Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [TestTool]



class TestTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Test Tool"
        self.description = "Check if install works properly"
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
        return
