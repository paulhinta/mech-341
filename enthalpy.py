import sympy as sp
from sympy import lambdify, nsolve

#Python functions to calculate the enthalpy & adiabatic flame temp of a species based on the a_n & b_n constants

#calculate enthalpy (absolute value) using sympy
def enthalpy(input:dict, T:int=298.15):
    x = sp.Symbol("x")
    
    #define the polynomial
    def f(x):
        return input["a1"]*x**-2 + input["a2"]*x**-1 + input["a3"] + input["a4"]*x + input["a5"]*x**2 + input["a6"]*x**3 + input["a7"]*x**4

    #print(f(x))
    #integrate the polynomial
    int_f = sp.integrate(f(x),x)
    b1 = input["b1"]

    #evaluate the polynomial
    return 8.314*float(int_f.subs(x, T) + b1)

#Symbolically represent the enthalpy as a function of T
#this does the same as the above function, but returns a function of T rather than evaluating the definite integral
def enthalpy_function(input:dict, T=298.15):
    x = sp.Symbol("x")
    
    def f(x):
        return input["a1"]*x**-2 + input["a2"]*x**-1 + input["a3"] + input["a4"]*x + input["a5"]*x**2 + input["a6"]*x**3 + input["a7"]*x**4

    int_f = sp.integrate(f(x),x)
    b1 = input["b1"]

    return 8.314*(int_f.subs(x, T) + b1)

#this function uses the enthalpy as a function of T (above) to evaluate the AFT for question 1
#each instance of an aft will have water, nitrogen, and an excess gas (h2 or o2)
def aft_t1(water:dict, nitrogen:dict, extra:dict,  er:float=1.0):
    er_2 = er
    if er >=1:
        er_2 = 1
    
    T = sp.Symbol("T")

    #sub the enthalpy as a function of T
    def f(T):
        return 2*er_2*enthalpy_function(water, T) + 3.76*enthalpy_function(nitrogen, T) + abs(2*(er - 1))*enthalpy_function(extra, T)
    
    eq = f(T)

    #numerically solve the function of T
    #this is done numerically because it's a nonlinear function, sympy can only symbolically solve linear functions
    T_aft = nsolve(eq, 1)

    return T_aft

#governing stoich eqn: 2*Al + 6H2O (l) -> Al2O3 + 3*H2 + 3*H2O (g)
def aft_t5(al:dict, water:dict, oxide:dict, hydro:dict, vapour:dict, temp:float):

    #return a function in T to solve aft
    def f(T):
        return enthalpy_function(oxide, T) + 3*enthalpy_function(hydro, T) + 3*enthalpy_function(vapour, T) - 2*al["hf0 [J/mol]"] - 6*water["hf0 [J/mol]"]

    return f(temp)