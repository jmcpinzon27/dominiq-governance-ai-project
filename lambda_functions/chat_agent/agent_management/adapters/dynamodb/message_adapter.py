import logging

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# TODO: not in use
# from domain.command.message_command import Message, GetListMessages, ListMessages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a session using your AWS credentials
session = boto3.Session() 
dynamodb = session.resource('dynamodb')
get_messages_table = lambda: dynamodb.Table('dominiq_message')


async def get_mesasge_by_attrs(data): #Message):
    attrs = data.model_dump(exclude_none=True)
    try:
        # Fetch the item using the primary key
        response = get_messages_table().get_item(Key=attrs)
        # Check if the item was found in the response
        if 'Item' in response:
            logger.info("Record found: %s", response['Item'])
            return response['Item']
        else:
            logger.warning("No record found with registration attrs: %s", attrs)
    except ClientError as e:
        logger.error("Error fetching record: %s", e)


async def get_list_mesasge_by_attrs(data): #: GetListMessages):
    attrs = {}
    for i in data.params:
        if i.attr in ('session_id'):
            attrs['KeyConditionExpression'] = getattr(Key(i.attr), i.op)(i.value)
        else:
            attrs['FilterExpression'] = getattr(Key(i.attr), i.op)(i.value)
    try:
        # Fetch the item using the primary key
        response = get_messages_table().query(**attrs)
        # Check if the item was found in the response
        if 'Items' in response:
            logger.info("Record found: %s", response['Items'])
            return ListMessages(response['Items'])
        else:
            logger.warning("No record found with registration attrs: %s", attrs)
    except ClientError as e:
        logger.error("Error fetching record: %s", e)


async def create_message(data): # Message):
    attrs = data.model_dump(exclude_none=True)
    try:
        # Insert the record into the table
        response = get_messages_table.put_item(
            Item=attrs
        )
        logger.warning("No record found with registration attrs: %s", attrs)
    except ClientError as e:
        logger.error("Error fetching record: %s", e.response['Error']['Message'])
