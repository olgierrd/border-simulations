import numpy as np

import agents
from model import DrugsModel
import matplotlib.pyplot as plt

# Create a model with 10 agents
model = DrugsModel(8, 5, 30, 30)
steps = 0

# Run the model while there are still smugglers
while any(isinstance(agent, agents.SmugglerAgent) for agent in model.schedule.agents):
    model.step()
    steps += 1



# Get the number of drugs police agents have
drugs = {f"{agent.__class__} with ID{agent.unique_id}": agent.drugs for agent in model.schedule.agents}

print(steps, drugs)




