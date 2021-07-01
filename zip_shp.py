import os
import shutil
import boto3

sqs_client = boto3.client('sqs', region_name='us-east-1')

def main():
    f = open('/home/ec2-user/save_dirs.txt', 'r')
    dir_name = f.read()
    zip_from = str('/home/ec2-user/') + dir_name + str('/shp/')
    zip_to = str('/home/ec2-user/') + dir_name
    shutil.make_archive(zip_to, 'zip', zip_from)
    f.close()
    return 200

if __name__ == '__main__':
    main()
    if main() != 200:
        error_response = sqs_client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
                MessageBody='ZIP: zip.py returned a code other than 200')