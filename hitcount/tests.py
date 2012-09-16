from __future__ import unicode_literals, print_function

import json

from django.conf.urls import patterns, include, url
from django.test import TestCase
from django.test.client import Client

from .models import HitCount, BlacklistIP

urlpatterns = patterns("",
    url(r"^hit$", "hitcount.views.update_hit_count_ajax"),
)

class AjaxViewTestCase(TestCase):
    urls = "hitcount.tests"

    def setUp(self):
        self.dummy_object_1 = BlacklistIP.objects.create(ip="0.0.0.0")
        self.dummy_object_2 = BlacklistIP.objects.create(ip="0.0.0.1")
        self.hitcount_1 = HitCount.objects.get_for_object(self.dummy_object_1)
        self.hitcount_2 = HitCount.objects.get_for_object(self.dummy_object_2)

    def _request(self, method="post", client=None, is_ajax=True, pk=0):
        client = client or Client()
        do_request = getattr(client, method)
        kwargs = {}
        if is_ajax:
            kwargs["HTTP_X_REQUESTED_WITH"] = "XMLHttpRequest"

        return do_request("/hit", {"hitcount_pk": pk}, **kwargs)

    def test_get_should_return_405(self):
        resp = self._request(method="get", pk=self.hitcount_1.pk)
        self.assertEqual(resp.status_code, 405)

    def test_should_accept_ajax_request_only(self):
        resp = self._request(is_ajax=False, pk=self.hitcount_1.pk)
        self.assertEqual(resp.status_code, 400)

    def test_should_return_error_for_invalid_pk(self):
        resp = self._request(pk=65535)
        self.assertEqual(resp.status_code, 400)

    def test_should_increase_hits(self):
        pk = self.hitcount_1.pk
        old_hits = HitCount.objects.get(pk=pk).hits
        
        resp = self._request(pk=pk)
        self.assertEqual(resp.status_code, 200)
        
        new_hits = HitCount.objects.get(pk=pk).hits
        self.assertEqual(new_hits, old_hits + 1)

    def test_should_only_increase_once_for_single_client(self):
        pk = self.hitcount_1.pk
        old_hits = HitCount.objects.get(pk=pk).hits
        client = Client()

        resp = self._request(pk=pk, client=client)
        self.assertEqual(resp.status_code, 200)
        resp = self._request(pk=pk, client=client)
        self.assertEqual(resp.status_code, 200)

        new_hits = HitCount.objects.get(pk=pk).hits
        self.assertEqual(new_hits, old_hits + 1)

    def test_should_increase_both_object_for_single_client(self):
        pks = [self.hitcount_1.pk, self.hitcount_2.pk]
        old_hits = [HitCount.objects.get(pk=pk).hits for pk in pks]
        client = Client()

        resp = self._request(pk=pks[0], client=client)
        self.assertEqual(resp.status_code, 200)
        resp = self._request(pk=pks[1], client=client)
        self.assertEqual(resp.status_code, 200)

        new_hits = [HitCount.objects.get(pk=pk).hits for pk in pks]
        self.assertEqual(new_hits[0], old_hits[0] + 1)
        self.assertEqual(new_hits[1], old_hits[1] + 1)

    def test_should_return_correct_hits_to_client(self):
        pk = self.hitcount_1.pk
        resp = self._request(pk=pk)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        new_hits = HitCount.objects.get(pk=pk).hits
        self.assertEqual(int(data["hits"]), new_hits)
