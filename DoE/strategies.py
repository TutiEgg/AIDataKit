import numpy as np
import itertools
import copy

from objects import Attribute, Plan, Experiment

# Change in future
RUNTIME_COST = 1 # ..todo:: solche GLobalen bitte immer Capital RUNTIME_COST

def full_fact(attributelist: list[Attribute], repetions) -> Plan:
    """
    😊
    Parameters
    ----------
    attributelist

    Returns
    -------

    >>> attr1 = Attribute("Pumpe", ["h01","h02","b03"], 1)
    >>> attr2 = Attribute("Schlauch", ["h02","h04","b01","b02"], 1)
    >>> p = full_fact([attr1, attr2])
    >>> type(p) == Plan
    True
    >>> len(p.plan)
    12
    >>> p.plan[0].attribute_dict
    {'Pumpe': 'h01', 'Schlauch': 'h02'}
    >>> p.plan[3].attribute_dict
    {'Pumpe': 'h01', 'Schlauch': 'b02'}
    >>> list(p.plan[0].attribute_dict.keys())[0]
    'Pumpe'
    """

    attr_mani_list = list() # 2-dim list of Attributes and their Manifestations

    # This part is for saving the combinations as index_values instead of names
    counter = 0
    for attribute in attributelist:

        mani_list = list() # List of manifestations of one Attribute
        for manifestation_index in range(0, len(attribute.manifestation)):
            attr_mani_str = "{},{}".format(counter, manifestation_index)
            mani_list.append(attr_mani_str)
        counter += 1
        attr_mani_list.append(mani_list)

    combination_list = list(itertools.product(*attr_mani_list))

    # Create an Experiment_obj for each Combination in Combination_list
    comb_counter = 0
    experiment_list = list()
    for combination in combination_list: # combination_exampls = ('0,0' , '1,0')
        # 1 Combination = 1 Experiment

        attr_mani_dict = dict()
        for attr_mani in combination: # attr_mani_exampls = '1,0'
            attr_mani_split = attr_mani.split(',') # attr_mani_split_example = ['1','0']

            # Get attr_obj and manifestation_string
            attr = attributelist[int(attr_mani_split[0])]
            mani = attr.manifestation[int(attr_mani_split[1])]

            attr_mani_dict[attr.name] = mani

        # Add Experiment*reps to Experiment_list
        for i in range(0, repetions):
            temp_dict = copy.deepcopy(attr_mani_dict)
            # TODO: RUNTIME_COST has to be calculated. Currently const=1

            # CALCULATED HOW MANY DIGITS ALL COMBINATIONS HAVE
            comb_amount = len(combination_list) * repetions
            digit_amount = len(str(comb_amount))

            exp = Experiment(str(comb_counter).zfill(digit_amount) + "_Exp", RUNTIME_COST, repetions)
            exp.attribute_dict = temp_dict

            experiment_list.append(exp)
            # Counter + 1
            comb_counter += 1



    plan = Plan("plan1")
    plan.plan = experiment_list # TODO: Sollte das nicht beim instanzieren der Klasse schon mitgegeben werden ?

    return plan


if __name__ == "__main__":
    attr1 = Attribute("Pumpe", ["h01","h02","b03"], 1)
    attr2 = Attribute("Schlauch", ["h02","h04","b01","b02"], 1)
    plan1 = full_fact([attr1, attr2], 2)
    print(plan1.plan)
    print(len(plan1.plan))
    print(plan1)
    print('shuffel')
    plan1.shuffle = True
    plan1.set_seed(1)
    print(plan1.plan)
    print('sort')
    print(sorted(plan1.plan))
