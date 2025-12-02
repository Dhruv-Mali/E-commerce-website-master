from django.core.management.base import BaseCommand
from store.models import Order

class Command(BaseCommand):
    help = 'Generate invoices for completed orders'

    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int, help='Order ID')

    def handle(self, *args, **options):
        order_id = options['order_id']
        try:
            order = Order.objects.get(id=order_id, complete=True)
            self.stdout.write(self.style.SUCCESS(f'Invoice for order #{order_id}'))
        except Order.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Order #{order_id} not found'))
