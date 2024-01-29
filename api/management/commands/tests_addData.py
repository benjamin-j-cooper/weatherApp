from django.core.management.base import BaseCommand
from backend.settings import BASE_DIR, DATABASE_URL
from api.models import weatherData, weatherStats

class Command(BaseCommand):
    help = "This command will test that the correct number of records were added to the database"

    def handle(self, *args, **kwargs):
        self.test_pgdb_verify(weatherData)
        self.test_pgdb_verify(weatherStats)

    def test_pgdb_verify(self, model):
        # Check that there are n records in the database
        if model.__name__ in 'weatherStats':
            expected_num_records = 4820  # Define expected number of records
        elif model.__name__ in 'weatherData':
            expected_num_records = 1729957
        num_records = model.objects.count()
        assertEqual = num_records == expected_num_records
        if not assertEqual:
            print(f"WARNING: Expected {expected_num_records} records in the weather database, found {num_records} records instead")

    def test_pgdb_validate(self, model):
        # Check that the values of the 'temp' field are within a range
        min_temp = -273.15  # Define minimum allowable temperature
        max_temp = 56.7  # Define maximum allowable temperature
        # test max_temp_mean field
        invalid_records = model.objects.filter(max_temp_mean__lt=min_temp) | model.objects.filter(max_temp_mean__gt=max_temp)
        assertEqual = invalid_records == 0
        if not assertEqual:
            print(f"WARNING: Found {len(invalid_records)} records with 'max_temp' values outside the range [{min_temp}, {max_temp}]")
        # test min_temp field
        invalid_records = model.objects.filter(min_temp_mean__lt=min_temp) | model.objects.filter(min_temp_mean__gt=max_temp)
        assertEqual = invalid_records == 0
        if not assertEqual:
            print(f"WARNING: Found  {len(invalid_records)} records with 'min_temp' values outside the range [{min_temp}, {max_temp}]")
