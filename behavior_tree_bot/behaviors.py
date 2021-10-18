#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

# attack the weakest planet and predict the amount of ships it will take to take over the planet
def smart_attack(state):

    # instead of waiting for the current fleet to reach their destination, send a new fleet to a new target
    # available_routes keeps track of all available targets
    available_routes = [planet for planet in state.enemy_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    if not state.my_planets() or not available_routes:
        return False
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships)
    weakest_planet = min(available_routes, key=lambda t: t.num_ships, default=None)
    if weakest_planet is not None and strongest_planet is not None:
        required_ships = weakest_planet.num_ships + state.distance(strongest_planet.ID, weakest_planet.ID) * \
                         weakest_planet.growth_rate + 5
    else:
        required_ships = None
    if not strongest_planet or not weakest_planet or strongest_planet.num_ships < required_ships:
        return False
    else:
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)





def spread_to_closest_neutral_planet(state):
    # if len(state.my_fleets()) >= 1:
    #    return False
    # keep track of available_routes
    available_routes = [planet for planet in state.neutral_planets() if
                        not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    selected_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    if not available_routes or not selected_planet or not state.neutral_planets():
        return False
    neutral_planets = sorted(available_routes, key=lambda d: state.distance(selected_planet.ID, d.ID))
    if not neutral_planets:
        return False
    destination_planet = neutral_planets[0]
    required_ships = destination_planet.num_ships + 1
    if not destination_planet or not selected_planet or required_ships > selected_planet.num_ships:
        return False
    else:
        for neutral in neutral_planets:
            required_ships = neutral.num_ships + 1
            if required_ships < selected_planet.num_ships:
                issue_order(state, selected_planet.ID, neutral.ID, required_ships)
        return False

def spread_to_neutral(state):
    if len(state.my_planets()) > len(state.not_my_planets()):
        return False
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    neutral_planets = [planet for planet in state.neutral_planets()
                       if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]

    if not my_planets or not neutral_planets:
        return False

    for planet in my_planets:
        neutral_planets.sort(key=lambda p: state.distance(planet.ID, p.ID))
        for neutral in neutral_planets:
            required_ships = neutral.num_ships + 1
            if planet.num_ships > required_ships and not any(fleet.destination_planet == planet.ID for fleet in state.enemy_fleets()):
                issue_order(state, planet.ID, neutral.ID, required_ships)
    return False


# retreat to nearest planet if available, if not retreat to closest own planet
def fight_or_flight(state):
    enemy_fleets = sorted(state.enemy_fleets(), key=lambda p: p.num_ships)
    my_planets = sorted(state.my_planets(), key=lambda d: d.num_ships)
    if not state.not_my_planets():
        return False
    weakest_planet = min(state.not_my_planets(), key=lambda p: p.num_ships)
    if not enemy_fleets or not my_planets or not weakest_planet:
        return False
    strongest_fleet = enemy_fleets[0]
    marked_planet = None
    for planet in my_planets:
        for enemy in enemy_fleets:
            if enemy.destination_planet == planet.ID:
                marked_planet = planet
            if marked_planet is None or marked_planet.num_ships > strongest_fleet.num_ships:
                return False
            else:
                if marked_planet.num_ships > weakest_planet.num_ships:
                    issue_order(state, marked_planet.ID, weakest_planet.ID, marked_planet.num_ships)
                near_planets = [planet for planet in state.my_planets()]
                near_planets.sort(key=lambda p: state.distance(marked_planet.ID, p.ID))
                if len(near_planets) < 2:
                    return False
                nearest_planet = near_planets[1]
                if nearest_planet.num_ships + marked_planet.num_ships > strongest_fleet.num_ships and \
                        not any(fleet.destination_planet == nearest_planet.ID for fleet in state.enemy_fleets()):
                    issue_order(state, nearest_planet.ID, marked_planet.ID, nearest_planet.num_ships)
                issue_order(state, marked_planet.ID, nearest_planet.ID, marked_planet.num_ships)
                return False


