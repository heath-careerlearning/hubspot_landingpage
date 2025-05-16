import os
import yaml
import requests
from datetime import datetime, timedelta
import json

def get_hubspot_token(portal_name='EmailReportingAccess'):
    """Get HubSpot access token and portal ID from config for specified portal."""
    try:
        # Read the local hubspot.config.yml file
        config_path = os.path.join(os.path.dirname(__file__), 'hubspot.config.yml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Get the portal configuration
        portals = config.get('portals', [])
        portal_config = next((p for p in portals if p.get('name') == portal_name), None)
        if not portal_config:
            raise ValueError(f"Portal configuration not found for {portal_name}")
            
        # Get the access token from auth.tokenInfo
        auth_config = portal_config.get('auth', {}).get('tokenInfo', {})
        access_token = auth_config.get('accessToken')
        if not access_token:
            raise ValueError(f"No access token found for portal {portal_name}")
            
        return access_token, portal_config.get('portalId')
    except Exception as e:
        raise ValueError(f"Error getting HubSpot token: {str(e)}")

def get_email_details(email_id, access_token):
    """Get email details using the documented endpoint."""
    url = f'https://api.hubapi.com/marketing/v3/emails/{email_id}'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting email details: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error getting email details: {e}")
        return None

def get_email_statistics(email_id, access_token, sent_timestamp=None):
    """Get statistics for a specific email using the documented endpoint."""
    url = "https://api.hubapi.com/marketing/v3/emails/statistics/list"
    
    # If we have a sent timestamp, use it to set the time range
    if sent_timestamp:
        # Convert to datetime if it's a string
        if isinstance(sent_timestamp, str):
            sent_time = datetime.fromisoformat(sent_timestamp.replace('Z', '+00:00'))
        else:
            sent_time = sent_timestamp
            
        # Set the time range to cover 180 days from when the email was sent
        start_time = sent_time
        end_time = sent_time + timedelta(days=180)
    else:
        # Default to last 180 days if no timestamp provided
        end_time = datetime.now()
        start_time = end_time - timedelta(days=180)
    
    params = {
        "startTimestamp": start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        "endTimestamp": end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        "emailIds": str(email_id)
    }
    
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting email statistics: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error getting email statistics: {e}")
        return None

def create_email(access_token, business_unit_id, email_data):
    """Create an email in HubSpot."""
    url = 'https://api.hubapi.com/marketing/v3/emails'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Ensure required fields
    email_data.update({
        "type": "MARKETING_EMAIL",
        "status": "DRAFT",
        "businessUnitId": business_unit_id
    })
    
    try:
        response = requests.post(url, headers=headers, json=email_data)
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Error creating email: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error creating email: {e}")
        return None 