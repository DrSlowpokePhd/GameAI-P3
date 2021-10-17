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
    #if len(state.my_fleets()) >= 3:
    #    return False
   
    # instead of waiting for the current fleet to reach their destination, send a new fleet to a new target
    # available_routes keeps track of all available targets
    available_routes = [planet for planet in state.enemy_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())] 

    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    weakest_planet = min(available_routes, key=lambda t: t.num_ships, default=None)
    if weakest_planet is not None and strongest_planet is not None:
        required_ships = weakest_planet.num_ships + state.distance(strongest_planet.ID, weakest_planet.ID ) * \
                         weakest_planet.growth_rate + 1
    else:
        required_ships = None

    
    if not strongest_planet or not weakest_planet or strongest_planet.num_ships < required_ships:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)   


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 2:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet or weakest_planet.num_ships >= strongest_planet.num_ships / 2:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def spread_to_closest_neutral_planet(state):
    #if len(state.my_fleets()) >= 1:
    #    return False
    # keep track of available_routes

    selected_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    neutral_planets = sorted(state.neutral_planets(), key=lambda d: state.distance(selected_planet.ID, d.ID))
    
    # determine target
    if not neutral_planets:
        return False
    destination_planet = neutral_planets[0]
    required_ships = destination_planet.num_ships + 1

    if not destination_planet or not selected_planet or required_ships > selected_planet.num_ships:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, selected_planet.ID, destination_planet.ID, required_ships)


    
    
    
# steal neutral planet from enemy
def steal_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False
    # Find strongest planet and strongest enemy fleet
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    strongest_enemy_fleet = max(state.enemy_fleets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet or not strongest_enemy_fleet:
        return False
    # Find neutral target of the enemy fleet
    enemy_target = strongest_enemy_fleet.destination_planet
    marked_planet = None
    for planet in state.neutral_planets():
        if enemy_target == planet.ID:
            marked_planet = planet
    if marked_planet is None:
        return False
    if enemy_target == marked_planet.ID and strongest_enemy_fleet.num_ships > marked_planet.num_ships:
        # Calculate the ships required to take over the planet
        required_ships = (strongest_enemy_fleet.num_ships - marked_planet.num_ships) + state.distance(strongest_planet.ID,
        marked_planet.ID ) * marked_planet.growth_rate + 1
        return issue_order(state, strongest_planet.ID, marked_planet.ID, required_ships)
    else:
        return False


# retreat if enemy can take the planet
def retreat_to_largest(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    strongest_enemy_fleet = max(state.enemy_fleets(), key=lambda p: p.num_ships, default=None)
    if not strongest_planet or not strongest_enemy_fleet:
        return False
    enemy_source = strongest_enemy_fleet.source_planet
    enemy_target = strongest_enemy_fleet.destination_planet
    marked_planet = None
    for planet in state.my_planets():
        if enemy_target == planet.ID:
            marked_planet = planet
            required_ships = planet.num_ships + state.distance(enemy_source, planet.ID ) * planet.growth_rate + 1
    if marked_planet is None:
        return False
    if enemy_target == marked_planet.ID and marked_planet.num_ships < required_ships:
        return issue_order(state, marked_planet.ID, strongest_planet.ID, marked_planet.num_ships / 2)
    else:
        return False
