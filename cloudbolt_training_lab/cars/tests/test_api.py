from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cars import models
from cars.models import Make, Manufacturer, Trim


# Create a class to test the manufacturer serializer and view
class ManufacturerTest(APITestCase):
    def setUp(self):
        # Create a manufacturer
        Manufacturer.objects.create(manufacturer="Ford")
        Manufacturer.objects.create(manufacturer="Toyota")

    def test_get_manufacturer(self):
        # Get the manufacturer
        response = self.client.get(reverse("manufacturer-list"))
        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the number of objects
        self.assertEqual(len(response.data), 2)

    def test_create_manufacturer(self):
        url = reverse("manufacturer-list")
        data = {"manufacturer": "Honda"}
        response = self.client.post(url, data)
        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check the number of objects
        self.assertEqual(len(Manufacturer.objects.all()), 3)
        # Check the name of the manufacturer
        # self.assertEqual(response.data[0]['manufacturer'], 'Honda')

    def test_update_manufacturer(self):
        url = reverse("manufacturer-detail", args=["Ford"])
        data = {"manufacturer": "Toyota"}
        # Update the manufacturer
        # request = factory.p
        response = self.client.put(url, data)
        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the name of the manufacturer
        self.assertEqual(response.data["manufacturer"], "Toyota")

    def test_delete_manufacturer(self):
        url = reverse("manufacturer-detail", args=["Ford"])
        # Delete the manufacturer
        response = self.client.delete(url)
        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that the manufacturer is deleted
        with self.assertRaises(Manufacturer.DoesNotExist):
            Manufacturer.objects.get(manufacturer="Ford")


class VehicleTests(APITestCase):
    def setUp(self):
        Manufacturer.objects.create(manufacturer="Chevrolet")
        Make.objects.create(manufacturer=Manufacturer.objects.get(manufacturer="Chevrolet"),
                            vehicle_model="Malibu")

    # test to ensure that the vehicle object is successfully created
    def test_get_vehicles(self):
        url = reverse("vehicle-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["make"], "Malibu")

    def test_create_vehicle(self):
        url = reverse("vehicle-list")
        data = {"manufacturer": "Chevrolet", "make": "Corvette"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Make.objects.get(vehicle_model='Corvette').make, "Corvette")

    def test_update_vehicle(self):
        url = reverse("vehicle-detail", args=['Malibu'])
        response = self.client.get(url)
        data = response.data
        response.data["make"] = "Corvette"

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Make.objects.get(vehicle_model='Corvette').make, "Corvette")

    def test_delete_vehicle(self):
        url = reverse("vehicle-detail", args=['Malibu'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Make.objects.count(), 0)

    # test to ensure that a vehicle model cannot be created without a manufacturer
    def test_vehicle_manufacturer(self):
        url = reverse("vehicle-list")
        data = {"make": "Corvette"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test to ensure that a vehicle model cannot be created without a vehicle model
    def test_vehicle_duplicates(self):
        url = reverse("vehicle-list")
        data = {"manufacturer": "Chevrolet"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test to ensure duplicate vehicle models cannot be created
    def test_vehicle_model_duplicate(self):
        Make.objects.create(
            manufacturer=Manufacturer.objects.get(manufacturer="Chevrolet"),
            vehicle_model="Impala",
        )

        url = reverse("vehicle-list")
        data = {"manufacturer": "Chevrolet", "make": "Impala"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Create a class to test the Trim serializer and view
class TrimTests(APITestCase):
    def setUp(self):
        Manufacturer.objects.create(manufacturer="Chevrolet")
        manufacturer=Manufacturer.objects.get(manufacturer="Chevrolet")
        Make.objects.create(manufacturer=manufacturer,
                            vehicle_model="Malibu")
        vehicle_model = Make.objects.get(vehicle_model="Malibu")
        Trim.objects.create(vehicle_model=vehicle_model, manufacturer=manufacturer, trim_model="base")

    def test_get_trims(self):
        url = reverse("trim-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["trim"], "base")

    def test_create_trim(self):
        url = reverse("trim-list")
        response = self.client.get(url)
        data = response.data
        data["trim"] = "Sport"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trim.objects.get(trim_model='Malibu').trim, "Sport")

    def test_update_trim(self):
        url = reverse("trim-detail", args=['Malibu'])
        response = self.client.get(url)
        data = response.data
        response.data["trim"] = "Corvette"

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Trim.objects.get(trim_model='Corvette').trim, "Corvette")

    def test_delete_trim(self):
        url = reverse("trim-detail", args=['Malibu'])
