# Transport = {
#   speed: float,
#   terain: list,
#   police_capacity: int,
# }

# Car(Transport) = {}
# Helicopter(Transport) = {}
# Feet(Transport) = {}

from dataclasses import dataclass


@dataclass
class Transport:
    speed: float
    terrain: list
    police_capacity: int


class Car(Transport):
    def __init__(self):
        super().__init__(
            speed=5.0, terrain=["road", "trail", "field"], police_capacity=4
        )


class Helicopter(Transport):
    def __init__(self):
        super().__init__(
            speed=8.0,
            terrain=["forest", "river", "swamp", "road", "trail", "field", "wall"],
            police_capacity=2,
        )


class Feet(Transport):
    def __init__(self):
        super().__init(
            speed=1.0,
            terrain=["forest", "river", "swamp", "road", "trail", "field"],
            police_capacity=1,
        )


class TransportFactory:
  def __init__(self):
    self.transports = {
      'car': Car(),
      'helicopter': Helicopter(),
      'feet': Feet()
    }

  def get_transport(self, transport_type):
    return self.transports.get(transport_type)
