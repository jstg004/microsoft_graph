# microsoft_graph

- Connecting to Microsoft's Graph API

## code

### graph_requests.py
- Hits graph with a POST request
  - Graph returns a token
- That token is used in a GET request to Graph
  - Graph returns the requested data
- Data is presented in a json format and can be used in custom apps or web pages
- Basically gets the results you would get from Microsoft's Graph Explorer
  without having to log in.
  - This allows for the data to be automatically requested and received
    then displayed to users without any intervention from the user, such as
    having to log into Microsoft.
