# import modules
import arcpy
import os
import csv

# establish input and output variables
schools = arcpy.GetParameterAsText(0)
parcels = arcpy.GetParameterAsText(1)
output_gdb = arcpy.GetParameterAsText(2)
walking_speed = float(arcpy.GetParameterAsText(3))
output_csv_folder = arcpy.GetParameterAsText(4)

# set overwrite and workspace
arcpy.env.overwriteOutput = True

# establsih walk times list (minutes) and walking speed (m/min) as variables
walk_times = [5, 10, 15]

# create an empty list to store the output buffer layers
buffer_fcs = []

# loop through walk times and create a new buffer for each
for minutes in walk_times:
    distance_meters = minutes * walking_speed # convert walking minutes into distance (m)
    out_fc = os.path.join(output_gdb, f"walk_{minutes}min") # create an output path

    # run the buffer tool
    arcpy.analysis.Buffer(
    in_features = schools, 
    out_feature_class = out_fc, 
    buffer_distance_or_field = f"{distance_meters} meters", 
    dissolve_option = "ALL") # this will have all buffers be desolved into a single feature

    # add buffer information to the empty list
    buffer_fcs.append((minutes, out_fc))

    # show message so you know where the tool is in the process
    arcpy.AddMessage(f"created buffer for {minutes} min: {out_fc}") # visible in tool window
    print(f"created buffer for {minutes} min: {out_fc}") # visible in notebook

# prep parcel data to be able to assign walkability score in the future

# tell ArcGIS where to save the new feature class
parcels_copy = os.path.join(output_gdb, "parcels_copy") 

# takes the original parcels data, makes a copy, and then saves inside the geodatabase
arcpy.management.CopyFeatures(
    in_features = parcels, 
    out_feature_class = parcels_copy)

# show message so you know where the tool is in the process
arcpy.AddMessage(f"created copy of {parcels} data: {parcels_copy}") # visible in tool window
print(f"created copy of parcels data: {parcels_copy}") # visible in notebook

# create the walkability field

# get all fields in the parcels_copy
fields = arcpy.ListFields(parcels_copy)

# make a list of the field names
field_names = [field.name for field in fields]

# if WalkScore does not exsist as a field, add it
if "WalkScore" not in field_names:
    arcpy.management.AddField(
        in_table = parcels_copy,
        field_name = "WalkScore",
        field_type = "SHORT")

# show message so you know where the tool is in the process
arcpy.AddMessage(f"new field 'WalkScore' added to: {parcels_copy}") # visible in tool window
print(f"new field 'WalkScore' added to: {parcels_copy}") # visible in notebook

# assign walkability scores

# set all of the walkabilitiy scores to 0
arcpy.management.CalculateField(
    in_table = parcels_copy,
    field = "WalkScore",
    expression = 0,
    expression_type = "PYTHON3")

# define the score system
scores = { 5:1, 10:2, 15:3}

# loop through each buffer to assign walkability score
for minutes, buffer in sorted(buffer_fcs, reverse = True): # reverse so that you end up with 0, 1, 2, and 3 for scores not just 0 and 3

    # make a temporary layer to select features from
    select = "temp_select"
    arcpy.management.MakeFeatureLayer(
        in_features = parcels_copy, 
        out_layer = select)

    # select parcels that intersect the current buffer
    arcpy.management.SelectLayerByLocation(
        in_layer = select,
        overlap_type = "INTERSECT",
        select_features = buffer)
    
    # use the score system
    score = scores.get(minutes, 0)

    # updated WalkScore only for selected parcels
    arcpy.management.CalculateField(
        in_table = select,
        field = "WalkScore",
        expression = f"{score}",
        expression_type = "PYTHON3")

    # remove the temporary layer
    arcpy.management.Delete(select)

# show message so you know where the tool is in the process
arcpy.AddMessage("walkability scoring complete for all parcels") # visible in tool window
print("walkability scoring complete for all parcels") # visible in notebook

# create final output to show which parcels are assigned which walkability score

# name and save the final output feature class
final_output = os.path.join(output_gdb, "parcels_with_walkscore")

# copy the parcels_copy
arcpy.management.CopyFeatures(
    in_features = parcels_copy,
    out_feature_class = final_output)

# show message so you know where the tool is in the process
arcpy.AddMessage(f"final walkability output created: {final_output}") # visitble in tool window
print(f"final walkability output created: {final_output}") # visible in notebook

# create a csv file from the final output

# set a variable to save to an output folder
output_folder = output_csv_folder

# define the fields you want to keep in the csv
fields_to_keep = ["PARCEL_ID", "PARCEL_ADD", "PARCEL_CIT", "PARCEL_ZIP", "WalkScore"]

# create an empty container to hold only the fields you need/want
field_mappings = arcpy.FieldMappings()

# loop though fields and add them
for field in fields_to_keep:
    fm = arcpy.FieldMap()
    fm.addInputField(final_output, field)
    field_mappings.addFieldMap(fm)

# name and save the csv file
csv_output = os.path.join(output_folder, "WalkabilityScores.csv")

# ensure the output folder exists
if not os.path.exists(output_csv_folder):
    os.makedirs(output_csv_folder)

# remove the CSV if it already exists
if os.path.exists(csv_output):
    os.remove(csv_output)

# export the final output as a csv
arcpy.conversion.ExportTable(
    in_table = final_output,
    out_table = csv_output,
    field_mapping = field_mappings)

# show message so you know that the tool is finished
arcpy.AddMessage(f"csv file created: {csv_output}. this tool is now finished!")
print(f"csv file created: {csv_output}. this tool is now finished!")


