from disruption_scenarios import *
from InputOutput import readFromXls
import matplotlib.pyplot as plt

def scenarioCloud(reference,colArray,filename,modeHL='L'):
    """
    Produces plot of the variability of some key scenario-dependent input parameters for 0Dsrupt, across a set of different plasma scenarios, 
    saved in various (consecutive or non-consecutive) columns in the input .xlsx file. 
    One of the scenarios should be indicated as the reference: its quantities will be highlighted in a different colour w.r.t. other scenarios

        Input:
            - reference:    dictionary-type scenario, deepcopy of the template SCENARIO.
            - filename:     name of the input Excel file.
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

    d_tE_vec   = np.zeros(len(colArray))
    d_t2_vec   = np.zeros(len(colArray))
    d_tCQ_vec  = np.zeros(len(colArray))
    d_Wpol_vec = np.zeros(len(colArray))
    d_Wth_vec  = np.zeros(len(colArray))
    
    i = 0

    namesArray = []

    # if (filename=="FrancisSpreadsheet_new1.xlsx"):  namesArray = ["68/A","68/B","69/A","69/B","70"]

    for col in colArray :
        scenario = readFromXls(col,filename=filename) 
        namesArray.append(scenario["name"])

    #    tE_vec[i]   = tauE(scenario)
        tE_vec[i]   = tauE(scenarioName=scenario,mode=modeHL)
        t2_vec[i]   = DTcool(scenario)*1e3
        tCQ_vec[i]  = tauCQlinmin(scenario)*1e3
        lQ_vec[i]   = lambdaMHD(scenario)*1e3
        lEich[i]    = lambdaEich(scenario)*1e3
        Wth_vec[i]  = scenario["Wth"]*1e-6
        Wpol_vec[i] = Wpol(scenario,li3_betap="li3")/1e6        # HCF=0  --> W_{pol,vv}
        dWpol_vec[i]= 0.1*Wpol_vec[i]

        Predictions(scenario)
        err = RMSE(scenario)

        d_tE_vec[i]   = err["tauPreTQ"][0]
        d_t2_vec[i]   = err["tauPreTQ"][7]
        d_tCQ_vec[i]  = err["tauCQ"][0]
        d_Wpol_vec[i] = err["WthCQ"]
        d_Wth_vec[i]  = err["Wth"]
        i += 1

    def errorBar(subplot,x,y,dy,colour):
        subplot.plot([x,x],[y-dy,y+dy],color=colour,linewidth=0.3)
        # subplot.plot([x-0.3,x+0.3],[y+dy,y+dy],color=colour)
        # subplot.plot([x-0.3,x+0.3],[y-dy,y-dy],color=colour)

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

    # for i in range(len(colArray)): errorBar(axs[0,0],namesArray[i],tE_vec[i],0.16*tE_vec[i],colour='grey')
    for i in range(len(colArray)): errorBar(axs[0,0],namesArray[i],tE_vec[i],d_tE_vec[i]*tE_vec[i],colour='grey')
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

    for i in range(len(colArray)): errorBar(axs[0,1],namesArray[i],d_t2_vec[i],t2_vec[i]*t2_vec[i],colour='grey')
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

    for i in range(len(namesArray)):  errorBar(axs[1,0],namesArray[i],tCQ_vec[i],d_tCQ_vec[i]*tCQ_vec[i],colour='grey')
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

    for i in range(len(colArray)): errorBar(axs[2,0],namesArray[i],Wpol_vec[i],d_Wpol_vec[i]*Wpol_vec[i],colour='grey')
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

    Sdiv = scenario["S_div"]
    S_FW = scenario["S_FW"]
    Scp = scenario["S_cp"]

    disruptions = ["MD\nlikely","MD\nstrong","cold VDE\nfast CQ","cold VDE\nslow CQ","hot VDE\nfast CQ","hot VDE\nslow CQ","MD\nmitig.","VDE\nmitig."]
    Swet_cond   = [ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    # Swet_rad    = [ Sdiv, Sdiv, S_FW, S_FW, S_FW, S_FW, Sdiv, S_FW ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]

    W_PFC(scenarioName=scenario,phase="TQ",peakingFactors=PF)
    W_PFC(scenarioName=scenario,phase="CQ",peakingFactors=PF)

    fig, axs = plt.subplots(1, 2, figsize=(15,5.5))

    fig.suptitle("Melting limit for tungsten ("+SPR+")",fontsize=18)

    ylimits = (1e-3,1e2)
    axs[0].semilogy(disruptions, scenario["WTQ_con1"]/(scenario["tauTQ"]*1*Swet_cond) / qcritTQ1 , color='red'  , linewidth=1 ) # , label="ramp-up phase" )
    axs[0].semilogy(disruptions, scenario["WTQ_con2"]/(scenario["tauTQ"]*3*Swet_cond) / qcritTQ2 , color='red'  , linewidth=1 , linestyle='--' ) # , label="ramp-down phase" )
    axs[0].semilogy(disruptions, scenario["WTQ_rad"]/(scenario["tauTQ"]*4*Swet_rad)  / qcritTQr , color='blue' , linewidth=1 )
    axs[0].semilogy(disruptions, scenario["WTQ_con1"]/(scenario["tauTQ"]*1*Swet_cond) / qcritTQ1 , 'o'          , color='red'  , label="conducted" )
    axs[0].semilogy(disruptions, scenario["WTQ_con2"]/(scenario["tauTQ"]*3*Swet_cond) / qcritTQ2 , 'o'          , color='red' )
    axs[0].semilogy(disruptions, scenario["WTQ_rad"]/(scenario["tauTQ"]*4*Swet_rad)  / qcritTQr , 'o'          , color='blue' , label="radiated"  )
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
    axs[0].text(6.7,350e-1,"rise\nphase",color='red',fontsize=10)
    axs[0].text(6.7,100e-1,"fall\nphase",color='red',fontsize=10)
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

    Sdiv = scenario["S_div"]
    S_FW = scenario["S_FW"]
    Scp = scenario["S_cp"]

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

        TTQrad[jj] = Tfinal( time=t_TQ*4 , q0=scenario["WTQ_rad"][jj]/(t_TQ*4*Swet_rad[jj]) )
        if (TTQrad[jj] >= Tvap): TTQrad[jj] = Tvap

        TCQcon[jj] = Tfinal( time=scenario["tauCQ"][jj] , q0=scenario["WCQ_con"][jj]/(scenario["tauCQ"][jj]*Swet_cond[jj]) )
        if (TCQcon[jj] >= Tvap): TCQcon[jj] = Tvap
        #if (scenario["tauCQ"][jj] >= scenario["tvs_CQ_con"][jj]): TCQcon[jj] = Tvap

        TCQrad[jj] = Tfinal( time=scenario["tauCQ"][jj] , q0=scenario["WCQ_rad"][jj]/(scenario["tauCQ"][jj]*Swet_rad[jj]) )
        if (TCQrad[jj] >= Tvap): TCQrad[jj] = Tvap


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
    axs[0].text(6.7,5e0,"rise\nphase",color='red',fontsize=10)
    axs[0].text(6.7,18e0,"fall\nphase",color='red',fontsize=10)
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

