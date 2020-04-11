from matplotlib import pyplot as plt
import math
import numpy as np

HOPS_CAPACITY = 45000
VAC_DAY = 90

def validateConst(gamma, delta, infectCount, iter, delta_t, vaccineDay=VAC_DAY, hopsCap=HOPS_CAPACITY):
        if infectCount >= hopsCap:
            g = gamma[1]
        else:
            g = gamma[0]
        if iter*delta_t >= vaccineDay:
            d = delta
        else:
            d = 0
        return g, d

def basicSIR(delta_t, alpha, beta, gamma, S0, I0, R0, D0, steps):
    # dS/dt = -alpha*S*I
    # dI/dt = alpha*S*I -beta*I -gamma*I
    # dR/dt = beta*I
    # dD/dt = gamma*I
    S, I, R, D = [S0], [I0], [R0], [D0]
    for i in range(steps):
        g, d = validateConst(gamma, 0, I[i], i, delta_t)

        S.append( S[i] + delta_t * ( -alpha*S[i]*I[i] ) )
        I.append( I[i] + delta_t * ( alpha*S[i]*I[i] -beta*I[i] -g*I[i] ) )
        R.append( R[i] + delta_t * ( beta*I[i] ) )
        D.append( D[i] + delta_t * ( g*I[i] ) )

    return S, I, R, D


def vaccineSIR(delta_t, alpha, beta, gamma, delta, S0, I0, R0, D0, V0, steps):
    # dS/dt = -alpha*S*I -delta*S
    # dI/dt = alpha*S*I -beta*I -gamma*I
    # dR/dt = beta*I
    # dV/dt = delta*S
    # dD/dt = gamma*I
    S, I, R, D, V = [S0], [I0], [R0], [D0], [V0]
    for i in range(steps):
        g, d = validateConst(gamma, delta, I[i], i, delta_t)

        S.append( S[i] + delta_t * ( -alpha*S[i]*I[i] -d*S[i] ) )
        I.append( I[i] + delta_t * ( alpha*S[i]*I[i] -beta*I[i] -g*I[i] ) )
        R.append( R[i] + delta_t * ( beta*I[i] ) )
        D.append( D[i] + delta_t * ( g*I[i] ) )
        V.append( V[i] + delta_t * ( d*S[i] ) )

    return S, I, R, D, V

def vaccineSIRDeathSplit(delta_t, alpha, beta, gamma, delta, S0, I0, R0, D0, V0, steps):
    # dS/dt = -alpha*S*I -delta*S
    # dI/dt = alpha*S*I -beta*I -gamma*I
    # dR/dt = beta*I
    # dV/dt = delta*S
    # dD/dt = gamma*I
    S, I, R, D, V = [S0], [I0], [R0], [D0], [V0]
    Dy, Da, De = [0], [0], [0]
    for i in range(steps):
        g, d = validateConst(gamma, delta, I[i], i, delta_t)

        S.append( S[i] + delta_t * ( -alpha*S[i]*I[i] -d*S[i] ) )
        I.append( I[i] + delta_t * ( alpha*S[i]*I[i] -beta*I[i] -g*I[i] ) )
        R.append( R[i] + delta_t * ( beta*I[i] ) )
        V.append( V[i] + delta_t * ( d*S[i] ) )

        D.append( D[i] + delta_t * ( g*I[i] ) )
        Dy.append( D[i] * .01 )
        Da.append( D[i] * .15 )
        De.append( D[i] * .84 )

    return S, I, R, D, V, Dy, Da, De

def displayModel(X, Y, names, title):
    plt.style.use("dark_background")
    plt.figure( figsize=(6.4*2, 4.8*2) )
    plt.suptitle(title)
    plt.xlabel("Days")
    plt.ylabel("# People")

    ax = plt.twinx()
    step = 5000
    maxTick = int(np.max(np.array(Y)))
    yticks = [v for v in range(0, maxTick, step)]
    ax.set_yticks(yticks)

    for y in Y:
        plt.plot(X, y)
    plt.legend( names )

    #plt.show()
    plt.savefig("model-visuals/" + title.replace(" ", "-") + ".png", bbox_inches="tight")


def main():
    # initial susceptible population, (population of Washington County in 2017)
    S0 = 165662
    # inital infections
    I0 = 1
    #  initial recoverd
    R0 = 0
    # initail death
    D0 = 0
    # initial vaccinations
    V0 = 0

    transProb = .8
    infectTime  = 14 # days
    # force of infection
    nInteract = 11 # number of people interacted with on a given day
    alpha = (nInteract/S0) / infectTime * transProb
    nSocialDist = 3
    alphaSocialDist = (nSocialDist/S0) / infectTime * transProb

    # recovery rate
    beta = 1/infectTime

    # death rate
    gamma = [.02, .034]

    # number of people vaccinated on a given day
    nVaccine = 460
    delta = nVaccine / S0

    # start time
    a = 0
    # end time (in days)
    b = 365
    # divisions of change 
    N = 25000
    steps = N
    delta_t = (b-a)/N

    X = [ i*delta_t for i in range(N+1) ]
    S, I, R, D = basicSIR(delta_t, alpha, beta, gamma, S0, I0, R0, D0, steps)
    displayModel(X, [S, I, R, D], ["Susceptible", "Infected", "Recovered", "Dead"], "Covid-19 SIDR")
    S, I, R, D = basicSIR(delta_t, alphaSocialDist, beta, gamma, S0, I0, R0, D0, steps)
    displayModel(X, [S, I, R, D], ["Susceptible", "Infected", "Recovered", "Dead"], "Covid-19 SIDR with Social Distancing")

    S, I, R, D, V = vaccineSIR(delta_t, alpha, beta, gamma, delta, S0, I0, R0, D0, V0, steps)
    displayModel(X, [S, I, R, D, V], ["Susceptible", "Infected", "Recovered", "Dead", "Vaccinated"], "Covid-19 SIDRV")
    S, I, R, D, V = vaccineSIR(delta_t, alphaSocialDist, beta, gamma, delta, S0, I0, R0, D0, V0, steps)
    displayModel(X, [S, I, R, D, V], ["Susceptible", "Infected", "Recovered", "Dead", "Vaccinated"], "Covid-19 SIDRV with Social Distancing")

    S, I, R, D, V, Dy, Da, De = vaccineSIRDeathSplit(delta_t, alpha, beta, gamma, delta, S0, I0, R0, D0, V0, steps)
    displayModel(X, [S, I, R, D, V, Dy, Da, De], ["Susceptible", "Infected", "Recovered", "Total Dead", "Vaccinated", "Dead 20-60", "Dead 60-80", "Dead 80+"], "Covid-19 SIDRV Age Groups")
    S, I, R, D, V, Dy, Da, De = vaccineSIRDeathSplit(delta_t, alphaSocialDist, beta, gamma, delta, S0, I0, R0, D0, V0, steps)
    displayModel(X, [S, I, R, D, V, Dy, Da, De], ["Susceptible", "Infected", "Recovered", "Total Dead", "Vaccinated", "Dead 20-60", "Dead 60-80", "Dead 80+"], "Covid-19 SIDRV Age Groups with Social Distancing")

    with open("model-visuals/constants.txt", 'w') as fout:
        fout.write("Initial population, (population of Washington County in 2017): " + str(S0) + "\n")
        fout.write("Initial infected: " + str(I0) + "\n")
        fout.write("Initial recoverd: " + str(R0) + "\n")
        fout.write("Initial dead: " + str(D0) + "\n")
        fout.write("Initial vaccinated: " + str(V0) + "\n")
        fout.write("Tranmission probability, given interaction with infected: " + str(transProb) + "\n")
        fout.write("Days until recovery: " + str(infectTime) + "\n")
        fout.write("# per day of regular interaction: " + str(nInteract) + "\n")
        fout.write("# per day of interaction with social distancing: " + str(nSocialDist) + "\n")
        fout.write("Hospital capacity: " + str(HOPS_CAPACITY) + "\n")
        fout.write("Death rate while hospital capacity NOT reached: " + str(round(100*gamma[0], 1)) + '%' + "\n")
        fout.write("Death rate while hospital capacity reached: " + str(round(100*gamma[1], 1)) + '%' + "\n")
        fout.write("# per day of people vaccinated: " + str(nVaccine) + "\n")
        fout.write("Days before vaccine available: " + str(VAC_DAY) + "\n")

main()