from rest_framework import serializers
from .models import UserWallet, TransactionHistory
from users.serializers import CustomUserSerializer

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['id', 'transaction_type', 'points', 'description', 'created_at']
        
class UserWalletSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    transactions = TransactionHistorySerializer(many=True, read_only=True)

    class Meta:
        model = UserWallet
        fields = ['id','user', 'total_points', 'current_points', 'total_carbon_saved','transactions', 'updated_at']

class LeaderboardSerializer(serializers.ModelSerializer):
    user_details = CustomUserSerializer(source='user', read_only=True)

    class Meta:
        model = UserWallet
        fields = ['user_details', 'total_points', 'total_carbon_saved']