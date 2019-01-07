# microsoft_graph

- Connecting to Microsoft's Graph API

## code

### graph_requests.py

- Hits Graph with a POST request
  - Graph returns a token
- That token is used in a GET request to Graph
  - Graph returns the requested data
- Data is presented in a json format and can be used in custom apps or web pages
- Basically gets the results you would get from Microsoft's Graph Explorer
  without having to log in.
  - This allows for the data to be automatically requested and received
    then displayed to users without any intervention from the user, such as
    having to log into Microsoft.

### graph_docker

- Creates a Docker container that can be hosted on services like AWS ECS running
  on Fargate.
- This app will access the Microsoft Graph API via an API key you assign through
  Microsoft Azure App Services.
- You can change the Graph API calls to access different sections of Sharepoint
  or OneDrive or other Office 365 services, depending on what access you grant.
- This app will search through the 1st level of files and 1 subfolder deep.
  - This code can be improved/consolidated and could also go into deeper levels
    of sub folders, I will improve upon this code to do so.