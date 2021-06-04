#!/usr/bin/env PYTHONHASHSEED=1234 python3

__all__ = ['Projectile']

class Projectile:
    def __init__(self, mass, velocity):
        self.mass = mass
        self.velocity = velocity