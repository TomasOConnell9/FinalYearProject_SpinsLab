import numpy as np
import random
import math as m
import tkinter as tk

Z_plus = np.array([1, 0, 0], dtype=complex)
Z_zero = np.array([0, 1, 0], dtype=complex)
Z_minus = np.array([0, 0, 1], dtype=complex)

X_plus = np.array([0.5, 1/np.sqrt(2), 0.5])
X_zero = np.array([1/np.sqrt(2), 0, -1/np.sqrt(2)])
X_minus = np.array([0.5, -1/np.sqrt(2), 0.5])

Y_plus = np.array([0.5, 1j/np.sqrt(2), -0.5])
Y_zero = np.array([1/np.sqrt(2), 0, 1/np.sqrt(2)])
Y_minus = np.array([0.5, -1j/np.sqrt(2), -0.5])

def get_angle_amplitudes(theta, phi):
    theta = np.deg2rad(theta)
    phi = np.deg2rad(phi)
    up = ((1 + m.cos(theta)) / 2) * (np.exp(-1j * phi))
    zero = (m.sin(theta) / m.sqrt(2))
    down = ((1 - m.cos(theta)) / 2) * (np.exp(1j * phi)) 
    amps = np.array([up,zero,down], dtype=complex)
    return amps

amps = get_angle_amplitudes(86, 153)



zp_plus  = np.abs(np.vdot(Z_plus, amps))**2
zp_zero  = np.abs(np.vdot(Z_zero, amps))**2
zp_minus = np.abs(np.vdot(Z_minus, amps))**2

xp_plus  = np.abs(np.vdot(X_plus, amps))**2
xp_zero  = np.abs(np.vdot(X_zero, amps))**2
xp_minus = np.abs(np.vdot(X_minus, amps))**2

yp_plus  = np.abs(np.vdot(Y_plus, amps))**2
yp_zero  = np.abs(np.vdot(Y_zero, amps))**2
yp_minus = np.abs(np.vdot(Y_minus, amps))**2


print(f"up: {(zp_plus * 100):.2f}% zero: {(zp_zero * 100):.2f}% down: {(zp_minus * 100):.2f}%")
print("Check sum for Z:", zp_plus + zp_zero + zp_minus, "\n")

print(f"up: {(yp_plus * 100):.2f}% zero: {(yp_zero * 100):.2f}% down: {(yp_minus * 100):.2f}%")
print("Check sum for Y:", yp_plus + yp_zero +yp_minus,"\n")

print(f"up: {(xp_plus * 100):.2f}% zero: {(xp_zero * 100):.2f}% down: {(xp_minus * 100):.2f}%")
print(f"Check sum for X: {(xp_plus + xp_zero + xp_minus):.2f}")