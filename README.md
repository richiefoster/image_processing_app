# image_processing_app

This app will download a zipped imagery folder from S3, unzip the folder, determine if the imagery is aerial or ground, extract the GPS coordinates of each image, create a shapefile of all the imagery, zip the shapefle, upload the shapefile to S3, cleans up everything that was downloaded to the local machine, and finally will send an "end" message to SQS. 

Here is the list of scripts and explainations of what they do:

app.py - the main script that runs all the following scripts in the order described. 

make_dirs.py - creates the directories needed to house the scripts and sets the working directory.

download_images.py - polls SQS for the folder path within S3 and downloads the zipped imagery folder. Once the message is pulled from SQS, the message is deleted to prevent two machines from working on the same circuit. Additionally, this script extracts a couple variables, such as the circuit name and whether the imagery corresponds to air or ground, that will be called in future scripts. These variables are stripped from the folder path in S3 and saved within txt files titled "save_dirs.txt" and "air_or_ground.txt." Finally, it checks to see if a local folder with the circuit name exists, and if not, will create it. This is where the zipped imagery will be extracted to. 

time.sleep(###) - while this command in app.py is not a script, it is important to note that time is needed for the imagery folder to download. More work is needed to determine the ideal amount of time for the script to sleep while the imagery downloads. Currently, this is set to 3 minutes (180 sec). Maybe an extra script can be added here to determine the sleep time based on the size of the imagery folder. 

unzip.py - reads the circuit name from "save_dirs.txt" to find the directory to extract the imagery to, and unzips the imagery to that directory. 

air_or_ground.py - reads which variable has been stored in "air_or_ground.txt" and will return a code based on the variable. Currently, the codes are "AIR" = 10, "GROUND" = 20, and an unknown variable will return an error code of 400, which results in an email being sent to notify me that I need to investigate. This step is essential, as Pentax and DJI store the metadata needed to extract the GPS coordinates in different forms, and will determine which script to use next.

process_images_air.py / process_images_ground.py - while these scripts vary in how they do what they do, the result is the same so they will be grouped together here. Each image is analyzed to find the latitude, longitude, altitude (aerial only), and heading. Once this data has been extracted, it is appended to a pandas dataframe. After all the images data have been appended, the dataframe is converted to a .csv, and then converted to a .shp where it stored in a subdirectory ("/home/ec2-user/CIRCUIT NAME/shp").

zip_shp.py - zips the contents of the directory "/home/ec2-user/CIRCUIT NAME/shp".

upload.py - uploads the zipped shapefile to a folder in S3 titled "processed_shapefiles".

cleanup.py - deletes the directory that was created to house the imagery, as well as the imagery within. Additionally, deletes the files "save_dirs.txt" and "air_or_ground.txt".

send_end_message - sends a message to another SQS queue. This queue has a lambda function that is triggered upon message arrival that will terminate the EC2 instance. 
