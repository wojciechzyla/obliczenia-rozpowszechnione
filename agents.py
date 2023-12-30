import mesa
import numpy as np
from enum import Enum
import uuid
import random

def new_uuid():
    # Generate a UUID
    unique_id = uuid.uuid4()

    # Convert the UUID to an integer
    int_uuid = int(unique_id.int)

    return int_uuid

class FireAgent(mesa.Agent):
    def __init__(self, unique_id, model, state: int):
        super().__init__(unique_id, model)
        # Agent może być w jednym z 6 stanów:
        # 0 - brak pożaru
        # 1 - wczesny ogień
        # 2 - średni ogień
        # 3 - pełny ogień
        # 4 - ekstremalny ogień
        # 5 - obszar spalony (obszar spalony nie może podpalić się po raz kolejny, gdyż całe paliwo zostało spalone) 
        self.state = state
        self.type = "Fire"
        self.fuel = 70
        self.time_in_state = 0
        self.max_time_in_step = 10

    def extinguised(self):
        if self.time_step <= 0:
            self.time_step = 0
            self.state = 0
            return True
        else:
            return False
        
    def check_if_burned(self):
        if self.fuel <= 0:
            self.fuel = 0
            self.state = 5
    
    def make_damage(self):
        if self.state == 1:
            self.fuel -= 0.5
        elif self.state == 2:
            self.fuel -= 1
        elif self.state == 3:
            self.fuel -= 2
        elif self.state == 4:
            self.fuel -= 4
    
    def apply_firefighters(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        firefighting_units = 0
        for c in cellmates:
            if c.type == "FireFighter":
                firefighting_units += 1
        
        if self.state == 1:
            # one firefighter needed to decrease time_in_state during step
            self.time_in_state -= firefighting_units*1.5
        elif self.state == 2:
            # two firefighters needed to decrease time_in_state during step
            self.time_in_state -= firefighting_units*1
        elif self.state == 3:
            # three firefighters needed to decrease time_in_state during step
            self.time_in_state -= firefighting_units*0.5
        elif self.state == 4:
            # four firefighters needed to decrease time_in_state during step
            self.time_in_state -= firefighting_units*0.3

    def change_state(self):
        if self.time_in_state > self.max_time_in_step:
            if self.state < 5:
                self.state += 1
                self.time_in_state = 0
        elif self.time_in_state < 0:
            if self.state > 0:
                self.state -= 1
                self.time_in_state = self.max_time_in_step

    def get_neighborhood(self):
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        fire_agents = []
        for n in neighborhood:
            agents_n = self.model.grid.get_cell_list_contents([(n[0], n[1])])
            for c in agents_n:
                if c.type == "Fire":
                   fire_agents.append(c)
        return fire_agents

    def spread_fire(self):
        neighborhood = self.get_neighborhood()
        sampled_neighbours = []
        if self.state == 3:
            sampled_neighbours = random.sample(neighborhood, 1)
        if self.state == 4:
            sampled_neighbours = random.sample(neighborhood, 2)
        for n in sampled_neighbours:
            if n.state == 0:
                n.state = 1
                n.time_in_state = 0
            elif n.state < 5:
                n.time_in_state += 1

    def step(self):
        if 0 < self.state < 5:
            self.make_damage()
            self.apply_firefighters()
            self.change_state()
            self.spread_fire()
            self.time_in_state += 1
        self.check_if_burned()

class FireFighterAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = "FireFighter"
        
    def step(self):
        pass


