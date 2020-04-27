import json

from aiohttp import hdrs, web


class AioRestException(Exception):
    pass


class ValidationError(web.HTTPBadRequest):
    def __init__(self, detail=None, **kwargs):
        super().__init__(**kwargs)
        self._headers[hdrs.CONTENT_TYPE] = "application/json"
        self.text = json.dumps(detail)


class ObjectNotFound(web.HTTPNotFound):
    def __init__(self, detail: str = None, **kwargs):
        super().__init__(**kwargs)
        self._headers[hdrs.CONTENT_TYPE] = "application/json"
        self.text = json.dumps({"error": detail or "Not found"})
