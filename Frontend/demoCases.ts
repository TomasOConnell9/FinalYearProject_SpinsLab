export const waveFunctionCollapseDesc = {
  title: "Wave Function Collapse: Z Axis Measurement",
  setup: [
    "Source fires 10,000 atoms in a random prepared state (R)",
    "Analyser 1 is aligned along Z axis with only spin-up (↑) open",
    "Analyser 2 is aligned along Z axis with both paths open",
  ],
  observe: [
    "Roughly 5,000 atoms make it through the first analyser ",
    "100% of remaining atoms are measured as spin-up (↑) at analyser 2",
    "Zero atoms are measured as spin-down (↓)",
  ],
  explanation: "When the atoms emerge from the first analyser a measurement is made, forcing the wavefunction to collapse into either the z-up or the z-down eigenstate. When the spin-down path is blocked only the spin-up eigenstate continues. The atoms are no longer in a superposition with respect to the Z axis. When the second measurement is made in the same basis, the outcome is spin-up with 100% certainty, confirming the system has collapsed.",
};


export const rotatingParticle = {
  title: "Rotating the measurement: θ/φ Axis Measurement",
  setup: [
    "Source fires 10,000 atoms in a random prepared state (R)",
    "Analyser 1 is aligned along Z axis with only spin-up (↑) open",
    "Analyser 2 is set to θ/φ and has theta set to 180° and phi set to 0°",
  ],
  observe: [
    "Roughly 5,000 atoms make it through Analyser 1",
    "100% of remaining atoms are measured as spin-up (↓) at Analyser 2",
    "Zero atoms are measured as spin-down (↑)",
  ],
  explanation: "When the first analyser collapses the state into a definite spin-up state along the Z-axis, the particle is then rotated by 180°. When the second analyser makes another measurement, the wavefunction collapses again, and the outcome is spin-down with complete certainty, the opposite direction of the initial state."
};

export const InformatioLoss =  {
  title: "Information Loss: Measurement in a Different Basis",
  setup: [
    "Source fires 10,000 atoms in a random prepared state (R) to the analyser 1",
    "Analyser 1 is aligned along Z with only spin-up (↑) open",
    "Analyser 2 is aligned along X with only spin-down (↓) open",
    "Final analyser is aligned along Z again, with both paths open",
  ],
  observe: [
    "Roughly 5,000 atoms make it through analyser 1",
    "Roughly 2,500 atoms make it through analyser 2",
    "50% of the remaining atoms are measured as spin-up and the other 50% as spin-down",
    "Information is lost",
  ],
  explanation: "The first analyser prepares the particle in the definite spin-up state along the Z-axis. When the particle is then measured along the X-axis, the wavefunction collapses into a definite X state. This destroys the original information regarding the Z-axis. When the particle enters the third analyser along the z axis, both spin-up and spin-down are equally likely. This is because the particle is now in a superposition of Z eigenstates.",
};


export const PreparedQuantumState = {
  title: "Prepared state: Prepared quantum state measured along Z",
  setup: [
    "Source fires 10,000 atoms in a prepared state (ψ) to the analyser 1",
    "The prepared state is |ψ⟩ = (1/2) |↑⟩  +  (((√(3)/2)*(e^(i*π/4)))) |↓⟩",
    "The analyser is orientated along the Z-axis with both paths open.",
    "The analyser measures each atom and calculates its probability of being spin-up or spin-down",
  ],
  observe: [
    "All 10,00 atoms makes it through",
    "Roughly 25% of the atoms are in the spin-up state",
    "Roughly 75% of the atoms are in the spin-down state",
  ],
  explanation: "Each atom is prepared in the same specific quantum state, |ψ⟩. The coefficients of the state determine the measurement probabilities through Born's rule. Since the analyser is oriented along the Z-axis the probability of measuring spin-up is |1/2|^2, and the probability of measuring spin-down is given by |(root(3)/2) * e^(iπ/4)|^2. Since the measurement is along the Z-axis, the exponential term does not effect the probability measurements."

};

export const SpinOneSystem = {
  title: "Spin One: Sequential Z into X measurement",
  setup: [
          "Source fires 10,000 atoms, all in a random state (R) to analyser 1",
          "Analyser 1 is aligned along the Z-axis with only spin-up (↑) open",
          "Anlyser 2 is aligned along the X-axis with all three paths open"

  ],
  observe: [
            "Roughly 33% of the particles make it through the first analyser",
            "After the second analysers the particles are split as 25% in +1, 50% in 0 and 25% in -1",


  ],
  explanation: "The initial random state contains equal populations of the three z-eigenstates, so only one third of the particles pass through the first analyser when the |+1⟩z channel is selected. The transmitted particles are therefore prepared in the definite state |+1⟩z. When this state enters the x-aligned analyser, it is no longer an eigenstate of the measurement axis. Instead, |+1⟩z can be written as a superposition of the x-basis eigenstates, expressed in terms of the z-basis. This change of basis leads to probabilistic outcomes. Using these x-eigenstates (relative to the z-basis) and applying Born’s rule gives probabilities of 1/4 for +1, 1/2 for 0, and 1/4 for −1, which explains the observed distribution.",

};