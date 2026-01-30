"""Management command to setup improvements"""
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Setup all improvements (migrations, static files)'

    def handle(self, *args, **options):
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('🚀 Setting up improvements...'))
        self.stdout.write('='*60)
        
        try:
            self.stdout.write('\n▶ Creating migrations...')
            call_command('makemigrations', 'store')
            
            self.stdout.write('\n▶ Running migrations...')
            call_command('migrate')
            
            self.stdout.write('\n▶ Collecting static files...')
            call_command('collectstatic', '--noinput')
            
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.SUCCESS('✅ Setup complete!'))
            self.stdout.write('='*60)
            self.stdout.write('\n🎉 New features ready:')
            self.stdout.write('   - Product Reviews & Ratings')
            self.stdout.write('   - Wishlist System')
            self.stdout.write('   - Newsletter Subscription')
            self.stdout.write('   - Enhanced Logging')
            self.stdout.write('   - Performance Caching')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error: {e}'))
