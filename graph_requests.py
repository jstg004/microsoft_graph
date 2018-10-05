# Simple request that gets a token from AzureAD.
# Then uses that token to fetch json data from document libraies in SharePoint365

import requests
import json

get_token = requests.post('https://login.microsoftonline.com/{app_id}/oauth2/token', data = {'grant_type':'client_credentials','client_id':'{client_id}','client_secret':'{client_secret}','resource':'https://graph.microsoft.com'})
get_token_reply = get_token.json()
access_token = (get_token_reply['access_token'])
    # Could be 'accessToken' instead

url = 'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_item_id}/children'
# For document libraries in groups:
# url = 'https://graph.microsoft.com/v1.0/groups/{group_id}/drives/{drive_id}/root/children'

headers = {'Authorization': 'Bearer ' + access_token}

graph_response = requests.get(url, headers=headers)
graph_data = graph_response.json()

print(graph_data)

'''
This is tested with a public files and folders with read persmissions set in AAD.
This is not secure for anything that should not be publicly readable.

This is very rough right now, but it works.
You must register app in AAD and set and grant permissions.
'''
