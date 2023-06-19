from datetime import datetime

from easy.singleton import Singleton

PATH = r".\Debug.log"

class Log_(Singleton):
    def __init__(self):
        self._stash = []
        self._f = open(PATH, "w+", encoding="utf-8")
        self._stash.append(datetime.now())
    def n(self, s, *args):
        self._append("[NORMAL]", self._join(s, *args))
    def w(self, s, *args):
        self._append("[WARN]", self._join(s, *args))
    def e(self, s, *args):
        self._append("[ERROR]", self._join(s, *args))
    # format          -> {}
    # %               -> %s
    def _join(self, s, *args):
        if "%s" not in s:
            s += str(args)
        else:
            s = s % args
        return s
    def _append(self, head, s):
        timestamp = datetime.strftime(datetime.now(), '%H:%M:%S')
        self._stash.append("{} {} {}".format(timestamp, head, s))
    def pop(self):
        ret = []
        for s in self._stash:
            ret.append(s)
            self._f.write(s)
        self._f.flush()
        self._stash.clear()
        return ret
    def closeEvent(self):
        for s in self._stash:
            self._f.write(s)
        self._f.close()


Log = Log_()