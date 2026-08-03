import numpy as np
from scipy.special import ellipk, ellipe

mu0 = 4e-7 * np.pi
S_FW= 815   #[m^2]
Sdiv= 385.4 #[m^2]
Scp = 6*0.5*3.902 #[m^2]    contact point between VDE and limiter(s)

# Template scenario. Variables are placeholders, to be filled with specific scenario-dependant quantities.
SPR068 = {
    "name": "template",
    "R0": 1,  # [m]
    "a": 1,   # [m]    
    "Ip": 1,  # [A]
    "li3": 1, # [H]
    "kappa": 1,  
    "delta": 1,  
    "B0": 1,
    "q95": 1, 
    "Csect": 1,  # [m2]     
    "Volume": 1, # [m3]
    "Wth": 1,    # [W]      
    "ne": 1,     # [m-3]
    "P_SOL": 1,  # [W]     # P_SOL = (0.95*P_fus/5 + P_aux)
    "Psep": 1,   # [W]     # Psep = P_SOL * (1-f_rad)
    "M_ion": 1,  # [amu]     
    "lamHD": 1,  # [m]
    "p_sep": 1,  # [Pa]
    "WthCQ": 1,  # [W]  
    "longCQtime": 100.,  # [ms]     
    "Zeff": 1,
    "betap": 1,
    "Tsep": 1,   # [eV]
    "Tcore": 1,  # [eV]
    "tauW": 0.2, # [s]
    #
    # OUTPUTS
    #
    "tauPreTQ" : np.zeros(8),
    "tauTQ" : np.zeros(8),
    "tauCQ" : np.zeros(8),
    "WTQ_con1" : np.zeros(8),
    "WTQ_con2" : np.zeros(8),
    "WTQ_rad2" : np.zeros(8),
    "tvs_TQ_con1" : np.zeros(8),
    "tvs_TQ_con2" : np.zeros(8),
    "tvs_TQ_rad" : np.zeros(8),
    "WthTQ2"   : np.zeros(8),
    "WthTQrad" : np.zeros(8),
    "WCQ_con"  : np.zeros(8),
    "WCQ_rad"  : np.zeros(8),
    "tvs_CQ_con" : np.zeros(8),
    "tvs_CQ_rad" : np.zeros(8),
    "Wpol_c"   : np.zeros(8),
    "Wpol_r"   : np.zeros(8),
    # Some external sources for the data:
    # [1]   https://ukaeauk.sharepoint.com/:x:/r/sites/STEP_Plasma_B1_2/_layouts/15/Doc.aspx?sourcedoc=%7B21AB2BE7-165D-4F7F-9075-8F4793F4A7F7%7D&file=Concept_Plasma_Comparison.xlsx&action=default&mobileredirect=true&DefaultItemOpen=1
}

# Most quatities derived from the internal STEP presentation given by Francis Casson on 15/05/2025. Additional sources are indicated within.
JET96867 = {
    "name": "JET_discharge96867",
    "R0": 2.96,  # [m]
    "a": 1.25,  # [m]       # Same aspect ratio as for SPR-045
    "Ip": 3e6,  # [A]
    "li3": (23e6/1.1) * 4 / (mu0 * (2.96) * (3e6)**2), 
    "kappa": 1.6,  #5.38/(np.pi*1.25)**2,  # Csection / (pi*a^2)
    "delta": 1,  # No idea... 
    "B0": 2.7,
    "q95": 3.0, # [9, 12] # Taken from file "SPR68_DDN_4low.geqdsk" in FRIDA simulation: https://simdb.step.ukaea.uk/alias/SPR68_DDN
    "Csect": 5.38,  # [m2]      # 46.86 <--- V / (2 * pi * R0). 48.38 <---- data file from FIESTA simulation
    "Volume": 100,  # [m3]
    "Wth": 7e6,  # [W]      # Tile BD-56 (SPR-068 / post CML5 pivot) in [1]
    "ne": 1.e20,  # [m-3]
    "P_SOL": 29e6+4e6,  # [W]  # P_SOL = (0.95*P_fus/5 + P_aux),    in this case, Pfus=0
    "Psep": 1, # [W]    # serves only to compute lambda_q   # Psep = P_SOL * (1-f_rad)
    "M_ion": 2,# 2.72,  # [amu]     
    "lamHD": 1,  # [m]
    "p_sep": 3.38e3,  # [Pa]
    "WthCQ": 23e6*1.1,  # [W]  
    "longCQtime": 100.,  # [ms]      # Not relevant: this is a mitigated case
    "Zeff": 1,
    "betap": 1,
    "Tsep": 1, # [eV]     # only useful for VS
    "Tcore": 1, # [eV]    # completely useless
    "tauW": 0.005, # [s]
    #
    # OUTPUTS
    #
    "tauPreTQ" : np.zeros(8),
    "tauTQ" : np.zeros(8),
    "tauCQ" : np.zeros(8),
    "WTQ_con1" : np.zeros(8),
    "WTQ_con2" : np.zeros(8),
    "WTQ_rad2" : np.zeros(8),
    "tvs_TQ_con1" : np.zeros(8),
    "tvs_TQ_con2" : np.zeros(8),
    "tvs_TQ_rad" : np.zeros(8),
    "WthTQ2"   : np.zeros(8),
    "WthTQrad" : np.zeros(8),
    "WCQ_con"  : np.zeros(8),
    "WCQ_rad"  : np.zeros(8),
    "tvs_CQ_con" : np.zeros(8),
    "tvs_CQ_rad" : np.zeros(8),
    "Wpol_c"   : np.zeros(8),
    "Wpol_r"   : np.zeros(8),
    # Some external sources for the data:
    # [1]   https://ukaeauk.sharepoint.com/:x:/r/sites/STEP_Plasma_B1_2/_layouts/15/Doc.aspx?sourcedoc=%7B21AB2BE7-165D-4F7F-9075-8F4793F4A7F7%7D&file=Concept_Plasma_Comparison.xlsx&action=default&mobileredirect=true&DefaultItemOpen=1
}

def readFromXls(scenarioLabel,cc,filename="FrancisSpreadsheet.xlsx"):
    """
    Builds a scenario dictionary, shaped ater SPR068, automatically reading the data from the local copy of Francis's spreadsheed

        Input:
            - scenarioLabel: name of the dictionary containing the new scenario
            - cc:            corresponding column on Francis's spreadsheet, according to Excel nomenclature: 'A','B'...'Z','AA','AB'

        Output:
            - scenarioOut:   new dictionary, shaped after SPR068, containing the new data reported on Francis's sreadsheet   
    """
    # url = "https://ukaeauk.sharepoint.com/:x:/r/sites/STEP_Plasma_B1_2/_layouts/15/"
    #     +"Doc.aspx?sourcedoc=%7B21AB2BE7-165D-4F7F-9075-8F4793F4A7F7%7D&file=Concept_Plasma_Comparison.xlsx"
    #     +"&action=default&mobileredirect=true&DefaultItemOpen=1"
    path = "./"+filename
    
    import pandas as pd

    file = pd.read_excel(path)  # For some reason:  line  X(python) = X(xlsx) - 2
                                #                   col.  Y(python) = Y(xlsx) - 1
    
    def col(colName) :
        colName = colName.upper()
        appo = 0
        for char in colName :
                appo = appo*26 - ord('A') + ord(char) + 1
        return appo-1
    
    def row(rowName):
        return rowName-2
    
    scenarioOut = SPR068.copy()

    scenarioOut["name"]  = scenarioLabel
    scenarioOut["R0"]    = file.iloc[row(10),col(cc)]
    scenarioOut["a"]     = file.iloc[row(11),col(cc)]
    scenarioOut["B0"]    = file.iloc[row(12),col(cc)]
    scenarioOut["Ip"]    = file.iloc[row(13),col(cc)]*1e6
    scenarioOut["betap"] = file.iloc[row(19),col(cc)]
    scenarioOut["kappa"] = file.iloc[row(23),col(cc)]
    scenarioOut["delta"] = file.iloc[row(24),col(cc)]
    scenarioOut["q95"]   = file.iloc[row(25),col(cc)]
    scenarioOut["li3"]   = file.iloc[row(27),col(cc)]
    scenarioOut["Volume"]= file.iloc[row(28),col(cc)]
    scenarioOut["Csect"] = scenarioOut["Volume"]/(2.*np.pi*scenarioOut["R0"])
    scenarioOut["Zeff"]  = file.iloc[row(33),col(cc)]
    scenarioOut["Tcore"] = file.iloc[row(38),col(cc)]*1e3
    scenarioOut["ne"]    = file.iloc[row(40),col(cc)]*1e20

    if (filename=="FrancisSpreadsheet.xlsx"):
        scenarioOut["Wth"]   = file.iloc[row(56),col(cc)]*1e6
        scenarioOut["P_SOL"] = file.iloc[row(63),col(cc)]*1e6
        scenarioOut["Psep"]  = file.iloc[row(64),col(cc)]*1e6
        #scenarioOut["M_ion"]    = file.iloc[row(10),col(cc)]
        scenarioOut["Tsep"]  = file.iloc[row(171),col(cc)]*1e3
        scenarioOut["p_sep"] = file.iloc[row(172),col(cc)]*1e3

    if (filename=="FrancisSpreadsheet_new1.xlsx"):
        # For Wth I also consider the energy stored in the alphas
        scenarioOut["Wth"]   = (file.iloc[row(176),col(cc)])*1e6
        scenarioOut["P_SOL"] = file.iloc[row(65),col(cc)]*1e6
        scenarioOut["Psep"]  = file.iloc[row(66),col(cc)]*1e6
        #scenarioOut["M_ion"]    = file.iloc[row(10),col(cc)]
        scenarioOut["Tsep"]  = file.iloc[row(169),col(cc)]*1e3
        scenarioOut["p_sep"] = file.iloc[row(171),col(cc)]*1e3
    
    if (filename=="FrancisSpreadsheet_SPP3.xlsx"):
        # For Wth I also consider the energy stored in the alphas
        scenarioOut["Wth"]   = (file.iloc[row(179),col(cc)])*1e6
        scenarioOut["P_SOL"] = file.iloc[row(66),col(cc)]*1e6
        scenarioOut["Psep"]  = file.iloc[row(67),col(cc)]*1e6
        #scenarioOut["M_ion"]    = file.iloc[row(10),col(cc)]
        scenarioOut["Tsep"]  = file.iloc[row(172),col(cc)]*1e3
        scenarioOut["p_sep"] = file.iloc[row(174),col(cc)]*1e3

    if (filename=="FrancisSpreadsheet_SPP1.xlsx"):
        scenarioOut["Wth"]   = file.iloc[row(58),col(cc)]*1e6
        scenarioOut["P_SOL"] = file.iloc[row(65),col(cc)]*1e6
        scenarioOut["Psep"]  = file.iloc[row(66),col(cc)]*1e6
        #scenarioOut["M_ion"]    = file.iloc[row(10),col(cc)]
        scenarioOut["Tsep"]  = file.iloc[row(168),col(cc)]*1e3
        scenarioOut["p_sep"] = file.iloc[row(170),col(cc)]*1e3

    return scenarioOut

def writeToXls(scenario):
    import pandas as pd

    df = pd.DataFrame(scenario)
    df.to_excel(scenario["name"]+".xlsx",index=False)
    return scenario["name"]+".xlsx"

def err(a,b): return abs(a-b)*2/(a+b)

def tauE(scenarioName, mode='L'):
    """
    tauE implements the models in https://iopscience.iop.org/article/10.1088/0029-5515/39/12/302 for the computation 
    of the energy confinement time.

        Inputs:
          - scenarioName:   python dictionary-type variable containing an SPP-2 scenario
          - mode:           'H'            -->  implements model IPB98(y,2) (see Tab. 5 + Eq. 22 in the reference)
                            'L' (default)  -->  implements model ITERL 96   (see Eq. 24 in the reference)

        Output:
          - tauE:           Energy confinement time, adopted as pre-TQ duration

    For the H-mode, a more precise pre-factor obtained from Ciemat Wiki: https://wiki.fusion.ciemat.es/wiki/H98
    """
    R0 = scenarioName["R0"]
    a = scenarioName["a"]
    Ip = scenarioName["Ip"]
    B0 = scenarioName["B0"]
    Csect = scenarioName["Csect"]
    ne = scenarioName["ne"]
    Psol = scenarioName["P_SOL"]
    M = scenarioName["M_ion"]
    AA = R0 / a

    kappa1 = Csect / (np.pi * a ** 2)

    if (mode=='H'): 
        tauE = 0.0562 * ( (Ip / 1e6) ** 0.93 * B0 ** 0.15 * (ne / 1e19) ** 0.41
                          * (Psol / 1e6) ** (-0.69) * R0 ** 1.97 * kappa1 ** 0.78 
                          * AA ** (-0.58) * M ** 0.19 )
    if (mode=='L'):
        tauE = 0.023 *  ( (Ip / 1e6) ** 0.96 * B0 ** 0.03 * (ne / 1e19) ** 0.40
                          * (Psol / 1e6) ** (-0.73) * R0 ** 1.83 * kappa1 ** 0.64 
                          * AA ** (-0.06) * M ** 0.20 )
    
    return tauE

def DTcool(scenarioName):
    """
    Characteristic time of the pre-TQ phase

        input:   name of a python dictionary relative to a scenario
        output:  time of cooling
    """
    return 0.6 * scenarioName["a"] * scenarioName["q95"]

# The Power load on the divertor has a ramp-up timescale of 1 tauTQ and a decay timescale of 3 tauTQ
def tauTQ(scenarioName):
    """
    Characteristic time of the heat load waveform on the divertor:

        input:   name of a python dictionary relative to a scenario
        output:  tau_TQ
    """
    return 0.33 * scenarioName["a"]

def tauCQlinmin(scenarioName, linexp="lin", mitigatedVDE=0, MDlikely=0, longCQ=0):
    """
    Characteristic time of the CQ:

        input:   - name of a python dictionary relative to a scenario
                 - linexp = "lin" --> time constant for a linear decay of Ip
                            "exp" --> time constant for an exponential decay
        flags (default value is "False"): 
                 - mitigatedVDE = 1 --> if the disruption is mitigated
                 - MDlikely =1      --> if this is an average major disruption (not a large one)
                 - longCQ = 1       --> if we assume that the CQ is very long (~100 s)
        output:  tau_TQ
    """
    SLstar = scenarioName["Csect"] * (
#                np.log(scenarioName["B0"] * scenarioName["R0"] / scenarioName["a"]) + scenarioName["li3"] / 2 - 2)
                np.log(8 * scenarioName["R0"] / scenarioName["a"]) + 0.5 / 2 - 2)
    tauCQ = 0.7*SLstar
    if (mitigatedVDE): tauCQ = SLstar/2
    if (MDlikely): tauCQ = SLstar*1.4
    if (longCQ): tauCQ = 3*SLstar#scenarioName["longCQtime"]#*scenarioName["a"]/SPR045["a"]
    if (linexp == "exp"): tauCQ *= 0.6 / np.log(4)
    return tauCQ

def qCyl(scenarioName):
    """
        Cylindrical safety factor, used for the MHD estimate of the minimal detachment length lambda_{q,MHD}
        Unlike on TD-0013190-B (where the numeric result is wrong), this value suffices to provide a reasonable estimate 
        of the corresponding physical quantity (~2 mm for SPR-045).

        input:  name of a python dictionary relative to a scenario
        output: qCyl
    """
    Ip = scenarioName["Ip"]
    a = scenarioName["a"]
    kappa = scenarioName["kappa"]
    B0 = scenarioName["B0"]
    R0 = scenarioName["R0"]
    #
    #    return a**2 * B0 * (1+kappa**2) / ( R0 * Ip * 4e-7 )
    Bpol = mu0 * Ip / (2 * np.pi * a * np.sqrt((1 + kappa ** 2) / 2))
    return a * B0 * np.sqrt((1 + kappa ** 2) / 2) / (R0 * Bpol)

def lambdaEich(scenarioName):
    Ip = scenarioName["Ip"]
    a = scenarioName["a"]
    kappa = scenarioName["kappa"]
    B0 = scenarioName["B0"]
    R0 = scenarioName["R0"]
    #
    #    return a**2 * B0 * (1+kappa**2) / ( R0 * Ip * 4e-7 )
    Bpol = mu0 * Ip / (2 * np.pi * a * np.sqrt((1 + kappa ** 2) / 2))

    return 0.63e-3 * Bpol**(-1.19)

def lambdaMHD(scenarioName,model='HD'):
    """
    Attempt to compute the power fall-off length using the formula provided by York University (Annex 1 in TD-0013190-B). 
    Incomplete owing to lack of physical parameters.

    Still incomplete  ---> DO NOT USE!
    """
    if (model == 'HD'):
        Z_average = 1  # charge imparity overall in the plasma: ne / Σ_s{ n_s }

        def kz(Zeff) : 
            return 0.672 + 0.076 * Zeff**0.5 + 0.252 * Zeff

        # result given in meters
        lamHD = 5671 * ( ( scenarioName["Psep"] * 1.5 )**(1./8) * 1.5 * ( 2. / ( 1. + Z_average ) )**(7./16) 
                         * ( 1 + scenarioName["kappa"]**2 )**(5./8) * scenarioName["a"]**(17/8) * scenarioName["B0"]**0.25 
                         / ( scenarioName["Ip"]**(9./8) * scenarioName["R0"] ) ) * kz(scenarioName["Zeff"])**(1./8)

        λ = lamHD
    else:
        λ = lambdaEich(scenarioName)*1e-3

    alphaCrit = scenarioName["kappa"] ** 1.2 * ( 1 + 1.5 * scenarioName["delta"] )

    alphaMHD = (qCyl(scenarioName)) ** 2 * scenarioName["R0"] * mu0 * scenarioName["p_sep"] / (
                scenarioName["B0"] ** 2 * λ )

    lamMHD = λ 
    print('lambdaHD[{lamhd}],   alphaMHD[{amhd}]  >?  alphaCrit[{acrit}]'.format(lamhd=lamMHD,amhd=alphaMHD,acrit=alphaCrit))
    if (alphaMHD > alphaCrit) :
        lamMHD *= ( alphaMHD / alphaCrit )**(7./9)
    return lamMHD #[m]

def lambdaMHD_rough(scenarioName):
    """
        Computation of the power fall-off length estimate from MHD using the rough scaling in the final equation of Annex 1 in TD-0013190-B.
        This is a rescaling of an empirical value obtained for a previous device configuration (STEP500)

            input:  name of a python dictionary relative to a scenario
            output: lambda_{q,MHD}
    """
    #    return 1.18e-3 * (scenarioName["R0"]/1.8)**(7/9) * (2.15/2.76)**(14/9) * (scenarioName["B0"]/2.43)**(-14/9)
    return 1.18e-3 * (scenarioName["R0"] / 1.8) ** (7 / 9) * (qCyl(scenarioName) / 2.76) ** (14 / 9) * (
                scenarioName["B0"] / 2.43) ** (-14 / 9) * (scenarioName["p_sep"] / 2.13e3) ** (7./9)

def Emax1(scenarioName,time,Wplasma,Swetted=1):
    """
        Computes time threshold and maximum energy absorbed by target per unitary surface, according
        to vapour shielding 'model 1' in https://doi.org/10.1063/1.4939537

            Input:
                - scenarioName  name of the STEP scenario
                - time          time duration of the disruption phase considered
                - Wplasma       energy lost by the plasma in the phase considered
                - Swetted       wetted area
            Output:
                - tau1          threshold time after which enough vapour has built up to see the shielding effect
                - Emax          maximum energy absorbed by the target material
    """
    #Swetted = 1 #[ m^2 ]
    X  = 0.13 # fraction of impinging power that gets to wall unshielded 
    q0 = (1-X) * Wplasma / ( Swetted * time )
    k  = 100  #[ W / m K ]   (heat conduction coefficient)
    Cp = 250  #[ J / kg K ]  (heat capacity)
    rho= 18e3 #[ kg / m^3 ]  (density)
    j0 = 1e33 #[ 1 / m^2 s ] (dN/dt = j0 * exp(-Eev / T))
#    j0 = 8.167e34/np.sqrt(94670)
    Eev= 94670#[ K ]         (melting point of Tungsten)
    
    def sigma(Te) :
        if (Te > 100):
            return 8.8e-13 / Te**1.71 - 1.62e-12 / Te**1.932
        else:
            return 1.1e-14 / Te
        
    Rprompt = 0.#99 # prompt redeposition of VS cloud on target
    Rdiffusion = 0.5#.99 # diffusion of VS away from target

    sig = sigma(scenarioName["Tsep"])*(1-Rprompt)*(1-Rdiffusion)
            
    G1   = np.sqrt( np.pi * Cp * k * rho ) * Eev / q0
    tau1 = G1**2 / ( 4*np.log( G1 * np.sqrt(j0 * sig)) )**2
    Emax = np.sqrt(4*Cp*rho*k/np.pi) * Eev * np.sqrt(time) / (np.log(time * j0 * sig * 2) )
    Emax += X * Wplasma / Swetted

    # If the impinging energy does not exceed Emax*Swetted, no VS must be considered
    # The time threshold computed on the report is not 100% accurate (to say the least) so that marginally active VS may be predicted
    # wrongly, bringing to uncceptable physical conclusions, such that Emax*Swetted > q0, and that reflected radiation is a negative number
    if ((time <= tau1) or (Emax*Swetted >= Wplasma)):
        Emax = q0 * time / (1-X)

    return (tau1,Emax) 

def Emax2(scenarioName,time,Swetted=1,material='Tungsten'):
    wettedArea = Swetted #[ m^2 ]
    q0 = scenarioName["Wth"] / (wettedArea * time)
    k  = 100  #[ W / m K ]   (heat conduction coefficient)
    Cp = 250  #[ J / kg K ]  (heat capacity)
    rho= 18e3 #[ kg / m^3 ]  (density)
    j0 = 1e33 #[ 1 / m^2 s ] (dN/dt = j0 * exp(-Eev / K T))
    Eev= 94670#[ K ]         (melting point of Tungsten)
    Edot=1e-9 #[ W ]         (radiated power per evaporated particle)

    if (material == 'Tungsten'):
        k  = 100  #[ W / m K ]   (heat conduction coefficient)
        Cp = 250  #[ J / kg K ]  (heat capacity)
        rho= 18e3 #[ kg / m^3 ]  (density)
        j0 = 1e33 #[ 1 / m^2 s ] (dN/dt = j0 * exp(-Eev / K T))
        Eev= 94670#[ K ]         (melting point of Tungsten)
        Edot=1e-9 #[ W ]         (radiated power per evaporated particle)
    
    t2   = q0 / (Edot*j0)
    G2   = np.sqrt(np.pi*Cp*rho*k/t2) * Eev / q0
    tau2 = G2**2/(np.log(G2)*4)**2
    Emax = np.sqrt(4*Cp*rho*k/np.pi) * Eev * np.sqrt(time) / (1.5*np.log(time/t2))

    return tau2*t2 , Emax 

def tvs1_Swet(Swet):
    return Swet**2 / (1. + 0.05*np.log(Swet))**2 

def qmelt(time, material="W"):
    """
    Computes the critical heat flux for wall melting.
    General assumptions are:
      - wall treated as an infinite slab
      - no coolant action
      - starting temperature is 550 Celsius
      - material properties are independent of time / temperature

        Inputs: 
          - time:       time duration of the transient
          - material:   "W" (default) --> if the wall is tungsten;   "Be" --> if the wall is Berillium

        Outputs:
          - qmelt:      if q_impinging > qmelt  -->  the wall will melt
    """
    Cp    = 130    # [J / kg K]
    k     = 170    # [W / m K]
    rho   = 19250  # [kg / m3]
    Tmelt = 3695   # [K]
    T0    = 550 + 273.15
    
    if (material=="Be"):
        Cp    = 1825   # [J / kg K]
        k     = 200    # [W / m K]
        rho   = 1845   # [kg / m3]
        Tmelt = 1560   # [K]

    return (Tmelt-T0)*np.sqrt(np.pi*Cp*rho*k/time)/2  #[W / m2]

def Wpol(scenarioName,li3_betap="li3",HCF=0.):
    """
        Predicts the poloidal magnetic energy using the tabulated value for either li(3) or beta poloidal.

        If switch parameter is 
                    li3_betap = "li3"

                        /'    Bp**2
        0.5 L Ip**2 =  /   { _______ dV } = poloidal magnetic energy
                     ,/ Vp    2 mu0
        
        li(3) = 2 L / (mu0 Rgeo) 

        If switch parameter is 
            li3_betap = "betap"

        beta_p = (2/3)*Wth / Wpol

    """
    if (li3_betap == "li3"):
        # return 1.1 * mu0 * (scenarioName["Ip"]*(1-HCF))**2 * scenarioName["R0"] * scenarioName["li3"] / 4. 
        return 1.1 * mu0 * (scenarioName["Ip"])**2 * scenarioName["R0"] * scenarioName["li3"] / 4. 
    if (li3_betap == "betap"):
        return 2 * scenarioName["Wth"] / (3 * scenarioName["betap"]) * 1.1

def Wcoupled(scenarioName,lin_exp=0):
    """
    Computes the coupled magnetic energy. Only induced currents by Ip drop are considered. 
    Induced currents coming from plasma motion are more scenario dependent and not considered to this point.

        Inputs:
          - scenarioName:      name of the scenario you want the calculation to be made for
          - lin_exp:           0 --> (default) assume a linear interpolant for the CQ current drop
                               1 --> assume an exponential interpolant for the CQ current drop
        Outputs:
          - Wcoupled:          coupled magnetic energy during CQ
    """
    a_wall = scenarioName["a"] * scenarioName["kappa"]
    R_wall = scenarioName["R0"]
    k0= (4*a_wall*R_wall)**0.5 / (a_wall + R_wall)
    L = mu0 * R_wall * ( np.log(8*R_wall/a_wall) - 2 )
    M = mu0/(2*np.pi) * (a_wall + R_wall) * ((1-k0**2/2)*ellipk(k0)-ellipe(k0))

    Wcoupled = (scenarioName["Ip"] * M * scenarioName["tauW"] / scenarioName["tauCQ"]  * ( 1 - np.exp(-scenarioName["tauCQ"]/scenarioName["tauW"]) ) )**2 / (2 * L)
    if lin_exp == 1:
        tauCQ = scenarioName["tauCQ"] * 0.6 / np.log(4) 
        Wcoupled = (scenarioName["Ip"] * M * scenarioName["tauW"] / (scenarioName["tauCQ"]-scenarioName["tauW"]) * ( np.exp(-1) - np.exp(-scenarioName["tauCQ"]/scenarioName["tauW"]) ) )**2 / (2 * L)

    return Wcoupled

def W_PFC(scenarioName,phase,peakingFactors=0):
    """
    Computes the heat loads on PFC, including Vapour Shielding action and Peaking Factors.
    
        Inputs:
            -  scenarioName:    name of the scenario you want the calculation to be made for
            -  phase:           can be either 'TQ' or 'CQ'
            -  peakingFactors:  0 --> do not consider peaking factors    (effectively considers pow(peaking_factors,0))
                                1 --> considers the peaking factors listed on my report
                                (do not set values different from 0 and 1!!!)
        Outputs:
            There is no real output, but the function overwrites in the scenario the fields reported below.
            IF (phase == 'TQ'):
            -  scenarioName["tauTQ"]:           array of durations for tau1 (tau_{ramp-up}=tau1, tau_{ramp-down}=3*tau1)
            -  scenarioName["tvs_TQ_con1"]:     array of vapour shielding threshold times for TQ ramp-up
            -  scenarioName["tvs_TQ_con2"]:     array of vapour shielding threshold times for TQ ramp-down
            -  scenarioName["WTQ_con1"]:        array of conducted loads on PFC for TQ ramp-up
            -  scenarioName["WTQ_con2"]:        array of conducted loads on PFC for TQ ramp-down
            -  scenarioName["WTQ_rad2"]:        array of radiated loads on PFC for TQ ramp-up + ramp-down

            IF (phase == 'CQ'):
            -  scenarioName["tauCQ"]:           array of durations of CQ for various disruption types, within the scenario indicated
            -  scenarioName["tvs_CQ_con"]:      array of vapour shielding threshold times for CQ
            -  scenarioName["WCQ_con"]:         array of conducted loads on PFC for CQ
            -  scenarioName["WTQ_rad"]:         array of radiated loads on PFC for CQ

    """
    Swet_cond   = [ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    #Swet_rad    = [ Sdiv, Sdiv, S_FW, S_FW, S_FW, S_FW, Sdiv, S_FW ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]
    disruptions = ["MD\nlikely","MD\nstrong","cold VDE\nfast CQ","cold VDE\nslow CQ","hot VDE\nfast CQ","hot VDE\nslow CQ","MD\nmitig.","VDE\nmitig."]

    def Wrad(time,t1,W_cond,EmaxSwet):
    # If time = tau1, still the VS effect must be neglected...
        if (time > t1*1.05):
            W_rad = (W_cond-EmaxSwet) / 2
        else:
            W_rad = 1e-20
        return W_rad

    if (phase=="TQ"): 
        C_cond  = [ 0.5 , 1.0 , 0.5 , 0.5 , 1.0 , 1.0 , 0.16, 0.16 ]
        C_rad   = [ 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.64, 0.64 ]
        Wth     = scenarioName["Wth"]
        RPF     = np.pow(4,peakingFactors) * np.ones(8)     # Radiation peaking factor (TPF x PPF)
        TPF     = np.ones(8)                                # Conduction toroidal peaking factor 
        tau     = tauTQ(scenarioName) * 1e-3
        scenarioName["tauTQ"] = np.ones(8) * tau
        
        for i in range(8):
            # I compute radiation from VS without considering peaking factors: 
            # this way I should have a better approximation, since peaks should average out with troughs
            # --> Final radiation load is the sum of {VS radiation (ramp-up + ramp down)} & {plasma emitted * RPF}
            (tvs_con1,Emax_con1) = Emax1(scenarioName, time=tau*1, Wplasma=0.3*C_cond[i]*Wth, Swetted=Swet_cond[i])
            (tvs_con2,Emax_con2) = Emax1(scenarioName, time=tau*3, Wplasma=0.7*C_cond[i]*Wth, Swetted=Swet_cond[i])
            scenarioName["tvs_TQ_con1"][i] = tvs_con1
            scenarioName["tvs_TQ_con2"][i] = tvs_con2
            scenarioName["WTQ_rad2"][i] = ( Wrad(time=tau*1, t1=tvs_con1, W_cond=0.3*C_cond[i]*Wth, EmaxSwet=Emax_con1*Swet_cond[i]) +
                                            Wrad(time=tau*3, t1=tvs_con2, W_cond=0.7*C_cond[i]*Wth, EmaxSwet=Emax_con2*Swet_cond[i]) +
                                            C_rad[i]*Wth*RPF[i])
            # After computing radiation I now compute conducted loads with VS, now considering peaking factors: 
            # asymmetries in the plasma column (e.g. nonaxisymmetric VDE) may cause nonaxisymmetric loads
            (tvs_con1,Emax_con1) = Emax1(scenarioName, time=tau*1, Wplasma=0.3*C_cond[i]*Wth*TPF[i], Swetted=Swet_cond[i])
            (tvs_con2,Emax_con2) = Emax1(scenarioName, time=tau*3, Wplasma=0.7*C_cond[i]*Wth*TPF[i], Swetted=Swet_cond[i])
            scenarioName["WTQ_con1"][i]  = Emax_con1 * Swet_cond[i]
            scenarioName["WTQ_con2"][i]  = Emax_con2 * Swet_cond[i]

    if (phase=="CQ"): 
        C_cond  = [ 1.0 , 1.0 , 1.0 , 0.7 , 1.0 , 0.7 , 0.2 , 0.2  ]
        C_rad   = [ 0.0 , 0.0 , 0.0 , 0.3 , 0.0 , 0.3 , 0.8 , 0.8  ]
        HCF     = [0.075, 0.075, 0.12, 0.2, 0.12, 0.2 , 0.05, 0.1  ]              # halo current fractions
        RPF     = np.pow(1.5**2,peakingFactors) * np.ones(8)                                   # Radiation peaking factor (TPF x PPF)
        TPF     = np.pow([ 2.0 , 2.0 , 2.0 , 2.0 , 2.0 , 2.0 , 1.0 , 1.0 ],peakingFactors)     # Conduction toroidal peaking factor 
        tau     = np.array([ tauCQlinmin(scenarioName,MDlikely=1)     , tauCQlinmin(scenarioName)                , 
                             tauCQlinmin(scenarioName)                , tauCQlinmin(scenarioName,longCQ=1)       ,
                             tauCQlinmin(scenarioName)                , tauCQlinmin(scenarioName,longCQ=1)       ,
                             tauCQlinmin(scenarioName,mitigatedVDE=1) , tauCQlinmin(scenarioName,mitigatedVDE=1)   ]) * 1e-3
        scenarioName["tauCQ"] = tau

        for i in range(8):
            # I compute radiation from VS without considering peaking factors: 
            # this way I should have a better approximation, since peaks should average out with troughs
            # --> Final radiation load is the sum of {VS radiation} & {plasma emitted * RPF}
            Wth                  = Wpol(scenarioName,HCF=HCF[i]) - Wcoupled(scenarioName,lin_exp=1)
            (tvs_con1,Emax_con1) = Emax1(scenarioName, time=tau[i], Wplasma=C_cond[i]*Wth[i], Swetted=Swet_cond[i])
            scenarioName["tvs_CQ_con"][i] = tvs_con1
            scenarioName["WCQ_rad"][i]  = ( Wrad(time=tau[i], t1=tvs_con1, W_cond=C_cond[i]*Wth[i], EmaxSwet=Emax_con1*Swet_cond[i]) +
                                            C_rad[i]*Wth[i]*RPF[i])
            # After computing radiation I now compute conducted loads with VS, now considering peaking factors: 
            # asymmetries in the plasma column (e.g. nonaxisymmetric VDE) may cause nonaxisymmetric loads
            (tvs_con1,Emax_con1) = Emax1(scenarioName, time=tau[i], Wplasma=C_cond[i]*Wth[i]*TPF[i], Swetted=Swet_cond[i])
            scenarioName["WCQ_con"][i] = Emax_con1 * Swet_cond[i]

def Predictions(scenarioName):
    """
        Predictions of the model are printed in the output file: 
        
                <scenarioName>_DisruptionScenarios.txt
        
            input:  name of a python dictionary relative to a scenario
            output: file output
    
    """
    tE = tauE(scenarioName=scenarioName,mode='L')
    t_preTQ = DTcool(scenarioName)
    lam_q = lambdaMHD(scenarioName)
    lamEich = lambdaEich(scenarioName)

    def tvs(scenarioName,Wplasma,Swetted) :
        (t,E) = Emax1(scenarioName,1,Wplasma,Swetted=Swetted)
        return t

    def Evs(scenarioName,Wplasma,Swetted) :
        (t,E) = Emax1(scenarioName,1,Wplasma,Swetted=Swetted)
        return E
    
    scenarioName["tauPreTQ"] = [ tE , 0 , 0 , 0 , 0 , 0 , t_preTQ , t_preTQ ]
    with open(f"{scenarioName['name']}_DisruptionsPredictions.txt", 'w', encoding='utf-8') as f:
        f.write("_______\nPre-TQ:\n")
        f.write("\t                 \t\tDuration:\t\tConduct. W_th,loss:\t\tRadiated W_th,loss:\t\tSOL broadening:\n")
        f.write("\t1) Major Disruption:\t{:.3} s\t\t\t\t{:.3} MJ\t\t\t\t0.000 MJ\t\t\t\t{:.3}/{:.3} mm\n".format(
            tE,
            scenarioName["Wth"] / 2e6,
            lamEich*1e3, lam_q * 1e3  ))
        f.write("\t3) Cold VDE, fast CQ:\tsee MHD modelling\t{:.3} MJ\t\t\t\t0.000 MJ\t\t\t\t{:.3}/{:.3} mm\n".format(
            scenarioName["Wth"] / 2e6, 
            lamEich*1e3, lam_q * 1e3  ))
        f.write("\t4) Cold VDE, fast CQ:\tsee MHD modelling\t{:.3} MJ\t\t\t\t0.000 MJ\t\t\t\t{:.3}/{:.3} mm\n".format(
            scenarioName["Wth"] / 2e6, 
            lamEich*1e3, lam_q * 1e3  ))
        f.write("\t7) Mitigated MDs:    \t{:.3} ms\t\t\t\t0.000 MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3}/{:.3} mm\n".format(
            t_preTQ,
            scenarioName["Wth"] * .2e-6,
            lamEich*1e3, lam_q * 1e3  ))
        f.write("\t8) Mitigated VDE:    \t{:.3} ms\t\t\t\t0.000 MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3}/{:.3} mm\n".format(
            t_preTQ,
            scenarioName["Wth"] * .2e-6,
            lamEich*1e3, lam_q * 1e3  ))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        W_PFC(scenarioName=scenarioName,phase='TQ',peakingFactors=0)

        f.write("\n___\nTQ:\n")
        f.write(
            "\t                 \t\t"
            +"Ramp up time for\t\tDecay time for \t\t\tW_th losses \t\tW_th losses:\t\tSOL broadening:\t\t\t\t"
            +"Ramp up t_vs\t\t\tRamp down t_vs\t\t\t\tEmax cond\t\t\tEmax rad\n")
        f.write(
            "\t                 \t\t"
            +"divertor heat load\t\tdivertor heat load\t\t(conducted):\t\t(radiated):\t\t\t (lam_q x 1)\t\t"
            +" ms\t\t\t\t ms\t\t\t\tMJ\t\t\t\tMJ\n")
        f.write(
            "\t1) Major Disruption:\t{:.3} ms (30% loss)\t\t{:.3} ms (70% loss)\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} mm\t\t\t\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
                scenarioName["tauTQ"][0]*1e3, 
                scenarioName["tauTQ"][0]*3e3, 
                scenarioName["Wth"] / 2e6, 
                0.0, 
                lam_q * 1e3,
                scenarioName["tvs_TQ_con1"][0]*1e3,
                scenarioName["tvs_TQ_con2"][0]*1e3,
                (scenarioName["WTQ_con1"][0]+scenarioName["WTQ_con2"][0])/1e6,
                scenarioName["WTQ_rad2"][0]/1e6 ))
        
        f.write(
            "\t2) Major D. strong: \t{:.3} ms (30% loss)\t\t{:.3} ms (70% loss)\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} mm\t\t\t\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
                scenarioName["tauTQ"][1]*1e3, 
                scenarioName["tauTQ"][1]*3e3, 
                scenarioName["Wth"] / 1e6, 
                0.0, 
                lam_q * 1e3,
                scenarioName["tvs_TQ_con1"][1]*1e3,
                scenarioName["tvs_TQ_con2"][1]*1e3,
                (scenarioName["WTQ_con1"][1]+scenarioName["WTQ_con2"][1])/1e6,
                scenarioName["WTQ_rad2"][1]/1e6 ))
        
        f.write(
            "\t3) Cold VDE, fast CQ:\t{:.3} ms (30% loss)\t\t{:.3} ms (70% loss)\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} mm\t\t\t\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
                scenarioName["tauTQ"][2]*1e3, 
                scenarioName["tauTQ"][2]*3e3, 
                scenarioName["Wth"] / 2e6, 
                0.0, 
                lam_q * 1e3,
                scenarioName["tvs_TQ_con1"][2]*1e3,
                scenarioName["tvs_TQ_con2"][2]*1e3,
                (scenarioName["WTQ_con1"][2]+scenarioName["WTQ_con2"][2])/1e6,
                scenarioName["WTQ_rad2"][2]/1e6 ))

        f.write(
            "\t4) Cold VDE, slow CQ:\t{:.3} ms (30% loss)\t\t{:.3} ms (70% loss)\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} mm\t\t\t\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
                scenarioName["tauTQ"][3]*1e3, 
                scenarioName["tauTQ"][3]*3e3, 
                scenarioName["Wth"] / 2e6, 
                0.0, 
                lam_q * 1e3,
                scenarioName["tvs_TQ_con1"][3]*1e3,
                scenarioName["tvs_TQ_con2"][3]*1e3,
                (scenarioName["WTQ_con1"][3]+scenarioName["WTQ_con2"][3])/1e6,
                scenarioName["WTQ_rad2"][3]/1e6 ))

        f.write(
            "\t5) Hot VDE, slow CQ:\t{:.3} ms (30% loss)\t\t{:.3} ms (70% loss)\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} mm\t\t\t\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
                scenarioName["tauTQ"][4]*1e3, 
                scenarioName["tauTQ"][4]*3e3, 
                scenarioName["Wth"] / 1e6, 
                0.0, 
                lam_q * 1e3,
                scenarioName["tvs_TQ_con1"][4]*1e3,
                scenarioName["tvs_TQ_con2"][4]*1e3,
                (scenarioName["WTQ_con1"][4]+scenarioName["WTQ_con2"][4])/1e6,
                scenarioName["WTQ_rad2"][4]/1e6 ))
        
        f.write(
            "\t6) Hot VDE, slow CQ:\t{:.3} ms (30% loss)\t\t{:.3} ms (70% loss)\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} mm\t\t\t\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
                scenarioName["tauTQ"][5]*1e3, 
                scenarioName["tauTQ"][5]*3e3, 
                scenarioName["Wth"] / 1e6, 
                0.0, 
                lam_q * 1e3,
                scenarioName["tvs_TQ_con1"][5]*1e3,
                scenarioName["tvs_TQ_con2"][5]*1e3,
                (scenarioName["WTQ_con1"][5]+scenarioName["WTQ_con2"][5])/1e6,
                scenarioName["WTQ_rad2"][5]/1e6 ))

        f.write(
            "\t7) Mitigated MDs:   \t{:.3} ms (30% loss)\t\t{:.3} ms (70% loss)\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t{:.3} mm\t\t\t\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
                scenarioName["tauTQ"][6]*1e3, 
                scenarioName["tauTQ"][6]*3e3, 
                scenarioName["Wth"] / 1e6 * 0.8 * 0.2, 
                scenarioName["Wth"] / 1e6 * 0.8 ** 2, 
                lam_q * 1e3,
                scenarioName["tvs_TQ_con1"][6]*1e3,
                scenarioName["tvs_TQ_con2"][6]*1e3,
                (scenarioName["WTQ_con1"][6]+scenarioName["WTQ_con2"][6])/1e6,
                scenarioName["WTQ_rad2"][6]/1e6 ))

        f.write(
            "\t8) Mitigated VDE:   \t{:.3} ms (30% loss)\t\t{:.3} ms (70% loss)\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t{:.3} mm\t\t\t\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
                scenarioName["tauTQ"][7]*1e3, 
                scenarioName["tauTQ"][7]*3e3, 
                scenarioName["Wth"] / 1e6 * 0.8 * 0.2, 
                scenarioName["Wth"] / 1e6 * 0.8 ** 2, 
                lam_q * 1e3,
                scenarioName["tvs_TQ_con1"][7]*1e3,
                scenarioName["tvs_TQ_con2"][7]*1e3,
                (scenarioName["WTQ_con1"][7]+scenarioName["WTQ_con2"][7])/1e6,
                scenarioName["WTQ_rad2"][7]/1e6 ))
        
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
        
        HCF = [0.075, 0.075, 0.12, 0.2, 0.12, 0.2 , 0.05, 0.1  ]              # halo current fractions
        W_PFC(scenarioName=scenarioName,phase='CQ',peakingFactors=0)
        WthCQ = np.ones(8)
        for i in range(8): 
            WthCQ[i] = Wpol(scenarioName,HCF=HCF[i])

        f.write("\n___\nCQ:\n")
        f.write("\t                     \tLinear decay t:\t\tExp decay t:\t\tW_th losses \t\tW_th losses:\t\ttvs(S=1) conduc\t\tW conduc\t\tW radiat\n")
        f.write("\t                     \t               \t\t            \t\t(conducted):\t\t(radiated): \t\t      [s]        \t\t  [MJ]  \t\t  [MJ]  \n")
        i = 0
        f.write("\t1) Major Disruption: \t{:.3} ms\t\t\t\t{:.3} ms\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
            scenarioName["tauCQ"][i]*1e3,
            tauCQlinmin(scenarioName, linexp="exp", mitigatedVDE=0, MDlikely=1), 
            WthCQ[i] * 1, 
            WthCQ[i] * 0.,
            scenarioName["tvs_CQ_con"][i]*1e3,  
            scenarioName["WCQ_con"][i]*1e-6,
            scenarioName["WCQ_rad"][i]*1e-6   ))
        i = 1
        f.write("\t2) Major D. strong: \t{:.3} ms\t\t\t\t{:.3} ms\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
            scenarioName["tauCQ"][i]*1e3,
            tauCQlinmin(scenarioName, linexp="exp", mitigatedVDE=0, MDlikely=0), 
            WthCQ[i] * 1, 
            WthCQ[i] * 0.,
            scenarioName["tvs_CQ_con"][i]*1e3, 
            scenarioName["WCQ_con"][i]*1e-6,
            scenarioName["WCQ_rad"][i]*1e-6   ))
        i = 2
        f.write("\t3) Cold VDE, fast CQ:\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
            scenarioName["tauCQ"][i]*1e3,
            tauCQlinmin(scenarioName, linexp="exp", mitigatedVDE=0, MDlikely=0), 
            WthCQ[i] * 1, 
            WthCQ[i] * 0.,
            scenarioName["tvs_CQ_con"][i]*1e3, 
            scenarioName["WCQ_con"][i]*1e-6,
            scenarioName["WCQ_rad"][i]*1e-6   ))
        i = 3
        f.write("\t4) Cold VDE, slow CQ:\t{:.3} ms\t\t\t{:.3} ms\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
            scenarioName["tauCQ"][i]*1e3,
            tauCQlinmin(scenarioName, linexp="exp", longCQ=1), 
            WthCQ[i] * 0.7, 
            WthCQ[i] * 0.3,
            scenarioName["tvs_CQ_con"][i]*1e3, 
            scenarioName["WCQ_con"][i]*1e-6,
            scenarioName["WCQ_rad"][i]*1e-6   ))
        i = 4
        f.write("\t5) Hot VDE,  fast CQ:\t{:.3} ms\t\t\t\t{:.3} ms\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
            scenarioName["tauCQ"][i]*1e3,
            tauCQlinmin(scenarioName, linexp="exp", mitigatedVDE=0, MDlikely=0), 
            WthCQ[i] * 1, 
            WthCQ[i] * 0.,
            scenarioName["tvs_CQ_con"][i]*1e3, 
            scenarioName["WCQ_con"][i]*1e-6,
            scenarioName["WCQ_rad"][i]*1e-6   ))
        i = 5
        f.write("\t6) Hot VDE,  slow CQ:\t{:.3} ms\t\t\t{:.3} ms\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
            scenarioName["tauCQ"][i]*1e3,
            tauCQlinmin(scenarioName, linexp="exp", longCQ=1), 
            WthCQ[i] * 0.7, 
            WthCQ[i] * 0.3,
            scenarioName["tvs_CQ_con"][i]*1e3, 
            scenarioName["WCQ_con"][i]*1e-6,
            scenarioName["WCQ_rad"][i]*1e-6   ))
        i = 6
        f.write("\t7) Mitigated MDs:    \t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
            scenarioName["tauCQ"][i]*1e3,
            tauCQlinmin(scenarioName, linexp="exp", mitigatedVDE=1), 
            WthCQ[i] * 0.2, 
            WthCQ[i] * 0.8,
            scenarioName["tvs_CQ_con"][i]*1e3, 
            scenarioName["WCQ_con"][i]*1e-6,
            scenarioName["WCQ_rad"][i]*1e-6   ))
        i = 7
        f.write("\t8) Mitigated VDE:    \t{:.3} ms\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\t\t\t\t{:.3} ms\t\t\t\t{:.3} MJ\t\t\t\t{:.3} MJ\n".format(
            scenarioName["tauCQ"][i]*1e3,
            tauCQlinmin(scenarioName, linexp="exp", mitigatedVDE=1), 
            WthCQ[i] * 0.2, 
            WthCQ[i] * 0.8,
            scenarioName["tvs_CQ_con"][i]*1e3, 
            scenarioName["WCQ_con"][i]*1e-6,
            scenarioName["WCQ_rad"][i]*1e-6   ))

    f.close()

def scenarioCloud(reference,colArray=['BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM'],filename='FrancisSpreadsheet.xlsx',modeHL='L'):
    """
    Produces a dependance plot that contains the mutual correlations among data
        Input:
            - colArray :    array of column names on the Francis's spreadsheet. 
            - filename :    name of the Excel file used to pick the inputs from.
            - modeHL:       'H' --> H-mode scaling for tauE;  'L' --> L-mode scaling (default)

    """
    tE_vec   = np.zeros(len(colArray))
    t2_vec   = np.zeros(len(colArray))
    tCQ_vec  = np.zeros(len(colArray))
    lQ_vec   = np.zeros(len(colArray))
    lEich    = np.zeros(len(colArray))
    Wpol_vec = np.zeros(len(colArray))
    Wth_vec  = np.zeros(len(colArray))
    dWpol_vec= np.zeros(len(colArray))
    i = 0

    namesArray = colArray

    if (filename=="FrancisSpreadsheet_new1.xlsx"):  namesArray = ["68/A","68/B","69/A","69/B","70"]

    for col in colArray :
        scenario = readFromXls(namesArray[i],col,filename=filename) 

    #    tE_vec[i]   = tauE(scenario)
        tE_vec[i]   = tauE(scenarioName=scenario,mode=modeHL)
        t2_vec[i]   = DTcool(scenario)
        tCQ_vec[i]  = tauCQlinmin(scenario)
        lQ_vec[i]   = lambdaMHD(scenario)*1e3
        lEich[i]    = lambdaEich(scenario)*1e3
        Wth_vec[i]  = scenario["Wth"]*1e-6
        Wpol_vec[i] = Wpol(scenario,li3_betap="li3",HCF=0)/1e6        # HCF=0  --> W_{pol,vv}
        dWpol_vec[i]= 0.1*Wpol_vec[i]
        i += 1

    def errorBar(subplot,x,y,dy,colour):
        subplot.plot([x,x],[y-dy,y+dy],color=colour,linewidth=0.3)
        # subplot.plot([x-0.3,x+0.3],[y+dy,y+dy],color=colour)
        # subplot.plot([x-0.3,x+0.3],[y-dy,y-dy],color=colour)

    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(3, 2, figsize=(9, 9))

    scen = ' '
    #if (( col(colArray[0]) > col('AG') ) and ( col(colArray[-1] < col('BD') ))) :
    #    scen=' of SPR045 '
    #    reference=SPR045
    #if (( col(colArray[0]) > col('BC') ) and ( col(colArray[-1] < col('BK') ))) :
    scen=' of SPP-2 '
    # if (( col(colArray[0]) > col('BC') ) and ( col(colArray[-1] < col('BQ') ))) :
    #     scen=' of SPR068 and SPR069 '
    #     reference=SPR068
    fig.suptitle('Variability'+scen+'derived quantities on different scenarios',fontsize=14)

    if (modeHL=='H'):
        plot1_title = r'$\tau^{*}_{E,98(y,2)}$ [s]'

    if (modeHL=='L'):
        plot1_title = r'$\tau_{ITERL 96}$ [s]'

    for i in range(len(colArray)): errorBar(axs[0,0],namesArray[i],tE_vec[i],0.16*tE_vec[i],colour='grey')
    axs[0,0].plot(namesArray,tE_vec,'o',color='grey',label='scenarios')
    axs[0,0].set_title(plot1_title)   
    axs[0,0].plot(namesArray[np.abs(tE_vec-tE_vec.max()).argmin()],tE_vec.max(),'o',color='blue',label='max / min')
    axs[0,0].plot(namesArray[np.abs(tE_vec-tE_vec.min()).argmin()],tE_vec.min(),'o',color='blue')
    #axs[0,0].plot(colArray[np.abs(tE_vec-tauE(reference)).argmin()],tauE(reference),"o",color='red')
    axs[0,0].axhline(y=tauE(reference,mode=modeHL),color='red',linestyle='--',label='reference setup')
    xlimits = [-0.5,len(namesArray)-0.5]#axs[0,0].get_xlim()
    axs[0,0].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    axs[0,0].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[0,0].set_xlim(xlimits)
    ylimits = axs[0,0].get_ylim()
    axs[0,0].set_ylim([ylimits[0],ylimits[1]*1.34])

    axs[0,0].legend()

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(colArray)): errorBar(axs[0,1],namesArray[i],t2_vec[i],0.3*t2_vec[i],colour='grey')
    axs[0,1].plot(namesArray,t2_vec,'o',color='grey')
    axs[0,1].set_title(r'$\Delta{t}_{cool}$ [ms]')   
    axs[0,1].plot(namesArray[np.abs(t2_vec-t2_vec.max()).argmin()],t2_vec.max(),'o',color='blue')
    axs[0,1].plot(namesArray[np.abs(t2_vec-t2_vec.min()).argmin()],t2_vec.min(),'o',color='blue')
    #axs[0,1].plot(colArray[np.abs(t2_vec-DTcool(reference)).argmin()],DTcool(reference),"o",color='red')
    axs[0,1].axhline(y=DTcool(reference),color='red',linestyle='--')
    axs[0,1].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    axs[0,1].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[0,1].set_xlim(xlimits)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(namesArray)):  errorBar(axs[1,0],namesArray[i],tCQ_vec[i],0.3*tCQ_vec[i],colour='grey')
    axs[1,0].plot(namesArray,tCQ_vec,'o',color='grey')
    axs[1,0].set_title(r'$\tau_{CQ}^{lin}$ [ms]')   
    axs[1,0].plot(namesArray[np.abs(tCQ_vec-tCQ_vec.max()).argmin()],tCQ_vec.max(),'o',color='blue')
    axs[1,0].plot(namesArray[np.abs(tCQ_vec-tCQ_vec.min()).argmin()],tCQ_vec.min(),'o',color='blue')
    #axs[1,0].plot(colArray[np.abs(lQ_vec-lambdaMHD_rough(reference)*1e3).argmin()],lambdaMHD_rough(reference)*1e3,"o",color='red')
    axs[1,0].axhline(y=tauCQlinmin(reference),color='red',linestyle='--')
    axs[1,0].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    axs[1,0].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[1,0].set_xlim(xlimits)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(colArray)): 
        axs[1,1].plot([namesArray[i],namesArray[i]],[lEich[i],lQ_vec[i]],color='grey',linewidth=0.3)
    axs[1,1].plot(namesArray,(lQ_vec+lEich)/2,'o',color='grey')
    axs[1,1].set_title(r'$\lambda_{q}$ [mm]')   
    axs[1,1].plot(namesArray[np.abs((lQ_vec+lEich)/2-(lQ_vec.max()+lEich.max())/2).argmin()],(lQ_vec.max()+lEich.max())/2,'o',color='blue')
    axs[1,1].plot(namesArray[np.abs((lQ_vec+lEich)/2-(lQ_vec.min()+lEich.min())/2).argmin()],(lQ_vec.min()+lEich.min())/2,'o',color='blue')
    #axs[1,0].plot(colArray[np.abs(lQ_vec-lambdaMHD_rough(reference)*1e3).argmin()],lambdaMHD_rough(reference)*1e3,"o",color='red')
    axs[1,1].axhline(y=(lambdaMHD(reference)+lambdaEich(reference))*5e2,color='red',linestyle='--')
    axs[1,1].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    axs[1,1].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[1,1].set_xlim(xlimits)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(colArray)): errorBar(axs[2,0],namesArray[i],Wpol_vec[i],dWpol_vec[i],colour='grey')
    axs[2,0].plot(namesArray,Wpol_vec,'o',color='grey')
    #axs[2,0].set_title(r'$W_{pol,vv} = 1.1 \times W_{pol}$ [MW]',fontsize=12)   
    axs[2,0].set_title(r'$W_{pol,vv} = W_{CQ} \, /\, (1-HCF)^2$ [MW]',fontsize=12)   
    axs[2,0].plot(namesArray[np.abs(Wpol_vec-Wpol_vec.max()).argmin()],Wpol_vec.max(),'o',color='blue')
    axs[2,0].plot(namesArray[np.abs(Wpol_vec-Wpol_vec.min()).argmin()],Wpol_vec.min(),'o',color='blue')
    # axs[1,1].plot(colArray[np.abs(Wpol_vec-Wth(reference)*1e-6).argmin()],Wth(reference)*1e-6,"o",color='red')
    axs[2,0].axhline( y=Wpol(reference,li3_betap="li3")/1e6 ,  color='red' , linestyle='--')
    axs[2,0].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    axs[2,0].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[2,0].set_xlim(xlimits)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    axs[2,1].plot(namesArray,Wth_vec,'o',color='grey')
    axs[2,1].set_title(r'$W_{th}$ [MW]',fontsize=12)   
    axs[2,1].plot(namesArray[np.abs(Wth_vec-Wth_vec.max()).argmin()],Wth_vec.max(),'o',color='blue')
    axs[2,1].plot(namesArray[np.abs(Wth_vec-Wth_vec.min()).argmin()],Wth_vec.min(),'o',color='blue')
    # axs[1,1].plot(colArray[np.abs(Wpol_vec-Wth(reference)*1e-6).argmin()],Wth(reference)*1e-6,"o",color='red')
    axs[2,1].axhline( y=reference["Wth"]/1e6 ,  color='red' , linestyle='--')
    axs[2,1].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    axs[2,1].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[2,1].set_xlim(xlimits)

    plt.subplots_adjust(hspace=0.5)
    #plt.tight_layout()
    plt.show()

def Melt1plot(scenario,SPR="SPR-69/B",PF=1):
    """
    Produces the plot showing ratio of the incoming conducted & radiated loads during TQ and CQ to the critical melting value, for the various
    disruption types considered in the study.

    Requires that you have already called the function "Predictions" on the same scenario

        Input:
          - scenario:   name of a python library-type scenario
          - SPR:        string type input corresponding to the scenario name (goes in the title of the figure) 
          - PF:         0 --> not considering peaking factors;   1 --> considering peaking factors 
    """
    qcritTQ1 = qmelt(scenario["tauTQ"])
    qcritTQ2 = qmelt(scenario["tauTQ"]*3)
    qcritTQr = qmelt(scenario["tauTQ"]*4)
    qcritCQ  = qmelt(scenario["tauCQ"])

    disruptions = ["MD\nlikely","MD\nstrong","cold VDE\nfast CQ","cold VDE\nslow CQ","hot VDE\nfast CQ","hot VDE\nslow CQ","MD\nmitig.","VDE\nmitig."]
    Swet_cond   = [ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    # Swet_rad    = [ Sdiv, Sdiv, S_FW, S_FW, S_FW, S_FW, Sdiv, S_FW ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]

    W_PFC(scenarioName=scenario,phase="TQ",peakingFactors=PF)
    W_PFC(scenarioName=scenario,phase="CQ",peakingFactors=PF)

    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(1, 2, figsize=(15,5.5))

    fig.suptitle("Melting limit for tungsten ("+SPR+")",fontsize=18)

    ylimits = (1e-3,1e2)
    axs[0].semilogy(disruptions, scenario["WTQ_con1"]/(scenario["tauTQ"]*1*Swet_cond) / qcritTQ1 , color='red'  , linewidth=1 ) # , label="ramp-up phase" )
    axs[0].semilogy(disruptions, scenario["WTQ_con2"]/(scenario["tauTQ"]*3*Swet_cond) / qcritTQ2 , color='red'  , linewidth=1 , linestyle='--' ) # , label="ramp-down phase" )
    axs[0].semilogy(disruptions, scenario["WTQ_rad2"]/(scenario["tauTQ"]*4*Swet_rad)  / qcritTQr , color='blue' , linewidth=1 )
    axs[0].semilogy(disruptions, scenario["WTQ_con1"]/(scenario["tauTQ"]*1*Swet_cond) / qcritTQ1 , 'o'          , color='red'  , label="conducted" )
    axs[0].semilogy(disruptions, scenario["WTQ_con2"]/(scenario["tauTQ"]*3*Swet_cond) / qcritTQ2 , 'o'          , color='red' )
    axs[0].semilogy(disruptions, scenario["WTQ_rad2"]/(scenario["tauTQ"]*4*Swet_rad)  / qcritTQr , 'o'          , color='blue' , label="radiated"  )
    limits = axs[0].get_xlim()
    axs[0].semilogy([-1,10]    ,   np.ones(2)                                                        , color='black', linestyle=':' )
    axs[0].set_ylim(ylimits)
    axs[0].set_xlim(limits)
    axs[0].set_title("Thermal Quench",fontsize=16)
    axs[0].set_ylabel(r"$q_{wall}$ / $q_{melt}$",fontsize=16)
    axs[0].axhspan(1e0,1e10,color='black',alpha=0.1 , label="wall melting" )
    axs[0].axhspan(1e-10,1e0,color='cyan',alpha=0.1 , label="not melting" )
    axs[0].text(0,1.5,"melting",color='black',fontsize=12)
    axs[0].text(0,5e-1,"not melting",color='black',fontsize=12)
    # axs[0].text(6.7,35,"ramp\ndown",color='red',fontsize=10)
    # axs[0].text(6.3,2e5,"ramp\nup",color='red',fontsize=10)
    axs[0].semilogy([6,6.5],[450e-1,450e-1],color='red')
    axs[0].semilogy([6,6.5],[150e-1,150e-1],color='red',linestyle='--')
    axs[0].text(6.7,350e-1,"ramp\nup",color='red',fontsize=10)
    axs[0].text(6.7,100e-1,"ramp\ndown",color='red',fontsize=10)
    axs[0].legend(loc='upper left',fontsize=12)

    axs[1].semilogy(disruptions, scenario["WCQ_con"] /(scenario["tauCQ"]*Swet_cond) / qcritCQ   , color='red'  , linewidth=1   )
    axs[1].semilogy(disruptions, scenario["WCQ_rad"] /(scenario["tauCQ"]*Swet_rad)  / qcritCQ   , color='blue' , linewidth=1   )
    axs[1].semilogy(disruptions, scenario["WCQ_con"] /(scenario["tauCQ"]*Swet_cond) / qcritCQ   , 'o'          , color='red'   )
    axs[1].semilogy(disruptions, scenario["WCQ_rad"] /(scenario["tauCQ"]*Swet_rad)  / qcritCQ   , 'o'          , color='blue'  )
    axs[1].semilogy([-1,10]    , np.ones(2)                                                     , color='black', linestyle=':' )
    axs[1].set_ylim(ylimits)
    axs[1].set_xlim(limits)
    axs[1].set_title("Current Quench",fontsize=16)
    axs[1].axhspan(1e0,1e10,color='black',alpha=0.1)
    axs[1].axhspan(1e-10,1e0,color='cyan',alpha=0.1 )
    axs[1].text(0,1.5,"melting",color='black',fontsize=12)
    axs[1].text(0,5e-1,"not melting",color='black',fontsize=12)
    #axs[1].set_ylabel(r"$q_{wall} / q_{melt}$")

    plt.show()

def Melt2plot(scenario,SPR="SPR-69/B",PF=1):
    """
    Produces the plot showing surface temperature increases during TQ and CQ, owing to conduction and radiation, for the various
    disruption types considered in the study.

    Requires that you have already called the function "Predictions" on the same scenario

        Input:
          - scenario:   name of a python library-type scenario
          - SPR:        string type input corresponding to the scenario name (goes in the title of the figure)  
          - PF:         0 --> not considering peaking factors;   1 --> considering peaking factors 
    """

    def Tfinal(q0,time):
        Cp    = 130    # [J / kg K]
        k     = 170    # [W / m K]
        rho   = 19250  # [kg / m3]
        T0    = 550 + 273.15

        return 2 * q0 * np.sqrt( time / (rho * Cp * k * np.pi) ) #+ T0

    T0    = 550 + 273.15
    Tmelt = 3695 - T0 # [K]
    Tvap  = 6203 - T0 # [K]

    disruptions = ["MD\nlikely","MD\nstrong","cold VDE\nfast CQ","cold VDE\nslow CQ","hot VDE\nfast CQ","hot VDE\nslow CQ","MD\nmitig.","VDE\nmitig."]
    Swet_cond   = [ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    # Swet_rad    = [ Sdiv, Sdiv, S_FW, S_FW, S_FW, S_FW, Sdiv, S_FW ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]

    TTQcon1 = np.zeros(8)
    TTQcon2 = np.zeros(8)
    TTQrad  = np.zeros(8)
    TCQcon  = np.zeros(8)
    TCQrad  = np.zeros(8)

    W_PFC(scenarioName=scenario,phase="TQ",peakingFactors=PF)
    W_PFC(scenarioName=scenario,phase="CQ",peakingFactors=PF)

    t_TQ = scenario["tauTQ"][0]
    for jj in range(8):
        TTQcon1[jj] = Tfinal( time=t_TQ , q0=scenario["WTQ_con1"][jj]/(t_TQ*Swet_cond[jj]) )
        if (TTQcon1[jj] >= Tvap): TTQcon1[jj] = Tvap
        if (t_TQ >= scenario["tvs_TQ_con1"][jj]): TTQcon1[jj] = Tvap   

        TTQcon2[jj] = Tfinal( time=t_TQ*3 , q0=scenario["WTQ_con2"][jj]/(t_TQ*3*Swet_cond[jj]) ) #+ TTQcon1[jj]
        if (TTQcon2[jj] >= Tvap): TTQcon2[jj] = Tvap
        if (t_TQ*3 >= scenario["tvs_TQ_con2"][jj]): TTQcon2[jj] = Tvap

        TTQrad[jj] = Tfinal( time=t_TQ*4 , q0=scenario["WTQ_rad2"][jj]/(t_TQ*4*Swet_rad[jj]) )
        if (TTQrad[jj] >= Tvap): TTQrad[jj] = Tvap

        TCQcon[jj] = Tfinal( time=scenario["tauCQ"][jj] , q0=scenario["WCQ_con"][jj]/(scenario["tauCQ"][jj]*Swet_cond[jj]) )
        if (TCQcon[jj] >= Tvap): TCQcon[jj] = Tvap
        #if (scenario["tauCQ"][jj] >= scenario["tvs_CQ_con"][jj]): TCQcon[jj] = Tvap

        TCQrad[jj] = Tfinal( time=scenario["tauCQ"][jj] , q0=scenario["WCQ_rad"][jj]/(scenario["tauCQ"][jj]*Swet_rad[jj]) )
        if (TCQrad[jj] >= Tvap): TCQrad[jj] = Tvap


    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(1, 2, figsize=(15,5.5))

    fig.suptitle("Tungsten wall temperature raise ("+SPR+")",fontsize=18)

    ylimits = (3e0,3e4)
    axs[0].semilogy(disruptions,   TTQcon1   , color='red'  , linewidth=1 )# , label="ramp-up phase" )
    axs[0].semilogy(disruptions,   TTQcon2   , color='red'  , linewidth=1 , linestyle='--' ) # , label="ramp-down phase" )
    axs[0].semilogy(disruptions[0:8],   TTQrad[0:8]    , color='blue' , linewidth=1 )
    axs[0].semilogy(disruptions,   TTQcon1   , 'o'          , color='red'  , label="conducted" )
    axs[0].semilogy(disruptions,   TTQcon2   , 'o'          , color='red' )
    axs[0].semilogy(disruptions,   TTQrad    , 'o'          , color='blue' , label="radiated"  )
    limits = axs[0].get_xlim()
    axs[0].semilogy([-1,10]    ,   np.ones(2)*Tmelt         , color='black', linestyle=':' )
    axs[0].semilogy([-1,10]    ,   np.ones(2)*Tvap          , color='black', linestyle=':' )
    axs[0].set_ylim(ylimits)
    axs[0].set_xlim(limits)
    axs[0].set_title("Thermal Quench",fontsize=16)
    axs[0].set_ylabel(r"$\Delta T_{wall}$ / $k_B$ [K]",fontsize=16)
    axs[0].axhspan(Tvap , 1e10 , color='red'   ,alpha=0.1 , label="vaporised wall" )
    axs[0].axhspan(Tmelt, Tvap , color='orange',alpha=0.1 , label="molten wall" )
    axs[0].axhspan(0    , Tmelt, color='cyan'  ,alpha=0.1 , label="solid wall" )
    axs[0].semilogy([6,6.5],[25e0,25e0],color='red')
    axs[0].semilogy([6,6.5],[8e0,8e0],color='red',linestyle='--')
    axs[0].text(6.7,5e0,"ramp\ndown",color='red',fontsize=10)
    axs[0].text(6.7,18e0,"ramp\nup",color='red',fontsize=10)
    # axs[0].text(6.7,35,"ramp\ndown",color='red',fontsize=10)
    # axs[0].text(6.3,2e5,"ramp\nup",color='red',fontsize=10)
    #axs[0].plot([6,6.5],[550,550],color='red')
    #axs[0].plot([6,6.5],[250,250],color='red',linestyle='--')
    #axs[0].text(6.7,180,"ramp\ndown",color='red',fontsize=10)
    #axs[0].text(6.7,450,"ramp\nup",color='red',fontsize=10)
    #axs[0].legend(loc='lower left',fontsize=12)

    axs[1].semilogy(disruptions,   TCQcon   , color='red'  , linewidth=1   )
    axs[1].semilogy(disruptions,   TCQrad   , color='blue' , linewidth=1   )
    axs[1].semilogy(disruptions,   TCQcon   , 'o'          , color='red'   , label="conducted" )
    axs[1].semilogy(disruptions,   TCQrad   , 'o'          , color='blue'  , label="radiated" )
    axs[1].semilogy([-1,10]    ,   np.ones(2)*Tmelt        , color='black', linestyle=':' )
    axs[1].semilogy([-1,10]    ,   np.ones(2)*Tvap         , color='black', linestyle=':' )
    axs[1].text(-.1,Tmelt*0.65,"melting point",color='black',fontsize=12)
    axs[1].text(-.1,Tvap *1.20,"vapour point",color='black',fontsize=12)
    axs[1].set_ylim(ylimits)
    axs[1].set_xlim(limits)
    axs[1].set_title("Current Quench",fontsize=16)
    axs[1].axhspan(Tvap , 1e10 , color='red'   , alpha=0.1 , label="vaporised wall" )
    axs[1].axhspan(Tmelt, Tvap , color='orange', alpha=0.1 , label="molten wall" )
    axs[1].axhspan(0    , Tmelt, color='cyan'  , alpha=0.1 , label="solid wall" )
    #axs[1].text(0,1.5,"melting",color='black',fontsize=12)
    #axs[1].text(0,5e-1,"not melting",color='black',fontsize=12)
    #axs[1].set_ylabel(r"$q_{wall} / q_{melt}$")
    axs[0].legend(loc='lower left',fontsize=12)

    plt.show()

    return TCQrad

def JETscenarios(shot=96867):
    scenario = JET96867.copy()

    if (shot==1):
        scenario["name"]  = "JET_1.2MA_mitigatedVDE"
        scenario["B0"]    = 1.15
        Wmag              = 3.2e6 
        scenario["P_SOL"] = 0
        scenario["Wth"]   = 0.5e6
        scenario["Ip"]    = 1.2e6
        scenario["q95"]   = 3.2
        scenario["li3"]   = Wmag * 4 / (1.1 * mu0 * scenario["R0"] * scenario["Ip"]**2)
    elif (shot==2):
        scenario["name"]  = "JET_2.5MA_mitigatedVDE"
        scenario["B0"]    = 2.5
        Wmag              = 16e6 
        scenario["P_SOL"] = 15e6 + 2e6
        scenario["Wth"]   = 4.1e6
        scenario["Ip"]    = 2.5e6
        scenario["q95"]   = 3.12
        scenario["li3"]   = Wmag * 4 / (1.1 * mu0 * scenario["R0"] * scenario["Ip"]**2)

    return scenario

def validation(number=0) :
    scenario = JETscenarios(number)

    def f(a,x):
        """
        Integral of Btor on an ellypse: (x/a)**2 + (y/ka)**2 = 1
        """
        S = (a**2-x**2)
        return -(S + x * np.arctan(x/S)) / x
    
    # Wtor     = ( scenario["B0"] * scenario["R0"] )**2 / (2 * mu0) * (
    #                                     f(scenario["a"],scenario["R0"]+scenario["a"]) - f(scenario["a"],scenario["R0"]-scenario["a"]) )
    #Wtor     = 0

    tau_cool   = DTcool(scenarioName=scenario) + tauTQ(scenarioName=scenario)
    tau_CQ_min = tauCQlinmin(scenarioName=scenario,mitigatedVDE=1)
    tau_CQ_ave = tauCQlinmin(scenarioName=scenario,mitigatedVDE=1,longCQ=1)
    Wrad       = scenario["Wth"] * (0.2 + 0.8**2) + Wpol(scenarioName=scenario,HCF=0.25)*0.8
    qcrit_Be   = qmelt(tauTQ(scenarioName=scenario),material="Be")
    qcrit_W    = qmelt(tauTQ(scenarioName=scenario),material="W")
    qcrit_Be_CQ= qmelt(tau_CQ_ave,material="Be")
    qcrit_W_CQ = qmelt(tau_CQ_ave,material="W")

    scenario["tauCQ"] = tau_CQ_ave*1e-3

    print("Ip [MA]:          ",scenario["Ip"]/1e6)
    print("tau[preTQ]+tau1:  ",tau_cool,"            [min,max]=[",0.7*tau_cool,",",1.3*tau_cool,"]")
    print("tau[CQ] min.:     ",tau_CQ_min," [min,max]=["          ,0.7*tau_CQ_min,",",1.3*tau_CQ_min,"]")
    print("tau[CQ] long:     ",tau_CQ_ave," [min,max]=["          ,0.7*tau_CQ_ave,",",1.3*tau_CQ_ave,"]")
    print("Wrad [MJ]:        ",Wrad/1e6,"             [min,max]=[",0.78e-6*Wrad,",",1.22e-6*Wrad,"]")
    print("qmelt TQ [MW/m2]: ",qcrit_Be/1e6," with Berillium (walls)")
    print("qmelt TQ [MW/m2]: ",qcrit_W/1e6," with Tungsten (divertor)")
    print("qmelt CQ [MW/m2]: ",qcrit_Be_CQ/1e6," with Berillium (walls)")
    print("qmelt CQ [MW/m2]: ",qcrit_W_CQ/1e6," with Tungsten (divertor)")
    print("---------------------------------------------------------------")
    print("W_TQ conduct. [MJ] ",scenario["Wth"]*0.8*0.2e-6)
    print("tauTQ [ms]:        ",tauTQ(scenario))
    print("S_limiter [m2] ~   ",4)
    print("q_plasma [MW/m2]   ",0.2*0.8*scenario["Wth"]/(4*tauTQ(scenario))/1e6)
    print("---------------------------------------------------------------")
    print("W_CQ conduct. [MJ] ",(Wpol(scenarioName=scenario)-Wcoupled(scenarioName=scenario,lin_exp=1))*0.2e-6)
    print("tauCQ [ms]:        ",tau_CQ_ave)
    print("S_limiter [m2] ~   ",4)
    print("q_plasma [MW/m2]   ",(Wpol(scenarioName=scenario)-Wcoupled(scenarioName=scenario,lin_exp=1))*0.2/(4*tau_CQ_ave)/1e6)
    print("---------------------------------------------------------------")
    print("W_TQ rad [MJ]      ",scenario["Wth"] * 0.8**2 / 1e6)
    print("tauCQ [ms]:        ",tauTQ(scenario))
    print("S_PFC [m2] ~       ",240)
    print("q_plasma [MW/m2]   ",scenario["Wth"] * 0.8**2/(240*tauTQ(scenario))/1e6)
    print("---------------------------------------------------------------")
    print("W_CQ rad [MJ]      ",(Wpol(scenarioName=scenario)-Wcoupled(scenarioName=scenario,lin_exp=1))*0.8e-6)
    print("tauCQ [ms]:        ",tau_CQ_ave)
    print("S_PFC [m2] ~       ",240)
    print("q_plasma [MW/m2]   ",(Wpol(scenarioName=scenario)-Wcoupled(scenarioName=scenario,lin_exp=1))*0.8/(240*tau_CQ_ave)/1e6)
    

if __name__ == "__main__":
    """ Run the code """
#    scenario = readFromXls('reference','BG',filename="FrancisSpreadsheet.xlsx")
#    scenario = readFromXls('reference','E',filename="FrancisSpreadsheet_new1.xlsx")

#    colArray_new = ['C','D','E','F','G','H','I']

    filename = "FrancisSpreadsheet_new1.xlsx"
    # filename = "FrancisSpreadsheet_SPP3.xlsx"
    # filename = "FrancisSpreadsheet_SPP1.xlsx"

    if (filename=="FrancisSpreadsheet.xlsx"):
        reference=readFromXls('reference','BG')
    if (filename=="FrancisSpreadsheet_new1.xlsx"):
        reference=readFromXls('reference','F',filename=filename)
        name = "SPR-69/B"
    if (filename=="FrancisSpreadsheet_SPP1.xlsx"):
        reference=readFromXls('reference','E',filename=filename)
        name = "SPR-46/clean"
    if (filename=="FrancisSpreadsheet_SPP3.xlsx"):
        reference=readFromXls('reference','F',filename=filename)
        name = 'SPP-3/temporary'
        Scp = Scp*0.73473
        S_FW = S_FW*0.73473
        Sdiv = Sdiv*0.73473

    #reference=readFromXls('SPR-70','G',filename=filename)
    # name = "SPR-68/A"
    # reference=readFromXls('reference','C',filename=filename)

    # name = "SPR-70"
    # reference=readFromXls('reference','G',filename=filename)

    # name = "SPR-68/B"
    # reference=readFromXls('reference','D',filename=filename)

    Predictions(scenarioName=reference)
    # #scenarioCloud(reference=reference, colArray=['C','D','E','F','G'], filename=filename, modeHL='L')
    # #scenarioCloud(reference=reference, colArray=['C','D','E','F','G','H','I','J'], filename=filename, modeHL='L')
    out=Melt1plot(scenario=reference,SPR=name,PF=1)
    out=Melt2plot(scenario=reference,SPR=name,PF=1)

    #dependancePlots(scenarioName=SPR068,scenarioBounds=SPR068_MinMax)


