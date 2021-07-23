from django.test import TestCase
import json
from django.test import Client

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PIK_test.settings')
django.setup()


class OrganisationTest(TestCase):
    client = Client()

    def test_success_create(self):
        response = self.client.post('/organisations/', {
            'name': 'ЛифтМастер',
            'email': 'liftmaster@mail.ru',
            'phone': '74950000001',
            'address': 'г. Москва, ул. Лифтовая, д. 5'
        })
        status_code = response.status_code

        self.assertEqual(status_code, 201)

    def test_fail_create(self):
        response = self.client.post('/organisations/', {
            'name': 'ЛифтМастер',
            'email': 'liftmaster',
            'phone': '74950000001',
            'address': 'г. Москва, ул. Лифтовая, д. 5'
        })
        status_code = response.status_code

        self.assertEqual(status_code, 400)

    def test_success_modify(self):
        self.client.post('/organisations/', {
            'name': 'ЛифтМастер',
            'email': 'liftmaster@mail.ru',
            'phone': '74950000001',
            'address': 'г. Москва, ул. Лифтовая, д. 5'
        })
        response = self.client.put('/organisation/1/', {
            'name': 'ЛифтМастер1',
            'email': 'liftmaster@mail.ru',
            'phone': '74950000001',
            'address': 'г. Москва, ул. Лифтовая, д. 6'
        }, content_type='application/json')
        status_code = response.status_code

        self.assertEqual(status_code, 200)


class ServiceTest(TestCase):
    def test_duplicate_check(self):
        self.client.post('/services/', {
            'name': 'name'
        })
        response = self.client.post('/services/', {
            'name': 'name',
        })
        status_code = response.status_code

        self.assertEqual(status_code, 400)


class GridTest(TestCase):
    def test_coordinate_info(self):
        self.client.get('/init_grid/')

        self.client.post('/organisations/', {
            'name': 'ЛифтМастер',
            'email': 'liftmaster@mail.ru',
            'phone': '74950000001',
            'address': 'г. Москва, ул. Лифтовая, д. 5'
        })
        self.client.post('/organisations/', {
            'name': 'РемЛифт',
            'email': 'remlift@mail.ru',
            'phone': '74950000002',
            'address': 'г. Москва, ул. Лифтовая, д. 15'
        })

        self.client.post('/services/', {
            'name': 'Обслуживание лифтов',
        })
        self.client.post('/services/', {
            'name': 'Монтаж лифтов',
        })

        self.client.post('/areas/', {
            'organisation': 1,
            'name': 'Область 1',
            'polygon': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [
                            37.74078369140625,
                            55.97072426231743
                        ],
                        [
                            37.59246826171875,
                            55.94919982336744
                        ],
                        [
                            37.61993408203125,
                            55.85989956952263
                        ],
                        [
                            37.79296875,
                            55.85219164310742
                        ],
                        [
                            37.82592773437499,
                            55.947661905375064
                        ],
                        [
                            37.74078369140625,
                            55.97072426231743
                        ]
                    ]
                ]
            }
        }, content_type='application/json')
        self.client.post('/areas/', {
            'organisation': 2,
            'name': 'Область 2',
            'polygon': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [
                            37.7215576171875,
                            55.88917574736247
                        ],
                        [
                            37.606201171875,
                            55.76266790754882
                        ],
                        [
                            37.85064697265625,
                            55.76112258901995
                        ],
                        [
                            37.7215576171875,
                            55.88917574736247
                        ]
                    ]
                ]
            }
        }, content_type='application/json')

        self.client.post('/costs/', {
            'service': 1,
            'area': 1,
            'value': 500,
        })
        self.client.post('/costs/', {
            'service': 2,
            'area': 2,
            'value': 600,
        })

        response = self.client.get('/coordinate_info/latitude=37.7215576171875&longitude=55.867605966997786/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        json_data = response.content
        data = json.loads(json_data)
        self.assertEqual(len(data), 2)
