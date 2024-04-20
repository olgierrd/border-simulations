import mesa
from agents import DealerAgent, PoliceAgent


class DrugsModel(mesa.Model):
    def __init__(self, NSmug, NPolice, width, height):
        super().__init__()
        self.num_smuglers = NSmug
        self.num_police = NPolice
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)

        # Agents creation
        for i in range(self.num_smuglers):
            smugler = DealerAgent(i, self)
            self.schedule.add(smugler)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(smugler, (x, y))

        for i in range(self.num_police):
            agent = PoliceAgent(i, self)
            self.schedule.add(agent)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

    def step(self) -> None:
        self.schedule.step()