from rest_framework import serializers
from .models import WasteCategory, PickupRequest
from users.serializers import CustomUserSerializer

class WasteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategory
        fields = ['id', 'name', 'carbon_multiplier', 'points_multiplier']

class PickupRequestSerializer(serializers.ModelSerializer): 
    user = CustomUserSerializer(read_only=True)
    recycler = CustomUserSerializer(read_only=True)
    category_detail = WasteCategorySerializer(source='category', read_only=True)

    class Meta:
        model = PickupRequest
        fields = ['id', 'user', 'recycler', 'category', 'category_detail', 'estimated_weight', 'actual_weight', 'pickup_address', 'latitude', 'longitude', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'recycler','actual_weight', 'status', 'created_at', 'updated_at']

        def validate_estimated_weight(self, value):
            if value <= 0:
                raise serializers.ValidationError("Estimated weight must be greater than zero.")
            return value