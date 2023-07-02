from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    gems = serializers.ListSerializer(
        child=serializers.CharField(allow_blank=False), source="get_common_items"
    )
    spent_money = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = ["username", "spent_money", "gems"]


class DealCreateSerializer(serializers.Serializer):
    data = serializers.FileField(allow_empty_file=False)
