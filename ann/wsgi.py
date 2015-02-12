import settings
from flask import Flask
from db import AccountDB, MessageDB

# overriding the default settings
try:
    import settings_local
    OVERRIDES = settings_local
except ImportError:
    OVERRIDES = None

class Weibo(Flask):
    """
    Main WSGI application for the webservice.
        - Configures settings
        - Enables authentication middleware
        - Returns all exceptions as JSON documents
    """

    def __init__(self, *args, **kwargs):
        super(Weibo, self).__init__(*args, **kwargs)
        self._configure()
        self._config_db()

    def _configure(self):
        # default
        self.config.from_object(settings)
        # local settings
        if OVERRIDES:
            self.config.from_object(OVERRIDES)

    def _config_db(self):
        _DB = "/var/weibo/weibo.db"
        self.acc = AccountDB(self.config.get('DB', _DB))
        self.msg = MessageDB(self.config.get('DB', _DB))
