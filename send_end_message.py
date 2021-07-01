import boto3

sqs_client = boto3.client('sqs', region_name='us-east-1')

def main():    
    client = boto3.client('sqs', region_name='us-east-1')

    response = client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/RF_EC2_queue',
        MessageBody='terminate instance')
    return 200

if __name__ == '__main__':
    main()
    if main() != 200:
        error_response = sqs_client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
                MessageBody='SEND END MESSAGE: send_end_message.py returned a code other than 200')