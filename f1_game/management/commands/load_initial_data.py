from django.core.management.base import BaseCommand
from f1_game.models import Driver, Car, Engineer

class Command(BaseCommand):
    help = 'Loads initial F1 game data'

    def handle(self, *args, **kwargs):
        # Create Drivers
        drivers_data = [
            {'name': 'Max Verstappen', 'cost': 40, 'skill': 95},
            {'name': 'Lewis Hamilton', 'cost': 35, 'skill': 94},
            {'name': 'Charles Leclerc', 'cost': 30, 'skill': 90},
            {'name': 'Lando Norris', 'cost': 25, 'skill': 88},
            {'name': 'George Russell', 'cost': 20, 'skill': 85},
        ]

        # Create Cars
        cars_data = [
            {'name': 'Red Bull RB19', 'cost': 40, 'performance': 95},
            {'name': 'Ferrari SF-23', 'cost': 35, 'performance': 90},
            {'name': 'Mercedes W14', 'cost': 30, 'performance': 88},
            {'name': 'McLaren MCL60', 'cost': 25, 'performance': 85},
            {'name': 'Aston Martin AMR23', 'cost': 20, 'performance': 83},
        ]

        # Create Engineers
        engineers_data = [
            {'name': 'Adrian Newey', 'cost': 35, 'strategy': 'Aggressive'},
            {'name': 'James Allison', 'cost': 30, 'strategy': 'Balanced'},
            {'name': 'Pierre Waché', 'cost': 25, 'strategy': 'Conservative'},
            {'name': 'Mike Elliott', 'cost': 20, 'strategy': 'Adaptive'},
            {'name': 'Simone Resta', 'cost': 15, 'strategy': 'Balanced'},
        ]

        # Clear existing data
        Driver.objects.all().delete()
        Car.objects.all().delete()
        Engineer.objects.all().delete()

        # Create new objects
        for data in drivers_data:
            Driver.objects.create(**data)
        
        for data in cars_data:
            Car.objects.create(**data)
        
        for data in engineers_data:
            Engineer.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
