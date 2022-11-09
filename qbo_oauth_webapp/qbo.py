import os
import json
import logging
import requests

from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.INFO)

AUTH_CONFIG_FILE_TEMPLATE = "~/.qb-api/%s-config-auth.json"

class QuickbooksConfig(object):

    def __init__(self, environment):
        self.qb_environment = environment
        self.logger = logging.getLogger(self.__class__.__name__)
        self.configure_request_with_retries()
        self.configure_settings()
        #self.auth_client = self.build_request_client(self.auth_config, self.access_config)

    def configure_request_with_retries(self):
        session = requests.Session()
        retries = Retry(total=20,
                        backoff_factor=0.1,
                        status_forcelist=[ 500, 502, 503, 504 ])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        self.request = session

    def configure_settings(self):
        self.logger.error("Configured environment: %s" % self.qb_environment)
        auth_config_filepath = os.path.expanduser(AUTH_CONFIG_FILE_TEMPLATE % self.qb_environment)
        self.auth_config = self.read_local_config(auth_config_filepath)

    def read_local_config(self, filepath):
        self.logger.error("Reading config filepath: %s" % filepath)
        with open(filepath, 'r') as openfile:
            data = json.load(openfile)
        return data

    def write_remote_config(self, endpoint, data):
        json_object = json.dumps(data, indent=4)
        self.logger.error("Writing remote config to endpoint: %s, data: %s" % (endpoint, json_object))
        resp = self.request.post(endpoint, data=data, verify=False)
        if resp.status_code != 200 or resp.text != "OK":
            self.logger.error("Could not write config access file: %s, %s" % (resp.status_code, resp.text))
        else:
            self.logger.error("Wrote config access file")

    def write_access_config(self, auth_client):
        if auth_client.access_token is not None and auth_client.refresh_token is not None and auth_client.realm_id is not None:
            data = {
                "access_token": auth_client.access_token,
                "refresh_token": auth_client.refresh_token,
                "realm_id": auth_client.realm_id,
                "server_access_token": self.auth_config['server_access_token'],
            }
            self.write_remote_config(self.auth_config['server_endpoint'], data)
        else:
            raise ValueError('Access token, refresh token, or realm id not specified.')
