# FinalYearProject_SpinsLab

This project involved building a web-based Stern-Gerlach simualtor. The project allows users to run their own unique Stern-Gerlach experiments to explore the quantum world.
The simulator allows users to set up their own experiments by selcting the spin system, the amount of analysers, predefining their own prepared quantum state and more.
The repositories contain both the Python backend source code, as well as other scripts developed in the development of the project and the backend source code for the web based interface.

## Repository structure

- `Frontend/` - Four main scripts in the development of the interface. The main React script, app.tsx contains the structure of the layout of the website and the handling of measurement requests. DemoCases.ts contains the descriptions off all the designed experiements. Instructions.tsx contains the text for the instructions box and lastly, calculatorInput.tsx contains the interface and handling of interactions for the user defined state prepration calculator.

- `Backend/` - This consists of two folders, spin_half and spin_one. Both folders contain multiple scripts for various parts of the project. Different aspects of the simulator were developed independently before being integrated into the final script. Backend also contains the final version of the script that was containerised by docker before being uploaded to Fly.io
