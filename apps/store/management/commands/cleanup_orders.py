from django.core.management.base import BaseCommand
from apps.store.models import Order, Customer
from django.db.models import Count, Q

class Command(BaseCommand):
    help = 'Clean up duplicate incomplete orders'

    def handle(self, *args, **options):
        # Find customers with multiple incomplete orders
        customers_with_duplicates = Customer.objects.annotate(
            incomplete_orders_count=Count('order', filter=Q(order__complete=False))
        ).filter(incomplete_orders_count__gt=1)

        total_cleaned = 0
        
        for customer in customers_with_duplicates:
            # Get all incomplete orders for this customer
            incomplete_orders = Order.objects.filter(
                customer=customer, 
                complete=False
            ).order_by('-date_ordered')
            
            # Keep the most recent one, delete the rest
            orders_to_delete = incomplete_orders[1:]
            
            for order in orders_to_delete:
                self.stdout.write(f"Deleting duplicate order {order.id} for customer {customer.name}")
                order.delete()
                total_cleaned += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully cleaned up {total_cleaned} duplicate orders')
        )