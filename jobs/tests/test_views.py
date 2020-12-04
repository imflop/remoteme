from django.test import TestCase
from django.urls import reverse


class MainPageTest(TestCase):
    def test_main_page_exist(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 200)

    def test_main_page_context_has_filter(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertIsNotNone(response.context['filter'])

    def test_main_page_context_has_paginator(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertIsNotNone(response.context['paginator'])

    def test_create_advert_page_exist(self):
        response = self.client.get(reverse('jobs:create'))
        self.assertEqual(response.status_code, 200)

    def test_create_advert_page_has_form(self):
        response = self.client.get(reverse('jobs:create'))
        self.assertIsNotNone(response.context['form'])
