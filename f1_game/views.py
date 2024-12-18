from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Driver, Car, Engineer, RaceState, RacePosition
from .utils import get_team_recommendations, handle_strategy
import random

def team_selection_view(request):
    """
    Handles team selection logic.
    """
    if request.method == 'POST':
        selected_driver_id = request.POST.get('driver')
        selected_car_id = request.POST.get('car')
        selected_engineer_id = request.POST.get('engineer')
        
        # Fetch selected team members
        selected_driver = Driver.objects.get(id=selected_driver_id)
        selected_car = Car.objects.get(id=selected_car_id)
        selected_engineer = Engineer.objects.get(id=selected_engineer_id)
        
        total_cost = selected_driver.cost + selected_car.cost + selected_engineer.cost
        if total_cost > 100:
            return render(request, 'f1/team_selection.html', {
                'error': 'Total cost exceeds budget!',
                'drivers': Driver.objects.all(),
                'cars': Car.objects.all(),
                'engineers': Engineer.objects.all(),
                'budget': 100
            })
        
        # Store team in session
        request.session['team'] = {
            'driver': selected_driver.name,
            'car': selected_car.name,
            'engineer': selected_engineer.name,
            'budget': 100 - total_cost
        }
        return redirect('race_setup')

    # Fetch all options for display
    drivers = Driver.objects.all()
    cars = Car.objects.all()
    engineers = Engineer.objects.all()
    budget = 100

    # AI Recommendations (optional)
    recommendations = get_team_recommendations(budget, drivers, cars, engineers)

    return render(request, 'f1/team_selection.html', {
        'drivers': drivers,
        'cars': cars,
        'engineers': engineers,
        'recommendations': recommendations,
        'budget': budget
    })

def race_setup_view(request):
    """
    Handles race setup logic.
    """
    team = request.session.get('team', None)
    if not team:
        return redirect('team_selection')

    # Initial game state
    game_state = {
        'tire_wear': 0,
        'fuel': 100,
        'position': 5
    }
    request.session['game_state'] = game_state

    # Weather simulation
    weather_timeline = [
        {'laps': '1-10', 'weather': 'Sunny'},
        {'laps': '11-20', 'weather': 'Cloudy'},
        {'laps': '21-30', 'weather': 'Rain'},
        {'laps': '31-40', 'weather': 'Sunny'}
    ]
    weathers = ['Sunny', 'Cloudy', 'Rainy']

    for timeline in weather_timeline:
        timeline['weather'] = random.choice(weathers)

    return render(request, 'f1/race_setup.html', {
        'team': team,
        'weather_timeline': weather_timeline
    })

def start_race_view(request):
    """
    Handles race start logic.
    """
    team = request.session.get('team')
    game_state = request.session.get('game_state')
    
    if not team or not game_state:
        return redirect('team_selection')
    
    # Initialize race state
    race_state = {
        'lap': 1,
        'position': game_state['position'],
        'tire_wear': game_state['tire_wear'],
        'fuel': game_state['fuel']
    }
    request.session['race_state'] = race_state

    # Generate race positions for the template
    race_positions = list(range(1, 21))  # Positions from 1 to 20



    return render(request, 'f1/race.html', {
        'team': team,
        'race_state': race_state,
        'race_positions': race_positions  # Pass the range as a context variable
    })

from django.http import JsonResponse
from django.shortcuts import render, redirect

def generate_v_shape_list(position, length):
    if position < 0 or position >= length:
        raise ValueError("Position must be within the bounds of the list length.")
    
    result = []
    for i in range(length):
        result.append(abs(i - position))
    return result

def race_strategy_view(request):
    """
    Handles race strategy decisions.
    """
    if request.method != 'POST':
        return redirect('start_race')

    team = request.session.get('team')
    race_state = request.session.get('race_state')

    if not team or not race_state:
        return redirect('team_selection')

    strategy = request.POST.get('strategy', 'normal')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Increment lap only during auto updates
    if is_ajax and strategy == 'normal':
        race_state['lap'] += 1

    # Apply strategy effects
    race_state = handle_strategy(strategy, race_state)

    # Ensure values stay within bounds
    race_state['tire_wear'] = min(100, max(0, race_state['tire_wear']))
    race_state['fuel'] = min(100, max(0, race_state['fuel']))

    # Generate race positions dynamically for the table
    max_positions = 20
    race_positions = []
    for i in range(1, max_positions + 1):
        if i == race_state['position']:
            race_positions.append({
                'number': i,
                'driver_code': team['driver'],
                'time_delta': f'+0.0'
            })
        else:
            race_positions.append({
                'number': i,
                'driver_code': f'Driver {i}',
                'time_delta': str(i-race_state['position'])
            })

    # Check race-ending conditions
    race_over = False
    end_message = None

    if race_state['tire_wear'] >= 100:
        request.session['final_position'] = race_state['position'] + 3
        end_message = "Race ended: Tire failure!"
        race_over = True
    elif race_state['fuel'] <= 0:
        request.session['final_position'] = 20
        end_message = "Race ended: Out of fuel!"
        race_over = True
    elif race_state['lap'] > 40:
        request.session['final_position'] = race_state['position']
        end_message = "Race completed!"
        race_over = True

    # Update session with race state
    request.session['race_state'] = race_state

    if race_over:
        request.session['end_message'] = end_message
        if is_ajax:
            return JsonResponse({
                'redirect': '/race-finish/',
                'message': end_message
            })
        return redirect('race_finish')

    if is_ajax:
        return JsonResponse({
            'race_state': race_state,
            'last_strategy': strategy,
            'race_positions': race_positions,
            'success': True
        })

    return render(request, 'f1/race.html', {
        'team': team,
        'race_state': race_state,
        'last_strategy': strategy,
        'race_positions': race_positions
    })

def race_finish_view(request):
    """
    Handles race completion and displays results.
    """
    team = request.session.get('team')
    final_position = request.session.get('final_position')
    
    if not team or not final_position:
        return redirect('team_selection')
    
    # Calculate prize money based on position
    prize_money = {
        1: 1000000,
        2: 500000,
        3: 250000,
        4: 100000,
        5: 50000
    }.get(final_position, 10000)  # Default prize for positions > 5
    
    # Clear game session data
    request.session.pop('race_state', None)
    request.session.pop('game_state', None)
    request.session.pop('final_position', None)
    end_message = request.session.get('end_message', 'Race completed!')
    request.session.pop('end_message', None)
    
    return render(request, 'f1/race_finish.html', {
        'team': team,
        'final_position': final_position,
        'prize_money': prize_money,
        'end_message': end_message
    })

def race_view(request):
    race_state = RaceState.objects.get(id=1)  # Example, adjust as needed
    race_positions = RacePosition.objects.all().order_by('position')  # Example, adjust as needed

    context = {
        'race_state': race_state,
        'last_strategy': request.session.get('last_strategy'),
        'race_positions': race_positions,
    }
    return render(request, 'f1/race.html', context)

def landing_page_view(request):
    """
    Handles the landing page display.
    """
    return render(request, 'f1/landing_page.html')

def build_team_view(request):
    """
    Displays information about building your team.
    """
    return render(request, 'f1/build_team.html')

def race_strategy_view(request):
    """
    Displays information about race strategy.
    """
    return render(request, 'f1/race_strategy.html')

def team_management_view(request):
    """
    Displays information about team management.
    """
    return render(request, 'f1/team_management.html')

def tracks_races_view(request):
    """
    Displays information about tracks and races.
    """
    return render(request, 'f1/tracks_races.html')

def f1_rules_view(request):
    """
    Displays information about F1 rules.
    """
    return render(request, 'f1/f1_rules.html')

def teams_drivers_view(request):
    """
    Displays information about teams and drivers.
    """
    return render(request, 'f1/teams_drivers.html')

def pit_stops_strategies_view(request):
    """
    Displays information about pit stops and strategies.
    """
    return render(request, 'f1/pit_stops_strategies.html')

def points_championships_view(request):
    """
    Displays information about points and championships.
    """
    return render(request, 'f1/points_championships.html')

def physics_car_view(request):
    """
    Displays information about the physics behind the car.
    """
    return render(request, 'f1/physics_car.html')
