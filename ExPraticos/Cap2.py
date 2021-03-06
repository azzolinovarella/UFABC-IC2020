import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import sin, cos, arccos, arctan, sqrt, pi
from celluloid import Camera

pd.set_option("display.max_columns", 15)


def ex_res_2_6(plot=False, animation=False):
    """
    Exercise:

    EXAMPLE 2.6 - Page 87
    Consider the crank-rocker four-bar linkage shown in Fig. 2.25 (pag. 88) with RBA = 100 mm, RCB =
    250 mm, RCD = 300 mm, and RDA = 200 mm. The paths of coupler pins B and C are
    shown by the circle and the circular arc, respectively. The location of coupler point P is
    given by RPB = 150 mm and α = ∠CBP = −45◦. Calculate the coordinates of coupler
    88 POSITION, POSTURE, AND DISPLACEMENT point P and plot the path of this point (the coupler curve)
    for a complete rotation of the crank.

    Let's use the equations:
        -> S = sqrt(r1**2 + r2**2 − 2*r1*r2*cos(theta2))
        -> beta = acos((r1**2 + S**2 - r2**2)/(2*r1*S))
        -> psi = acos((r3**2 + S**2 - r4**2)/(2*r3*S))
        -> lambda = acos((r4**2 + S**2 - r3**2)/(2*r4*S))
        -> gama = +/- acos((r3**2 + r4**2 - S**2)/(2*r3*r4))
        -> theta3 =
            * if 0 <= theta2 <= pi: - beta +/- psi
            * else: beta +/- psi
        -> Rp = sqrt(Ra ** 2 + Rpa ** 2 + 2*Ra*Rpa*cos(theta3 + alfa - theta2))
        -> theta6 = atan((Ra*sin(theta2) + Rpa*sin(theta3 + alfa))/(Ra*cos(theta2) + Rpa*cos(theta3 + alfa)))
    """
    # For our case we have that:
    r1 = 200  # ||AD|| in our example
    r2 = 100  # ||AB|| in our example
    r3 = 250  # ||BC|| in our example
    r4 = 300  # ||DC|| in our example
    Ra = r2  # ||AB|| in our example
    Rpa = 150  # ||BP|| in our example
    alfa = - pi / 4  # CBP in our example

    theta2 = np.linspace(0, 2 * pi, 361)  # Creating a Series with 361 elements, each one From 0 to 360 degree
    S = sqrt(r1 ** 2 + r2 ** 2 - 2 * r1 * r2 * cos(theta2))
    beta = arccos((r1 ** 2 + S ** 2 - r2 ** 2) / (2 * r1 * S))
    psi = arccos((r3 ** 2 + S ** 2 - r4 ** 2) / (2 * r3 * S))
    theta3 = np.array([psi[i] - beta[i] if 0 <= theta2[i] <= pi else psi[i] + beta[i] for i in range(0, len(theta2))])
    Rp = sqrt(Ra ** 2 + Rpa ** 2 + 2 * Ra * Rpa * cos(theta3 + alfa - theta2))
    theta6 = arctan((Ra * sin(theta2) + Rpa * sin(theta3 + alfa)) / (Ra * cos(theta2) + Rpa * cos(theta3 + alfa)))
    Rpx = Rp * cos(theta6)
    Rpy = Rp * sin(theta6)

    df = pd.DataFrame.from_dict({"theta2 (deg)": (theta2 * 180 / pi).round(1),
                                 "theta3 (deg)": (theta3 * 180 / pi).round(1),
                                 "Rp (mm)": Rp.round(1),
                                 "theta6 (deg)": (theta6 * 180 / pi).round(1),
                                 "Rpx (mm)": Rpx.round(1),
                                 "Rpy (mm)": Rpy.round(1)}).set_index(['theta2 (deg)'])

    if plot is True:
        plt.figure()
        plt.plot(Rpx, Rpy)
        plt.title("Curve made by the point P")
        plt.xlabel("x (mm)")
        plt.ylabel("y (mm)")
        plt.xlim((0, 250))
        plt.ylim((0, 150))
        plt.grid()
        plt.show()

    if animation is True:
        fig2, ax = plt.subplots()
        camera = Camera(fig2)
        plt.title("Curve made by the point P")
        plt.xlabel(f"x (mm)")
        plt.ylabel(f"y (mm)")
        plt.grid()
        for cont in range(0, len(Rpx)):
            plt.plot(Rpx, Rpy, color='grey')
            Px_i = Rpx[:cont]
            Py_i = Rpy[:cont]
            plt.plot(Px_i, Py_i, color='blue')
            ax.text(min(Rpx), max(Rpy), f"theta2 = {int(theta2[cont] * 180 / pi)}°")
            camera.snap()
        animation = camera.animate()
        animation.save('..\\gifs\\ex_res_2_6.gif', fps=20)

    return df


def ex_prop_2_23(r1, r2, r3, r4, coord1, coord2, coord_type='rectangular', unit='mm', animation=False):
    """
    Exercise:

    EXERCISE 2.23 - Page 101
    Write a computer program to plot the coupler
    curve of any crank-rocker or double-crank form of
    the four-bar linkage. The program should accept
    four link lengths and either rectangular or polar
    coordinates of the coupler point with respect to
    the coupler.
    :param r1: Lenght of the link1.
    :param r2: Lenght of the link2.
    :param r3: Lenght of the link3.
    :param r4: Lenght of the link3.
    :param coord1: First coordinate of the point P (x or R).
    :param coord2: Second coordinate of the point P (y or theta).
    :param coord_type: Coordinate type (can be rectangular or polar).
    :param unit: The unit used to measure the lenght of the links.
    :param animation: If you wanna generate a gif related to the curve, use it as True
    :return: A DataFrame and the curve made by the point P.
    """
    if coord_type not in ('rectangular', 'polar'):
        raise ValueError("Only rectangular and polar types accepted.")

    list_values = [r1, r2, r3, r4]
    list_values.sort()
    if list_values[0] + list_values[3] > list_values[1] + list_values[2]:
        raise ValueError("The Grashof Law was not satisfied.")

    if coord_type == 'polar':
        P0x, P0y = coord1 * cos(coord2), coord1 * sin(coord2)
        P0 = np.array([P0x, P0y])

    else:
        P0x, P0y = coord1, coord2
        P0 = np.array([P0x, P0y])

    theta2 = np.linspace(0, 2 * pi, 361)  # Our "input"

    # Now, calculating our variables in function of theta2:
    S = sqrt(r1 ** 2 + r2 ** 2 - 2 * r1 * r2 * cos(theta2))

    beta = arccos((r1 ** 2 + S ** 2 - r2 ** 2) / (2 * r1 * S))
    psi = arccos((r3 ** 2 + S ** 2 - r4 ** 2) / (2 * r3 * S))
    lamb = arccos((r4 ** 2 + S ** 2 - r3 ** 2) / (2 * r4 * S))

    theta3 = np.array([psi[i] - beta[i] if 0 <= theta2[i] <= pi else psi[i] + beta[i] for i in range(0, len(theta2))]) # There is any constraint?? PROBABLY YES! Check latter!!!
    theta4 = np.array([pi - beta[i] - lamb[i] if 0 <= theta2[i] <= pi else pi + beta[i] - lamb[i] for i in range(0, len(theta2))])  # There is any constraint?? PROBABLY YES! Check latter!!!

    # Calculating the points position:
    O = np.array([0, 0])  # Definition --> Do not change position!
    A = np.array([r2 * cos(theta2), r2 * sin(theta2)])
    B = np.array([r1 + r4 * cos(theta4), r4 * sin(theta4)])
    C = np.array([r1, 0])  # Definition --> In the same horizontal position as O and do not change its position!

    AP = np.linalg.norm(P0 - A[:, 0])
    alfa = arccos((P0x - r2 * cos(theta2[0])) / AP) - theta3[0]

    # Finally
    Px = r2 * cos(theta2) + AP * cos(theta3 + alfa)
    Py = r2 * sin(theta2) + AP * sin(theta3 + alfa)
    P = np.array([Px, Py])

    plt.figure()
    plt.plot(Px, Py)
    plt.title("Curve made by the point P")
    plt.xlabel(f"x ({unit})")
    plt.ylabel(f"y ({unit})")
    plt.grid()
    plt.show()

    if animation is True:
        fig2, ax = plt.subplots()
        camera = Camera(fig2)
        plt.title("Curve made by the point P")
        plt.xlabel(f"x ({unit})")
        plt.ylabel(f"y ({unit})")
        plt.grid()
        for cont in range(0, len(Px)):
            plt.plot(Px, Py, color='grey')
            Px_i = Px[:cont]
            Py_i = Py[:cont]
            plt.plot(Px_i, Py_i, color='blue')
            ax.text(min(Px), max(Py), f"theta2 = {int(theta2[cont] * 180 / pi)}°")
            camera.snap()
        animation = camera.animate()
        animation.save('..\\gifs\\ex_prop_2_23.gif', fps=20)

    df = pd.DataFrame.from_dict({"theta2 (deg)": (theta2 * 180 / pi).round(1),
                                 "theta3 (deg)": (theta3 * 180 / pi).round(1),
                                 "theta4 (deg)": (theta4 * 180 / pi).round(1),
                                 "Px (mm)": Px.round(1),
                                 "Rpy (mm)": Py.round(1)}).set_index(['theta2 (deg)'])

    return df


if __name__ == '__main__':
    print(ex_res_2_6(plot=True, animation=True))
    print(ex_prop_2_23(r1=260, r2=130, r3=250, r4=300, coord1=150, coord2=200, coord_type='rectangular', animation=True))

