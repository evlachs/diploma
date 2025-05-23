from idlelib.debugger_r import restart_subprocess_debugger

import yaml


class ConfigHandler:
    def __init__(self, config_path: str):
        self.path = config_path
        self.config = self.__read_config_file()

    def __read_config_file(self) -> dict:
        with open(self.path) as file:
            config = yaml.safe_load(file)
        return config

    def get_service_attributes_params(self):
        """NEED TO UPDATE"""
        pass
        # result = {}
        # def extract_config_params(config):
        #     if isinstance(config, list):
        #         for value in config:
        #             extract_config_params(value)
        #     elif isinstance(config, dict):
        #         for k, v in config.items():
        #             result.join(v)
        #             extract_config_params(v)
        #     else:
        #         result.join(config)
        # extract_config_params(self.config['services'])
        # return result
