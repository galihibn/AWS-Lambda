from __future__ import print_function
from botocore.exceptions import ClientError
import boto3
import json
import os

def handler(event, context):
    try:
        # Initialize EC2 client
        ec2 = boto3.client('ec2')
        
        # Retrieve the instance ID from environment variables
        instanceID = os.environ.get('INSTANCE_ID')
        if not instanceID:
            raise ValueError("Missing environment variable 'INSTANCE_ID'")
        
        # Attempt to stop the EC2 instance
        response = ec2.stop_instances(
            InstanceIds=[instanceID],
        )
        
        # Log the essential parts of the response
        stopping_instance = response.get('StoppingInstances', [])
        print(f"Stopping Instances Response: {json.dumps(stopping_instance)}")
        
    except ClientError as e:
        # Log the AWS ClientError
        error_message = f"ClientError: {e.response['Error']['Message']}"
        print(error_message)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }
    except ValueError as e:
        # Log the ValueError
        error_message = str(e)
        print(error_message)
        return {
            'statusCode': 400,
            'body': json.dumps({'error': error_message})
        }
    except Exception as e:
        # Log any other exceptions
        error_message = f"Exception: {str(e)}"
        print(error_message)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }
    
    # Return a success response with essential information
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Instance stopping initiated', 'response': stopping_instance})
    }

