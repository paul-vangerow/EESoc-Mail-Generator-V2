import configparser
from graph import Graph


def main():

    # Load settings
    
    print("test!")
    

    

def generate_email():

    # Setup access token and so on.
    # Will send one specific YAML file which is modified by a flask front-end

    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']
    graph: Graph = Graph(azure_settings)
    
    print ( graph.get_user_token() ) # Temporary

main()