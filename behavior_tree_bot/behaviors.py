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
    if len(state.my_fleets()) >= 2:
        return False
    
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    required_ships = weakest_planet.num_ships + state.distance(strongest_planet.ID, weakest_planet.ID ) * weakest_planet.growth_rate + 1
    
    if not strongest_planet or not weakest_planet or strongest_planet.num_ships < required_ships:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)   


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
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

def retreat_to_largest(state):
    if len(state.my_fleets()) >= 1:
        return False

    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        return False
    else:
        return issue_order(state, weakest_planet.ID, strongest_planet.ID, weakest_planet.num_ships / 2)
