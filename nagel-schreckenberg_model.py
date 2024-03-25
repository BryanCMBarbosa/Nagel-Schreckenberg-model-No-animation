import numpy as np
import os
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-rs", "--road_size", type=int, help="Specify how many positions the array representing the road must have.")
parser.add_argument("-nc", "--num_cars", type=int, help="Specify how many cars the simulation must have.")
parser.add_argument("-ms", "--max_speed", type=int, help="Specify the maximum number of positions per time step a car can travel.")
parser.add_argument("-bp", "--brake_prob", type=float, help="Specify the probability a car have to randomly braking.")
parser.add_argument("-ne", "--num_episodes", type=int, help="Specify the how many iterations will the simulation have.")
args = parser.parse_args()

class Car():
    def __init__(self, position, emoji):
        self.speed = 0
        self.position = position
        self.emoji = emoji

class Road():
    def __init__(self, road_size, num_cars, max_speed, brake_prob, num_episodes):
        self.road = [None] * road_size
        self.road_size = road_size
        self.num_cars = num_cars
        self.max_speed = max_speed
        self.brake_prob = brake_prob
        self.num_episodes = num_episodes
        self.car_emojis = ["\U0001F68C", "\U0001F68E", "\U0001F690", "\U0001F691", "\U0001F692", "\U0001F693", "\U0001F695", "\U0001F697", "\U0001F699", "\U0001F69A", "\U0001F69B", "\U0001F6FA", "\U0001F6FB", "\U0001F6F5", "\U0001F6B4", "\U0001F3CD", "\U0001F9BC", "\U0001F3CE", "\U0001F3C7", "\U0001F9BD"]
        self.flux_marker = int(road_size / 2)
        self.flux_counter = 0
        self.flux_sum = 0
        self.flux = 0.0
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

    def flux_counter_verifier(self, init_position, end_position):
        return (init_position > self.flux_marker) and (end_position < self.flux_marker)


    def move_cars(self):
        new_road = [None] * self.road_size
        for car in self.road:
            if car:
                new_position = (car.position - car.speed + self.road_size) % self.road_size
                if self.road[new_position] and car.speed > 0:
                   new_position = (new_position + 1) % self.road_size
                   car.speed -= 1
                if self.flux_counter_verifier(car.position, new_position):
                    self.flux_counter += 1
                car.position = new_position
                new_road[car.position] = car
            self.flux_sum = self.flux_counter
            self.flux_counter = 0   
        self.road = new_road

    def calculate_average_flux(self):
        self.flux = self.flux_sum / self.num_episodes
    
    def run(self):
        self.print_road()
        for i in range(self.num_episodes):
            self.update_speed_cars()
            self.move_cars()
            self.print_road()
        self.calculate_average_flux()


if __name__ == "__main__":
    r = Road(args.road_size, args.num_cars, args.max_speed, args.brake_prob, args.num_episodes)
    r.run()