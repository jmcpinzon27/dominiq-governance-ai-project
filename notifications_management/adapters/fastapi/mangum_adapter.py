import json
import os
import uuid
import requests
import smtplib

import boto3
from fastapi import FastAPI
from google.cloud import firestore, storage
from mangum import Mangum

app = FastAPI()

# Initialize a session
dynamodb = boto3.resource('dynamodb')
db = firestore.Client()

# Function to send emails
def send_email(to, subject, text):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASSWORD']

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        message = f'Subject: {subject}\n\n{text}'
        server.sendmail(sender, to, message)

# Function to remove undefined keys from a dictionary
def remove_undefined_fields(data):
    return {k: v for k, v in data.items() if v is not None}

# Main function for the Cloud Function
@app.route('/send_email_function', methods=['GET', 'POST'])
def send_email_function(request):
    if request.method == 'OPTIONS':
        return '', 204

    try:
        # Get the data from the request body
        data = request.json
        industry = data.get('industry')
        domain = data.get('domain')
        subdomain = data.get('subdomain')
        responsible = data.get('responsible')
        email = data.get('email')

        # Create a registration data object
        registration_data = {
            'industry': industry,
            'domain': domain,
            'subdomain': subdomain,
            'responsible': responsible,
            'email': email
        }

        # Clean up the data
        cleaned_data = remove_undefined_fields(registration_data)

        # Save to Firestore
        db.collection('registrations').add(cleaned_data)
        # Get the table
        table = dynamodb.Table('registrations')
        table.put_item(cleaned_data)

        # Send email
        email_text = (
            f'Saludos {responsible},\n\n'
            f'Usted ha sido registrado en DominiQ como encargado del subdominio {subdomain}, '
            f'perteneciente al dominio {domain} en la industria {industry}. '
            f'Puede comunicarse con nuestro asistente IA dando clic en el siguiente link '
            f'para una experiencia óptima: '
            f'http://localhost:5173/dominiQ?email={email}'
        )
        send_email(email, 'Registro en DominiQ', email_text)

        # Successful response
        return jsonify({'message': 'Datos guardados y correo enviado'}), 200
    except Exception as error:
        print(f'Error: {error}')
        return {'message': 'Error al guardar los datos o enviar el correo'}, 500

if __name__ == '__main__':
    app.run(debug=True)
