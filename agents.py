import mesa
import numpy as np


# The dealer agent.
class DealerAgent(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.drugs = 1
        self.speed = 1  # Initial walking speed

    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def flee_from_police(self, target) -> None:
        dx, dy = target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]
        distance = np.sqrt(dx ** 2 + dy ** 2)
        if distance <= 2:
            # Within 1 square, run faster
            self.speed *= 1.5
        else:
            pass

    def step(self):
        self.move()
        if self.drugs > 0:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for other in cellmates:
                if isinstance(other, PoliceAgent):
                    self.flee_from_police(other)
                    other.drugs += 1
                    self.drugs -= 1


# The police agent.
class PoliceAgent(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.drugs = 0
        self.speed = 1

    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_drugs(self) -> None:
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.drugs += 1
            self.drugs -= 1

    def step(self) -> None:
        self.move()
        if self.drugs > 0:
            self.give_drugs()
