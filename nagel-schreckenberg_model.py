import numpy as np
import os
from time import sleep


class Car():
    def __init__(self, position, emoji):
        self.speed = 0
        self.position = position
        self.emoji = emoji
        

class Road():
    def __init__(self, road_size, num_cars, max_speed, brake_prob):
        self.road = [None] * road_size
        self.road_size = road_size
        self.num_cars = num_cars
        self.max_speed = max_speed
        self.brake_prob = brake_prob
        self.car_emojis = ["\U0001F68C", "\U0001F68E", "\U0001F690", "\U0001F691", "\U0001F692", "\U0001F693", "\U0001F695", "\U0001F697", "\U0001F699", "\U0001F69A", "\U0001F69B", "\U0001F6FA", "\U0001F6FB", "\U0001F6F5", "\U0001F6B4", "\U0001F3CD", "\U0001F9BC", "\U0001F3CE", "\U0001F3C7", "\U0001F9BD"]

        self.populate_road()
            
    def populate_road(self):
        cars_positions = np.random.choice(self.road_size, self.num_cars, replace=False)
        cars_positions.sort()
        for p in cars_positions:
            self.road[p] = Car(p, np.random.choice(self.car_emojis))

    def print_road(self):
        sleep(0.10)
        os.system("clear")
        street = "="
        for car in self.road:
            if car:
                print(f"{car.emoji:1s}", end="")
            else:
                print(f"{street:1s}", end="")
        print("")
    
    def verify_collision(self, car):
        speed = car.speed
        position = car.position
        distance = 0

        while(speed > 0):
            position = (position - 1 + self.road_size) % self.road_size
            speed-=1
            distance += 1
            if self.road[position]:
                return distance, position
        
        return distance, position
            
    def update_speed_cars(self):
        for car in self.road:
            if car:

                if car.speed < self.max_speed and all(x == None for x in self.road[max(0, car.position - car.speed - 1):car.position]) and all(x == None for x in self.road[min(self.road_size + (car.position - car.speed - 1), self.road_size):self.road_size]):
                    car.speed+=1
                elif  car.speed > 0:
                    distance, position = self.verify_collision(car)
                    if(self.road[position]):
                        car.speed = distance-1

                if car.speed > 0 and np.random.choice(a=[False, True], p=[1-self.brake_prob, self.brake_prob]):
                    car.speed -= 1


    def move_cars(self):
        new_road = [None] * self.road_size
        for car in self.road:
           if car:
                new_position = (car.position - car.speed + self.road_size) % self.road_size
                if self.road[new_position] and car.speed > 0:
                   new_position = (new_position + 1) % self.road_size
                   car.speed -= 1
                car.position = new_position
                new_road[car.position] = car
        self.road = new_road


r = Road(60, 20, 4, 0.1)
r.print_road()
for i in range(100):
    r.update_speed_cars()
    r.move_cars()
    r.print_road()