import sys
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np

path = (Path(__file__).resolve()).parent

sys.path.append('..')
from disruption_scenarios import *
from InputOutput import readFromXls, readGeneric, read_excel_file, row, col

JET_template = {
    "name"    : "template",
    "tauCQ"   : 0,
    "tauTQ"   : 0,
    "Tmax_TQ" : 0,      # max temperature reached by Be wall during TQ
    "Tmax_CQ" : 0       # max temperature reached by Be wall during CQ
}

def validation1(s1,jet1,s2,jet2,s3,jet3,s4,jet4) :
    """
    Inputs:
      - s1, s2, s3, s4:     simulations done with 0Dsrupt.
      - jet1 ... jet4:      results in JET database.
    """
    fig, axs = plt.subplots(1, 2, figsize=(15,5.5))

    tauTQ_0Dsrupt = np.array([(s1["tauTQ1"][3]+s1["tauTQ2"][3])*1e3 , 
                              (s2["tauTQ1"][3]+s2["tauTQ2"][3])*1e3 , 
                              (s3["tauTQ1"][3]+s3["tauTQ2"][3])*1e3 , 
                              (s4["tauTQ1"][3]+s4["tauTQ2"][3])*1e3   ])

    tauCQ_0Dsrupt = np.array([ s1["tauCQ"][3]*1e3 , s2["tauCQ"][3]*1e3 , s3["tauCQ"][3]*1e3 , s4["tauCQ"][3]*1e3 ])

    scenarioNames = [jet1["name"],jet2["name"],jet3["name"],jet4["name"]]
    JET_TQ        = np.array([jet1["tauTQ"]*1e3,jet2["tauTQ"]*1e3,jet3["tauTQ"]*1e3,jet4["tauTQ"]*1e3])
    JET_CQ        = np.array([jet1["tauCQ"]*1e3,jet2["tauCQ"]*1e3,jet3["tauCQ"]*1e3,jet4["tauCQ"]*1e3])

    fig.suptitle("Validation on unmitigated VDEs in JET",fontsize=18)

    for a in axs[:]: 
        a.tick_params(axis="both",labelsize=14)

    axs[0].plot(scenarioNames, JET_TQ,'kD')
    axs[0].set_title("Thermal quench duration",fontsize=16)
    axs[0].set_ylabel(r'$\tau_{TQ}$ [ms]',fontsize=16)
    axs[0].plot(scenarioNames, tauTQ_0Dsrupt, linestyle='-', color='blue')
    axs[0].fill_between(np.arange(len(scenarioNames)),tauTQ_0Dsrupt*0.7,tauTQ_0Dsrupt*1.3,color="blue",alpha=0.1)
    
    axs[1].plot(scenarioNames,JET_CQ,'kD')
    axs[1].set_title("Current quench duration",fontsize=16)
    axs[1].set_ylabel(r'$\tau_{CQ,lin}$ [ms]',fontsize=16)
    axs[1].plot(scenarioNames, tauCQ_0Dsrupt , linestyle='-', color='blue')
    axs[1].fill_between(np.arange(len(scenarioNames)) , tauCQ_0Dsrupt*0.7, tauCQ_0Dsrupt*1.3, color="blue", alpha=0.1)

    plt.show()

def validation2(sim,jet):
    file = read_excel_file("Inputs_JET.xlsx")

    time_wall = np.array( file.iloc[ row(np.arange(39,64)) , col('B') ] )
    Temp_wall = np.array( file.iloc[ row(np.arange(39,64)) , col('C') ] ) + 273.15

    Tmax1 = Tfinal(q0=sim["WTQ_con1"][3]/(sim["tauTQ1"][3]*sim["S_wet_cond_TQ1"][3]) , time=sim["tauTQ1"][3] , 
                   Swet=sim["S_wet_cond_TQ1"][3] , material="Be" , T0=Temp_wall[0])
    Tmax2 = Tfinal(q0=sim["WTQ_con2"][3]/(sim["tauTQ2"][3]*sim["S_wet_cond_TQ2"][3]), time=sim["tauTQ2"][3], 
                       Swet=sim["S_wet_cond_TQ2"][3] , material="Be" , T0=Tmax1)
    Tmax3 = Tfinal(q0=sim["WCQ_con"][3] /(sim["tauCQ"][3]*sim["S_wet_cond_CQ"][3])  , time=sim["tauCQ"][3] , 
                   Swet=sim["S_wet_cond_CQ"][3] , material="Be" , T0=Temp_wall[0])
    Tmax4 = Tfinal(q0=(sim["WTQ_con1"][3]+sim["WTQ_con2"][3])/((sim["tauTQ1"][3]+sim["tauTQ2"][3])*sim["S_wet_cond_TQ2"][3]), 
                   time=sim["tauTQ1"][3]+sim["tauTQ2"][3], Swet=sim["S_wet_cond_TQ2"][3] , material="Be" , T0=Tmax1)
            
    time_0Dsrupt = np.array([time_wall[0]       ,       time_wall[8]        , time_wall[8]+sim["tauTQ1"][3] ,  
                             time_wall[8]+sim["tauTQ1"][3]+sim["tauTQ2"][3] , time_wall[8]+sim["tauTQ1"][3]+sim["tauTQ2"][3]*1.1 ,  
                             time_wall[9]                                   , time_wall[9]+sim["tauCQ"][3] ])
    Temp_0Dsrupt = np.array([Temp_wall[0]       ,       Temp_wall[0]        , Tmax1 , 
                             Tmax2                                          , Temp_wall[0] ,
                             Temp_wall[0]                                   , Tmax3          ])
    time_0Dsrupt4= np.array([time_wall[0]       ,       time_wall[8]        ,   
                             time_wall[8]+sim["tauTQ1"][3]+sim["tauTQ2"][3] , time_wall[8]+sim["tauTQ1"][3]+sim["tauTQ2"][3]*1.1 ,  
                             time_wall[9]                                   , time_wall[9]+sim["tauCQ"][3] ])
    Temp_0Dsrupt4= np.array([Temp_wall[0]       ,       Temp_wall[0]        , 
                             Tmax4                                          , Temp_wall[0] ,
                             Temp_wall[0]                                   , Tmax3          ])

    time_offset = 40    # Costumary for JET pulses to subtract 40 sec, which is the time before breakdown 

    plt.plot(time_wall     - time_offset , Temp_wall    , 'r-'  , label=jet["name"])
    plt.plot(time_0Dsrupt  - time_offset , Temp_0Dsrupt , 'b-'  , label="0Dsrupt - TQ 2 steps")
    plt.plot(time_0Dsrupt4 - time_offset , Temp_0Dsrupt4, 'c--' , label="0Dsrupt - TQ 1 step")
    plt.xlim([58.0-time_offset,58.2-time_offset])
    plt.fill_between(time_0Dsrupt - time_offset , Temp_0Dsrupt*0.7 , Temp_0Dsrupt*1.3 ,alpha=0.1 )
    plt.title("Be wall temperature (upper dump plates) - #85386 KL14-P5WA")
    plt.xlabel("time [s]")
    plt.ylabel("Temperature [K]")
    plt.plot(np.array([time_wall[0],time_wall[-1]]) - time_offset , np.ones(2)*1560 , 'k:' )
    plt.text(time_wall[6] - time_offset , 1610 , 'melting point' , color='black' , fontsize=10 )
    plt.legend()

    plt.show()


if __name__ == "__main__":
    JET_86615 = readFromXls(filename=str(path / "Inputs_JET.xlsx"),cc='D')
    JET_85386 = readFromXls(filename=str(path / "Inputs_JET.xlsx"),cc='E')
    JET_84675 = readFromXls(filename=str(path / "Inputs_JET.xlsx"),cc='F')
    JET_84832 = readFromXls(filename=str(path / "Inputs_JET.xlsx"),cc='G')

    vv = ["tauCQ","tauTQ","Tmax_TQ","Tmax_CQ"]
    pp = [  28   ,  29   ,   30    ,    31   ]

    out_86615 = readGeneric(variables=vv, positions=pp, filename=str(path / "Inputs_JET.xlsx"), cc='D')
    out_85386 = readGeneric(variables=vv, positions=pp, filename=str(path / "Inputs_JET.xlsx"), cc='E')
    out_84675 = readGeneric(variables=vv, positions=pp, filename=str(path / "Inputs_JET.xlsx"), cc='F')
    out_84832 = readGeneric(variables=vv, positions=pp, filename=str(path / "Inputs_JET.xlsx"), cc='G')

    W_PFC(JET_84675,phase="TQ",peakingFactors=0,Ndiv=1,singleCase=5,rescale_a=1.0,CQ_lin_exp=0)
    W_PFC(JET_84675,phase="CQ",peakingFactors=1,Ndiv=1,singleCase=5,rescale_a=1.0,CQ_lin_exp=0)
    W_PFC(JET_85386,phase="TQ",peakingFactors=0,Ndiv=1,singleCase=3,rescale_a=1.0,CQ_lin_exp=1)
    W_PFC(JET_85386,phase="CQ",peakingFactors=1,Ndiv=1,singleCase=3,rescale_a=1.0,CQ_lin_exp=1)
    W_PFC(JET_86615,phase="TQ",peakingFactors=0,Ndiv=1,singleCase=3,rescale_a=1.0,CQ_lin_exp=0)
    W_PFC(JET_86615,phase="CQ",peakingFactors=1,Ndiv=1,singleCase=3,rescale_a=1.0,CQ_lin_exp=0)
    W_PFC(JET_84832,phase="TQ",peakingFactors=0,Ndiv=1,singleCase=3,rescale_a=1.0,CQ_lin_exp=0)
    W_PFC(JET_84832,phase="CQ",peakingFactors=1,Ndiv=1,singleCase=3,rescale_a=1.0,CQ_lin_exp=0)

    validation1(JET_86615,out_86615,JET_85386,out_85386,JET_84675,out_84675,JET_84832,out_84832)
    validation2(JET_85386,out_85386)


