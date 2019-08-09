from pytest_requests.testcase import TestCase
from tests.httpbin.api import *


class TestUpdatePostBody(TestCase):

    def run_test(self):
        session = self.create_session()

        kwargs = {
            "custname": "leo",
            "custtel": "18699999999"
        }
        form_data_body = self.parse_body(ApiHttpBinPostHtmlForm.body, kwargs)
        ApiHttpBinPostHtmlForm(session)\
            .set_headers({"User-Agent": "pytest-requests"})\
            .set_body(form_data_body)\
            .run()\
            .assert_status_code(200)\
            .assert_header("Content-Type", "application/json")\
            .assert_body("form.comments", "hello world")\
            .assert_body("form.topping[0]", "cheese")\
            .assert_body("form.custname", "leo")\
            .assert_body("form.custtel", "18699999999")

        json_body = self.parse_body(ApiHttpBinPostJson.body, kwargs)
        ApiHttpBinPostJson(session)\
            .set_headers({"User-Agent": "pytest-requests"})\
            .set_body(json_body)\
            .run()\
            .assert_status_code(200)\
            .assert_header("Content-Type", "application/json")\
            .assert_body("json.comments", "hello world")\
            .assert_body("json.topping[0]", "cheese")\
            .assert_body("json.custname", "leo")\
            .assert_body("json.custtel", "18699999999")


class TestLoginStatus(TestCase):

    def run_test(self):
        session = self.create_session()

        # step1: login and get cookie
        ApiHttpBinGetSetCookies(session)\
            .set_querystring({"freeform": "567"})\
            .run()

        # step2: request another api, check cookie
        resp = ApiHttpBinPost(session)\
            .set_body({"abc": 123})\
            .run()\
            .get_response_object()

        request_headers = resp.request.headers
        assert "freeform=567" in request_headers["Cookie"]
