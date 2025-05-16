import os
from dotenv import load_dotenv
import requests
from pprint import pprint
import json
from hubspot_utils import get_hubspot_token

# Load environment variables
load_dotenv()

def get_marketing_events(access_token, portal_id, limit=100):
    """Get marketing events using the direct API endpoint."""
    url = 'https://api.hubapi.com/marketing/v3/marketing-events/'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    params = {
        'limit': limit,
        'portalId': portal_id
    }
    
    all_events = []
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                all_events.extend(data['results'])
                
                # Check if there's a next page
                if 'paging' in data and 'next' in data['paging']:
                    params['after'] = data['paging']['next']['after']
                else:
                    break
            else:
                print(f"Error getting marketing events: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"Error getting marketing events: {e}")
            return None
    
    return {'results': all_events}

def filter_events_by_name(events, search_term):
    """Filter events by name containing the search term."""
    if not events or 'results' not in events:
        return []
    
    return [event for event in events['results'] 
            if search_term.lower() in event['eventName'].lower()]

def get_event_performance(access_token, portal_id, event_id):
    """Get performance metrics for a specific event."""
    url = f'https://api.hubapi.com/marketing/v3/marketing-events/{event_id}/performance'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    params = {
        'portalId': portal_id
    }
    
    try:
        print(f"Fetching performance data for event {event_id}")
        print(f"URL: {url}")
        response = requests.get(url, headers=headers, params=params)
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting event performance: {response.status_code}")
            print(f"Response text: {response.text}")
            return None
    except Exception as e:
        print(f"Error getting event performance: {e}")
        return None

def save_events_to_file(events, filename='marketing_events.json'):
    """Save events data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(events, f, indent=2)
        print(f"Events data saved to {filename}")
    except Exception as e:
        print(f"Error saving events to file: {e}")

try:
    # Get access token using the utility function
    access_token, portal_id = get_hubspot_token()
    
    # Get marketing events with no limit (will get all pages)
    events = get_marketing_events(access_token, portal_id)
    
    if events:
        # Save to file first
        save_events_to_file(events)
        
        # Search for events with "Manager" in the name
        manager_events = filter_events_by_name(events, "Manager")
        
        if manager_events:
            print("\nFound events with 'Manager' in the name:")
            for event in manager_events:
                print(f"\nEvent Name: {event['eventName']}")
                print(f"Event Type: {event['eventType']}")
                print(f"Start Date: {event['startDateTime']}")
                print(f"Event ID: {event['objectId']}")
        else:
            print("\nNo events found with 'Manager' in the name")
            
        print("\nTotal number of events retrieved:", len(events['results']))
        
        # Get performance for a specific event
        event_id = "398502371626"  # ChatGPT for Payroll Pros event
        performance = get_event_performance(access_token, portal_id, event_id)
        if performance:
            print("\nEvent Performance Metrics:")
            pprint(performance)
    else:
        print("Failed to retrieve marketing events")
except Exception as e:
    print(f"Exception when getting marketing events: {e}") 