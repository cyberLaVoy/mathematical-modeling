import math

# initial amount in account
p0 = 10000 
# compound interest rate (typically as APY) 
r = .017
# deposit amount per time unit t
k = 1000
# how long the acount is active (could be in years, months, days, etc.)
t = 20 

# to aproximate continous compounding (aka numerical method)
time_steps = 100
# values over time_steps
k_continuous = k/time_steps
r_continuous = r/time_steps
t_continuous = t*time_steps

P = p0
for _ in range(t_continuous):
    P += r_continuous*P + k_continuous

print("Approximation:", P)

derived_equation = p0*math.exp(r*t) + k*math.exp(r*t)/r*(1-math.exp(-r*t))
print( "Actual:", derived_equation )
