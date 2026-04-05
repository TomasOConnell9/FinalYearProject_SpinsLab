import numpy as np

#creating and input fucntion so users can define their own state
def get_input_state():

    print("Enter the coefficients for your quantum state ψ = a|1> + b|2>")

    a_str = input("Enter a (e.g., 1, 0.5, 1j, 0.5+0.5j, 1/√2 as 1/2**0.5): ")
    b_str = input("Enter b (e.g., 1, 0.5, 1j, 0.5+0.5j, 1/√2 as 1/2**0.5): ")

    try:
        a = complex(eval(a_str))
        b = complex(eval(b_str))
    except Exception:
        print("Invalid input. Use numbers like 1, 0.5, 1j, 0.5+0.5j, 1/2**0.5")
        return None

    vec = np.array([a, b], dtype=complex)

    norm = np.linalg.norm(vec)

    vec /= norm  # normalize state vector 
    return vec

psi = get_input_state()
if psi is not None:
    print("Normalized state vector:", psi)