import os
import shutil
import boto3

sqs_client = boto3.client('sqs', region_name='us-east-1')
def main():
    f = open('/home/ec2-user/save_dirs.txt', 'r+')
    delete_name = f.read()
    for files in os.listdir('/home/ec2-user/'):
        if files.startswith(delete_name):
            path = str('/home/ec2-user/') + files
            try:
                shutil.rmtree(path)
            except:
                os.remove(path)
    f.close()
    os.remove('/home/ec2-user/save_dirs.txt')
    os.remove('/home/ec2-user/air_or_ground.txt')
    return 200

if __name__ == '__main__':
    main()
    if main() != 200:
        error_response = sqs_client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
                MessageBody='CLEANUP: cleanup.py returned a code other than 200')
