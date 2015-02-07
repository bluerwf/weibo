import settings
from flask import Flask, jsonify, Request

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

    def _configure(self):
        # default
        self.config.from_object(settings)
        # local settings
        if OVERRIDES:
            self.config.from_object(OVERRIDES)
