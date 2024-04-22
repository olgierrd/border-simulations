import mesa
from nonagent_functions import distance_find, neighbor_find

# TODO:
#  1) define border area -- done
#  2) count agents that crossed the border -- done
#  3) remove agents that crossed the border -- done
#  4) optimize the code (distance calculation) -- done


class SmugglerAgent(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.drugs = 1
        self.speed = 1

    def move(self) -> list:
        neighbors = neighbor_find(self, 4)
        police = [agent for agent in neighbors if isinstance(agent, PoliceAgent)]

        if police:
            # Calculate the distance to each officer
            distances = [
                distance_find(self, officer)[0]  # Calculate distance
                for officer in police
            ]
            target = police[distances.index(min(distances))]

            # Calculate the direction vector to the target
            distance, dx, dy = distance_find(self, target)
            dx /= distance
            dy /= distance
            # Move the police agent with its speed
            dx, dy = int(dx * self.speed), int(dy * self.speed)

            new_position = (self.pos[0] - dx, self.pos[1] - dy)
        else:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)
        return neighbors

    def flee_from_police(self, target) -> None:
        distance = distance_find(self, target)[0]
        if distance <= 3:
            self.speed = 2
        elif distance <= 1:
            target.drugs += self.drugs
            self.drugs = 0

    def border_crossed(self) -> bool:
        return self.pos[1] in range(self.model.grid.width - 4, self.model.grid.width)

    def step(self) -> None:
        neighbors = self.move()
        if self.border_crossed():
            # If smuggler crossed the border, it is removed
            self.model.schedule.remove(self)
        elif self.drugs > 0:
            for other in neighbors:
                if isinstance(other, PoliceAgent):
                    self.flee_from_police(other)
                    other.drugs += 1
                    self.drugs -= 1
        else:
            # If smuggler has no drugs, it is removed
            self.model.schedule.remove(self)


class PoliceAgent(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.drugs = 0
        self.speed = 1

    def move(self) -> list:
        neighbors = neighbor_find(self, 5)
        smugglers = [agent for agent in neighbors if isinstance(agent, SmugglerAgent)]

        if smugglers:
            # Calculate the distance to each smuggler
            distances = [distance_find(self, smuggler)[0] for smuggler in smugglers]
            target = smugglers[distances.index(min(distances))]

            # Calculate the direction vector to the target
            distance, dx, dy = distance_find(self, target)
            dx /= distance
            dy /= distance
            # Move the police agent with its speed
            dx, dy = int(dx * self.speed), int(dy * self.speed)

            new_position = (self.pos[0] + dx, self.pos[1] + dy)
        else:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)
        return neighbors

    def chase_smuggler(self, target) -> None:
        distance = distance_find(self, target)[0]
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
