import mesa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class PoliceAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.drugs = 1
        self.speed = 1  # Initial walking speed

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def chase_smuggler(self, target):
        dx, dy = target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]
        distance = np.sqrt(dx**2 + dy**2)
        if distance <= 1:
            # Within 1 square, start running
            self.speed *= 2
        else:
            # Continue walking
            self.speed = 1

    def step(self):
        self.move()
        if self.drugs > 0:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for other in cellmates:
                if isinstance(other, SmugglersAgent):
                    self.chase_smuggler(other)
                    other.drugs += 1
                    self.drugs -= 1


class SmugglersAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.drugs = 1
        self.speed = 1  # Initial walking speed

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def flee_from_police(self, target):
        dx, dy = target.pos[0] - self.pos[0], target.pos[1] - self.pos[1]
        distance = np.sqrt(dx**2 + dy**2)
        if distance <= 1:
            # Within 1 square, run faster
            self.speed *= 1.5
        else:
            # Continue walking
            self.speed = 1

    def step(self):
        self.move()
        if self.drugs > 0:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            for other in cellmates:
                if isinstance(other, PoliceAgent):
                    self.flee_from_police(other)
                    other.drugs += 1
                    self.drugs -= 1


class DrugsModel(mesa.Model):
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)  # Initialize the schedule

        # Create and place agents
        for i in range(N):
            police_agent = PoliceAgent(i, self)
            self.schedule.add(police_agent)
            self.grid.place_agent(police_agent, (i, 0))  # Top row

            smuggler_agent = SmugglersAgent(N + i, self)
            self.schedule.add(smuggler_agent)
            self.grid.place_agent(smuggler_agent, (i, height - 1))  # Bottom row

    def step(self):
        self.schedule.step()

    def plot_grid_animation(self, interval=500):
        # Create a figure and axis for the animation
        fig, ax = plt.subplots()

        # Initialize the grid with zeros (black)
        grid_array = np.zeros((self.grid.width, self.grid.height))

        # Function to update the animation
        def update(frame):
            ax.clear()

            # Update grid with zeros (black) for each step
            grid_array.fill(0)

            # Move agents
            self.step()

            # Update agents' positions
            for agent in self.schedule.agents:
                if isinstance(agent, PoliceAgent):
                    grid_array[agent.pos] = 3  # Blue for police agents
                elif isinstance(agent, SmugglersAgent):
                    grid_array[agent.pos] = 2  # Red for smugglers agents

            # Display grid with appropriate colors
            ax.imshow(grid_array, cmap='RdYlBu', interpolation='nearest')
            ax.set_title('Agents and Drugs Distribution (Step {})'.format(frame))

        # Create the animation
        ani = FuncAnimation(fig, update, frames=range(10), interval=interval)
        plt.colorbar(ax.imshow(np.zeros((self.grid.width, self.grid.height)), cmap='RdYlBu', interpolation='nearest'))
        plt.title('Agents and Drugs Distribution (Step 0)')
        plt.show()

# Create the model
model = DrugsModel(N=10, width=20, height=20)

# Plot the grid animation
model.plot_grid_animation(interval=1000)