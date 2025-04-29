#!/usr/bin/env python3
import os
import argparse
import json
import yaml
from landing_page_creator import LandingPageCreator

def get_hubspot_token_from_config():
    """Get HubSpot token from hubspot.config.yml"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                             'hubspot-reporting', 'hubspot.config.yml')
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            # Get the personal access key from the career-learning portal
            for portal in config.get('portals', []):
                if portal.get('name') == 'career-learning':
                    return portal.get('personalAccessKey')
    except Exception as e:
        print(f"Error reading hubspot.config.yml: {e}")
        return None

def load_course_config(config_path=None):
    """Load course configuration from JSON file"""
    if not config_path:
        config_path = os.path.join(os.path.dirname(__file__), 'course_config.json')
    
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading course configuration: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Create a course landing page in HubSpot')
    parser.add_argument('--token', help='HubSpot API token with content scope')
    parser.add_argument('--folder-id', help='HubSpot folder ID', default=None)
    parser.add_argument('--course', help='Course ID from configuration file', required=True)
    parser.add_argument('--template', help='Template ID from configuration file', default='default')
    parser.add_argument('--config', help='Path to course configuration file')
    parser.add_argument('--section-html', help='Path to HTML section content to include')
    args = parser.parse_args()
    
    # Get token from args, environment, or config file
    token = args.token or os.environ.get('HUBSPOT_ASANA_ACCESS_TOKEN') or get_hubspot_token_from_config()
    if not token:
        raise ValueError("HubSpot API token is required. Provide it with --token, set HUBSPOT_ASANA_ACCESS_TOKEN environment variable, or ensure hubspot.config.yml is properly configured.")
    
    # Load course configuration
    config = load_course_config(args.config)
    if not config:
        raise ValueError("Failed to load course configuration")
    
    # Check if course exists in configuration
    if args.course not in config['courses']:
        raise ValueError(f"Course '{args.course}' not found in configuration. Available courses: {', '.join(config['courses'].keys())}")
    
    # Get course data
    course_data = config['courses'][args.course]
    
    # Get template path
    if args.template not in config['templates']:
        raise ValueError(f"Template '{args.template}' not found in configuration. Available templates: {', '.join(config['templates'].keys())}")
    
    template_path = config['templates'][args.template]
    
    # Create the landing page creator
    creator = LandingPageCreator(token)
    
    # If using a custom template, upload it first
    template_id = None
    if args.template != 'default' and template_path.startswith('custom/'):
        template_name = template_path.split('/')[1].split('.')[0]
        template_file_path = os.path.join(os.path.dirname(__file__), f'{template_name}.html')
        
        if os.path.exists(template_file_path):
            try:
                print(f"Uploading custom template '{template_name}'...")
                template_response = creator.upload_template(template_file_path, template_name)
                template_id = template_response.get('id')
                if template_id:
                    print(f"Template uploaded successfully with ID: {template_id}")
            except Exception as e:
                print(f"Error uploading template: {e}")
                print("Continuing with page creation using template path only...")
    
    # Create the landing page
    try:
        print(f"Creating '{course_data['course_title']}' landing page...")
        
        # Determine section HTML path
        section_html_path = args.section_html
        if not section_html_path and args.course == 'leave_of_absence':
            # Default to leave_of_absence_section.html for leave of absence course
            section_html_path = os.path.join(os.path.dirname(__file__), 'leave_of_absence_section.html')
            
        # Create the landing page with template path, ID, and section HTML
        response = creator.create_course_landing_page(
            course_data=course_data, 
            folder_id=args.folder_id, 
            template_id=template_id,
            template_path=template_path,
            section_html_path=section_html_path
        )
        
        print(f"Landing page created successfully!")
        print(f"URL: {response.get('url', 'URL not available')}")
        print(f"ID: {response.get('id', 'ID not available')}")
        print(f"State: {response.get('state', 'State not available')}")
        
    except Exception as e:
        print(f"Error creating landing page: {e}")

if __name__ == "__main__":
    main()
