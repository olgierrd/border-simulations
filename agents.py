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
        self.radius = max((self.model.grid.width + self.model.grid.height) // 10, 3)
        self.state = "active"  # Initial state
        self.states = {  # State machine
            "active": self.active_state,
            "caught": self.caught_state,
            "crossed_border": self.crossed_border_state,
        }

    def flee_from_police(self, target) -> None | tuple:
        # Calculate the direction vector to the target
        distance, dx, dy = distance_find(self, target)
        if distance in range(1, self.radius + 1):
            self.speed = 2
            # Normalize the direction vector
            dx /= distance
            dy /= distance
            # Move the smuggler agent with its speed
            dx, dy = int(dx * self.speed), int(dy * self.speed)

            self.pos = (self.pos[0] - dx, self.pos[1] - dy)
        if distance <= 1:
            target.drugs += self.drugs
            self.drugs = 0

    def border_crossed(self) -> bool:
        return self.pos[1] in range(self.model.grid.height - 4, self.model.grid.height)

    def move(self) -> list:
        neighbors = neighbor_find(self, self.radius)
        police = [agent for agent in neighbors if isinstance(agent, PoliceAgent)]

        if police:
            # Calculate the distance to each officer
            distances = [
                distance_find(self, officer)[0]  # Calculate distance
                for officer in police
            ]
            target = police[distances.index(min(distances))]
            self.flee_from_police(target)
        elif self.pos[1] not in range(self.model.grid.height - self.radius, self.model.grid.height + 1):
            self.pos = (self.pos[0], self.pos[1] + 1)

    def active_state(self) -> None:
        self.move()
        if self.drugs == 0:
            self.state = "caught"
        elif self.border_crossed():
            self.state = "crossed_border"

    def caught_state(self) -> None:
        # If smuggler has no drugs, it is removed
        self.model.smugglers.remove(self)
        self.model.schedule.remove(self)

    def crossed_border_state(self) -> None:
        # If smuggler crossed the border, it is removed
        self.model.smugglers.remove(self)
        self.model.schedule.remove(self)

    def step(self) -> None:
        self.states[self.state]()


class PoliceAgent(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.drugs = 0
        self.speed = 1
        self.radius = max((self.model.grid.width + self.model.grid.height) // 8, 5)

    def chase_smuggler(self, target) -> None:
        distance, dx, dy = distance_find(self, target)
        if distance in range(1, self.radius + 1):
            self.speed = 3
            # Normalize the direction vector
            dx /= distance
            dy /= distance
            # Move the police agent with its speed
            dx, dy = int(dx * self.speed), int(dy * self.speed)

            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        if distance <= 1:
            self.drugs += target.drugs
            target.drugs = 0

    def move(self) -> list:
        neighbors = neighbor_find(self, self.radius)
        smugglers = [agent for agent in neighbors if isinstance(agent, SmugglerAgent)]

        if smugglers:
            # Calculate the distance to each smuggler
            distances = [distance_find(self, smuggler)[0] for smuggler in smugglers]
            target = smugglers[distances.index(min(distances))]
            self.chase_smuggler(target)
        else:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            self.pos = self.random.choice(possible_steps)
        return neighbors

    def step(self) -> None:
        self.move()
