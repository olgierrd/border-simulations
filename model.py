import mesa
from agents import SmugglerAgent, PoliceAgent


class DrugsModel(mesa.Model):
    def __init__(self, smugnum, polnum, width, height):
        super().__init__()
        self.num_smugglers = smugnum
        self.num_police = polnum
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)

        # Agents creation
        for i in range(self.num_smugglers):
            smuggler = SmugglerAgent(i, self)
            self.schedule.add(smuggler)

            # Keep trying until the agent is added to an empty grid cell in the lower quarter
            while True:
                x = self.random.randrange(3 * self.grid.width // 4, self.grid.width)
                y = self.random.randrange(3 * self.grid.height // 4, self.grid.height)
                if self.grid.is_cell_empty((x, y)):
                    self.grid.place_agent(smuggler, (x, y))
                    break

        for i in range(self.num_police):
            policeman = PoliceAgent(i, self)
            self.schedule.add(policeman)

            # Keep trying until the agent is added to an empty grid cell in the upper quarter
            while True:
                x = self.random.randrange(0, self.grid.width // 4)
                y = self.random.randrange(0, self.grid.height // 4)
                if self.grid.is_cell_empty((x, y)):
                    self.grid.place_agent(policeman, (x, y))
                    break

    def step(self) -> None:
        self.schedule.step()