#!/usr/bin/env python
# coding: utf-8

# In[1]:


from matplotlib.figure import Figure
import math
import numpy as np
import pandas as pd
import uuid


def beamDesign(L,Deadload,Liveload,h,b,fprimec,fy):

    # L = input("Beam Length (m): ")
    # Deadload = input("Dead Load (not including self weight) (kN/m): ")
    # Liveload = input("Live Load (kN/m): ")
    # h =input("h (m): ")
    # b = input("b (m): ")
    # fprimec= input("f'c (MPa): ")
    # fy= input("fy (MPA): ")

    L = float(L)
    Deadload = float(Deadload)
    Liveload = float(Liveload)
    h = float(h)
    b = float(b)
    fprimec= float(fprimec)
    fy= float(fy)
    phi=0.9
    ß1=0.85
    if fprimec > 28:
        ß1= max(0.85-(0.05*((fprimec-28)/7)), 0.65)

    selfWeight= 24*h*b
    Wu=1.2*(selfWeight+Deadload)+1.6*(Liveload)
    Wu1 = (selfWeight + Deadload) + (Liveload)
    Mu= Wu*L**2/8
    d= h-0.04
    Rn= Mu/(1000*phi*b*d**2)
    ρ= (0.85*fprimec/fy)*(1-math.sqrt(1-(2*Rn/(0.85*fprimec))))
    Area_steel= ρ*b*d*1000000
    Asmin1= 0.25*math.sqrt(fprimec)*b*d*1000000/fy
    Asmin2= 1.4*b*d*1000000/fy
    Asmin= max(Asmin1, Asmin2)
    As= max(Area_steel, Asmin)

    R = Wu*L/2
    x= np.linspace(0,L,200)

    X =[]
    moment =[]
    shear =[]
    deflection = []
    for i in x:
        V = R - Wu*i
        M = R*i - Wu*(i**2/2)
        y = -((Wu1 * i) / (24)) * (L * L * L - 2 * L * i * i + i * i * i)
        moment.append(M)
        shear.append(V)
        X.append(i)
        deflection.append(y)

    fig1 = Figure()
    # ax.subplot(2,1,1)
    ax1 = fig1.add_subplot(2,1,1)
    ax1.plot(X,moment)
    ax1.set_xlabel('Length (m)')
    ax1.set_ylabel('Moment (kN.m)')
    ax1.fill_between(X, moment)
    fileName1 = str(uuid.uuid4())

    fig2 = Figure()
    ax2 = fig2.add_subplot(2,1,1)
    ax2.plot(X,shear)
    ax2.set_xlabel('Length (m)')
    ax2.set_ylabel('Shear (kN)')
    ax2.fill_between(X, shear)
    fileName2 = str(uuid.uuid4())

    fig3 = Figure()
    ax3 = fig3.add_subplot(2,1,1)
    ax3.plot(X, deflection)
    ax3.set_xlabel('Length (m)')
    ax3.set_ylabel('Deflection/EI (m)')
    ax3.fill_between(X, deflection)
    fileName3 =  str(uuid.uuid4())

    fig1.savefig( fileName1 + ".png")
    fig2.savefig( fileName2 + ".png")
    fig3.savefig( fileName3 + ".png")





    print(f"Wu: {Wu:.2f} kN/m\nMu: {Mu:.2f} kN.m\nρ: {ρ:.5f}\nArea steel: {Area_steel:.2f} mm²\nAsmin: {Asmin:.2f} mm² \nAs: {As:.2f} mm²")
    print("Concrete cover is assumed as 40 mm")



    bars = [12, 14, 16, 18, 20, 22]
    Abar= []
    As_list = []
    n = []
    a= []
    c=[]
    εt=[]
    Φ=[]
    ΦMn = []
    Classification=[]

    for dbar in bars:
        Abar_value = (math.pi)*(dbar**2)/4
        Abar.append(Abar_value)

        n_value = math.ceil((As/Abar_value))
        n.append(n_value)

        As_value =n_value* (dbar**2 * math.pi) / 4
        As_list.append(round(As_value, 2))

        a_value= (As_value*fy)/(0.85*fprimec*b*1000000)
        a.append(a_value)

        c_value = (a_value/ß1)
        c.append(c_value)

        εt_value =((d-c_value)/c_value)*0.003
        εt.append(εt_value)
        Φ_value = 0
        if εt_value <= 0.002:

            Φ_value = 0.65
            Classification.append('Compression controlled')
        elif εt_value > 0.002 and εt_value < 0.005:
            Φ_value = 0.65+(εt_value-0.002)*250/3
            Classification.append('Transition')

        else:
            Φ_value= 0.9
            Classification.append('Tension controlled')

        Φ.append(Φ_value)
        ΦMn_value = Φ_value * (As_value*fy*(d-a_value/2)/1000)
        ΦMn.append(round(ΦMn_value,2))

    approval = []
    for value in ΦMn:
        if value > Mu:
            approval.append("Ok")
        else:
            approval.append("Not Ok")



    dict=[bars, n, As_list, a,  εt, Classification,  ΦMn,  approval]

    df= pd.DataFrame(dict)

    print (df)

    return [fileName1,fileName2,fileName3, dict]

