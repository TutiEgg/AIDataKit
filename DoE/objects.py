
from dataclasses import dataclass
import json
import random


@dataclass
class Attribute:
    name: str
    manifestation: list[str]
    modification_cost: float

    def add_manifestation(self, manifest: str):
        self.manifestation.append(manifest)




@dataclass
class Experiment:

    name: str
    runtime_cost: float
    attribute_dict = dict()
    repetitions: int

    def __lt__(self, other):
        # ..todo:: Sortieren nach Values in attribute_dict
        return self.name < other.name

    def __str__(self):
        return "Experiment {}, Attribute: {}".format(self.name, self.attribute_dict)

class Plan:
    def __init__(self, name, shuffle=False, seed=None):
        self.name = name
        self.__plan = list()
        self.attribute_list = list()
        self.shuffle = shuffle
        random.seed(seed)

    def __str__(self):
        return "Yes {}: {}".format(self.name, self.__plan) # Call obj.__str__ for each Experiment in plan

    @property
    def plan(self):
        if self.shuffle:
            random.shuffle(self.__plan)
        return self.__plan

    @plan.setter
    def plan(self, plan):
        if not isinstance(plan, list):
            raise TypeError('Argument has to be of type List.')
        self.__plan = plan

    def append(self, val):
        if not isinstance(val, Experiment):
            raise TypeError('Argument has to be of type Experiment.')
        self.__plan.append(val)

    def set_seed(self, seed:int):
        """ set seed value

        Parameters
        ----------
        seed : int
            Value of Seed


        """
        random.seed(seed)

