import boto3
import os

sqs_client = boto3.client('sqs', region_name='us-east-1')

def main():
    f = open('/home/ec2-user/save_dirs.txt', 'r')
    dir_name = f.read()
    f1 = open('/home/ec2-user/air_or_ground.txt', 'r')
    air_or_ground = f1.read()
    target_path = str('/home/ec2-user/')
    client = boto3.client('s3')
    s3 = boto3.resource('s3')
    if str('Ground') in air_or_ground or str('ground') in air_or_ground:
        air_or_ground = str('GROUND')
    else:
        air_or_ground = str('AIR')
    key_dir = str('processed_shapefiles/') + air_or_ground + str('/')  + dir_name
    key = key_dir +  str('.zip')
    #make_folder = client.put_object(
           # Bucket='rf-training-1',
           # Key=dir_name
           # )
    for files in os.listdir(target_path):
        if files.endswith('.zip'):
            zip_key = str('/home/ec2-user/') + files
            s3.meta.client.upload_file(zip_key, 'rf-training-1', key)
    f.close()
    return 200

if __name__ == '__main__':
    main()
    if main() != 200:
        error_response = sqs_client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
                MessageBody='UNZIP: unzip.py returned a code other than 200')

