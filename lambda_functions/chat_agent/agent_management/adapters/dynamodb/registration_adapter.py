import logging
import os

import boto3

from domain.command.registration_command import GetUser, RegistrationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a session using your AWS credentials
session = boto3.Session() 
dynamodb = session.resource('dynamodb')

# Specify the table name
get_registration_table = lambda: dynamodb.Table('dominiq_registrations')


async def get_registration_by_attrs(rergistration): #GetUser) -> RegistrationResponse|None:
    attrs = rergistration.model_dump(exclude_none=True)
    try:
        # Fetch the item using the primary key
        response = get_registration_table().get_item(Key=attrs)
        # Check if the item was found in the response
        if 'Item' in response:
            logger.info("Record found: %s", response['Item'])
            return RegistrationResponse(**response['Item'])
        else:
            logger.warning("No record found with registration attrs: %s", attrs)
            return None

    except Exception as e:
        logger.error("Error fetching record: %s", e)
        return None
