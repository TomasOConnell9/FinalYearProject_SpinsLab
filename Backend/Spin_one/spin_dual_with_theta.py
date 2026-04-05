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

def measure_θφ(state, theta_deg, phi_deg):
    theta = np.deg2rad(theta_deg)
    phi = np.deg2rad(phi_deg)
    
    T_plus = np.array([
        ((1 + np.cos(theta)) / 2) * np.exp(-1j * phi),
        (np.sin(theta) / np.sqrt(2)),
        ((1 - np.cos(theta)) / 2) * np.exp(1j * phi)
    ], dtype=complex)

    T_zero = np.array([
        (-np.sin(theta) / np.sqrt(2)) * np.exp(-1j * phi),
        np.cos(theta),
        (np.sin(theta) / np.sqrt(2)) * np.exp(1j * phi)
    ], dtype=complex)

    T_minus = np.array([
        ((1 - np.cos(theta)) / 2) * np.exp(-1j * phi),
        (-np.sin(theta) / np.sqrt(2)),
        ((1 + np.cos(theta)) / 2) * np.exp(1j * phi)
    ], dtype=complex)

    # 3. Calculate probabilities using the Born Rule: P = |<basis|state>|^2
    prob_up   = np.abs(np.vdot(T_plus, state))**2
    prob_zero = np.abs(np.vdot(T_zero, state))**2
    prob_down = np.abs(np.vdot(T_minus, state))**2

    # 4. Roll the dice
    num = random.random()
    if num < prob_up:
        return T_plus, "up"
    elif num < prob_up + prob_zero:
        return T_zero, "zero"
    else:
        return T_minus, "down"

def measure(state, axis, theta_deg=0, phi_deg=0):   
    if axis == "z":
        return measure_z(state)
    elif axis == "x":
        return measure_x(state)
    elif axis == "y":
        return measure_y(state)
    elif axis == "θφ":
        return measure_θφ(state, theta_deg, phi_deg)
    else:
        raise ValueError("Invalid axis. Choose x, y, z, or θφ.")


def run_two_measurements():
    axis1 = axis1_var.get()
    axis2 = axis2_var.get()
    filter_choice = filter_var.get()
    
    try:
        N = int(entry_atoms.get())
        # Fetch angles from entry boxes - make sure these variable names match your GUI
        t_val = float(entry_theta.get()) 
        p_val = float(entry_phi.get())
    except ValueError:
        result_label.config(text="Check numbers for Atoms, Theta, and Phi.")
        return

    # Tracking outcomes
    second_up = 0
    second_zero = 0
    second_down = 0

    for i in range(N):
        psi = random_state() 
  
        collapsed_state, outcome1 = measure(psi, axis1, theta_deg=t_val, phi_deg=p_val)


        if outcome1 == filter_choice: 
            
            _, outcome2 = measure(collapsed_state, axis2, theta_deg=t_val, phi_deg=p_val)
            
            if outcome2 == "up":
                second_up += 1
            elif outcome2 == "zero":
                second_zero += 1
            elif outcome2 == "down":
                second_down += axis1
                
    result_label.config(
        text=f"Filter: {axis1.upper()} ({filter_choice})\n"
             f"Measured on: {axis2.upper()}\n"
             f"-------------------\n"
             f"Up:    {second_up}\n"
             f"Zero:  {second_zero}\n"
             f"Down:  {second_down}"
    )


root = tk.Tk()
root.title("Stern-Gerlach Simulator")


axis1_var = tk.StringVar(value="z")
tk.Label(root, text="First analyzer axis:").pack()
tk.OptionMenu(root, axis1_var, "x", "y", "z", "θφ").pack()

filter_var = tk.StringVar(value="up")
tk.Label(root, text="Filter outcome from first analyzer:").pack()
tk.OptionMenu(root, filter_var, "up", "zero", "down").pack()

axis2_var = tk.StringVar(value="z")
tk.Label(root, text="Second analyzer axis:").pack()
tk.OptionMenu(root, axis2_var, "x", "y", "z", "θφ").pack()


tk.Label(root, text="Angle θ (degrees):").pack()
entry_theta = tk.Entry(root)
entry_theta.insert(0, "0")
entry_theta.pack()

tk.Label(root, text="Angle φ (degrees):").pack()
entry_phi = tk.Entry(root)
entry_phi.insert(0, "0")
entry_phi.pack()


tk.Label(root, text="Number of atoms:").pack()
entry_atoms = tk.Entry(root)
entry_atoms.insert(0, "10000")
entry_atoms.pack()


tk.Button(root, text="Run Sequential Measurement", command=run_two_measurements).pack(pady=5)


result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()