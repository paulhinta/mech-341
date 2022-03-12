from gc import garbage
import sympy as sp
import numpy as np

x = sp.Symbol("x")
t = sp.Symbol("t")

def f(x):
    return 5*x + 3*x**4

f = sp.integrate(f(x), x)
print(f)

g = float(f.subs(x, 1))
h = f.subs(x, t)

out = h - g

print(out)