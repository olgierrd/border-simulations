import seaborn as sns
import numpy as np
from model import DrugsModel
import matplotlib.pyplot as plt

# Create a model with 10 agents
model = DrugsModel(3, 10, 20, 20)
for _ in range(1):
    model.step()

# Create a 2D numpy array representing the grid
grid = np.zeros((model.grid.width, model.grid.height))

# Fill the array with the number of smugglers and policemen in each cell
for agent in model.schedule.agents:
    x, y = agent.pos
    grid[x][y] += 1

# Plot the grid using seaborn
plt.figure(figsize=(10, 10))
sns.heatmap(grid, annot=True, fmt=".0f", cmap='viridis')
plt.title('Number of agents on each cell of the grid')
plt.show()