import json, humanfriendly, requests, maya
from flask import Flask, render_template, request, session

# These variables can be stored in a config file or elsewhere in a secure manor:
token_url = 'MICROSOFT API TOKEN'
client_id = 'MICROSOFT API CLIENT ID'
client_secret = 'MICROSOFT API CLIENT SECRET'

# Insert the unique ID of the SharePoint group you want into the URL below:
graph_url_pre = \
    'https://graph.microsoft.com/v1.0/groups/THE_SHAREPOINT_GROUP_ID/drives/'

graph_url_end = '/root/children'


app = Flask(__name__)


@app.route('/folder/', methods = ['GET'])
def folder(child = None):
    # The 'drive_id' is the ID of the main folder in which the data is located.
    drive_id = request.args.get('drive_id')

    # GET token from Microsoft Graph API:
    get_token = requests.post(
        token_url,
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': 'https://graph.microsoft.com'
            }
        )

    # Store the received token from Microsoft Graph API in a variable:
    graph_token = get_token.json()
    access_token = (graph_token['access_token'])

    # Form the URL used to query the Microsoft Graph API needed to GET the
    # data from SharePoint:
    graph_url = graph_url_pre + drive_id + graph_url_end

    # Use the received token from Microsoft Graph API to gain access to
    # the SharePoint folder data:
    headers = {'Authorization': 'Bearer ' + access_token}
    graph_reply = requests.get(graph_url, headers = headers)

    # Stores the response data from Microsoft Graph API in json format:
    raw_json = graph_reply.json()

    # The dictionary key labeled 'value' from the Microsoft Graph API response
    # contains the file information from the SharePoint folder:
    json_value = raw_json['value']

    # Initialize the dictionaries that will be used to store received
    # SharePoint data:
    subfolder_dict = {}
    filename_dict = {}

    # Extract the data needed from the Microsoft Graph API json response:
    for item in json_value:
        '''
        Initializes a list and a dictionary, which resets every iteration
        of the for loop, to store the extracted json data:
        '''
        file_list = []
        subfilename_dict = {}

        if '@microsoft.graph.downloadUrl' in item:
            '''
            If the item is a file, then extract the data from the response
            needed to display the file on the web page:
            '''
            filename = item['name']

            # Converts the time format an easily readable format & adds the
            # time to the list:
            date_mod0 = maya.when(item['lastModifiedDateTime'])
            file_list.append(date_mod0.slang_time())

            # Converts file size format to an easily readable format & adds
            # the files size to the list:
            file_list.append(humanfriendly.format_size(item['size']))

            # Adds the file download URL to the list:
            file_list.append(item['@microsoft.graph.downloadUrl'])

            # Stores the data from the files located in the main SharePoint
            # folder directory:
            filename_dict[filename] = file_list

        else:
            '''
            If the item is a folder, then extract the folder ID and make another
            Graph API call to get the data from the files within the folder
            needed to display them on the web page:
            '''
            graph_sub_url = graph_url_pre + drive_id + '/items/' + \
                            item['id'] + '/children'

            graph_sub_reply = requests.get(graph_sub_url, headers = headers)
            subfolder_details = graph_sub_reply.json()
            subraw_json = subfolder_details
            subjson_value = subraw_json['value']

            # Extracts the data from within the folder:
            for subitem in subjson_value:
                '''
                Initializes a list, which resets every iteration of the for
                loop, to store the extracted json data:
                '''
                subfolder_files_list = []

                # Adds the subfolder name to the dictionary:
                subfilename = subitem['name']

                if '@microsoft.graph.downloadUrl' in subitem:
                    '''
                    If the item is a file, then extract the data from the
                    response needed to display the file on the web page:
                    '''
                    # Converts the time format an easily readable format & adds
                    # the time to the list:
                    date_mod1 = maya.when(subitem['lastModifiedDateTime'])
                    subfolder_files_list.append(date_mod1.slang_time())

                    # Converts file size format to an easily readable format &
                    # adds the files size to the list:
                    subfolder_files_list.append( \
                        humanfriendly.format_size(subitem['size']))

                    # Adds the file download URL to the list:
                    subfolder_files_list.append(subitem \
                        ['@microsoft.graph.downloadUrl'])

                    # Stores the data from the files located in the SharePoint
                    # subfolder directory:
                    subfilename_dict[subfilename] = subfolder_files_list

            # Stores the data from the subfolder file in a dictionary by the
            # subfolder name:
            subfolder_dict[item['name']] = subfilename_dict

    # Output the data from the files into a web page:
    return render_template('index.html', \
        subfolder_dict = subfolder_dict, filename_dict = filename_dict)