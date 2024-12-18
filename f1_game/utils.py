def get_team_recommendations(budget, drivers, cars, engineers):
    """
    Recommends a team based on budget and available options.
    """
    recommendations = {
        "drivers": [d for d in drivers if d.cost <= budget],
        "cars": [c for c in cars if c.cost <= budget],
        "engineers": [e for e in engineers if e.cost <= budget]
    }
    return recommendations

def handle_strategy(strategy, game_state):
    """
    Adjust game state based on chosen strategy.
    """
    if strategy == 'push':
        game_state['tire_wear'] += 10
        game_state['fuel'] -= 5
        game_state['position'] = max(1, game_state['position'] - 1)
    elif strategy == 'conserve':
        game_state['tire_wear'] += 3
        game_state['fuel'] -= 2
        game_state['position'] = min(10, game_state['position'] + 1)
    elif strategy == 'pit':
        game_state['tire_wear'] = 0
        game_state['fuel'] = 100
        game_state['position'] += 2  # Pit stop penalty
    else:  # Neutral strategy
        game_state['tire_wear'] += 5
        game_state['fuel'] -= 3
    return game_state
