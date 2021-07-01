from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pandas as pd
import os
from shapely.geometry import Point
import geopandas
import boto3

sqs_client = boto3.client('sqs', region_name ='us-east-1')

def main():
    file1 = open('/home/ec2-user/save_dirs.txt', 'r+')
    dir_var = file1.read()
    print(dir_var)
    df_name = str(dir_var) + str('_dataframe')
    df_name = pd.DataFrame()
    dir_path = '/home/ec2-user/' + str(dir_var) + str('/')
    shp_dir = dir_path + str('shp/')
    print('shp dir created at : ' + shp_dir)
    exif_table = {}
    for files in os.listdir(dir_path):
        img_path = dir_path + files
        exif_table = {}
        print(img_path)        
        with Image.open(img_path) as im:
            for segment, content in im.applist:
                marker, body = content.rsplit(b'\x00', 1)
                if segment == 'APP1' and marker == b'http://ns.adobe.com/xap/1.0/':
                    body = str(body)
                    alt_str = 'RelativeAltitude'
                    yaw_str = 'GimbalYawDegree'
                    for line in body.split('\\n'):
                        if alt_str in line:
                            new_line = line.strip()
                            final_alt_str = new_line.strip('drone-dji:RelativeAltitude="+')
                        elif yaw_str in line:
                            new_line = line.strip()
                            final_yaw_str = new_line.strip('drone-dji:GimbalYawDegree="')
                            final_yaw_str = str(final_yaw_str)
                            if str('+') in final_yaw_str:
                                final_yaw_str = float(final_yaw_str)
                            else:
                                final_yaw_str = str('-') + final_yaw_str
                                final_yaw_str = float(final_yaw_str)
                        else:
                            pass
                        
        exif_table = {}
        image = Image.open(img_path)
        info = image.getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_table[decoded] = value
        gps_info = {}
        for key in exif_table['GPSInfo'].keys():
            decode = GPSTAGS.get(key,key)
            gps_info[decode] = exif_table['GPSInfo'][key]
        for key in gps_info:
            lat_ref = gps_info.get("GPSLatitudeRef")
            lat = gps_info.get("GPSLatitude")
            lon_ref = gps_info.get("GPSLongitudeRef")
            lon = gps_info.get("GPSLongitude")
            lat = list(lat)
            lon = list(lon)
            lat.append(lat_ref)
            lon.append(lon_ref)
            #lat convert
            lat_deg = lat[0]
            lat_min = lat[1]
            lat_sec = lat[2]
            lat_ref = lat[3]
            if lat_ref == 'S':
                lat_ref_sign = -1
            else:
                lat_ref_sign = 1  
            lat_min_new = lat_min / 60
            lat_sec_new = lat_sec / 3600
            lat_min_fin = lat_min_new + lat_sec_new
            lat_dec = (lat_deg + lat_min_fin) * lat_ref_sign
            lat_dec = float(lat_dec)
            
            #lon convert
            lon_deg = lon[0]
            lon_min = lon[1]
            lon_sec = lon[2]
            lon_ref = lon[3]
            if lon_ref == 'W':
                lon_ref_sign = -1
            else:
                lon_ref_sign = 1  
            lon_min_new = lon_min / 60
            lon_sec_new = lon_sec / 3600
            lon_min_fin = lon_min_new + lon_sec_new
            lon_dec = (lon_deg + lon_min_fin) * lon_ref_sign
            lon_dec = float(lon_dec)

        datadict = {
            'Image Name': files, 
            'lat': lat_dec,
            'lon': lon_dec,
            'Heading': final_yaw_str,
            'Altitude': final_alt_str
        }
        print(datadict)
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

if __name__ == "__main__":
    main()
