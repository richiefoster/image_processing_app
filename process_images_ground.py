
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 09:37:48 2021

@author: Richie Foster
"""

import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from shapely.geometry import Point
import geopandas
import boto3

sqs_client = boto3.client('sqs', region_name='us-east-1')

def main():
    file1 = open('/home/ec2-user/save_dirs.txt', 'r+')
    dir_var = file1.read()
    print(dir_var)   
    df_name = str(dir_var) + str('_dataframe')
    df_name = pd.DataFrame()
    dir_path = '/home/ec2-user/' + str(dir_var) + str('/')
    shp_dir = dir_path + str('shp/')
    exif_table = {}
    for files in os.listdir(dir_path):
        img_path = dir_path + files
        exif_table = {}
        print(img_path)
        image = Image.open(img_path)
        info = image._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_table[decoded] = value
        gps_info = {}
        #things working to this point
        for key in exif_table['GPSInfo'].keys():
            decode = GPSTAGS.get(key,key)
            gps_info[decode] = exif_table['GPSInfo'][key]
        #print(gps_info)
        for key in gps_info:
            lat_ref = gps_info.get("GPSLatitudeRef")
            lat = gps_info.get("GPSLatitude")
            lon_ref = gps_info.get("GPSLongitudeRef")
            lon = gps_info.get("GPSLongitude")
            img_direction_tup = gps_info.get('GPSImgDirection')
            (good_img_dir, dividend) = img_direction_tup
            img_direction = good_img_dir / dividend
            lat = list(lat)
            lon = list(lon)
            lat.append(lat_ref)
            lon.append(lon_ref)
            #lat convert
            lat_deg = lat[0]
            #extract lat deg from tuple
            (my_lat_deg, trash1) = lat_deg
            lat_min = lat[1]
            (lat_x, dividend_x) = lat_min
            lat_min_int = lat_x / dividend_x 
            #back to normal
            lat_ref = lat[3]
            if lat_ref == 'S':
                lat_ref_sign = int(-1)
            else:
                lat_ref_sign = int(1)
            lat_min_new = lat_min_int / 60
            lat_dec = (my_lat_deg + lat_min_new) * lat_ref_sign
            lat_dec = float(lat_dec)
    
            #lon convert
            lon_deg = lon[0]
            #extract lon deg from tuple
            (my_lon_deg, trash2) = lon_deg
            lon_min = lon[1]
            (lon_y, dividend_y) = lon_min
            lon_min_int = lon_y / dividend_y
            #back to normal
            lon_ref = lon[3]
            if lon_ref == 'W':
                lon_ref_sign = int(-1)
            else:
                lon_ref_sign = int(1)
            lon_min_new = lon_min_int / 60
            lon_dec = (my_lon_deg + lon_min_new) * lon_ref_sign
            lon_dec = float(lon_dec)
            #except:
            
        datadict = {
            'Image Name': files,
            'lat': lat_dec,
            'lon': lon_dec,
            'Heading': img_direction
        }
    
        df_name = df_name.append(datadict, ignore_index=True)
    print(df_name)
    csv_name = dir_path + dir_var + str('_gps_data.csv')
    df_name.to_csv(csv_name)
    df_name['geometry'] = df_name.apply(lambda x: Point((float(x.lon), float(x.lat))), axis=1)
    df_geo_name = geopandas.GeoDataFrame(df_name, geometry='geometry')
    os.mkdir(shp_dir)
    shp_path = shp_dir + dir_var + str('.shp')
    df_geo_name.to_file(shp_path, driver='ESRI Shapefile')
    return 200

if __name__ == '__main__':
    main()
    if main() != 200:
        error_response = sqs_client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
                MessageBody='PROCESS IMAGES: process_images.py returned a code other than 200')
