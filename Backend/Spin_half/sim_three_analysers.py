import numpy as np
import random
import tkinter as tk


Z_plus = np.array([1, 0], dtype=complex)
Z_minus = np.array([0, 1], dtype=complex)
X_plus = (1/np.sqrt(2)) * np.array([1, 1], dtype=complex)
X_minus = (1/np.sqrt(2)) * np.array([1, -1], dtype=complex)
Y_plus = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)


def random_state():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b], dtype=complex)
    vec /= np.linalg.norm(vec)
    return vec

def measure_z(state):
    prob_up = np.abs(np.vdot(Z_plus, state))**2
    return (Z_plus, "up") if random.random() < prob_up else (Z_minus, "down")

def measure_x(state):
    prob_up = np.abs(np.vdot(X_plus, state))**2
    return (X_plus, "up") if random.random() < prob_up else (X_minus, "down")

def measure_y(state):
    prob_up = np.abs(np.vdot(Y_plus, state))**2
    return (Y_plus, "up") if random.random() < prob_up else (Y_minus, "down")

def measure(state, axis):
    if axis == "z": return measure_z(state)
    if axis == "x": return measure_x(state)
    if axis == "y": return measure_y(state)
    raise ValueError("Invalid axis. Choose x, y, or z.")


def run_three_measurements():
    axis1 = axis1_var.get()
    axis2 = axis2_var.get()
    axis3 = axis3_var.get()
    filter1 = filter1_var.get()
    filter2 = filter2_var.get()


    try:
        N = int(entry_atoms.get())
    except ValueError:
        result_label.config(text="Please enter a valid number of atoms.")
        return

    second_up = second_down = 0
    third_up = third_down = 0

    for i in range(N):
        psi = random_state()
        collapsed_state1, outcome1 = measure(psi, axis1)

        #allow atom through if both paths are open, otherwise only allow the atoms travelling along open path through
        if filter1 == "both" or outcome1 == filter1:
            collapsed_state2, outcome2 = measure(collapsed_state1, axis2) #measure the collapsed state along a second analyser

            #same idea as first analyser atoms follow the same rules
            if filter2 == "both" or outcome2 == filter2:
                if outcome2 == "up":
                    second_up += 1
                else:
                    second_down += 1
                
                #make final measurement
                _, outcome3 = measure(collapsed_state2, axis3)
                if outcome3 == "up":
                    third_up += 1
                else:
                    third_down += 1

    result_label.config(
        text=f"Second measurement ({axis2.upper()}):\n"
             f"  Up:   {second_up}\n"
             f"  Down: {second_down}\n\n"
             f"Third measurement ({axis3.upper()})\n"
             f"  Up:   {third_up}\n"
             f"  Down: {third_down}"
    )


root = tk.Tk()
root.title("Three-Analyzer Stern–Gerlach Simulator")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="First analyzer axis:").grid(row=0, column=0, padx=5, pady=2)
axis1_var = tk.StringVar(value="z")
tk.OptionMenu(frame_top, axis1_var, "x", "y", "z").grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_top, text="Filter outcome (1st):").grid(row=1, column=0, padx=5, pady=2)
filter1_var = tk.StringVar(value="up")
tk.OptionMenu(frame_top, filter1_var, "up", "down", "both").grid(row=1, column=1, padx=5, pady=2)


tk.Label(frame_top, text="Second analyzer axis:").grid(row=0, column=2, padx=5, pady=2)
axis2_var = tk.StringVar(value="y")
tk.OptionMenu(frame_top, axis2_var, "x", "y", "z").grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_top, text="Filter outcome (2nd):").grid(row=1, column=2, padx=5, pady=2)
filter2_var = tk.StringVar(value="up")
tk.OptionMenu(frame_top, filter2_var, "up", "down", "both").grid(row=1, column=3, padx=5, pady=2)


tk.Label(frame_top, text="Third analyzer axis:").grid(row=2, column=0, padx=5, pady=2)
axis3_var = tk.StringVar(value="z")
tk.OptionMenu(frame_top, axis3_var, "x", "y", "z").grid(row=2, column=1, padx=5, pady=2)

tk.Label(root, text="Number of atoms:").pack()
entry_atoms = tk.Entry(root)
entry_atoms.insert(0, "10000")
entry_atoms.pack()

tk.Button(root, text="Run Three Measurements", command=run_three_measurements).pack(pady=8)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
