import configparser
config = configparser.ConfigParser()
config.read('/home/anhbt/Documents/github/sample_socket/dist/config.ini')

HOST = config['DEFAULT']['HOST']
PORT = int(config['DEFAULT']['PORT'])
PWD_FOLDER_IMAGE = config['DEFAULT']['PWD_FOLDER_IMAGE']
PWD_FOLDER_UI_IMAGE = config['DEFAULT']['PWD_FOLDER_UI_IMAGE']
