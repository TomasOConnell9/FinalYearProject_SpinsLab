import numpy as np 
import random

Z_plus = np.array([1, 0], dtype=complex)
Z_minus = np.array([0, 1], dtype=complex)


def random_state():
    #generate two random complex numbers 
    a = np.random.randn() + 1j*np.random.randn() 
    b = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b], dtype=complex) #convert to vector 
    #print(vec)
    vec = vec / np.linalg.norm(vec) #normalise state
    return vec

def measure_z(state):
    #Use Born's rule to find probabilities
    prob_up = np.abs(np.vdot(Z_plus, state))**2
    prob_down = np.abs(np.vdot(Z_minus, state))**2
    
    print(f" Probabilities: Up = {prob_up:.2f}, Down = {prob_down:.2f}, Total = {prob_up+prob_down:.2f}")
    
    #enforce probablistic nature of quantum mechancics
    if random.random() < prob_up:
        return Z_plus, "up"
    else:
        return Z_minus, "down"
    

N = 1
up_count = 0
down_count = 0
for i in range(N):
    #generate thee quantum state
    psi = random_state()
    a = psi[0]
    b = psi[1]
    
    print(f"||ψ⟩ = ({a:.2f})|1⟩ + ({b:.2f})|2⟩")
    
    _, outcome = measure_z(psi) #returns eigen state and outcome, we only care about the outcome 
    print("Measurement result: ", outcome)
    if outcome == "up":
        up_count += 1
    else:
        down_count += 1
    
print("Z-up:", up_count)
print("Z-down", down_count)



