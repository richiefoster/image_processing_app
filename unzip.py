import os
import shutil
import boto3


sqs_client = boto3.client('sqs', region_name='us-east-1')
def main():
    f = open('/home/ec2-user/save_dirs.txt', 'r')
    dir_name = f.read()
    print(dir_name)
    target_dir = str('/home/ec2-user/') + dir_name
    for file in os.listdir(target_dir):
        if file.endswith('.zip'):
            target_zip = file
            print(target_zip)
            target_path = target_dir + str('/') + target_zip
            shutil.unpack_archive(target_path, target_dir)
            os.remove(target_path)
        else:
            pass
    f.close()
    return 200

if __name__ == '__main__':
    main()
    if main() != 200:
        error_response = sqs_client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
                MessageBody='UNZIP: unzip.py returned a code other than 200')

