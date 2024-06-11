from dataclasses import dataclass


@dataclass
class Terrain():
  speed_constraint: int


class Forest(Terrain):
  def __init__(self):
    super().__init__(speed_constraint=0.7)


class River(Terrain):
  def __init__(self):
    super().__init__(speed_constraint=0.4)


class Swamp(Terrain):
  def __init__(self):
    super().__init__(speed_constraint=0.6)


class Road(Terrain):
  def __init__(self):
    super().__init__(speed_constraint=1.0)


class Trail(Terrain):
  def __init__(self):
    super().__init__(speed_constraint=0.9)


class Field(Terrain):
  def __init__(self):
    super().__init__(speed_constraint=0.8)
    

class Wall(Terrain):
  def __init__(self):
    super().__init__(speed_constraint=0.05)
    

class TerrainFactory:
  def __init__(self):
    self.terrain = {
      'forest': Forest(),
      'river': River(),
      'swamp': Swamp(),
      'road': Road(),
      'trail': Trail(),
      'field': Field(),
      'wall': Wall()
    }

  def get_terrain(self, terrain_type):
    return self.terrain.get(terrain_type)