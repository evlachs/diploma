import yaml


class Config:
    def __init__(self, config_path: str):
        self.__path = config_path
        self.config_params = self.__read_config_file()
        self.classification_params = self.__get_classification_params()

    def __read_config_file(self) -> dict:
        with open(self.__path) as file:
            config = yaml.safe_load(file)
        return config

    def __get_classification_params(self) -> dict:
        res = {}
        def extract_classification_params(config, result, count):
            if count == 3:
                res[result.lstrip('.')] = config[0] | config[1]
            elif isinstance(config, dict):
                count += 1
                for value in config:
                    result += f'.{value}'
                    extract_classification_params(config[value], result, count)
            else:
                for value in config:
                    extract_classification_params(value, result, count)
            return res
        extract_classification_params(self.config_params['services'], '', 0)
        return res
