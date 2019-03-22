'''
Wokring on different way to query the Microsoft Graph API and use the data.
'''


@app.route('/find/', methods = ['GET'])
def find_files():
    '''
    This will search the Microsoft Graph API in a specific library,
        defined in the 'website_library' variable, for the specified argument
        added to the end of the URL to get to this app route.
        - The 'website_library' variable needs to be formatted to get to the
            specific library you need to search in SharePoint.
    This argument is a custom field added to SharePoint files in a specific
        document library. SharePoint appends the value of the custom field
        to the metadata of the file.
    This app route will grab the necessary data from the file on SharePoint.
    '''

    # Grabs the user information when the user visits the webpage:
    browser   = request.user_agent.browser
    platform  = request.user_agent.platform
    uas       = request.user_agent.string

    # Grabs the choice desired from the URL argument:
    comm_choice = request.args.get('comm') # /?comm=search_variable

    # Formats the string fro the API query and builds the URL for the API query:
    comm_choice_str  =  "'" + comm_choice + "'"
    url              =  website_library + comm_choice_str

    # Builds and makes the Microsoft Graph API call:
    access_token           =   graph_token(client_id, client_secret)
    headers                = {'Authorization': 'Bearer ' + access_token}
    graph_data             =   requests.get(url, headers = headers)
    graph_data_json        =   graph_data.json()
    graph_data_json_value  =   graph_data_json['value']

    # Creates and empty dictionary to store data organized by file name:
    file_dict = {}

    # Parses the returned json from the API call:
    for item in json_value:
        find_list = [] # Creates an empty list to store data for each file

        # Pulls the metadata from each file found from the API call:
        name    = item["fields"]["FileLeafRef"]
        modtime = item["lastModifiedDateTime"]
        size    = item["fields"]["FileSizeDisplay"]
        dl_url  = item["driveItem"]["@microsoft.graph.downloadUrl"]

        # Build metadata list:
        find_list.append(modtime)
        find_list.append(size)


        # Trying to figure out how to display a PDF from SharePoint
        #   in a browser window (not just download) for certain platforms.
        '''
        Only need direct graph api download link for the following:
            - if not pdf
            - if pdf and iphone and android
        Need base64 if:
            - pdf and not iphone and android
        '''

        if 'pdf' in name and (platform.lower() != 'iphone'
                              or platform.lower() != 'android'):

            # GET request to the SharePoint download URL to get the data:
            get_dl_data = requests.get(dl_url)

            # Encode the data in base64:
            pdf_base64 = (base64.b64encode(get_dl_data.content).decode("utf-8"))

            ### Figure out what to do next with the base64 PDF data ###
            find_list.append(pdf_base64)

        else:
            # Otherwise only need the SharePoint download link:
            find_list.append(dl_url)

        # Builds a dictionary of file metadata organized by file name:
        file_dict[name] = find_list


        # Can add to this list in the dictionary if needed
        '''
        Example of the dictionary format:

        {
            name : [
                modtime,
                size,
                dl_url
            ]
        }

        '''

    return jsonify(file_dict) # For now just display json dataset built
