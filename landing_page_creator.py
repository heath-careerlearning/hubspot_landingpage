import os
import json
import sys
import requests
from typing import Dict, List, Optional

# Add the parent directory to the path to import the HubSpot client
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'hubspot_figma_integration', 'src'))
from hubspot_client import HubSpotClient

class LandingPageCreator:
    def __init__(self, access_token: str):
        """Initialize with HubSpot access token."""
        self.client = HubSpotClient(access_token)
        
    def create_course_landing_page(self, 
                                  course_data: Dict,
                                  folder_id: Optional[str] = None,
                                  template_id: Optional[str] = None,
                                  template_path: Optional[str] = None,
                                  section_html_path: Optional[str] = None) -> Dict:
        """
        Create a course landing page using the template.
        
        Args:
            course_data: Dictionary containing all course information
            folder_id: Optional HubSpot folder ID to place the page in
            template_id: Optional template ID to use for the landing page
            template_path: Optional template path to use for the landing page
            section_html_path: Optional path to HTML section content to include
            
        Returns:
            Response from HubSpot API
        """
        # Prepare the landing page data with correct field names for v3 API
        landing_page = {
            "name": course_data["course_title"],
            "slug": self._generate_slug(course_data["course_title"]),
            "metaDescription": f"Learn about {course_data['course_title']} with {course_data['instructor_name']}",
            "state": "DRAFT",
            "htmlTitle": course_data["course_title"],
            "values": course_data  # This contains the template variables
        }
        
        # Add folder ID if provided
        if folder_id:
            landing_page["folderId"] = folder_id
        
        # Set template information - prioritize template_path if provided
        if template_path:
            landing_page["templatePath"] = template_path
        elif template_id:
            landing_page["templateId"] = template_id
        else:
            # Default template path
            landing_page["templatePath"] = "custom/course_landing_template.html"
        
        # Add HTML content from section file if provided
        html_content = ""
        if section_html_path and os.path.exists(section_html_path):
            try:
                with open(section_html_path, 'r') as file:
                    html_content = file.read()
                print(f"Loaded HTML content from {section_html_path}")
            except Exception as e:
                print(f"Error loading HTML content: {e}")
        
        # Add layout sections structure with rich text module containing the HTML content
        landing_page["layoutSections"] = {
            "dnd_area": {
                "cells": [],
                "cssClass": "",
                "cssId": "",
                "cssStyle": "",
                "label": "Main section",
                "name": "dnd_area",
                "params": {},
                "rowMetaData": [
                    {
                        "cssClass": "dnd-section",
                        "styles": {
                            "backgroundColor": {
                                "a": 1,
                                "b": 250,
                                "g": 248,
                                "r": 245
                            },
                            "forceFullWidthSection": False
                        }
                    }
                ],
                "rows": [
                    {
                        "0": {
                            "cells": [],
                            "cssClass": "",
                            "cssId": "",
                            "cssStyle": "",
                            "name": "dnd_area-column-1",
                            "params": {
                                "css_class": "dnd-column"
                            },
                            "rowMetaData": [
                                {
                                    "cssClass": "dnd-row"
                                }
                            ],
                            "rows": [
                                {
                                    "0": {
                                        "cells": [],
                                        "cssClass": "",
                                        "cssId": "",
                                        "cssStyle": "",
                                        "name": "dnd_area-module-1",
                                        "params": {
                                            "child_css": {},
                                            "css": {},
                                            "css_class": "dnd-module",
                                            "extra_classes": "widget-type-rich_text",
                                            "html": f"""<style>
                                                @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap');
                                                
                                                /* Reset HubSpot default styles */
                                                .dnd-section, .dnd-column, .dnd-row, .dnd-module, .content-wrapper, .main-content, .page-center, .row-fluid {{  
                                                    max-width: 100% !important;
                                                    padding: 0 !important;
                                                    margin: 0 !important;
                                                    width: 100% !important;
                                                }}
                                                
                                                body {{  
                                                    background-color: rgb(248, 249, 254) !important;
                                                }}
                                                
                                                .leave-absence-wrapper {{  
                                                    max-width: 1200px !important;
                                                    margin: 0 auto !important;
                                                    padding-left: 133px !important;
                                                    padding-right: 133px !important;
                                                    width: 100% !important;
                                                    box-sizing: border-box !important;
                                                }}
                                                
                                                .leave-absence-content::before {{  
                                                    content: '';
                                                    position: absolute;
                                                    top: 0;
                                                    right: 0;
                                                    width: 100%;
                                                    height: 100%;
                                                    background-image: url("data:image/svg+xml,%3Csvg width='301' height='335' viewBox='0 0 301 335' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='150.5' cy='184.5' r='150' stroke='%2315C1EC' stroke-opacity='0.4' stroke-dasharray='9 9'/%3E%3Ccircle cx='191' cy='40' r='40' fill='%232B2B5E' fill-opacity='0.07'/%3E%3C/svg%3E");
                                                    background-repeat: no-repeat;
                                                    background-position: right top;
                                                    z-index: -1;
                                                }}
                                                
                                                .leave-absence-content h1, .leave-absence-content h2, .leave-absence-content h3 {{  
                                                    color: #2B2B5E;
                                                    font-weight: 700;
                                                }}
                                                
                                                .leave-absence-content h1 {{  
                                                    font-size: 2.5rem;
                                                    margin-bottom: 1.5rem;
                                                    font-family: 'Raleway', sans-serif;
                                                }}
                                                
                                                .leave-absence-content .breadcrumb {{  
                                                    margin-bottom: 1.5rem;
                                                    font-size: 0.9rem;
                                                    color: #666;
                                                }}
                                                
                                                .leave-absence-content .breadcrumb a {{  
                                                    color: #1f60ae;
                                                    text-decoration: none;
                                                }}
                                                
                                                .leave-absence-content .instructor {{  
                                                    display: flex;
                                                    align-items: center;
                                                    margin-bottom: 1.5rem;
                                                }}
                                                
                                                .leave-absence-content .instructor-image {{  
                                                    width: 40px;
                                                    height: 40px;
                                                    border-radius: 50%;
                                                    margin-right: 0.75rem;
                                                    object-fit: cover;
                                                }}
                                                
                                                .leave-absence-content .instructor-name {{  
                                                    font-weight: 600;
                                                    color: #1f60ae;
                                                    letter-spacing: 0.5px;
                                                }}
                                                
                                                .leave-absence-content .course-description {{  
                                                    margin-bottom: 2rem;
                                                    line-height: 1.6;
                                                    color: #333;
                                                }}
                                                
                                                .leave-absence-content .learning-outcomes h2 {{  
                                                    font-size: 1.5rem;
                                                    margin-bottom: 1rem;
                                                    font-family: 'Raleway', sans-serif;
                                                }}
                                                
                                                .leave-absence-content .learning-outcomes ul {{  
                                                    padding-left: 1.5rem;
                                                    list-style-type: disc;
                                                }}
                                                
                                                .leave-absence-content .learning-outcomes li {{  
                                                    margin-bottom: 0.75rem;
                                                    line-height: 1.5;
                                                    color: #333;
                                                }}
                                                
                                                .leave-absence-content .course-badges {{  
                                                    display: flex;
                                                    gap: 10px;
                                                    margin-bottom: 20px;
                                                    position: absolute;
                                                    top: 10px;
                                                    left: 10px;
                                                }}
                                                
                                                .leave-absence-content .badge {{  
                                                    font-size: 0.7rem;
                                                    font-weight: 600;
                                                    padding: 0.25rem 0.5rem;
                                                    border-radius: 4px;
                                                    text-transform: uppercase;
                                                    color: white;
                                                    letter-spacing: 0.5px;
                                                }}
                                                
                                                .leave-absence-content .badge.live {{  
                                                    background-color: #1f60ae;
                                                    color: white;
                                                }}
                                                
                                                .leave-absence-content .badge.certification {{  
                                                    background-color: #00b0f0;
                                                    color: white;
                                                }}
                                                
                                                .leave-absence-content .badge.on-demand {{  
                                                    background-color: #4a5c9a;
                                                    color: white;
                                                }}
                                                
                                                .leave-absence-content .course-card {{  
                                                    background: white;
                                                    border-radius: 16px;
                                                    overflow: hidden;
                                                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                                                }}
                                                
                                                .leave-absence-content .course-details {{  
                                                    padding: 1.5rem;
                                                }}
                                                
                                                .leave-absence-content .session-info h3 {{  
                                                    font-size: 1.25rem;
                                                    margin-bottom: 0.5rem;
                                                    font-weight: 600;
                                                }}
                                                
                                                .leave-absence-content .session-info p {{  
                                                    margin: 0.25rem 0;
                                                    color: #4a5568;
                                                }}
                                                
                                                .leave-absence-content .session-info p:last-child {{  
                                                    color: #93c5fd;
                                                }}
                                                
                                                .leave-absence-content .date-options {{  
                                                    margin: 1.5rem 0;
                                                    border-bottom: 1px solid #e2e8f0;
                                                    padding-bottom: 1.5rem;
                                                }}
                                                
                                                .leave-absence-content .date-options h3 {{  
                                                    font-size: 1.1rem;
                                                    margin-bottom: 0.75rem;
                                                    font-weight: 600;
                                                }}
                                                
                                                .leave-absence-content .date-selector {{  
                                                    display: flex;
                                                    flex-direction: column;
                                                    gap: 0.75rem;
                                                }}
                                                
                                                .leave-absence-content .date-options-header {{  
                                                    display: flex;
                                                    justify-content: space-between;
                                                    align-items: center;
                                                    margin-bottom: 0.75rem;
                                                }}
                                                
                                                .leave-absence-content .date-option {{  
                                                    display: flex;
                                                    align-items: center;
                                                    cursor: pointer;
                                                    padding: 12px;
                                                    border-radius: 30px;
                                                    position: relative;
                                                    border: 1px solid #e2e8f0;
                                                    margin-bottom: 8px;
                                                }}
                                                
                                                .leave-absence-content .date-option.selected {{  
                                                    background-color: #f0f7ff;
                                                    border-color: #1f60ae;
                                                }}
                                                
                                                .leave-absence-content .date-option input {{  
                                                    position: absolute;
                                                    opacity: 0;
                                                    cursor: pointer;
                                                    height: 0;
                                                    width: 0;
                                                }}
                                                
                                                .leave-absence-content .radio-custom {{  
                                                    position: relative;
                                                    display: inline-block;
                                                    width: 22px;
                                                    height: 22px;
                                                    background-color: #f0f7ff;
                                                    border: 2px solid #ccc;
                                                    border-radius: 50%;
                                                    margin-right: 12px;
                                                    vertical-align: middle;
                                                }}
                                                
                                                .leave-absence-content .date-option input:checked ~ .radio-custom::after {{  
                                                    content: '';
                                                    position: absolute;
                                                    display: block;
                                                    top: 3px;
                                                    left: 3px;
                                                    width: 8px;
                                                    height: 8px;
                                                    border-radius: 50%;
                                                    background: #1f60ae;
                                                }}
                                                
                                                .leave-absence-content .pricing {{  
                                                    display: flex;
                                                    justify-content: space-between;
                                                    align-items: center;
                                                    margin: 0;
                                                    padding: 0;
                                                }}
                                                
                                                .leave-absence-content .price {{  
                                                    font-size: 1.5rem;
                                                    font-weight: 700;
                                                    color: #2B2B5E;
                                                }}
                                                
                                                .leave-absence-content .quantity {{  
                                                    display: flex;
                                                    align-items: center;
                                                    gap: 0.75rem;
                                                }}
                                                
                                                .leave-absence-content .qty-controls {{  
                                                    display: flex;
                                                    align-items: center;
                                                    border-radius: 30px;
                                                    overflow: hidden;
                                                    background-color: #f0f7ff;
                                                }}
                                                
                                                .leave-absence-content .qty-btn {{  
                                                    width: 36px;
                                                    height: 36px;
                                                    display: flex;
                                                    align-items: center;
                                                    justify-content: center;
                                                    background-color: #f0f7ff;
                                                    border: none;
                                                    cursor: pointer;
                                                    font-size: 18px;
                                                    color: #1f60ae;
                                                    font-weight: bold;
                                                }}
                                                
                                                .leave-absence-content .qty-input {{  
                                                    width: 36px;
                                                    height: 36px;
                                                    text-align: center;
                                                    border: none;
                                                    background-color: #f0f7ff;
                                                    padding: 0;
                                                    font-size: 16px;
                                                    color: #333;
                                                }}
                                                
                                                .leave-absence-content .purchase-options {{  
                                                    margin: 20px 0;
                                                    padding-bottom: 20px;
                                                }}
                                                
                                                .leave-absence-content .option-label {{  
                                                    display: flex;
                                                    align-items: center;
                                                    flex-wrap: wrap;
                                                    cursor: pointer;
                                                    position: relative;
                                                    padding: 12px 0;
                                                    margin-bottom: 8px;
                                                }}
                                                
                                                .leave-absence-content .option-label input {{  
                                                    position: absolute;
                                                    opacity: 0;
                                                    cursor: pointer;
                                                    height: 0;
                                                    width: 0;
                                                }}
                                                
                                                .leave-absence-content .option-label span:not(.radio-custom):not(.option-price):not(.available-now) {{  
                                                    flex: 1;
                                                    margin-left: 28px;
                                                    font-size: 0.9rem;
                                                    color: #333;
                                                }}
                                                
                                                .leave-absence-content .available-now {{  
                                                    color: #6b7280;
                                                    font-size: 0.85rem;
                                                    margin-left: 5px;
                                                }}
                                                
                                                .leave-absence-content .option-price {{  
                                                    margin-left: auto;
                                                    font-weight: 600;
                                                    color: #2B2B5E;
                                                    padding-left: 8px;
                                                }}
                                                
                                                .leave-absence-content .add-to-cart-btn {{  
                                                    width: 100%;
                                                    padding: 0.85rem;
                                                    background-color: #1f60ae;
                                                    color: white;
                                                    border: none;
                                                    border-radius: 30px;
                                                    font-weight: 600;
                                                    cursor: pointer;
                                                    transition: background-color 0.2s;
                                                    font-size: 1rem;
                                                    letter-spacing: 0.5px;
                                                }}
                                                
                                                .leave-absence-content .add-to-cart-btn:hover {{  
                                                    background-color: #00b0f0;
                                                }}
                                                
                                                @media (max-width: 768px) {{  
                                                    .leave-absence-content .leave-absence-wrapper {{  
                                                        grid-template-columns: 1fr;
                                                    }}
                                                }}
                                            </style>
                                            <div class='leave-absence-content'>{html_content}</div>""",
                                            "path": "@hubspot/rich_text",
                                            "schema_version": 2,
                                            "smart_objects": [],
                                            "smart_type": "NOT_SMART",
                                            "wrap_field_tag": "div"
                                        },
                                        "rowMetaData": [],
                                        "rows": [],
                                        "type": "custom_widget",
                                        "w": 12,
                                        "x": 0
                                    }
                                }
                            ],
                            "type": "cell",
                            "w": 12,
                            "x": 0
                        }
                    }
                ],
                "type": "cell",
                "w": 12,
                "x": 0
            }
        }
        
        # Call the HubSpot API to create the landing page
        return self._create_landing_page(landing_page)
    
    def _create_landing_page(self, landing_page_data: Dict) -> Dict:
        """Call the HubSpot API to create a landing page."""
        url = f"{self.client.base_url}/cms/v3/pages/landing-pages"
        
        # Print the landing page data for debugging
        print(f"\nLanding page data:")
        print(json.dumps(landing_page_data, indent=2))
        
        response = self.client._make_request("POST", url, json=landing_page_data)
        return response
    
    def _generate_slug(self, title: str) -> str:
        """Generate a URL slug from a title."""
        # Convert to lowercase, replace spaces with hyphens, remove special chars
        slug = title.lower().replace(" ", "-")
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        return slug

    def get_template_by_path(self, template_path: str) -> Dict:
        """
        Get a template by its path.
        
        Args:
            template_path: Path of the template in HubSpot (e.g., 'custom/template_name.html')
            
        Returns:
            Template data if found, empty dict if not found
        """
        url = f"{self.client.base_url}/content/api/v2/templates"
        
        try:
            response = self.client._make_request("GET", url)
            templates = response.get('objects', [])
            
            # Find the template with the matching path
            for template in templates:
                if template.get('path') == template_path:
                    return template
            
            return {}
        except Exception as e:
            print(f"Error getting templates: {e}")
            return {}
    
    def upload_template(self, template_path: str, template_name: str) -> Dict:
        """
        Upload a landing page template to HubSpot using the v2 API endpoint.
        First checks if the template exists, and if so, returns the existing template.
        
        Args:
            template_path: Path to the template file
            template_name: Name for the template in HubSpot
            
        Returns:
            Response from HubSpot API
        """
        # Check if template already exists
        hubspot_template_path = f"custom/{template_name}.html"
        existing_template = self.get_template_by_path(hubspot_template_path)
        
        if existing_template and 'id' in existing_template:
            print(f"Template already exists with ID: {existing_template['id']}")
            return existing_template
        
        # Read the template file
        with open(template_path, 'r') as file:
            template_content = file.read()
        
        # Prepare the API endpoint - using the correct v2 API endpoint for template creation
        url = f"{self.client.base_url}/content/api/v2/templates"
        
        # Prepare the template data
        template_data = {
            "source": template_content,
            "path": hubspot_template_path,
            "name": template_name,
            "type": "page",
            "is_available_for_new_content": True
        }
        
        # Make the request using the client's method
        try:
            response = self.client._make_request("POST", url, json=template_data)
            return response
        except Exception as e:
            print(f"Template upload error: {e}")
            # If we get a 409 conflict error, the template already exists
            if '409' in str(e):
                # Try to get the template again
                return self.get_template_by_path(hubspot_template_path)
            # Return empty dict to continue with page creation
            return {}


# Add a helper method to the HubSpotClient class for general requests
def _make_request(self, method: str, url: str, **kwargs):
    """Make a request to the HubSpot API."""
    response = requests.request(method, url, headers=self.headers, **kwargs)
    print(f"\nHubSpot {method} request to {url}")
    print(f"Status code: {response.status_code}")
    
    # Only try to print JSON if the response has content
    if response.text:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except json.JSONDecodeError:
            print(f"Response text: {response.text}")
    
    response.raise_for_status()
    
    if response.text:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"text": response.text}
    return {"status": "success"}

# Monkey patch the HubSpotClient class
HubSpotClient._make_request = _make_request
