import configparser
from os import path
from yaml import safe_load, YAMLError
from jinja2 import Environment, FileSystemLoader, select_autoescape
from graph import Graph
from urllib import parse
from datetime import datetime

class email_content:

    subject: str
    body: str
    recipients: list
    importance: str
    events: list

    loaded_document: dict

    def update_parameters(self, file_path = "gen/gen.yaml"):

        # Open up the .YAML file and load the different email parameters

        with open( path.abspath(file_path) , "r") as stream:
            try:
                loaded_document = safe_load(stream)
            except YAMLError as exc:
                print(exc)
                exit(1)

        env = Environment(
            loader = FileSystemLoader("templates"),
            autoescape=select_autoescape()
        )

        mail_template = env.get_template("mail_template.html")

        # Set parameters based on the .YAML

        try:
            self.subject = loaded_document["subject"]
            self.importance = loaded_document["importance"]
            self.recipients = self.get_recipients(loaded_document["recipients"])
            self.events = self.get_events(loaded_document["body"])
            self.body = mail_template.render(doc = loaded_document["body"])

            with open( path.abspath('gen/gen.html'), "w") as edit:
                edit.write(self.body)
        except:
            with open( path.abspath('gen/gen.html'), "w") as edit:
                edit.write('ERROR')
    
    def get_recipients(self, recipients: list):
        output_list = []
        for address in recipients:
            output_list.append( { 'emailAddress': { 'address': address } } )
        return output_list

    def get_events(self, loaded: dict):
        
        output = []

        for item in loaded["sections"]:
            if item["type"] == "Body":
                for content in item["contents"]:
                    if content["type"] == "button" and content["url"] == "":
                        output.append(content)
                        url = 'https://outlook.office.com/calendar/0/deeplink/compose?allday=false'
                        url += '&body=' + parse.quote(content["body"])
                        url += '&enddt=' + parse.quote(content["end"])
                        url += '&location=' + parse.quote(content["location"])
                        url += '&path=%2Fcalendar%2Faction%2Fcompose&rru=addevent'
                        url += '&startdt=' + parse.quote(content["start"])
                        url += '&subject=' + parse.quote(content["subject"])
                        content["url"] = url
        return output

    def send_email(self):

        # Setup parameters for accessing the Graph API

        config = configparser.ConfigParser()
        config.read(['config.cfg', 'config.dev.cfg'])
        azure_settings = config['azure']
        graph: Graph = Graph(azure_settings)

        curr_yaml = ""

        # Send the HTTP request to send the email

        graph.create_mail(self.subject, self.body, self.recipients, self.importance)

        for events in self.events:
            graph.create_calendar_event(events["subject"], events["body"], events['start'], events['end'], events['location'], events['calendar'])


        with open( path.abspath('gen/gen.yaml'), 'r' ) as file:
            curr_yaml = file.read()

        fileName = datetime.now().strftime("%d%m%Y%h%m%s")

        with open(path.abspath('generated_specification/'+fileName+'.yaml'), 'w') as file:
            file.write(curr_yaml)
        
