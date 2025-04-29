#!/usr/bin/env python3
import os
import argparse
import yaml
from landing_page_creator import LandingPageCreator

# Note: This script requires a HubSpot API token with the 'content' scope enabled
# The 'content' scope provides access to create and manage CMS content including landing pages

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

def main():
    parser = argparse.ArgumentParser(description='Create a Leave of Absence Certification landing page in HubSpot')
    parser.add_argument('--token', help='HubSpot API token with content scope')
    parser.add_argument('--folder-id', help='HubSpot folder ID', default=None)
    args = parser.parse_args()
    
    # Get token from args, environment, or config file
    token = args.token or os.environ.get('HUBSPOT_ASANA_ACCESS_TOKEN') or get_hubspot_token_from_config()
    if not token:
        raise ValueError("HubSpot API token is required. Provide it with --token, set HUBSPOT_ASANA_ACCESS_TOKEN environment variable, or ensure hubspot.config.yml is properly configured.")
    
    # Create the landing page creator
    creator = LandingPageCreator(token)
    
    # First, upload the template using the v2 API endpoint
    template_path = os.path.join(os.path.dirname(__file__), 'course_landing_template.html')
    try:
        print("Uploading landing page template using v2 API...")
        template_response = creator.upload_template(template_path, 'course_landing_template')
        print("Template uploaded successfully!")
        
        # If we have a template ID, we can reference it in the landing page
        template_id = template_response.get('id')
        if template_id:
            print(f"Template ID: {template_id}")
    except Exception as e:
        print(f"Error uploading template: {e}")
        print("Continuing with page creation...")
    
    # Define the course data to match the modern design in the second image
    leave_absence_data = {
        "course_title": "Leave of Absence Certification",
        "category_name": "COMPLIANCE",
        "category_url": "/compliance",
        "course_short_name": "LEAVE OF ABSENCE CERTI...",
        "instructor_name": "TERI MORNING",
        "instructor_image": "https://f.hubspotusercontent10.net/hubfs/21151322/teri-morning.jpg",
        "course_description": "FMLA expert Teri Morning will teach you everything you need to know about leaves of absence in just one week. As leave requests increase and rules evolve, this training will help you perform your job better, support employees, and protect your employer.",
        "outcomes_title": "What You'll Learn",
        "learning_outcomes": """
        <ul>
            <li>Protect your organization from potential legal liability</li>
            <li>Help colleagues who request leaves</li>
            <li>Expand your professional knowledge and propel your career</li>
            <li>Prove your knowledge with a certificate</li>
            <li>All courses include a PDF version of the presentation slides along with any additional materials or resources provided by the presenter</li>
            <li>One certification exam attempt is included</li>
        </ul>
        """,
        "course_image": "https://f.hubspotusercontent10.net/hubfs/21151322/absent-from-work.jpg",
        "course_badges": [
            {"type": "live", "text": "LIVE SESSION"},
            {"type": "certification", "text": "CERTIFICATION"},
            {"type": "on-demand", "text": "ON-DEMAND"}
        ],
        "sessions_count": "5",
        "session_duration": "Each 90 Minutes",
        "session_days": "Monday - Friday",
        "session_features": "Q&A; Included",
        "session_dates": [
            {"value": "sept", "text": "Sept 9 - Sept 13 - 1:00 PM EST", "selected": True},
            {"value": "oct", "text": "Oct 28 - Nov 1 - 2:00 PM EST", "selected": False}
        ],
        "course_price": "1,374.00",
        "purchase_options": [
            {
                "value": "add-recordings",
                "text": "Add On Demand Recordings to your Live Sessions",
                "price": "+$275",
                "selected": False
            },
            {
                "value": "recordings-only",
                "text": "On Demand Recordings only (Available now)",
                "price": "$1,374",
                "selected": False
            }
        ],
        "button_text": "Add to cart",
        "additional_sections": [
            {
                "title": "Training Overview",
                "content": "<p>Comprehensive training on managing leave requests and compliance requirements.</p>"
            },
            {
                "title": "Who Should Attend?",
                "content": """
                <ul>
                    <li>HR Managers</li>
                    <li>Benefits Administrators</li>
                    <li>Leave Coordinators</li>
                    <li>HR Business Partners</li>
                </ul>
                """
            }
        ]
    }
    
    # Create the landing page
    try:
        print("Creating Leave of Absence Certification landing page...")
        # Get template information
        template_id = template_response.get('id') if 'template_response' in locals() and template_response else None
        
        # Use a standard HubSpot template path or custom template path
        # You can use a standard HubSpot template like this one, or your custom template path
        template_path = "@hubspot/growth/templates/paid-consultation.html"
        
        # Create the landing page with both template ID and path
        response = creator.create_course_landing_page(
            course_data=leave_absence_data, 
            folder_id=args.folder_id, 
            template_id=template_id,
            template_path=template_path
        )
        print(f"Landing page created successfully! URL: {response.get('url', 'URL not available')}")
    except Exception as e:
        print(f"Error creating landing page: {e}")

if __name__ == "__main__":
    main()
