# SRK_Method
SRK Method implemented in Python to calculate fugacity coefficient, fugacity and Pxy diagram for a non-ideal binary mixture. 

This work includes:
- **Properties_Comp.csv file** containing properties for different (but limited) components. Feel free to extend the database! 
  
  *Note:* A,B,C correspond to Antoines' Equation coefficients; whereas the tMin and tMax columns represent the temperature range where those coefficients are valid.
- **CubicEquationSolver.py** created by Shril Kumar (github.com/devojoyti) &  Devojoyti Halder (github.com/devojoyti) to solve the equation for the compressibility factor Z.
- **SRK_functions.py** containg the main calculations of the SRK Method.
- **main.py** as the main program, where the components of the binary mixture are selected and all the calculations take place to obtain the Pxy diagram as the final outcome.

Here is a little tutorial (It's in Spanish tho!): 
https://www.youtube.com/watch?v=3CBiNfR1i0s&list=PLkW6J7xryaYhj10gocZeWL77ku9UBzCaF&index=15


# Copyright
Copyright (C): Ing. Alejandra Risco B, Guayaquil, Ecuador.

This work aims to be a guide for undergrad students who are learning thermodynamics. 

The book used for developing the SRK Method is: Matsoukas, T. (2012). *Fundamentals of Chemical Engineering Thermodynamics* (1st ed.). Prentice Hall.

The code was developed at the *Escuela Superior Politécnica del Litoral*, Guayaquil, Ecuador. Please give the authors the credit.

