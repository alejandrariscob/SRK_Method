#Programa principal Método SRK
# Created by     :   Alejandra Risco (arisco@espol.edu.ec)
import FuncionesSRK
import matplotlib.pyplot as plt
import numpy as np

#Datos iniciales
R = 8.314 #J/mol-K
l_comp = FuncionesSRK.lcomp() #Lista de todos los componentes disponibles en el database
l_op = list(range(len(l_comp)))

FuncionesSRK.menu(l_comp)

#Componente 1
n_comp1 = input("# del Componente 1 (Más volátil):")
while FuncionesSRK.val_ncomp(n_comp1,l_op):
    n_comp1 = input("\tIngrese correctamente un # para el Componente 1:")
comp_1 = l_comp[int(n_comp1) - 1]

#Componente 2
n_comp2 = input("# del Componente 2 (Menos volátil):")
while FuncionesSRK.val_ncomp(n_comp2,l_op):
    n_comp2 = input("\tIngrese correctamente un # para el Componente 2:")
comp_2 = l_comp[int(n_comp2) - 1]

k12 = input("Parámetro de interacción:")
k12 = FuncionesSRK.val_numero(k12)

T = input("Temperatura del sistema (°C):")
T = FuncionesSRK.val_numero(T)

print("\n")
Psat_comp1 = FuncionesSRK.P_sat(T,comp_1)
Psat_comp2 = FuncionesSRK.P_sat(T,comp_2)

#Puntos para el diagrama - Método SRK
#punto = 0.2
#La función solo se usa para puntos intermedios
#x1,x2,y1,y2,P1 = FuncionesSRK.punto_SRK(punto,comp_1,Psat_comp1,comp_2,Psat_comp2,k12,T)
n= 3

x = [0,0.2,0.4,0.6,0.8,1]  #Linea de burbuja
y = [] #Linea de rocio
l_P = [] #Presiones la mezcla


for xi in x: #Repetir un lazo n veces
  if xi == 0:
    y1 = 0
    P = Psat_comp2
  elif xi ==1:
    y1 = 1
    P = Psat_comp1
  else: #Puntos intermedios
    x1,x2,y1,y2,P = FuncionesSRK.punto_SRK(xi,comp_1,Psat_comp1,comp_2,Psat_comp2,k12,T)
  y.append(y1)
  l_P.append(P)


#Diagrama Pxy
plt.plot(x,l_P,color='blue', label = 'Linea de burbuja')
plt.plot(y,l_P,color='red', label = 'Linea de rocio')
plt.xlabel('Composicion (x1,y1) %s'%(comp_1.title()))
plt.ylabel('P [bar]')
s = 'Diagrama Pxy %s/%s' %(comp_1.title(),comp_2.title())
plt.title(s)
plt.legend()
plt.show()