import agents
from model import DrugsModel
# Create a model with n agents
model = DrugsModel(70, 100, 20, 20)
drugs_initial = model.num_smugglers
steps = 0

# Run the model while there are still smugglers
while any(isinstance(agent, agents.SmugglerAgent) for agent in model.schedule.agents):
    model.step()
    steps += 1


# Get the number of drugs police agents have
drugs_captured_indiv = {
    f"{agent.__class__} with ID{agent.unique_id}": agent.drugs
    for agent in model.schedule.agents
}
drugs_captured = sum(drugs_captured_indiv.values())

print(
f"Steps: {steps}",
f"Initial: {drugs_initial}",
f"Captured: {drugs_captured}",
f"Crossed the border: {drugs_initial - drugs_captured}",)

