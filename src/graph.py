import json
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential, InteractiveBrowserCredential
from msgraph.core import GraphClient
from requests import request

class Graph:
    settings: SectionProxy
    browser_credential: InteractiveBrowserCredential
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['authTenant']
        client_secret = self.settings['clientSecret']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.browser_credential = InteractiveBrowserCredential(client_id = client_id, tenant_id = tenant_id, client_secret = client_secret)
        self.user_client = GraphClient(credential=self.browser_credential, scopes=graph_scopes)
    
    def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.browser_credential.get_token(graph_scopes)
        return access_token.token
    
    def create_mail(self, subject: str, body_content: str, recipients: list, importance: str):
        request_body = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'html',
                    'content': body_content
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': "eesoc-publicity-officer@imperial.ac.uk"
                        }
                    }
                ],
                'bccRecipients': recipients,
                'importance': importance,
                'inferenceClassification': 'focused'
            }
        }

        request_url = '/me/sendMail'

        self.user_client.post(request_url,
                            data=json.dumps(request_body),
                            headers={'Content-Type': 'application/json', 'Content-Length' : '0'})

    def create_calendar_event(self, subject: str, content, start: str, end: str, location: str, mode: str):
        time_zone = "Europe/London"
        
        request_body = {
            "subject": subject,
            "body": {
                "contentType": "text",
                "content": content
            },
            "start": {
                "dateTime": start, # "2022-09-10T14:00:00"
                "timeZone": time_zone
            },
            "end": {
                "dateTime": end,
                "timeZone": time_zone
            },
            "location":{
                "displayName": location
            },
            "allowNewTimeProposals": 'false'
        }

        if mode == "events":
            id = 'AAMkAGQ3Y2NmZjhjLWQxYzgtNGYyOC1hMDUxLWExMmI5ZGVjOGZjMwBGAAAAAADlWTOtwh4rR5e93T1eLsugBwCkZWCAN_MASrJmSgfTv6muAAAAAAEGAACkZWCAN_MASrJmSgfTv6muAATjAN5LAAA='
        elif mode == "industry":
            id = 'AAMkAGQ3Y2NmZjhjLWQxYzgtNGYyOC1hMDUxLWExMmI5ZGVjOGZjMwBGAAAAAADlWTOtwh4rR5e93T1eLsugBwCkZWCAN_MASrJmSgfTv6muAAAAAAEGAACkZWCAN_MASrJmSgfTv6muAATjAN5MAAA='
        else:
            id = ''

        request_url = '/me/calendars/'+id+'/events'

        self.user_client.post(request_url,
                              data=json.dumps(request_body),
                              headers={'Content-Type': 'application/json'})

        # print (response.json()['webLink'])

