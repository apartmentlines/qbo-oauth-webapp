import os
import json
import logging

logging.basicConfig(level=logging.INFO)

AUTH_CONFIG_FILE_TEMPLATE = "~/.qb-api/%s-config-auth.json"
ACCESS_CONFIG_FILE_TEMPLATE = "~/.qb-api/%s-config-access.json"

class QuickbooksConfig(object):

    def __init__(self, environment):
        self.qb_environment = environment
        self.logger = logging.getLogger(self.__class__.__name__)
        self.configure_settings()
        #self.auth_client = self.build_request_client(self.auth_config, self.access_config)

    def configure_settings(self):
        self.logger.error("Configured environment: %s" % self.qb_environment)
        auth_config_filepath = os.path.expanduser(AUTH_CONFIG_FILE_TEMPLATE % self.qb_environment)
        #access_config_filepath = os.path.expanduser(ACCESS_CONFIG_FILE_TEMPLATE % self.qb_environment)
        self.auth_config = self.read_config(auth_config_filepath)
        #self.access_config = self.read_config(access_config_filepath)

    def read_config(self, filepath):
        self.logger.error("Reading config filepath: %s" % filepath)
        with open(filepath, 'r') as openfile:
            data = json.load(openfile)
        return data

    def write_config(self, filepath, data):
        json_object = json.dumps(data, indent=4)
        with open(filepath, "w") as outfile:
            self.logger.error("Writing config filepath: %s, data: %s" % (filepath, data))
            outfile.write(json_object)

    def write_access_config(self, auth_client):
        if auth_client.access_token is not None and auth_client.refresh_token is not None and auth_client.realm_id is not None:
            access_config_filepath = os.path.expanduser(ACCESS_CONFIG_FILE_TEMPLATE % self.qb_environment)
            data = {
                "access_token": auth_client.access_token,
                "refresh_token": auth_client.refresh_token,
                "realm_id": auth_client.realm_id,
            }
            self.write_config(access_config_filepath, data)
        else:
            raise ValueError('Access token, refresh token, or realm id not specified.')
