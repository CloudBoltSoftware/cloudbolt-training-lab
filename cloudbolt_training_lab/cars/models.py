from django.db import models


class Manufacturer(models.Model):
    manufacturer = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.manufacturer


class Make(models.Model):
    make = models.CharField(max_length=255, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.make


class Trim(models.Model):
    trim = models.CharField(max_length=255)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return self.trim
