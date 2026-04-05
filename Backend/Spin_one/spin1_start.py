import numpy as np
import random
import math as m

Z_plus = np.array([1, 0, 0], dtype=complex)
Z_zero = np.array([0, 1, 0], dtype=complex)
Z_minus = np.array([0, 0, 1], dtype=complex)

X_plus = np.array([0.5, 1/np.sqrt(2), 0.5])
X_zero = np.array([1/np.sqrt(2), 0, -1/np.sqrt(2)])
X_minus = np.array([0.5, -1/np.sqrt(2), 0.5])

Y_plus = np.array([0.5, 1j/np.sqrt(2), -0.5])
Y_zero = np.array([1/np.sqrt(2), 0, 1/np.sqrt(2)])
Y_minus = np.array([0.5, -1j/np.sqrt(2), -0.5])

def get_manual_state():
    print("Enter the coefficients for your quantum state ψ = a|1> + b|2> + c|3>")
    
    a_str = input("Enter a: ").replace("root", "np.sqrt")
    b_str = input("Enter b: ").replace("root", "np.sqrt")
    c_str = input("Enter c: ").replace("root", "np.sqrt")
    
    try:
        a = complex(eval(a_str))
        b = complex(eval(b_str))
        c = complex(eval(c_str))
    except Exception as e:
        print(f"Error: {e}")
        return None

    vec = np.array([a, b, c], dtype=complex)
    vec /= np.linalg.norm(vec)
    return vec


def random_state():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    c = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b, c], dtype=complex)
    #print(vec)
    vec = vec / np.linalg.norm(vec)
    #print(vec)
    return vec

def measure_z(state):
    prob_up = np.abs(np.vdot(Z_plus, state))**2
    prob_zero = np.abs(np.vdot(Z_zero, state))**2
    prob_down = np.abs(np.vdot(Z_minus, state))**2
    
    num = random.random()
    
    if num < prob_up:
        return Z_plus, "up"
    elif num < prob_up + prob_zero:
        return Z_zero, "zero"
    else:
        return Z_minus, "down"
    
    #print(f" Probabilities: Up = {prob_up:.2f}, Zero = {prob_zero:.2f}  Down = {prob_down:.2f}, Total = {prob_up+prob_zero+prob_down:.2f}")
    
def measure_x(state):
    prob_up = np.abs(np.vdot(X_plus, state))**2
    prob_zero = np.abs(np.vdot(X_zero, state))**2
    prob_down = np.abs(np.vdot(X_minus, state))**2
    
    num = random.random()
    
    if num < prob_up:
        return X_plus, "up"
    elif num < prob_up + prob_zero:
        return X_zero, "zero"
    else:
        return X_minus, "down"
        
    #print(f" Probabilities: Up = {prob_up:.2f}, Zero = {prob_zero:.2f}  Down = {prob_down:.2f}, Total = {prob_up+prob_zero+prob_down:.2f}")
        
def measure_y(state):
    prob_up = np.abs(np.vdot(Y_plus, state))**2
    prob_zero = np.abs(np.vdot(Y_zero, state))**2
    prob_down = np.abs(np.vdot(Y_minus, state))**2
    
    num = random.random()
    
    if num < prob_up:
        return Y_plus, "up"
    elif num < prob_up + prob_zero:
        return Y_zero, "zero"
    else:
        return Y_minus, "down"
    
    #print(f" Probabilities: Up = {prob_up:.2f}, Zero = {prob_zero:.2f}  Down = {prob_down:.2f}, Total = {prob_up+prob_zero+prob_down:.2f}")




N = 10000
up_count = 0
zero_count = 0
down_count = 0
psi = get_manual_state()

if psi is not None:
    for i in range(N):
        _, outcome = measure_y(psi)
        
        if outcome == "up":
            up_count += 1
        elif outcome == "zero":
            zero_count += 1
        else:
            down_count += 1
            
    print(f"Results after {N} simulations:")
    print("up:", up_count)
    print("zero:", zero_count)
    print("down:", down_count)
else:
    print("Simulation aborted: No valid quantum state provided.")
    
