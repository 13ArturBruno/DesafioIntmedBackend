from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import datetime
from django.urls import reverse
import requests
from products.models import Processor, MotherBoard, VideoBoard, RamMemory, Brand
from .models import Order

class APITests(APITestCase):
    def setUp(self):
        #criando produtos no database.
        Brand.objects.create(name="Intel")
        Brand.objects.create(name="AMD")

        intel = Brand.objects.get(name="Intel")
        amd = Brand.objects.get(name="AMD")

        Processor.objects.create(product="Processador Intel Core i5", brand=intel)
        Processor.objects.create(product="Processador Intel Core i7", brand=intel)
        Processor.objects.create(product="Processador AMD Athlon", brand=amd)
        Processor.objects.create(product="Processador AMD Ryzen 7", brand=amd)

        RamMemory.objects.create(product="Hiper X", size=4)
        RamMemory.objects.create(product="Hiper X", size=8)
        RamMemory.objects.create(product="Hiper X", size=16)
        RamMemory.objects.create(product="Hiper X", size=32)
        RamMemory.objects.create(product="Hiper X", size=64)

        m1 = MotherBoard.objects.create(
            product="Placa Mãe ASRock Fatal",
            ramSlots=4,
            maxMemorySize=64,
            videoOnboard=True
        )
        m1.cpuSupport.add(intel,amd)
        m1.save()

        m2 = MotherBoard.objects.create(
            product="Placa Mãe Gigabyte",
            ramSlots=2,
            maxMemorySize=16,
            videoOnboard=False
        )
        m2.cpuSupport.add(amd)
        m2.save()

        m3 = MotherBoard.objects.create(
            product="Placa Mãe Asus Prime",
            ramSlots=2,
            maxMemorySize=16,
            videoOnboard=False
        )
        m3.cpuSupport.add(intel)
        m3.save()

        VideoBoard.objects.create(product="Placa de Video Radeon RX 580 8GB")
        VideoBoard.objects.create(product="Placa de Video PNY RTX 2060 6GB")
        VideoBoard.objects.create(product="Placa de Video Gigabyte Geforce GTX 1060 6GB")

    def test_listing_all_orders(self):
        url = 'http://localhost:8000/api/order/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listing_orders_with_data(self):
        url = 'http://localhost:8000/api/order/?email=teste@teste.com'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_orders_per_email(self):
        url = 'http://localhost:8000/api/order/?ordering=email'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_passing_correct_data(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [8,4],\"motherBoard\": {\"product\": \"Placa Mãe ASRock Fatal\"},\"videoBoard\": {\"product\": \"Placa de Video PNY RTX 2060 6GB\"}}"
        response = self.client.post(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_without_params(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [8,4],\"motherBoard\": {\"product\": \"Placa Mãe ASRock Fatal\"},\"videoBoard\": {\"product\": \"Placa de Video PNY RTX 2060 6GB\"}}"
        response = self.client.post(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_content_type_invalid(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [8,4],\"motherBoard\": {\"product\": \"Placa Mãe ASRock Fatal\"},\"videoBoard\": {\"product\": \"Placa de Video PNY RTX 2060 6GB\"}}"
        response = self.client.post(url, data=payload, content_type="application/text")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_invalid_params(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Invalido\"},\"ramMemory\": [8,4],\"motherBoard\": {\"product\": \"Placa Mãe ASRock Fatal\"},\"videoBoard\": {\"product\": \"Placa de Video PNY RTX 2060 6GB\"}}"
        response = self.client.post(url, data=payload, content_type="application/text")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_memory_capacity_exceeding_motherboard_limit(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [8,64],\"motherBoard\": {\"product\": \"Placa Mãe ASRock Fatal\"},\"videoBoard\": {\"product\": \"Placa de Video PNY RTX 2060 6GB\"}}"
        response = self.client.post(url, data=payload, content_type="application/text")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_amount_memory_greater_than_motherboard_slots(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [8,8,8,8,4],\"motherBoard\": {\"product\": \"Placa Mãe ASRock Fatal\"},\"videoBoard\": {\"product\": \"Placa de Video PNY RTX 2060 6GB\"}}"
        response = self.client.post(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_without_videoboard_and_without_onboard(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [8,4],\"motherBoard\": {\"product\": \"Placa Mãe Asus Prime\"},\"videoBoard\": {\"product\": \"\"}}"
        response = self.client.post(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_without_videoboard_and_with_onboard(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [8,4],\"motherBoard\": {\"product\": \"Placa Mãe ASRock Fatal\"},\"videoBoard\": {\"product\": \"\"}}"
        response = self.client.post(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_processor_without_support_motherboard(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [8,4],\"motherBoard\": {\"product\": \"Placa Mãe Gigabyte\"},\"videoBoard\": {\"product\": \"Placa de Video PNY RTX 2060 6GB\"}}"
        response = self.client.post(url, data=payload, content_type="application/json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_without_memory_ram(self):
        url = 'http://localhost:8000/api/order/'
        payload = "{\"email\": \"teste@teste.com\",\"processor\": {\"product\": \"Processador Intel Core i5\"},\"ramMemory\": [],\"motherBoard\": {\"product\": \"Placa Mãe ASRock Fatal\"},\"videoBoard\": {\"product\": \"Placa de Video PNY RTX 2060 6GB\"}}"
        response = self.client.post(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)





