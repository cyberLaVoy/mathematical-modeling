from matplotlib import pyplot as plt

def basicSIR(delta_t, beta, gamma, S0, I0, R0, steps):
    # dS/dt = -beta*S*I
    # dI/dt = beta*S*I - gamma*I
    # dR/dt = gamma*I

    # susceptible pool, with initial population
    S = [S0]
    # infected pool, with inital infections
    I = [I0]
    # recovered pool, with initial recoverd
    R = [R0]
    for i in range(steps):
        S.append( S[i] - delta_t * beta*S[i]*I[i] )
        I.append( I[i] + delta_t * ( beta*S[i]*I[i] - gamma*I[i] ) )
        R.append( R[i] + delta_t * gamma*I[i] )
    return S, I, R


def vaccineSIR(delta_t, beta, gamma, alpha, S0, I0, R0, V0, steps):
    # dS/dt = -beta*S*I -alpha*S
    # dV/dt = alpha*S
    # dI/dt = beta*S*I - gamma*I
    # dR/dt = gamma*I

    # susceptible pool, with initial population
    S = [S0]
    # vaccinated pool, with initial vaccinated
    V = [V0]
    # infected pool, with inital infections
    I = [I0]
    # recovered pool, with initial recoverd
    R = [R0]
    for i in range(steps):
        S.append( S[i] - delta_t * beta*S[i]*I[i] - alpha*S[i])
        V.append( V[i] + alpha*S[i] )
        I.append( I[i] + delta_t * ( beta*S[i]*I[i] - gamma*I[i] ) )
        R.append( R[i] + delta_t * gamma*I[i] )
    return S, I, R, V

def displayModel(X, Y, names):
    for y in Y:
        plt.plot(X, y)
    plt.legend( names )
    plt.show()


def main():
    # initial susceptible population
    S0 = 84000
    # inital infections
    I0 = 1
    #  initial recoverd
    R0 = 0
    # initial vaccinations
    V0 = 0


    # number of people interacted with on a given day
    n = 11 # lack of social distancing
    #n = 3 # social distancing
    interProb = n/S0
    transProb = 1
    infectTime  = 14 # days
    # force of infection
    beta = interProb / infectTime * transProb
    # recovery rate
    gamma = 1/infectTime
    # number of people vaccinated on a given day
    n = 10
    alpha = n / S0

    # start time
    a = 0
    # end time (in days)
    b = 120
    # divisions of change 
    N = 10000
    steps = N
    delta_t = (b-a)/N

    X = [ i*delta_t for i in range(N+1) ]
    S, I, R = basicSIR(delta_t, beta, gamma, S0, I0, R0, steps)
    displayModel(X, [S, I, R], ["Suseptable", "Infected", "Recovered"])
    S, I, R, V = vaccineSIR(delta_t, beta, gamma, alpha, S0, I0, R0, V0, steps)
    displayModel(X, [S, I, R, V], ["Suseptable", "Infected", "Recovered", "Vaccinated"])


main()