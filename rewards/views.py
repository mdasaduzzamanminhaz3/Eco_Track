from django.shortcuts import render
from rest_framework import viewsets, permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserWallet
from .serializers import UserWalletSerializer, LeaderboardSerializer

# Create your views here.


class RewardViewSet(viewsets.GenericViewSet):
    queryset = UserWallet.objects.all()
    serializer_class = UserWalletSerializer
    # User's own wallet profile
    @action(detail=False, methods=['get'], url_path='my-wallet')
    def my_wallet(self,request):
        wallet, _ = UserWallet.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    
    
    
    
    # Leaderboard view to show top users based on points and carbon saved
    """Global leaderboard (visible to everyone)"""
    @action(detail=False, methods=['get'], url_path='leaderboard',permission_classes=[permissions.AllowAny])
    def leaderboard(self,request):
        top_wallets = UserWallet.objects.order_by('-total_points')[:10]
        serializer = LeaderboardSerializer(top_wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



