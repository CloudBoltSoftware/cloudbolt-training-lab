from django.contrib.auth.models import User
from rest_framework import serializers
from cars.models import Manufacturer, Make, Trim


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class MakeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = '__all__'


class TrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trim
        fields = '__all__'
