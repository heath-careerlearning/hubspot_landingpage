import os
import pprint
import hubspot
from hubspot.marketing.events.api.basic_api import BasicApi

# or set your access token later
client = hubspot.Client.create(access_token=os.getenv('ACCESS_TOKEN'))

try:
    api_response = client.marketing.events.basic_api.do_search(q="*")
    pprint(api_response)
except Exception as e:
    print("Exception when calling basic_api->do_search: %s\n" % e)