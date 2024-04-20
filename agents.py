import mesa
import numpy as np


# The dealer agent.
class SmugglerAgent(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.drugs = 1
        self.speed = 1  # Initial walking speed

    def move(self) -> None:
        for _ in range(self.speed):
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
            self.speed = 2
        elif distance <= 1:
            target.drugs += self.drugs
            self.drugs = 0

    def step(self) -> None:
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
        for _ in range(self.speed):
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False)
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def chase_smuggler(self, target) -> None:
        dx, dy = target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]
        distance = np.sqrt(dx ** 2 + dy ** 2)
        if distance <= 4:
            # Within 4 squares, start running
            self.speed = 2
        elif distance <= 1:
            self.drugs += target.drugs
            target.drugs = 0

    def step(self) -> None:
        self.move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if isinstance(other, SmugglerAgent):
                self.chase_smuggler(other)
                other.drugs -= 1
                self.drugs += 1

