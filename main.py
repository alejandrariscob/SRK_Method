# Created by: Alejandra Risco (arisco@espol.edu.ec)

import FuncionesSRK
import matplotlib.pyplot as plt
import numpy as np

R = 8.314 #J/mol-K
l_comp = FuncionesSRK.lcomp() #List of components on the database
l_op = list(range(len(l_comp)))

FuncionesSRK.menu(l_comp)

#Component 1
n_comp1 = input("# of Component 1 (Most volatile):")
while FuncionesSRK.val_ncomp(n_comp1,l_op):
    n_comp1 = input("\tCorrectly enter a # for Component 1:")
comp_1 = l_comp[int(n_comp1) - 1]

#Componente 2
n_comp2 = input("# of Component 2 (Least volatile):")
while FuncionesSRK.val_ncomp(n_comp2,l_op):
    n_comp2 = input("\tCorrectly enter a # for Component 2:")
comp_2 = l_comp[int(n_comp2) - 1]

k12 = input("Interaction parameter for the mixture:")
k12 = FuncionesSRK.val_numero(k12)

T = input("Temperature (°C):")
T = FuncionesSRK.val_numero(T)

print("\n")
Psat_comp1 = FuncionesSRK.P_sat(T,comp_1)
Psat_comp2 = FuncionesSRK.P_sat(T,comp_2)

#Pxy diagram
l_x,l_y,l_P = [],[],[]
for x1 in np.linspace(0,1,5): 
    if x1 == 0:
        y1 = 0
        P = Psat_comp2
    elif x1 ==1:
        y1 = 1
        P = Psat_comp1
    else: 
        x1,x2,y1,y2,P = FuncionesSRK.punto_SRK(x1,comp_1,Psat_comp1,comp_2,Psat_comp2,k12,T)
    l_x.append(x1)
    l_y.append(y1)
    l_P.append(P)

plt.plot(l_x,l_P,color='blue', label = 'Bubble line')
plt.plot(l_y,l_P,color='red', label = 'Dew line')
plt.xlabel('Composition (x1,y1) %s'%(comp_1.title()))
plt.ylabel('P [bar]')
s = 'Pxy Diagram %s/%s' %(comp_1.title(),comp_2.title())
plt.title(s)
plt.legend()
plt.show()
