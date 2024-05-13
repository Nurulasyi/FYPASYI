from django.core.management.base import BaseCommand
from pass.models import PasswordData
import csv

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def handle(self, *args, **kwargs):
        with open('data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                password_data = PasswordData(password=row['password'], strength=row['strength'])
                password_data.save()
