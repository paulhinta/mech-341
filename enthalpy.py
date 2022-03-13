import sympy as sp
from sympy import lambdify, nsolve

def enthalpy(input:dict, T:int=298.15):
    x = sp.Symbol("x")
    
    def f(x):
        return input["a1"]*x**-2 + input["a2"]*x**-1 + input["a3"] + input["a4"]*x + input["a5"]*x**2 + input["a6"]*x**3 + input["a7"]*x**4

    #print(f(x))
    int_f = sp.integrate(f(x),x)
    b1 = input["b1"]

    return 8.314*float(int_f.subs(x, T) + b1)

def enthalpy_function(input:dict, T=298.15):
    x = sp.Symbol("x")
    
    def f(x):
        return input["a1"]*x**-2 + input["a2"]*x**-1 + input["a3"] + input["a4"]*x + input["a5"]*x**2 + input["a6"]*x**3 + input["a7"]*x**4

    #print(f(x))
    int_f = sp.integrate(f(x),x)
    b1 = input["b1"]

    return 8.314*(int_f.subs(x, T) + b1)

def aft(water:dict, nitrogen:dict, extra:dict,  er:float=1.0):
    er_2 = er
    if er >=1:
        er_2 = 1
    
    T = sp.Symbol("T")

    def f(T):
        return 2*er_2*enthalpy_function(water, T) + 3.76*enthalpy_function(nitrogen, T) + abs(2*(er - 1))*enthalpy_function(extra, T)
    
    eq = f(T)

    T_aft = nsolve(eq, 1)

    return T_aft