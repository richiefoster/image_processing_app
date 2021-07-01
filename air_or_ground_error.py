import boto3

def main():
    sqs_client = boto3.client('sqs', region_name='us-east-1')
    error_response = sqs_client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
        MessageBody='AIR/GROUND: air_or_ground.py returned a value other than "air" or "ground"')

if __name__ == '__main__':
    main()
