import json
import os
import sys
import time
import asyncio
from collections import OrderedDict
from typing import Final

def read_json_file(file_path: str, default_data: dict = {}):
    """ 读取 JSON 文件，如果文件不存在则创建一个新的 JSON 文件并写入默认内容 """

    if not os.path.exists(file_path):
        # 如果文件不存在，则创建文件并写入默认数据
        print(f"File '{file_path}' not found. Creating a new file with default data.")
        # with open(file_path, 'w', encoding='utf-8') as file:
        #     json.dump(default_data, file, indent=4)
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

def get_size(d):
    size = 0  # 字典本身的大小
    if type(d) == dict:
        for key, value in d.items():
            size += sys.getsizeof(key)  # 键的大小
            size += get_size(value)  # 值的大小
    elif type(d) == list:
        for v in d:
            size += get_size(v)
    else:
        size += sys.getsizeof(d)
    return size



SPLIT_SIZE: Final = 100*1024
NEW_INDEX: Final = -1
class BaseConfig:
    def __init__(self, file: str, name: str):
        self._file = file
        self._name = name

    def json_load(self, key=None, default=None):
        file_path = ""
        if key is not None:
            file_path = './static/json/{}_{}_{}.json'.format(self._name, self._file, key)
        else:
            file_path = './static/json/{}_{}.json'.format(self._name, self._file)

        if not os.path.exists(file_path):
            return default

        start_time = time.time()  # 记录开始时间

        data = None
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算耗时
        print(f"json.load{file_path} cost: {elapsed_time:.6f}秒")
        return data

    def json_save(self, data, key=None):
        file_path = ""
        if key is not None:
            file_path = './static/json/{}_{}_{}.json'.format(self._name, self._file, key)
        else:
            file_path = './static/json/{}_{}.json'.format(self._name, self._file)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

class ListConfig(BaseConfig):
    def __init__(self, file: str, name: str, single: bool):
        super().__init__(file, name)

        self._items = []
        self._single = single
        # self._sorted = sort_f

        if not single:
            self._keys: dict = {}
            self._loaded_index: dict = {}

    def load(self):
        if self._single:
            self._items = self.json_load(default=[])
            return

        self._keys = self.json_load('keys', default={})

    def load_part(self, index):
        result = []
        if index < len(self._keys):
            if self._loaded_index.get(index, False) == False:
                result = self.json_load(str(index), default=[])
                self.extend(result)
                self._loaded_index[index] = True
        return result

    def get_part(self, index):
        self.load_part(index)

        result = []
        for v in self._items:
            if self._keys[v["id"]] == index:
                result.append(v)
        return result

    def save(self):
        if self._single:
            self.json_save(self._items)
            return

        size = 0
        ret = []
        index = 0
        for v in self._items:
            size += get_size(v)
            ret.append(v)
            self._keys[v["id"]] = index
            if size > SPLIT_SIZE or v == self._items[len(self._items) - 1]:
                size = 0
                self.json_save(ret, str(index))
                index = index + 1
                ret.clear()
        self.json_save(self._keys, "keys")

    def __getitem__(self, index):
        """支持索引访问"""
        return self._items[index]

    def __iter__(self):
        """支持遍历功能"""
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def extend(self, item_list: list):
        if self._single:
            self._items.extend(item_list)
            return

        for v in item_list:
            if self._keys.get(v["id"]) == None:
                self._keys[v["id"]] = NEW_INDEX
                self._items.append(v)

    def earse_filter(self, f):
        self._items = list(filter(f, self._items))

    def next_filter(self, f):
        return next((item for item in self._items if f(item)), None)

    def sort(self, f):
        self._items = sorted(self._items, key=f)

    def remove(self, v):
        return self._items.remove(v)

    @property
    def items(self):
        return self._items

class DictConfig(BaseConfig):
    def __init__(self, file: str, name: str, single: bool):
        super().__init__(file, name)

        self._single = single
        self._items = OrderedDict()
        if single:
            pass
        else:
            self._keys: dict = {}
            self._loaded_index: dict = {}

    def load(self):
        if self._single:
            self._items = self.json_load(default=OrderedDict())
            return

        self._keys = self.json_load('keys', default=OrderedDict()) # key to index

    def load_part(self, key):
        index = self._keys.get(key)
        if index is not None:
            if self._loaded_index.get(index, False) == False:
                self._items.update(self.json_load(str(index), default=OrderedDict()))
                self._loaded_index[index] = True

    def save(self, sorted_keys=None):
        if self._single:
            self.json_save(self._items)
            return
        keys = self._items.keys()
        if sorted_keys is None:
            sorted_keys = keys

        size = 0
        index = 0
        ret = {}
        self._keys.clear()
        for key in sorted_keys:
            if self._items.get(key):
                size += get_size(self._items[key])
                ret[key] = self._items[key]
                self._keys[key] = index
                if size > SPLIT_SIZE or key == sorted_keys[len(sorted_keys) - 1]:
                    self.json_save(ret, str(index))
                    size = 0
                    index = index + 1
                    ret.clear()
        self.json_save(self._keys, "keys")

    def get(self, key):
        self.load_part(key)
        return self._items.get(key)

    def earse_key(self, key):
        del self._keys[key]
        self.load_part(key)
        del self._items[key]

    def update(self, v):
        self._items.update(v)

    def items(self):
        return self._items.items()

    def values(self):
        return self._items.values()

    def __getitem__(self, index):
        """支持索引访问"""
        return self._items[index]

    def __sizeof__(self) -> int:
        return len(self._items)

class DataConfig(BaseConfig):
    def __init__(self, file: str, name: str, default):
        super().__init__(file, name)

        self._items = default

    def load(self):
        self._items = self.json_load(default=self._items)

    def save(self):
        self.json_save(self._items)

    def value(self, k, v=None):
        if v is None:
            return self._items[k]
        self._items[k] = v

class ModuleBase:
    def __init__(self, name):
        self.name = name
        self._config = None
        self.is_first = True
        # self._config_reader = ModuleConfigReader(name, self.config_default())
        # self._resources: ModuleResource = ModuleResource()

    def init(self):
        raise NotImplementedError("Module init should be overridden.")

    def open(self):
        raise NotImplementedError("Module open should be overridden.")

    def close(self):
        raise NotImplementedError("Module close should be overridden.")

    def delete_item(self, key: str | int):
        pass

    def get_item(self, key: str | int):
        pass

    # @property
    # def resources(self):
    #     return self._resources

    # @property
    # def config(self):
    #     if self._config is None:
    #         self._config = {}
    #         for k, v in self.config_default().items():
    #             config_file = './module/{}/{}.json'.format(self.name, k)
    #             self._config[k] = v
    #         # config_file = '{}.json'.format(self.name)
    #         # self._config = read_json_file(config_file, self.config_default())
    #     return self._config

    # def save_config(self):
    #     save_data = self._config
    #     file_path = '{}.json'.format(self.name)
    #     with open(file_path, 'w', encoding='utf-8') as file:
    #         json.dump(save_data, file, indent=4)

    # def config_default(self):
    #     return {}

    def on_app_quit(self):
        raise NotImplementedError("Module on_app_quit should be overridden.")

    def __str__(self):
        return f"{self.name} (Type: {self.name})"