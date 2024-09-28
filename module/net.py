from flask import Flask

class _AppNet:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(_AppNet, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._app: Flask = None

    def run(self, app, debug=False):
        self._app = app
        self._app.run(host='0.0.0.0', port=5000, debug=debug)

    @property
    def app(self) -> Flask:
        return self._app


AppNet = _AppNet()