import bcrypt
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')


dynamodb = boto3.resource('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
table = dynamodb.Table('phone-checker')  

def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def create_user(username, password):
    """Create a new user with a hashed password."""
    hashed_password = hash_password(password)
    user_id = str(uuid.uuid4())  
    
    try:
        table.put_item(
            Item={
                'user_id': user_id, 
                'username': username,
                'password': hashed_password,
                'phone_usage_count': 0  
            },
            ConditionExpression='attribute_not_exists(username)'  
        )
        print("User created successfully.")
        return user_id
    except Exception as e:
        print("Error creating user:", e)

def increment_phone_usage(user_id):
    """Increment the phone usage counter for a user."""
    try:
        response = table.update_item(
            Key={
                'user_id': user_id
            },
            UpdateExpression='SET phone_usage_count = phone_usage_count + :val',
            ExpressionAttributeValues={
                ':val': 1
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Phone usage count updated successfully:", response)
    except Exception as e:
        print("Error updating phone usage count:", e)
        
def authenticate_user_and_get_id(username, password):
    response = table.scan(
        FilterExpression=Attr('username').eq(username)
    )
    items = response['Items']
    if items:
        hashed_password = items[0]['password']
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.value):
            return items[0]['user_id']
    return None
