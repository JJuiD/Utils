import hashlib
import feedparser
from plugin.base import Plugin
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
    def __init__(self, plugin, url: str, seconds: int):
        self._plugin = plugin
        self._url = url
        self._seconds = seconds
        self._over = False

    def parse(self):
        feed = feedparser.parse(self._url)
        if feed.bozo == 0 or feed.bozo is False:
            entries = [[], {}]
            # published = None
            for entry in feed.entries:
                seconds = self._plugin.calc_lerptime(datetime.strptime(entry.published, GMT0800_FORMAT))
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


class RSSPlugin(Plugin):
    _nowTimeStruct: datetime
    _urls: list[_RSSUrl]

    def init(self):
        self._urls = []
        self._urls.append(_RSSUrl(self, "http://www.gcores.com/rss", 60*60*24))
        self._urls.append(_RSSUrl(self, "https://indienova.com/feed/", 60*60*24))
        self.refresh_item()

    def open(self):
        self.refresh_item()
        return {
            "updatetime": self.updatetime,
            "history": self.history
        }

    def close(self):
        pass

    @property
    def updatetime(self):
        return self.config["updatetime"]

    @property
    def history(self) -> list:
        return self.config["history"]
    
    @property
    def summary(self) -> dict:
        return self.config["summary"]

    @updatetime.setter
    def updatetime(self, value):
        self.config["updatetime"] = value

    def calc_lerptime(self, strptime: datetime):
        now_time = datetime.strptime(self.updatetime, GMT0800_FORMAT)
        return (strptime - now_time).total_seconds()
    
    def delete_item(self, key: str | int):
        self.config["history"] = list(filter(lambda item: item["md5"] != key, self.history))
        del self.summary[key]

    def get_item(self, key: str | int):
        first_item = next((item for item in self.history if item['md5'] == key), None)
        if first_item is not None:
            first_item["is_read"] = 1
        return self.summary.get(key)

    def refresh_item(self):
        articles = []
        for p in self._urls:
            info = p.parse()
            if info is not None:
                articles.append(info)

        # 将新的提要内容写入本地文件
        if len(articles) > 0:
            for item in articles:
                self.history.extend(item[0])
                self.summary.update(item[1])
            self.updatetime = datetime.now().strftime(GMT0800_FORMAT)
            print(f"RSS提要已保存, 拉取时间 {datetime.now().strftime(GMT0800_FORMAT)}")

    def config_default(self):
        return {
            "updatetime": UPDATE_TIME,
            "history": [],
            "summary": {}
        }
