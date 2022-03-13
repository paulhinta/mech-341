import sympy as sp

def enthalpy(input:dict, T:int=298.15):
    x = sp.Symbol("x")
    
    def f(x):
        return input["a1"]*x**-2 + input["a2"]*x**-1 + input["a3"] + input["a4"]*x + input["a5"]*x**2 + input["a6"]*x**3 + input["a7"]*x**4

    #print(f(x))

    int_f = sp.integrate(f(x),x)
    lower_f = float(int_f.subs(x, 298.15))
    b1 = input["b1"]

    return float(int_f.subs(x, T) - lower_f + 8.314*b1)