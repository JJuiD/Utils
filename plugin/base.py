import json
import os
from define import PluginType

def read_json_file(file_path: str, default_data: dict = {}):
    """ 读取 JSON 文件，如果文件不存在则创建一个新的 JSON 文件并写入默认内容 """

    if not os.path.exists(file_path):
        # 如果文件不存在，则创建文件并写入默认数据
        print(f"File '{file_path}' not found. Creating a new file with default data.")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(default_data, file, indent=4)
        return default_data

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


class PluginConfig:
    def to_json(self):
        raise NotImplementedError("PluginConfig to_json should be overridden.")

    
class Plugin:
    def __init__(self, name):
        self.name = name

        self._config = None
        # self._resources: PluginResource = PluginResource()

    def init(self):
        raise NotImplementedError("Plugin init should be overridden.")

    def open(self):
        raise NotImplementedError("Plugin open should be overridden.")

    def close(self):
        raise NotImplementedError("Plugin close should be overridden.")
    
    def delete_item(self, key: str | int):
        pass

    def get_item(self, key: str | int):
        pass

    # @property
    # def resources(self):
    #     return self._resources

    @property
    def config(self):
        if self._config is None:
            config_file = '{}.json'.format(self.name)
            self._config = read_json_file(config_file, self.config_default())
        return self._config

    def save_config(self):
        save_data = self._config
        file_path = '{}.json'.format(self.name)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(save_data, file, indent=4)

    def config_default(self):
        return {}
    
    def on_app_quit(self):
        self.save_config()

   

    def __str__(self):
        return f"{self.name} (Type: {self.name})"