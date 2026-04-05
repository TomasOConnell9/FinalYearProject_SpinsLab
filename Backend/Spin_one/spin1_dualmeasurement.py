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


def measure(state, axis):
    """General measurement along chosen axis."""
    if axis == "z":
        return measure_z(state)
    elif axis == "x":
        return measure_x(state)
    elif axis == "y":
        return measure_y(state)
    else:
        raise ValueError("Invalid axis. Choose x, y, or z.")


def run_two_measurements():
    axis1 = axis1_var.get() #Pick what axis for first measurment
    axis2 = axis2_var.get() #Pick second axis
    filter_choice = filter_var.get() #Up or down 
    try:
        N = int(entry_atoms.get()) #Pick how many atoms we want to measure
    except ValueError:
        result_label.config(text="Please enter a valid number of atoms.")
        return

    first_up = 0
    first_down = 0
    first_zero = 0
    second_zero = 0
    second_up = 0
    second_down = 0 #these four set each state measurement to 0

    for i in range(N): #for every index, i, in N we are going to:
        psi = random_state() #generate a random state
        collapsed_state, outcome1 = measure(psi, axis1) #Measure along first axis, collapsed state is now tied to outcome from measurement 1

        if outcome1 == "up":
            first_up += 1
        elif outcome1 == "zero":
            first_zero += 1
        else:
            first_down += 1

        if outcome1 == filter_choice: #if outcome of axis1 is the same as the filter choice, outcome passes through. Otherwise its blocked. 
            _, outcome2 = measure(collapsed_state, axis2)  # Measure the same atom along the second axis; outcome2 is "up" or "down" based on quantum probabilities
            if outcome2 == "up":
                second_up += 1
            elif outcome2 == "zero":
                second_zero += 1
            else:
                second_down += 1

    result_label.config(
        text=f"Second measurement ({axis2.upper()})"
             f"\nUp:   {second_up}"
             f"\nZero: {second_zero}"
             f"\nDown: {second_down}"
    )



root = tk.Tk()
root.title("Stern-Gerlach Simulator")


axis1_var = tk.StringVar(value="z")
tk.Label(root, text="First analyzer axis:").pack()
tk.OptionMenu(root, axis1_var, "x", "y", "z").pack()


filter_var = tk.StringVar(value="up")
tk.Label(root, text="Filter outcome from first analyzer:").pack()
tk.OptionMenu(root, filter_var, "up", "zero", "down").pack()

axis2_var = tk.StringVar(value="z")
tk.Label(root, text="Second analyzer axis:").pack()
tk.OptionMenu(root, axis2_var, "x", "y", "z").pack()

tk.Label(root, text="Number of atoms:").pack()
entry_atoms = tk.Entry(root)
entry_atoms.insert(0, "10000")
entry_atoms.pack()

tk.Button(root, text="Run Sequential Measurement", command=run_two_measurements).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()