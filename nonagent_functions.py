import numpy as np


def distance_find(agent, target) -> list:
    dx = target.pos[0] - agent.pos[0]
    dy = target.pos[1] - agent.pos[1]
    distance = np.sqrt(dx**2 + dy**2)
    return [distance, dx, dy]


def neighbor_find(agent, radius) -> list:
    return agent.model.grid.get_neighbors(
        agent.pos, moore=True, include_center=False, radius=radius
    )
