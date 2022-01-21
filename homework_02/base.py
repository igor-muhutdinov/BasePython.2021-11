from abc import ABC
from homework_02 import exceptions


class Vehicle(ABC):
    weight: float = 0
    started: bool = False
    fuel: float = 0
    fuel_consumption: float = 0

    def __init__(self, weight, fuel, fuel_consumption):
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if self.started is False:
            if self.fuel > 0:
                self.started = True
            else:
                raise exceptions.LowFuelError

    def move(self, distance):
        necessary_fuel = distance * self.fuel_consumption
        if necessary_fuel <= self.fuel:
            self.fuel -= necessary_fuel
        else:
            raise exceptions.NotEnoughFuel

