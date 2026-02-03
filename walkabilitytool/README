Walkability Tool 


Purpose 
The purpose of this tool is to evaluate the walkability around schools. It creates buffer zones at 5, 10, and 25 minute walking distances from schools, then assigns a walkability score to parcels based on their proximity to a school. This tool is meant to help urban planners, school districts, and families make informed choices about where to build schools/neighborhoods, how to adjust bus routes, and where to live in relationship to a school. 


Data Inputs 

1. Schools layer 
Type: Point feature class. 
Format: .shp or feature class inside a .gdb 
Attribute requirements: None. 

2. Parcels layer 
Type: Polygon feature class. 
Format: .shp or feature class inside a .gdb 
Attribute requirements: Must include fields PARCEL\_ID, PARCEL\_ADD, PARCEL\_CIT, PARCEL\_ZIP to generate the final CSV output. 

3. Output geodatabase 
Type: File geodatabase. 
Format: .gdb 
Description: Destination for all intermediate and final feature classes, including buffers and parcels with walkability scores. 

4. Walking speed 
Type: Float. 
Description: Walking speed in meters per minute. Used to convert walking times into buffer distances. The average walking speed for adults is 78 to 84 meters per second. 

5. Output CSV folder 
Type: Folder path. 
Description: Location where the final CSV table with walkability scores will be saved. 


Data Outputs 

1. Buffer feature classes 
Names: walk\_5min, walk\_10min, walk\_15min 
Location: Output geodatabase. 
Description: Each buffer represents the parcels that are within a 5, 10, and 15 minute walk of the school. 
The messages "created buffer for 5 min: (output path), created buffer for 10 min: (output path), and created buffer for 15 min: (output path)" will appear in the messages as the tool runs. 

2. Parcel feature class copy 
Name: parcels\_copy Location: Output geodatabase. 
Description: A working copy of the parcels layer used to calculate and store the walkability scores. 
The messages "created copy of (original parcels data): (parcels\_copy file path) and new field 'WalkScore' added to: (parcels\_copy file path)" will appear in the messages as the tool runs. 

3. Final parcels with walkability score 
Name: parcels\_with\_walkscore 
Location: Output geodatabase. 
Decription: The original parcels with a new WalkScore field, where scores are: 0 = not within a 15 minute walk of a school 1 = within a 5 minute walk of a school 2 = within a 10 minute walk of a school 3 = within a 15 minute walk of a school 
The message "walkability scoring complete for all parcels. final walkability output created: (output path)" will appear in the messages as the tool runs. 

4. CSV output 
Name: WalkabilityScores.csv 
Location: Output CSV folder 
Description: Contains the parcel attributes along with the assigned walkability scores. 
The message "csv file created: (output file path) this tool is now finished!" will appear once the tool succesfully runs. 


Requirements 
Required python libraries 
arcpy 
os 
csv 

Expected folder structure 
project\_folder/ input\_data/ schools.shp parcels.shp output\_gdb/ output\_csv/ 


Troubleshooting 
Common errors 
Field not found: Make sure that your parcels layer includes PARCEL\_ID, PARCEL\_ADD, PARCEL\_CIT, and PARCEL\_ZIP fields. 

Tips 
Make sure that all input layers are project in the same coordinate system to get accurate buffer distances. 
If walkability scores do not seem correct, be sure to verify the walking speed value. Credits 



Developed by Alyssa Alder for GEOG3700 final project at USU
