#!/usr/bin/env python

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

# def have_higher_production(state):
#     return sum(planet.growth_rate for planet in state.my_planets()) > \
#             sum(planet.growth_rate for planet in state.enemy_planets())

def is_not_under_attack(state):
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    enemy_fleets = sorted(state.enemy_fleets(), key=lambda p: p.num_ships)
    if not enemy_fleets or not my_planets:
        return True
    strongest_planet = my_planets[0]
    for fleet in enemy_fleets:
        if fleet.destination_planet == strongest_planet.ID:
            return False
    return True

