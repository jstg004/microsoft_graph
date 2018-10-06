'''
    This is a simple request that gets a token from Azure AD.
    Then uses that token to fetch json data from document libraries in
    SharePoint Office 365.
'''


import requests
import json


'''
    Replace sections in this code that look like {app_id} with the string of
    the ID. So {app_id} would be the application_id string received from
    Azure AD App Registration.
'''

get_token =
    requests.post('https://login.microsoftonline.com/{app_id}/oauth2/token',
    data = {
        'grant_type':'client_credentials','client_id':'{client_id}',
        'client_secret':'{client_secret}',
        'resource':'https://graph.microsoft.com'
        }
    )

get_token_reply = get_token.json()

# The key could be named 'accessToken' instead, check the json response from the
# post token request above.
access_token = (get_token_reply['access_token'])

'''
    Use the Microsoft Graph explorer to figure out how you need to structure
    your GET or POST request.
    https://developer.microsoft.com/en-us/graph/graph-explorer
'''

url = 'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_item_id}/children'

# For document libraries located inside SharePoint Groups use this format:
# url = 'https://graph.microsoft.com/v1.0/groups/{group_id}/drives/{drive_id}/root/children'

headers = {'Authorization': 'Bearer ' + access_token}
graph_response = requests.get(url, headers=headers)
graph_data = graph_response.json()

print(graph_data)


'''
    You must register this app in Azure AD, then set and grant permissions.
    This is tested with public files and folders with only read permissions set.
    This is not secure for anything that should not be publicly readable.
'''
