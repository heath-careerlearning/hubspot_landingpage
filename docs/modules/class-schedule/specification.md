# Class Schedule Module Specification

## Overview
A HubSpot custom module for emails that displays event schedules in a table format, pulling data from HubSpot's native events system.

## Module Metadata
- **Module Label**: "Class Schedule Table"
- **Module Description**: "Displays a responsive table of upcoming events filtered by brand category"
- **Module Help Text**: "This module displays a table of upcoming events from your selected brand category. Events are automatically pulled from HubSpot's marketing events system and include clickable links with UTM tracking."
- **Preview Image**: "class-schedule-preview.png" (to be created)

## Technical Details

### Module Type
- Custom HubSpot Module for Emails
- Data Source: HubSpot Events System

### Table Structure
| Display Name | Data Source Field | Description |
|--------------|-------------------|-------------|
| Program Date | startDateTime | Event start date in MM/DD format |
| Program Time | startDateTime | Event start time in hh:mm AM/PM format |
| Program Name | eventName | Title of the event (linked to website_url with UTM) |
| Description | eventDescription | Event description text |
| Type | eventType | Category of the event (On-Demand, Webinar, etc.) |

### Custom Properties
| Property Name | Field | Description |
|--------------|-------|-------------|
| brand | customProperties.brand | Brand category (HR, Marketing, etc.) |
| class_id | customProperties.class_id | Comma-separated class IDs for UTM tracking |
| website_url | customProperties.website_url | Landing page URL for the event |

### Display Configuration
- Format: Responsive table layout
- Date Format: MM/DD (e.g., "04/30")
- Time Format: hh:mm AM/PM (e.g., "1:00 PM")
- Event Display Range: 3-7 events
- Default Display: 5 events

### Type-Specific Styling
Header colors based on brand:
- HR: #8a00c4
- Education: #ff3000
- Nonprofit: #ff00b1

### Module Fields
1. Brand Filter (Dropdown)
   - Required: Yes
   - Default: HR
   - Options: HR, Marketing, Education, Nonprofit
   - Help Text: "Select which brand's events to display"
   - Editor Label: "Brand Category"

2. Display Count (Number)
   - Required: Yes
   - Default: 5
   - Min: 3
   - Max: 7
   - Help Text: "Number of events to display (3-7)"
   - Editor Label: "Number of Events"

### Event Filtering
- Filter events by customProperties.brand field
- Map brand values to categories:
  - "HR" → HR events
  - "Marketing" → Marketing events
  - "Education" → Education events
  - "Nonprofit" → Nonprofit events

## Dependencies
- HubSpot Events System
- HubSpot Design Manager

## Implementation Notes

### Module Setup
1. Create new module in Design Manager
   - Type: Email Module
   - Scope: Global
   - Name: "class_schedule"

### Content Options
1. Select "Marketing Event" as the CRM object type
2. Map the following fields:
   - startDateTime
   - eventName
   - eventDescription
   - eventType
   - customProperties

### Module Code
The module implementation is defined in `class_schedule.hubl`. This file contains:
- Brand filter dropdown implementation
- Display count field implementation
- Table structure and styling
- Event filtering logic
- UTM parameter construction
- Error handling

### Email-Specific Requirements
1. Use inline styles only (no external CSS)
2. Use table-based layout for maximum email client compatibility
3. Keep HTML structure simple and clean
4. Test in major email clients before deployment