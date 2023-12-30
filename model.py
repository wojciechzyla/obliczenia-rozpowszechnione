import mesa
import random
import numpy as np
from agents import FireAgent, FireFighterAgent, new_uuid


class FireControllerAgentModel(mesa.Model):
    def __init__(self, width, height, fire_fighters, fire_agents_values: list):
        """
        width, height - rozmiary lasu (dla symulacji przyjmujemy rozmiar 10x10
        
        fire_fighters - ilość jednostek straży pożarnej, jakie FCA ma do dyspozycji
        
        fire_agents_values - lista wartości ze zbioru {1,2,3,4} określająca początkowe wartości pożaru w losowo wybranych komórkach.
        Maksymalna długość listy to 100 (tyle ile mamy komórek w siatce 10x10). Przykładowo, dla listy [1,1,3,2], cztery losowo 
        wybrane komórki zostaną zainicjalizowane właśnie takimi wartościami poziomu pożaru
        """
        self.width = width
        self.height = height
        self.fire_fighters = fire_fighters
        self.grid = mesa.space.MultiGrid(width=width, height=height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.firefighters_exposure_to_fire = 0

        all_indices = [(i, j) for i in range(width) for j in range(height)]
        fire_cells = random.sample(all_indices, len(fire_agents_values))
        no_fire_cells = [index for index in all_indices if index not in fire_cells]
        for i, index in enumerate(fire_cells):
            a = FireAgent(new_uuid(), self, fire_agents_values[i])
            self.grid.place_agent(a, index)
            self.schedule.add(a)
        for i, index in enumerate(no_fire_cells):
            a = FireAgent(new_uuid(), self, 0)
            self.grid.place_agent(a, index)
            self.schedule.add(a)

    def step(self):
        self.assign_firefighters_to_grid()
        self.firefighters_exposure_to_fire += self.get_firefighters_exposure()
        self.schedule.step()

    def set_fire_fighters(self, fire_fighters):
        self.fire_fighters = fire_fighters

    def print_grid(self):
        values = np.zeros((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                fire = self.get_fire_agent(x, y)
                fighters = self.get_firefighter_agent(x, y)
                values[x,y] = fire.state + len(fighters)*10
        print(values)

    def get_total_fire_level(self):
        result = 0
        for x in range(self.width):
            for y in range(self.height):
                fire = self.get_fire_agent(x, y)
                result += fire.state if fire.state < 5 else 0
        return result

    def get_total_burned_level(self):
        result = 0
        for x in range(self.width):
            for y in range(self.height):
                fire = self.get_fire_agent(x, y)
                result += fire.state if fire.state == 5 else 0
        return result
    
    def get_remaining_fuel(self):
        result = 0
        for x in range(self.width):
            for y in range(self.height):
                fire = self.get_fire_agent(x, y)
                result += fire.fuel
        return result

    def get_fire_agent(self, x, y):
        agents = self.grid.get_cell_list_contents([(x,y)])
        for a in agents:
            if a.type == "Fire":
                return a
            
    def get_firefighter_agent(self, x, y):
        agents = self.grid.get_cell_list_contents([(x,y)])
        result = []
        for a in agents:
            if a.type == "FireFighter":
                result.append(a)
        return result
    
    def get_all_firefighters(self):
        result = []
        for x in range(self.width):
            for y in range(self.height):
                result += self.get_firefighter_agent(x, y)
        return result
    
    def get_firefighters_exposure(self):
        result = 0
        for x in range(self.width):
            for y in range(self.height):
                all_agents = self.grid.get_cell_list_contents([(x,y)])
                firefighters = len(all_agents)-1 #number of firefighters in cell is equal to all agents minus fire agent
                result += firefighters*self.get_fire_agent(x, y).state
        return result

    def delete_firefighters(self):
        for x in range(self.width):
            for y in range(self.height):
                agents = self.grid.get_cell_list_contents([(x,y)])
                for a in agents:
                    if a.type == "FireFighter":
                        self.schedule.remove(a)
                        self.grid.remove_agent(a)
        
    def assign_firefighters_to_grid(self):
        self.delete_firefighters()
        values = np.zeros((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                fire = self.get_fire_agent(x, y)
                values[x,y] = fire.state if fire.state < 5 else 0
                
        # Get the indices in descending order of values
        indices = np.argsort(values.ravel())[::-1]
        # Convert the 1D indices to 2D indices
        row_indices, col_indices = np.unravel_index(indices, values.shape)
        # Filter indices where the value is greater than zero
        non_zero_indices = (values[row_indices, col_indices] > 0).nonzero()
        # Get the final indices
        sorted_indices = []
        for x, y in zip(row_indices[non_zero_indices], col_indices[non_zero_indices]):
            sorted_indices.append((x,y))

        available_firefighters = self.fire_fighters
        while available_firefighters > 0:
            for index in sorted_indices:
                x, y = index
                if self.get_fire_agent(x,y).state == 4:
                    new_firefighters = min(4, available_firefighters)
                elif self.get_fire_agent(x,y).state == 3:
                    new_firefighters = min(3, available_firefighters)
                elif self.get_fire_agent(x,y).state == 2:
                    new_firefighters = min(2, available_firefighters)
                else:
                    new_firefighters = min(1, available_firefighters) 
                for _ in range(new_firefighters):
                    a = FireFighterAgent(new_uuid(), self)
                    self.grid.place_agent(a, (x, y))
                    self.schedule.add(a)
                available_firefighters -= new_firefighters
                if available_firefighters == 0:
                    break
        