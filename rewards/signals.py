from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import UserWallet, TransactionHistory 
from waste.models import PickupRequest  
@receiver(post_save, sender=PickupRequest)
def calculate_rewards_on_collection(sender,instance,created, **kwargs):
    if created:
        return
    if instance.status == 'COLLECTED' and not TransactionHistory.objects.filter(pickup_request=instance).exists():
        with transaction.atomic():
            # user wallet create or get
            wallet, _ = UserWallet.objects.get_or_create(user=instance.user)
            # Calculating points and carbon with category multipliers
            weight = instance.actual_weight or instance.estimated_weight
            points_earned = int(weight * instance.category.points_multiplier)
            carbon_saved = float(weight * instance.category.carbon_multiplier)
            # Update wallet
            wallet.total_points += points_earned
            wallet.current_points += points_earned
            wallet.total_carbon_saved += carbon_saved
            wallet.save()
            # Create transaction history record
            TransactionHistory.objects.create(
                wallet=wallet,
                pickup_request=instance,
                transaction_type='EARNED',
                points=points_earned,
                description=f"Earned {points_earned} points from {instance.category.name} recycling ({weight} KG)."
            )