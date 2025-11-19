import pygame
import random

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

# --- Enemy Definitions ---
ENEMY_LIST = [
    {"name": "an evil dark vampire", "health": 25, "attack": 10},
    {"name": "a large strong ogre", "health": 60, "attack": 20},
    {"name": "an evil witch", "health": 40, "attack": 15},
    {"name": "an extremely large rat", "health": 20, "attack": 8},
    {"name": "an evil wizard", "health": 45, "attack": 18},
    {"name": "a large poisonous toad", "health": 30, "attack": 12},
    {"name": "a large poisonous snake", "health": 35, "attack": 14},
    {"name": "a large poisonous spider", "health": 30, "attack": 16},
    {"name": "a large troll", "health": 70, "attack": 25},
    {"name": "an evil dark knight", "health": 80, "attack": 30},
]

def get_random_enemy():
    data = random.choice(ENEMY_LIST)
    return Enemy(data["name"], data["health"], data["attack"])

