from django.test import Client
from django.test import TestCase
from django.http import Http404


class AccordanceTestCase(TestCase):
    fixtures = ['fixtures.json']
    def setUp(self):
        pass

    def test_filter_category_fine(self):
        c = Client()
        response = c.get('/api/catalog/', {'categories': '1,2,3'})
        self.assertEqual(response.status_code, 200)

    def test_filter_category_noninteger_val_fail(self):
        c = Client()
        response = c.get('/api/catalog/', {'categories': '1,2,a'})
        self.assertEqual(response.status_code, 400)

    def test_filter_category_negative_val_fail(self):
        c = Client()
        response = c.get('/api/catalog/', {'categories': '1,2,-5'})
        self.assertEqual(response.status_code, 400)

    def test_filter_limit_fine(self):
        c = Client()
        response = c.get('/api/catalog/', {'limit': '10'})
        self.assertEqual(response.status_code, 200)

    def test_filter_limit_negative_val_fail(self):
        c = Client()
        response = c.get('/api/catalog/', {'limit': '-10'})
        self.assertEqual(response.status_code, 400)

    def test_filter_limit_noninteger_val_fail(self):
        c = Client()
        response = c.get('/api/catalog/', {'limit': 'a'})
        self.assertEqual(response.status_code, 400)

    def test_filter_offset_fine(self):
        c = Client()
        response = c.get('/api/catalog/', {'offset': '0'})
        self.assertEqual(response.status_code, 200)

    def test_filter_offset_negative_val_fail(self):
        c = Client()
        response = c.get('/api/catalog/', {'offset': '-5'})
        self.assertEqual(response.status_code, 400)

    def test_filter_offset_noninteger_val_fail(self):
        c = Client()
        response = c.get('/api/catalog/', {'offset': 'a'})
        self.assertEqual(response.status_code, 400)

    def test_filter_offset_with_limit_fine(self):
        c = Client()
        response = c.get('/api/catalog/', {'offset': '0', 'limit': '10'})
        self.assertEqual(response.status_code, 200)

    def test_filter_offset_with_limit_with_category_fine(self):
        c = Client()
        response = c.get('/api/catalog/', {'categories': '1,2,-5', 'offset': 'a', 'limit': '-10'})
        self.assertEqual(response.status_code, 400)

    def test_filter_offset_with_limit_with_category_fail(self):
        c = Client()
        response = c.get('/api/catalog/', {'categories': '1,2,-5', 'offset': 'a', 'limit': '-10'})
        self.assertEqual(response.status_code, 400)

