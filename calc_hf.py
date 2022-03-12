#script to represent f as a function of T
import math

#base data (kJ/mol)
base = {
    'Al': 0,
    'AlOH3' : -1293.5,
    'AlOOH' : -996.4,
    'Al2O3' : -1675.7,
    'H2O_l' : -285.3,
    'H2O_g' : -241.8,
    'H2' : 0,
    'O2' : 0,
    'N2' : 0
}

def calc(input: dict, output: dict, er:float=1)->int:

    return er