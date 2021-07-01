
import boto3
import os


def main():
    client = boto3.client('sqs', region_name='us-east-1')
    S3 = boto3.resource('s3', region_name='us-east-1')



    response = client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/RF_EC2_queue2',
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5,
        )
    if response is not None:
        print('received resopnse')
    
        raw_res = eval(str(response))
        print(raw_res)
    
        if str('Messages') in response:
            res = response['Messages'][0]['Body']
            res = eval(res)
            print(res)
            file_name = str(res['object'])            
            print(file_name)
            file_name_split = file_name.split('/')
            save_dir = file_name_split[-5]
            air_or_ground = file_name_split[-2]
            print(air_or_ground)
            f = open('/home/ec2-user/save_dirs.txt', 'w')
            f.write(save_dir)
            f.close()
            f2 = open('/home/ec2-user/air_or_ground.txt', 'w')
            f2.write(air_or_ground)
            f2.close()
            check_folder = os.path.isdir('/home/ec2-user/' + save_dir)
            if not check_folder:
                os.makedirs('/home/ec2-user/' + save_dir)
                
                    #file1.write(str_append)
            else:
                pass
            save_name = '/home/ec2-user/' + save_dir + '/' + file_name_split[-1]
            # download file from S3 to EC2
            S3.meta.client.download_file('rf-training-1', file_name, save_name)
            print('Downloading file: ' + str(file_name))
            receipt_handle = str(response['Messages'][-1]['ReceiptHandle'])
            del_response = client.delete_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/RF_EC2_queue2',ReceiptHandle=receipt_handle)
            print('Removing message from queue with id: ' + str(receipt_handle))
            return 200
        else:
            print('response received did not contain a valid payload')
            error_response1 = client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
                MessageBody='DOWNLOAD IMAGES: response received did not contain a valid payload')
            return 0
    else:
        print('no response received. script will now terminate.')
        error_response2 = client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/637137674144/rf_ec2_errors',
                MessageBody='DOWNLOAD IMAGES: no response received')
        return 0
    

    print('script has ended.')

if __name__ == '__main__':
    main()

