import hashlib
import feedparser
from module.base import DataConfig, DictConfig, ListConfig, ModuleBase
from datetime import datetime

GMT0800_FORMAT = "%a, %d %b %Y %H:%M:%S +0800"
UPDATE_TIME = "Thu, 18 Sep 2024 16:33:40 +0800"

_now_time: datetime = None

def calc_lerptime(strptime: datetime):
    global _now_time
    return (strptime - _now_time).total_seconds()

def rss_sort(item):
    dateStr = item["published"]
    date = datetime.strptime(dateStr, GMT0800_FORMAT)
    return (False, -date.timestamp())

def string_to_md5(input_string: str):
    # 创建一个 md5 哈希对象
    md5_hash = hashlib.md5()

    # 更新哈希对象，必须将字符串编码为字节
    md5_hash.update(input_string.encode('utf-8'))

    # 获取十六进制表示的哈希值
    return md5_hash.hexdigest()

class _RSSUrl:
    def __init__(self, module, url: str, seconds: int):
        self._module = module
        self._url = url
        self._seconds = seconds
        self._over = False

    def parse(self):
        feed = feedparser.parse(self._url)
        if feed.bozo == 0 or feed.bozo is False:
            entries = [[], {}]
            # published = None
            for entry in feed.entries:
                seconds = self._module.calc_lerptime(datetime.strptime(entry.published, GMT0800_FORMAT))
                if seconds > 0:
                    md5 = string_to_md5(entry.link)
                    entries[0].append({
                        "web_title": feed.feed.title,
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.published,
                        "md5": md5,
                        "is_read": 0
                    })
                    entries[1][md5] = entry.summary
                else:
                    break

            # if published is not None:
            #     self._updateTimeStr = published
            #     self._nowTimeStruct = datetime.strptime(self._updateTimeStr, GMT0800_FORMAT)
                # self.setting()
            return entries
        return None


class RSSModule(ModuleBase):
    _nowTimeStruct: datetime
    _urls: list[_RSSUrl]

    _setting: DataConfig
    _history: ListConfig
    _summary: DictConfig

    def init(self):
        self._urls = []
        self._urls.append(_RSSUrl(self, "http://www.gcores.com/rss", 60*60*24))
        self._urls.append(_RSSUrl(self, "https://indienova.com/feed/", 60*60*24))
        self._setting = DataConfig("setting", self.name, {
            "updatetime": UPDATE_TIME,
            "count": 0,
            "delete_read": 1
        })
        self._history = ListConfig("history", self.name, True)
        self._summary = DictConfig("summary", self.name, False)

        # test
        # self._setting.load()
        # self._history.load()
        # self._summary.load()

        # self.refresh_item()

    def open(self):
        if self.is_first:
            self._setting.load()
            self._history.load()
            self._summary.load()

        self.refresh_item()
        return {
            "updatetime": self.updatetime,
            "history": self._history
        }

    def close(self):
        pass

    @property
    def updatetime(self):
        return self._setting.value("updatetime")

    @updatetime.setter
    def updatetime(self, value):
        self._setting.value("updatetime", value)

    def calc_lerptime(self, strptime: datetime):
        now_time = datetime.strptime(self.updatetime, GMT0800_FORMAT)
        return (strptime - now_time).total_seconds()

    def delete_item(self, key: str | int):
        self._history.earse_filter(lambda item: item["md5"] != key)
        self._summary.earse_key(key)

    def get_item(self, key: str | int):
        first_item = self._history.next_filter(lambda item: item["md5"] == key)
        if first_item is not None:
            first_item["is_read"] = 1
        return self._summary.get(key)

    def on_app_quit(self):
        self._setting.save()
        self._history.save()

        sorted_keys = []
        for v in self._history:
            sorted_keys.append(v["md5"])
        self._summary.save(sorted_keys=sorted_keys)

    def refresh_item(self):
        articles = []
        for p in self._urls:
            info = p.parse()
            if info is not None:
                articles.append(info)

        # 将新的提要内容写入本地文件
        if len(articles) > 0:
            for item in articles:
                self._history.extend(item[0])
                self._summary.update(item[1])
            self._setting.value("count", len(self._history))
            self.updatetime = datetime.now().strftime(GMT0800_FORMAT)
            print(f"RSS提要已保存, 拉取时间 {datetime.now().strftime(GMT0800_FORMAT)}")

