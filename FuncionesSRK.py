# Created by: Alejandra Risco (arisco@espol.edu.ec)

def a_comp(R, Tc, Pc, omega, Tr):
    a=0.42748 * (((R ** 2) * (Tc ** 2)) / Pc) * ((1 + omega * (1 - (Tr ** (1 / 2)))) ** 2)
    return(a)

def b_comp(R,Tc,Pc):
    b=0.08664 * (R * Tc/Pc)
    return b

def a_fase(x1,x2,a1,a2,k12):
    a=(x1 ** 2) * a1 + (x2 ** 2) * a2 + 2 * x1 * x2 * (1 - k12) * ((a1 * a2) ** (1 / 2))
    return a

def b_fase(x1,x2,b1,b2):
    b=(x1 * b1) + (x2 * b2)
    return b

def A_fase(a,P,R,T):
    A=(a*P)/(((R*(T+273.15))**2))
    return A

def B_fase(b,P,R,T):
    B=(b * P) / (R * (T + 273.15))
    return B

def C_comp_fase(A,B,b_comp,b,a,x1,x2,a1,a2,k12):
    import math
    C=((A/B) * ((-b_comp/b) + (2 / a) * (x1 * a1 + x2 * (math.sqrt(a1 * a2)* (1 - k12)))))
    return C

def coef_fugacidad(b_comp,b, Z,B,C_comp):
    import numpy as np
    import math
    coef = math.exp((b_comp/b)*(Z-1) - np.log(Z - B) - C_comp*np.log((Z+B)/Z))
    return coef

def filtrarcomplejos(lista):
    import numpy as np
    vector = np.array(lista)
    filtrado = vector[vector.imag == 0]
    return filtrado.tolist()

def lcomp():
    archivo = open("Properties_Comp.csv", "r")
    archivo.readline()
    lcomp = []
    for linea in archivo:
        l= linea.split(";")
        lcomp.append(l[0])
    archivo.close()
    return lcomp

def coef_Antoine(comp):
    archivo = open("Properties_Comp.csv","r")
    archivo.readline()
    for linea in archivo:
        l= linea.split(";")
        if comp == l[0]:
            A = float(l[1].replace(",","."))
            B = float(l[2].replace(",","."))
            C = float(l[3].replace(",","."))
    archivo.close()
    return [A,B,C]

def rangoT(comp):
    archivo = open("Properties_Comp.csv", "r")
    archivo.readline()
    for linea in archivo:
        l = linea.split(";")
        if comp == l[0]:
            T_min = int(l[4].split(",")[0])
            T_max = int(l[5].split(",")[0])
    archivo.close()
    return list(range(T_min,T_max+1))

def menu(l_comp):
    print("*" * 10 + "SRK Method" + "*" * 10 + "\n")
    print("Available components:")
    rango = list(range(0, len(l_comp), 4))
    for i in rango:
        print("{:>3}. {:20} {:>3}. {:20} {:>3}. {:20} {:>3}. {:20}".format(i+1, l_comp[i].title(),i+2,l_comp[i+1].title(),i+3,l_comp[i+2].title(),i+4,l_comp[i+3].title()))
    print("\n")

def val_ncomp(ncomp,l_op):
    if not ncomp.isdigit():
        return True
    elif ncomp.isdigit():
        if int(ncomp) - 1 not in l_op:
            return True
        else:
            return False

def val_numero(x):
    while x.isalpha():
        x = input("\tEnter correctly a number:")
    if "," in x:
        x=x.replace(",",".")
    return float(x)

def w_Tc_Pc(comp):
    archivo = open("Properties_Comp.csv", "r")
    archivo.readline()
    for linea in archivo:
        l = linea.split(";")
        if comp == l[0]:
            w = float(l[6].replace(",","."))
            Tc = float(l[7].replace(",","."))
            Pc = float(l[8].replace(",","."))
    archivo.close()
    return w,Tc,Pc

def punto_SRK(punto,comp_1,Psat_comp1,comp_2,Psat_comp2,k12,T,R=8.314):
    import CubicEquationSolver
    w_1,Tc_1,Pc_1 = w_Tc_Pc(comp_1)
    Pc_1 = Pc_1*100000 #Pa
    w_2,Tc_2,Pc_2 = w_Tc_Pc(comp_2)
    Pc_2 = Pc_2*100000 #Pa
    
    #Reduced temperature
    Tr_1 =(T+273.15)/ Tc_1
    Tr_2 =(T+273.15)/ Tc_2
    
    #Omega
    omega_1 = 0.48 + (1.574*w_1) - (0.176*(w_1**2))
    omega_2 = 0.48 + (1.574*w_2) - (0.176*(w_2**2))
    
    print("\nx1 = %.2f\nInitial guess: x1=y1" % punto)
    P_inicial = ((Psat_comp1+Psat_comp2)/2) #bar
    P_final = P_inicial 
    contador = 0
    
    while P_inicial == P_final and contador < 5:
        x1 = punto
        x2 = 1 - x1
        y1_asumido = x1  #Intial guess
        error_y1 = 1
        
        # a and b parameters for each component
        a1 = a_comp(R, Tc_1, Pc_1, omega_1, Tr_1)
        a2 = a_comp(R, Tc_2, Pc_2, omega_2, Tr_2)
        b1 = b_comp(R, Tc_1, Pc_1)
        b2 = b_comp(R, Tc_2, Pc_2)
        
        while error_y1 > 0.001:  # First loop for y1
            y2 = 1 - y1_asumido
            
            #Parameters (a and b) for each phase
            a_liq = a_fase(x1, x2, a1, a2, k12)
            a_vap = a_fase(y1_asumido, y2, a1, a2, k12)
            b_liq = b_fase(x1, x2, b1, b2)
            b_vap = b_fase(y1_asumido, y2, b1, b2)
            
            #Parameters (A and B) for each phase
            A_liq = A_fase(a_liq, P_inicial, R, T)
            A_vap = A_fase(a_vap, P_inicial, R, T)
            B_liq = B_fase(b_liq, P_inicial, R, T)
            B_vap = B_fase(b_liq, P_inicial, R, T)
            
            #Parameter C for each phase and component
            C1_liq = C_comp_fase(A_liq, B_liq, b1, b_liq, a_liq, x1, x2, a1, a2, k12)
            C1_vap = C_comp_fase(A_vap, B_vap, b1, b_vap, a_vap, y1_asumido, y2, a1, a2, k12)
            C2_liq = C_comp_fase(A_liq, B_liq, b2, b_liq, a_liq, x2, x1, a2, a1, k12)
            C2_vap = C_comp_fase(A_vap, B_vap, b2, b_vap, a_vap, y2, y1_asumido, a2, a1, k12)

            #Paremeters for Z ---- Z**3 - Z**2 + (A-B-B**2) Z - A*B = 0
            c_liq = A_liq - B_liq - B_liq ** 2
            d_liq = -A_liq * B_liq
            c_vap = A_vap - B_vap - B_vap ** 2
            d_vap = -A_vap * B_vap

            Z_liq = (min(filtrarcomplejos(CubicEquationSolver.solve(1, -1, c_liq, d_liq)))).real  # min solution
            Z_vap = (max(filtrarcomplejos(CubicEquationSolver.solve(1, -1, c_vap, d_vap)))).real  # max solution

            #Fugacity coefficient
            
            ##Liquid phase
            coef1_liq = coef_fugacidad(b1, b_liq, Z_liq, B_liq, C1_liq)
            coef2_liq = coef_fugacidad(b2, b_liq, Z_liq, B_liq, C2_liq)
            
            ##Vapor phase
            coef1_vap = coef_fugacidad(b1, b_vap, Z_vap, B_vap, C1_vap)
            coef2_vap = coef_fugacidad(b2, b_vap, Z_vap, B_vap, C2_vap)
            k1 = coef1_liq / coef1_vap
            k2 = coef2_liq / coef2_vap
            k1x1 = k1 * x1
            k2x2 = k2 * x2
            sumatoria_y = k1x1 + k2x2
            y1 = k1x1 / sumatoria_y  # New y1 calculated
            error_y1 = abs(y1 - y1_asumido)
            y1_asumido = y1
        P = P_inicial
        while abs(1 - sumatoria_y) > 0.00001:  #Second loop for pressure
            if sumatoria_y > 1:
                P = P * sumatoria_y
                y2 = 1 - y1_asumido
                
            else:
                P = P / sumatoria_y
                y2 = 1 - y1_asumido
                
            #Parameters (a and b) for each phase
            a_liq = a_fase(x1, x2, a1, a2, k12)
            a_vap = a_fase(y1_asumido, y2, a1, a2, k12)
            b_liq = b_fase(x1, x2, b1, b2)
            b_vap = b_fase(y1_asumido, y2, b1, b2)
            
            #Parameters (A and B) for each phase
            A_liq = A_fase(a_liq, P, R, T)
            A_vap = A_fase(a_vap, P, R, T)
            B_liq = B_fase(b_liq, P, R, T)
            B_vap = B_fase(b_liq, P, R, T)
            
            #Parameter C for each phase and component
            C1_liq = C_comp_fase(A_liq, B_liq, b1, b_liq, a_liq, x1, x2, a1, a2, k12)
            C1_vap = C_comp_fase(A_vap, B_vap, b1, b_vap, a_vap, y1_asumido, y2, a1, a2, k12)
            C2_liq = C_comp_fase(A_liq, B_liq, b2, b_liq, a_liq, x2, x1, a2, a1, k12)
            C2_vap = C_comp_fase(A_vap, B_vap, b2, b_vap, a_vap, y2, y1_asumido, a2, a1, k12)

            #Paremeters for Z ---- Z**3 - Z**2 + (A-B-B**2) Z - A*B = 0
            c_liq = A_liq - B_liq - B_liq ** 2
            d_liq = -A_liq * B_liq
            c_vap = A_vap - B_vap - B_vap ** 2
            d_vap = -A_vap * B_vap

            Z_liq = (min(filtrarcomplejos(CubicEquationSolver.solve(1, -1, c_liq, d_liq)))).real  # min solution
            Z_vap = (max(filtrarcomplejos(CubicEquationSolver.solve(1, -1, c_vap, d_vap)))).real

            # Fugacity coefficient
            ##Liquid phase
            coef1_liq = coef_fugacidad(b1, b_liq, Z_liq, B_liq, C1_liq)
            coef2_liq = coef_fugacidad(b2, b_liq, Z_liq, B_liq, C2_liq)
            
            ##Vapor phase
            coef1_vap = coef_fugacidad(b1, b_vap, Z_vap, B_vap, C1_vap)
            coef2_vap = coef_fugacidad(b2, b_vap, Z_vap, B_vap, C2_vap)

            k1 = coef1_liq / coef1_vap
            k2 = coef2_liq / coef2_vap
            k1x1 = k1 * x1
            k2x2 = k2 * x2
            sumatoria_y = k1x1 + k2x2
            y1 = k1x1 / sumatoria_y  #New y1 calculated
            y1_asumido = y1
            
        if P != P_inicial:
            P = P / 100000
            print("\n\tResults:\n\ty1 = %.4f\t\tP (bar) = %.4f\n" % (y1, P))
            y2 = 1 - y1
            P_final = 0
        else:
            P_inicial = P_inicial / 100000
            print("\n\tWith the initial guess for P [bar] = %.2f, there is no convergence for the solution" % P_inicial)
            P_inicial = float(input("\tEnter another initial guess for P[bar]:")) * 100000
            P_final = P_inicial
            contador += 1
    if contador == 5:
        print("****5 attempts have been made and it does not converge to a solution****\n")
        return 0,0,0,0,0
    else:
        return x1,x2,y1,y2,P

def P_sat(T,comp):
  rangoT_comp = rangoT(comp)
  T1 = round(T,0)
  if T1 in rangoT_comp:
    A,B,C = coef_Antoine(comp)
    Psat_comp = 10**(A-((B)/(T+C))) #mmHg
    Psat_comp = Psat_comp*(1.01325/760) #bar
  else:
    Psat_comp = input("Antoine coefficients for %s are not valid for the T of the system\nEnter its Psat [bar] a %.2f ??C: "%(comp,T)) #bar
    Psat_comp = val_numero(Psat_comp)
  return Psat_comp