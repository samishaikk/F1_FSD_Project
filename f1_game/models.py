# models.py
from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    skill = models.IntegerField()

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    performance = models.IntegerField()

    def __str__(self):
        return self.name

class Engineer(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    strategy = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RacePosition(models.Model):
    position = models.IntegerField()
    driver_code = models.CharField(max_length=3)
    time_delta = models.CharField(max_length=10)  # Example format: "+0.123s"

    def __str__(self):
        return f"{self.position} - {self.driver_code} - {self.time_delta}"

class RaceState(models.Model):
    lap = models.IntegerField()
    position = models.IntegerField()
    tire_wear = models.FloatField()
    fuel = models.FloatField()

    def __str__(self):
        return f"Lap: {self.lap}, Position: {self.position}, Tire Wear: {self.tire_wear}%, Fuel: {self.fuel}%"

# Utility functions for AI Team Recommendations (from aiTeam.js)
def get_team_recommendations(budget, drivers, cars, engineers):
    """
    Recommends balanced team combinations based on budget.
    """
    recommendations = []
    
    # Convert querysets to lists for easier manipulation
    drivers_list = list(drivers)
    cars_list = list(cars)
    engineers_list = list(engineers)

    # Sort components by performance/skill
    drivers_list.sort(key=lambda x: x.skill, reverse=True)
    cars_list.sort(key=lambda x: x.performance, reverse=True)
    engineers_list.sort(key=lambda x: x.cost, reverse=True)

    # Try to find combinations starting with top performers
    for driver in drivers_list[:3]:
        remaining = budget - driver.cost
        if remaining <= 0:
            continue

        for car in cars_list[:3]:
            if car.cost > remaining:
                continue
            
            remaining2 = remaining - car.cost
            for engineer in engineers_list:
                if engineer.cost <= remaining2:
                    total_cost = driver.cost + car.cost + engineer.cost
                    perf_score = (driver.skill + car.performance) / 2
                    
                    recommendations.append({
                        'description': (
                            f"Driver: {driver.name} (Skill: {driver.skill})\n"
                            f"Car: {car.name} (Performance: {car.performance})\n"
                            f"Engineer: {engineer.name} (Style: {engineer.strategy})"
                        ),
                        'total_cost': total_cost,
                        'performance_score': perf_score,
                        'remaining_budget': budget - total_cost
                    })
                    break  # Found a valid engineer, move to next car
            
            if len(recommendations) >= 3:
                break
        
        if len(recommendations) >= 3:
            break

    return recommendations[:3]

# Strategy handler (from strategy.js)
def handle_strategy(strategy, race_state):
    """
    Adjust game state based on chosen strategy.
    Sets wear rates instead of instant changes.
    """
    # Base rates per lap
    base_tire_wear = 2
    base_fuel_consumption = 2

    if strategy == 'push':
        race_state['tire_wear'] += base_tire_wear * 2
        race_state['fuel'] -= base_fuel_consumption * 1.5
        if race_state['position'] > 1:
            race_state['position'] -= 1
    elif strategy == 'conserve':
        race_state['tire_wear'] += base_tire_wear * 0.5
        race_state['fuel'] -= base_fuel_consumption * 0.5
        if race_state['position'] < 20:
            race_state['position'] += 1
    elif strategy == 'pit':
        race_state['tire_wear'] = 0
        race_state['fuel'] = 100
        race_state['position'] = min(20, race_state['position'] + 3)
    else:  # Normal strategy
        race_state['tire_wear'] += base_tire_wear
        race_state['fuel'] -= base_fuel_consumption

    return race_state
