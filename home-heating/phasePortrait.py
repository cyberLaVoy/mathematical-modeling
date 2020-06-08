import numpy as np
import matplotlib.pyplot as plt

def dydx(y):
    A = 0
    k = -.01
    r0 = .21
    return k*(y-A) + r0

def main():
    plt.style.use("dark_background")
    x = np.arange(0, 100, 10)
    y = np.arange(-9, 43, 2)
    X, Y = np.meshgrid(x, y)
    U = np.ones(Y.shape)
    V = dydx(Y)

    plt.title("Home Heating Phase Portrait")
    plt.quiver(X, Y, U, V, abs(V))
    plt.grid()
    plt.xlabel("Time (Hours)")
    plt.ylabel("Temperature (Celsius)")
    plt.show()

main()