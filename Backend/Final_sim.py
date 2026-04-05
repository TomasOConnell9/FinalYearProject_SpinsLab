from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import re
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Z_plus_half = np.array([1, 0], dtype=complex)
Z_minus_half = np.array([0, 1], dtype=complex)

X_plus_half = (1/np.sqrt(2)) * np.array([1, 1], dtype=complex)
X_minus_half = (1/np.sqrt(2)) * np.array([1, -1], dtype=complex)

Y_plus_half = (1/np.sqrt(2)) * np.array([1, 1j], dtype=complex)
Y_minus_half = (1/np.sqrt(2)) * np.array([1, -1j], dtype=complex)


Z_plus_one = np.array([1, 0, 0], dtype=complex)
Z_minus_one = np.array([0, 0, 1], dtype=complex)
Z_zero_one = np.array([0, 1, 0], dtype=complex)

X_plus_one = np.array([0.5, 1/np.sqrt(2), 0.5], dtype=complex)
X_zero_one = np.array([1/np.sqrt(2), 0, -1/np.sqrt(2)], dtype=complex)
X_minus_one = np.array([0.5, -1/np.sqrt(2), 0.5], dtype=complex)

Y_plus_one = np.array([0.5, -1j/np.sqrt(2), -0.5], dtype=complex)
Y_zero_one = np.array([1/np.sqrt(2), 0, 1/np.sqrt(2)], dtype=complex)
Y_minus_one = np.array([0.5, 1j/np.sqrt(2), -0.5], dtype=complex)

#generate random complex vectors for spin half and spin one
def random_state_half():
    a = np.random.randn() + 1j*np.random.randn() 
    b = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b], dtype=complex)
    vec = vec / np.linalg.norm(vec)
    return vec


def random_state_one():
    a = np.random.randn() + 1j*np.random.randn()
    b = np.random.randn() + 1j*np.random.randn()
    c = np.random.randn() + 1j*np.random.randn()
    vec = np.array([a, b, c], dtype=complex)
    #print(vec)
    vec = vec / np.linalg.norm(vec)
    #print(vec)
    return vec

def manual_input_half(a, b):
    namespace = {"np": np, "i": 1j, "complex": complex}
    
    a = complex(eval(convert_expression(a), namespace))
    b = complex(eval(convert_expression(b), namespace))
    
    state = np.array([a, b], dtype=complex)
    raw = np.linalg.norm(state)
    #flag if the normalisation factor is greater than 1
    was_normalised = bool(abs(raw - 1.0) > 1e-6)
    
    state /= np.linalg.norm(state)
    return state, was_normalised

def manual_input_one(a, b, c):
    namespace = {"np": np, "i": 1j, "complex": complex}
    
    a = complex(eval(convert_expression(a), namespace))
    b = complex(eval(convert_expression(b), namespace))
    c = complex(eval(convert_expression(c), namespace))
    
    state = np.array([a, b, c], dtype=complex)
    raw = np.linalg.norm(state)
    was_normalised = bool(abs(raw - 1.0) > 1e-6)
    
    state /= np.linalg.norm(state)
    return state, was_normalised


def theta_plus_half(theta, phi=0):
    θ = np.radians(theta)
    φ = np.radians(phi)
    return np.array([np.cos(θ/2), np.exp(1j*φ)*np.sin(θ/2)], dtype=complex)

def theta_minus_half(theta, phi=0):
    θ = np.radians(theta)
    φ = np.radians(phi)
    return np.array([-np.exp(-1j*φ)*np.sin(θ/2), np.cos(θ/2)], dtype=complex)


def theta_plus_one(theta, phi=0):
    θ = np.radians(theta)
    φ = np.radians(phi)
    return np.array([((1 + np.cos(θ))/2)*np.exp(1j*φ), np.sin(θ)/np.sqrt(2), ((1 - np.cos(θ))/2)*np.exp(-1j*φ)], dtype=complex)

def theta_zero_one(theta, phi=0):
    θ = np.radians(theta)
    φ = np.radians(phi)
    return np.array([(-np.sin(θ)/np.sqrt(2))*np.exp(1j*φ), np.cos(θ), (np.sin(θ)/np.sqrt(2))*np.exp(-1j*φ)], dtype=complex)

def theta_minus_one(theta, phi=0):
    θ = np.radians(theta)
    φ = np.radians(phi)
    return np.array([((1 - np.cos(θ))/2)*np.exp(1j*φ), -np.sin(θ)/np.sqrt(2), ((1 + np.cos(θ))/2)*np.exp(-1j*φ)], dtype=complex)


def measure_half_axis(state, basis_plus, basis_minus):
    probs = [abs(np.vdot(basis_plus, state))**2, abs(np.vdot(basis_minus, state))**2] #probabilities for eigenstates 
    outcome = "up" if random.random() < probs[0] else "down" #probablistic determination of outcome
    return (basis_plus if outcome == "up" else basis_minus, outcome)

def measure_one_axis(state, basis_up, basis_zero, basis_down):
    probs = [abs(np.vdot(basis_up, state))**2, abs(np.vdot(basis_zero, state))**2, abs(np.vdot(basis_down, state))**2]
    num = random.random()
    outcome = ("up" if num < probs[0] else "zero" if num < probs[0] + probs[1] else "down")
    return (basis_up if outcome == "up" else basis_zero if outcome == "zero" else basis_down , outcome)

#converts buttons on the calculator the calculations python understands 
def convert_expression(expr: str):
    if not expr:
        return expr
    expr = re.sub(r"√\(([^)]+)\)", r"(\1)**0.5", expr)
    expr = expr.replace("^", "**")
    expr = expr.replace("e^", "exp")
    expr = expr.replace("π", "np.pi")
    expr = expr.replace("e", "(np.e)")
    expr = re.sub(r'(\d)i', r'\1*(1j)', expr)
    expr = re.sub(r'\bi\b', '(1j)', expr) #for user experience "i" is better than "1j", this convert "3i" → "3*(1j)" so Python can evaluate it
    #print(f"Final converted: {expr}")#for debugging, verify conversion
    return expr 

#Pydantic model which represents an analyser box in the simulation
class AnalyserInput(BaseModel):
    axis: str 
    filter: str 
    theta: float = None 
    phi: float = 0

#Pydantic model for the full simulation request
class MeasurementRequest(BaseModel):
    SQN: str 
    analysers: list[AnalyserInput] 
    atoms: int 
    a: str = None 
    b: str = None 
    c: str = None 
    streaming: bool = False 


#Function that takes in the type of spin, the quantum state, the selceted axis and the polar/azimuthal angle if selected
def measure(SQN, state, axis, theta=None, phi=0):
    if SQN == "1/2": #first case, if user selected spin 1/2 system
        # depending on which axis was selected, pass the state into their respective measurement functions and find their probabilities
        if axis == "x":
            return measure_half_axis(state, X_plus_half, X_minus_half)
        elif axis == "y":
            return measure_half_axis(state, Y_plus_half, Y_minus_half)
        elif axis == "z":
            return measure_half_axis(state, Z_plus_half, Z_minus_half)
        elif axis == "θ/φ":
            return measure_half_axis(state, theta_plus_half(theta, phi), theta_minus_half(theta, phi))
        else:
            raise ValueError("Invalid axis")
    else: #second case, if spin 1 is selected
        if axis == "x":
            return measure_one_axis(state, X_plus_one, X_zero_one, X_minus_one)
        elif axis == "y":
            return measure_one_axis(state, Y_plus_one, Y_zero_one, Y_minus_one)
        elif axis == "z":
            return measure_one_axis(state, Z_plus_one, Z_zero_one, Z_minus_one)
        elif axis == "θ/φ":
            return measure_one_axis(state, theta_plus_one(theta, phi), theta_zero_one(theta, phi), theta_minus_one(theta, phi))
        else:
            raise ValueError("Invalid axis")
            
@app.post("/measurements")
def run_measurements(sim: MeasurementRequest):
    """
    Simulation endpoint that receives the full user configuration
    from the frontend and returns the measurement results.

    FastAPI validates the incoming JSON and automatically converts
    it into a MeasurementRequest object, passed as 'sim'.
    """
    
    counts = {"up": 0, "down": 0} if sim.SQN == "1/2" else {"up": 0, "zero": 0, "down": 0} #step the initial counts to 0 across all spin types
    need_to_norm = False #for detection of normalisation
    
    for i in range(sim.atoms): #simulate each atom independently

        #build the atoms initial qunatum state
        if sim.SQN == "1/2":
            if sim.a and sim.b: #if coefficients are provided by user
               state , was_normalised = manual_input_half(sim.a, sim.b)
               if was_normalised:
                   need_to_norm = True
            else:
                state = random_state_half()
        else:
            if sim.a and sim.b and sim.c:
                state, was_normalised = manual_input_one(sim.a, sim.b, sim.c)
                
                if was_normalised:
                    need_to_norm = True
            else:
                state = random_state_one()
                
        final_outcome = None #set the final_outcome to none so if the atom gets blocked

        #Passing each atom through each analyser in order
        for idx, analyser in enumerate(sim.analysers):
            is_last = (idx == len(sim.analysers) - 1) #need to know last analyser as its connected to the detector

            #Both paths are open and not the final counter
            if analyser.filter == "all" and not is_last:
                # The atom passes through no change, coherance
                continue 

            # spin-1 one measurement with one or two paths blocked
            elif not is_last and analyser.filter != "all" and sim.SQN == "1":
                allowed = analyser.filter.split(",")
                
                #search for what paths are blocked, and project out the eigenstate
                if "up" not in allowed:
                    if analyser.axis == "z":
                        state = state - np.vdot(Z_plus_one, state) * Z_plus_one
                    if analyser.axis == "y":
                        state = state - np.vdot(Y_plus_one, state) * Y_plus_one
                    if analyser.axis == "x":
                        state = state - np.vdot(X_plus_one, state) * X_plus_one
                    if analyser.axis == "θ/φ":
                        up_vec = theta_plus_one(analyser.theta, analyser.phi)
                        state = state - np.vdot(up_vec, state) * up_vec
                
                if "zero" not in allowed:
                    if analyser.axis == "z":
                        state = state - np.vdot(Z_zero_one, state) * Z_zero_one
                    if analyser.axis == "y":
                        state = state - np.vdot(Y_zero_one, state) * Y_zero_one
                    if analyser.axis == "x":
                        state = state - np.vdot(X_zero_one, state) * X_zero_one
                    if analyser.axis == "θ/φ":
                        zero_vec = theta_zero_one(analyser.theta, analyser.phi)
                        state = state - np.vdot(zero_vec, state) * zero_vec

                if "down" not in allowed:
                    if analyser.axis == "z":
                        state = state - np.vdot(Z_minus_one, state) * Z_minus_one
                    if analyser.axis == "y":
                        state = state - np.vdot(Y_minus_one, state) * Y_minus_one
                    if analyser.axis == "x":
                        state = state - np.vdot(X_minus_one, state) * X_minus_one
                    if analyser.axis == "θ/φ":
                        down_vec = theta_minus_one(analyser.theta, analyser.phi)
                        state = state - np.vdot(down_vec, state) * down_vec
                
                updated_norm = np.linalg.norm(state)
                
                #probablistic blocking of particles
                if random.random() > updated_norm ** 2:
                    final_outcome = None
                    break
                
                state = state/updated_norm

            else: # measurement is performed and state collapses to an eigenstate where outcome is recorded
                state, outcome = measure(sim.SQN, state, analyser.axis, theta=analyser.theta, phi=analyser.phi)


                if analyser.filter != "all": #if user blocked a path see if the atom took that path
                    allowed = analyser.filter.split(",") 
                    if outcome not in allowed:
                        final_outcome = None #if the atom landed in blocked path, change the final_outcome to none
                        break

                #if it's the very last analyser, save the outcome for the counts
                if is_last:
                    final_outcome = outcome

        if final_outcome :#only count the atoms that make it through the entire chain without being blocked
            counts[final_outcome] += 1 #count[final_outcome] will be something like counts["up"] and will increase the up count by 1

    return {"results": [counts], "need_to_norm": need_to_norm}