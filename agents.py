import mesa
import numpy as np


class SmugglerAgent(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.drugs = 1
        self.speed = 1

    def move(self) -> list:
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=5)
        police = [agent for agent in neighbors if isinstance(agent, PoliceAgent)]

        if police:
            # Calculate the distance to each smuggler
            distances = [np.sqrt((self.pos[0] - officer.pos[0]) ** 2 + (self.pos[1] - officer.pos[1]) ** 2) for
                         officer in police]
            target = police[distances.index(min(distances))]

            # Calculate the direction vector to the target
            dx = target.pos[0] - self.pos[0]
            dy = target.pos[1] - self.pos[1]

            # Normalize the direction vector
            distance = np.sqrt(dx ** 2 + dy ** 2)
            dx /= distance
            dy /= distance
            # Move the police agent with its speed
            dx, dy = int(dx * self.speed), int(dy * self.speed)

            new_position = (self.pos[0] + dx, self.pos[1] + dy)
        else:
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)
        return neighbors

    def flee_from_police(self, target) -> None:
        dx, dy = target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]
        distance = np.sqrt(dx ** 2 + dy ** 2)
        if distance <= 3:
            self.speed = 2
        elif distance <= 1:
            target.drugs += self.drugs
            self.drugs = 0

    def step(self) -> None:
        neighbors = self.move()
        if self.drugs > 0:
            for other in neighbors:
                if isinstance(other, PoliceAgent):
                    self.flee_from_police(other)
                    other.drugs += 1
                    self.drugs -= 1
        else:
            # If smuggler has no drugs, it dies
            self.model.schedule.remove(self)


class PoliceAgent(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.drugs = 0
        self.speed = 1

    def move(self) -> list:
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=5)
        smugglers = [agent for agent in neighbors if isinstance(agent, SmugglerAgent)]

        if smugglers:
            # Calculate the distance to each smuggler
            distances = [np.sqrt((self.pos[0] - smuggler.pos[0]) ** 2 + (self.pos[1] - smuggler.pos[1]) ** 2) for
                         smuggler in smugglers]
            target = smugglers[distances.index(min(distances))]

            # Calculate the direction vector to the target
            dx = target.pos[0] - self.pos[0]
            dy = target.pos[1] - self.pos[1]

            # Normalize the direction vector
            distance = np.sqrt(dx ** 2 + dy ** 2)
            dx /= distance
            dy /= distance
            # Move the police agent with its speed
            dx, dy = int(dx * self.speed), int(dy * self.speed)

            new_position = (self.pos[0] + dx, self.pos[1] + dy)
        else:
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)
        return neighbors

    def chase_smuggler(self, target) -> None:
        dx, dy = target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]
        distance = np.sqrt(dx ** 2 + dy ** 2)
        if distance <= 4:
            # Within 4 squares, start running
            self.speed = 2
        if distance <= 1:
            self.drugs += target.drugs
            target.drugs = 0

    def step(self) -> None:
        neighbors = self.move()
        for other in neighbors:
            if isinstance(other, SmugglerAgent):
                self.chase_smuggler(other)
