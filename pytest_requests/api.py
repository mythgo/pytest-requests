
import copy
import json

import requests

from pytest_requests.response import ResponseObject


class BaseApi(object):

    method = "GET"
    url = ""
    params = None
    headers = None
    cookies = None
    body = None

    # config part
    verify = None
    auth = None
    timeout = None
    proxies = None
    allow_redirects = True
    hooks = None
    stream = None
    cert = None

    def __init__(self):
        self.resp_obj = None

    def set_param(self, key, value):
        """ update request param
        """
        param = {key: value}
        return self.set_params(**param)

    def set_params(self, **params):
        """ update request params
        """
        if not hasattr(self, "_params"):
            self._params = copy.deepcopy(self.__class__.params or {})

        self._params.update(params)
        return self

    def set_header(self, key, value):
        """ update request header
        """
        header = {key: value}
        return self.set_headers(**header)

    def set_headers(self, **headers):
        """ update request headers
        """
        if not hasattr(self, "_headers"):
            self._headers = copy.deepcopy(self.__class__.headers or {})

        self._headers.update(headers)
        return self

    def set_cookie(self, key, value):
        """ update request cookie
        """
        cookie = {key: value}
        return self.set_cookies(**cookie)

    def set_cookies(self, **kwargs):
        """ update request cookies
        """
        if not hasattr(self, "_cookies"):
            self._cookies = copy.deepcopy(self.__class__.cookies or {})

        self._cookies.update(kwargs)
        return self

    def set_body(self, body):
        """ set request body
        """
        self.body = body
        return self

    def run(self, session = None):

        session = session or requests.sessions.Session()
        self._headers = getattr(self, "_headers", None) or self.headers

        kwargs = {
            "params": getattr(self, "_params", None) or self.params,
            "headers": self._headers,
            "cookies": getattr(self, "_cookies", None) or self.cookies
        }

        if isinstance(self.body, dict):
            if self._headers and \
                self._headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
                kwargs["data"] = json.dumps(self.body)
            else:
                kwargs["json"] = self.body
        else:
            kwargs["data"] = self.body

        _resp_obj = session.request(
            self.method,
            self.url,
            **kwargs
        )
        self.resp_obj = ResponseObject(_resp_obj)
        return self

    def extract_response(self, field):
        return self.resp_obj.extract(field)

    def __assert_with_expected(self, actual_value, expected_value):
        assert actual_value == expected_value
        return self

    def assert_(self, field, expected_value):
        """ universal assertion with expected value

        Params:
            field (str): any field in response
                status_code
                headers.Content-Type
                body.details[0].name

        """
        return self.__assert_with_expected(
            self.resp_obj.extract(field),
            expected_value
        )

    def assert_status_code(self, expected_value):
        return self.assert_("status_code", expected_value)

    def assert_header(self, field, expected_value):
        """ assert header filed equivalent to expected value

        Params:
            field (str): case insensitive string, content-type or Content-Type are both okay.
            expected_value: expected value in any type

        """
        return self.__assert_with_expected(
            self.resp_obj.extract_header(field),
            expected_value
        )

    def assert_body(self, field, expected_value):
        """ assert body filed equivalent to expected value

        Params:
            field (str): jmespath string
            expected_value: expected value in any type

        """
        return self.__assert_with_expected(
            self.resp_obj.extract_body(field),
            expected_value
        )

    def get_response(self):
        return self.resp_obj
