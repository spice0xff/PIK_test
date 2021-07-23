from abc import ABC

from rest_framework import serializers
from service_organizations.models import Organisation, Service, Area, Cost


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['id', 'name', 'email', 'phone', 'address', ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', ]


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['organisation', 'name',  'polygon', ]


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = ['service', 'area',  'value', ]


class CoordinateSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

