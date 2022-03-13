import sympy as sp
import math

x = sp.Symbol("x")

def f(x):
    return x**-1

g = sp.integrate(f(x), x)

print(g)

upper = float(g.subs(x, math.e))
lower = float(g.subs(x, 1))

print(upper - lower)