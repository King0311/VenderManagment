from rest_framework import serializers
from .models import *

class Vendor_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class Purchase_Order_Serializer(serializers.ModelSerializer):
    del_date = serializers.DateField(format='%Y-%m-%d')
    issue_date = serializers.DateField(format='%Y-%m-%d')
    # ack_date = serializers.DateField(format='%Y-%m-%d')
    class Meta:
        model = Purchase_Order
        fields = '__all__'

class Vendor_Performance_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Performance
        fields = "__all__"