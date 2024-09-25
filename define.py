from enum import Enum, auto

# 定义插件的类型枚举
# class ModuleType(Enum):
#     RSS = auto()  # RSS 订阅插件

def singleton(cls):
   instances = {}

   def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
   return get_instance