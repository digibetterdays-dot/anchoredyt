import math
RE=6371e3; gE=9.81; H=8000.0; CD=2.0
def run(L0,rho_i,v0,theta_deg,rho_t,r_km_list,verbose=True):
    th=math.radians(theta_deg)
    # atmospheric entry (Eqs 9-20), pancake model; integrate numerically
    Yi=10**(2.107+0.0624*math.sqrt(rho_i))
    If=4.07*CD*H*Yi/(rho_i*L0*v0**2*math.sin(th))
    if If<1:
        zs=-H*(math.log(Yi/(1.0*v0**2))+1.308-0.314*If-1.303*math.sqrt(1-If))
    else: zs=0
    # velocity at surface via Eq 17
    if zs>0:
        rho_zs=math.exp(-zs/H)
        l=L0*math.sin(th)*math.sqrt(rho_i/(CD*rho_zs))
        def Lz(z): return L0*math.sqrt(1+(2*H/l)**2*(math.exp((zs-z)/(2*H))-1)**2)
        n=20000; dz=zs/n; integ=0
        for k in range(n):
            z=(k+0.5)*dz
            integ+=math.exp((zs-z)/H)*Lz(z)**2*dz
        vz=v0*math.exp(-3*CD*rho_zs/(4*rho_i*L0**3*math.sin(th))*integ)
        fp=Lz(0)/L0
    else: vz=v0; fp=1
    vi=vz
    m=rho_i*math.pi/6*L0**3
    E=0.5*m*vi**2
    Emt=E/4.184e15
    # crater
    Dtc=1.161*(rho_i/rho_t)**(1/3)*L0**0.78*vi**0.44*gE**-0.22*math.sin(th)**(1/3)
    Dc=3200
    if Dtc/1e3>2.56: Dfr=1.17*(Dtc/1e3)**1.13/(Dc/1e3)**0.13*1e3; typ='complex'
    else: Dfr=1.25*Dtc; typ='simple'
    M=0.67*math.log10(E)-5.87
    Rf=0.002*E**(1/3) if v0>15e3 else 0
    out=dict(zs=zs/1e3,fp=fp,vi=vi/1e3,E=E,Emt=Emt,Dtc=Dtc/1e3,Dfr=Dfr/1e3,typ=typ,M=M,Rf=Rf/1e3)
    Ekt=E/4.184e12
    # damage radii from Table 4 (scaled by Ekt^(1/3))
    t4=[(126,426000,'cars/trucks displaced and distorted'),(133,379000,'girder bridges collapse'),(155,273000,'steel office frames: extreme distortion'),(229,121000,'truss bridges collapse'),(389,42600,'multistory wall-bearing bldgs collapse'),(502,26800,'wood-frame bldgs almost completely collapse'),(549,22900,'wood-frame roofs severely damaged'),(1160,6900,'glass windows shatter')]
    out['dmg']=[(d1*Ekt**(1/3)/1e3,desc) for d1,p,desc in t4]
    rows=[]
    for rk in r_km_list:
        r=rk*1e3; D=r/RE
        # thermal
        if Rf>0:
            h=(1-math.cos(D))*RE; Rfm=Rf
            if h>=Rfm: f=0
            else:
                dl=math.acos(h/Rfm); f=2/math.pi*(dl-h/Rfm*math.sin(dl))
            Phi=3e-3*E/(2*math.pi*r**2)*f
            tau=3e-3*E/(2*math.pi*Rfm**2*5.67e-8*3000**4)
        else: Phi=0;tau=0
        # ignition factors (MJ/m2 at 1 Mt) scaled E_Mt^(1/6)
        ign={k:val*Emt**(1/6) for k,val in dict(clothing=1.0,plywood=0.67,grass=0.38,trees=0.25,third_deg_burns=0.42,second_deg_burns=0.25).items()}
        # overpressure (surface burst, Eq 54-57)
        r1=r/Ekt**(1/3); px=75000; rx=290
        p=px*rx/(4*r1)*(1+3*(rx/r1)**1.3)
        P0=1e5;c0=330
        u=5*p/(7*P0)*c0/math.sqrt(1+6*p/(7*P0))
        # seismic
        if rk<60: Meff=M-0.0238*rk
        elif rk<700: Meff=M-0.0048*rk-1.1644
        else: Meff=M-1.66*math.log10(D)-6.399
        # ejecta
        te=(Dtc)**4/(112*r**3) if r>Dfr/2 else float('nan')
        Tb=r/c0; Ts=rk/5
        rows.append(dict(rk=rk,Phi=Phi/1e6,tau=tau,ign=ign,p=p/1e5,u=u,Meff=Meff,te=te,Tb=Tb,Ts=Ts))
    return out,rows
if __name__=="__main__":
    print("VALIDATE vs Table 6 (1.75 km, 2700, 20 km/s, 45 deg, crystalline 2750, r=200 km)")
    o,r=run(1750,2700,20e3,45,2750,[200])
    print({k:(round(v,3) if isinstance(v,float) else v) for k,v in o.items() if k!='dmg'})
    print({k:(round(v,3) if isinstance(v,float) else v) for k,v in r[0].items() if k!='ign'})
