import os
import boto3

ses = boto3.client('ses', region_name=os.environ.get('SES_REGION', 'eu-west-1'))


def send_invite_email(to_address: str, link: str):
    ses.send_email(
        Source=os.environ.get('SES_SENDER', 'no-reply@tuempresa.com'),
        Destination={'ToAddresses': [to_address]},
        Message={
            'Subject': {'Data': 'Invitación al cuestionario de madurez'},
            'Body': {
                'Html': {
                    'Data': f"""
                        <p>Hola,</p>
                        <p>Haz clic <a href=\"{link}\">aquí</a> para comenzar el cuestionario.</p>
                        <p>Gracias.</p>
                    """
                }
            }
        }
    )