from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import WasteCategory, PickupRequest
from .serializers import WasteCategorySerializer, PickupRequestSerializer
from rest_framework.decorators import action
# Create your views here.
class WasteCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing and retrieving waste categories. but not creating, updating, or deleting them(only for the admin pannel )."""
    queryset = WasteCategory.objects.all()
    serializer_class = WasteCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class PickupRequestViewSet(viewsets.ModelViewSet):
    """Main API life cycle on pickup request.ViewSet for managing pickup requests. Normal users can create and view their own requests, while recyclers can view and update assigned requests."""
    queryset = PickupRequest.objects.all()
    serializer_class = PickupRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'RECYCLER':
            return PickupRequest.objects.all() #Recyclers can see all requests to pick from 
        # Normal users can only see their own requests
        return PickupRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='PENDING') # Set the user and default status when creating a new pickup request

    # custom action to allow recyclers to accept a pickup request
    @action(detail=True,methods=['post'], url_path='accept')
    def accept_pickup(self,request,pk=None):
        pickup = self.get_object()
        if request.user.role != 'RECYCLER':
            return Response({'error': 'Only recyclers can accept pickup requests.'}, status=status.HTTP_403_FORBIDDEN)
        if pickup.status != 'PENDING':
            return Response({'error': 'Only pending pickup requests can be accepted.'}, status=status.HTTP_400_BAD_REQUEST)
        pickup.recycler = request.user
        pickup.status = 'ACCEPTED'
        pickup.save()
        return Response({'message': 'Pickup request accepted successfully.'}, status=status.HTTP_200_OK)
    

    # The recycler will go to the spot and push the actual weight.
    @action(detail=True, methods=['post'], url_path='complete')
    def complete_pickup(self,request, pk=None):
        pickup = self.get_object()
        if request.user.role !='RECYCLER' or pickup.recycler !=request.user:
            return Response({'error': 'Only recyclers can complete pickup requests.'}, status=status.HTTP_403_FORBIDDEN)
        
        if pickup.status != 'ACCEPTED':
            return Response({'error': 'Only accepted pickup requests can be completed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        actual_weight = request.data.get('actual_weight')
        if not actual_weight or float(actual_weight) <= 0:
            return Response({'error': 'Actual weight must be provided and greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
        pickup.actual_weight = float(actual_weight)
        pickup.status = 'COLLECTED'
        pickup.save()
# Note] Here later we will connect the logic to add wallet and points to the 'rewards' app
        return Response({
            'message': 'Pickup request completed successfully and actual weight verified.',
            'actual_weight': pickup.actual_weight,
            'status': pickup.status
            
            }, status=status.HTTP_200_OK)

