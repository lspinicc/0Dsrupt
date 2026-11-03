from disruption_scenarios import *
from InputOutput import readFromXls
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def scenarioCloud(reference,colArray,filename,modeHL='L'):
    """
    Produces plot of the variability of some key scenario-dependent input parameters for 0Dsrupt, across a set of different plasma scenarios, 
    saved in various (consecutive or non-consecutive) columns in the input .xlsx file. 
    One of the scenarios should be indicated as the reference: its quantities will be highlighted in a different colour w.r.t. other scenarios

        Input:
            - reference:    dictionary-type scenario, deepcopy of the template SCENARIO.
            - colArray:     array of column names on the input spreadsheet file, whose data should be included in the comparison.
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
        tCQ_vec[i]  = tauCQlinmin(scenario,longCQ=1)*1e3
        lQ_vec[i]   = lambdaMHD(scenario,model='HD',MHD_turbulence_on=False)*1e3
        lEich[i]    = lambdaMHD(scenario,model='Eich',MHD_turbulence_on=False)*1e3
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
    fig.suptitle('Variability'+scen+'main scalar quantities among different scenarios',fontsize=14)

    if (modeHL=='H'):
        plot1_title = r'(a) $\tau^{*}_{E,98(y,2)}$ [s]'

    if (modeHL=='L'):
        plot1_title = r'(a) $\tau_{ITERL 96}$ [s]'

    # for i in range(len(colArray)): errorBar(axs[0,0],namesArray[i],tE_vec[i],0.16*tE_vec[i],colour='grey')
    for i in range(len(colArray)): errorBar(axs[0,0],namesArray[i],tE_vec[i],d_tE_vec[i]*tE_vec[i],colour='grey')
    axs[0,0].plot(namesArray,tE_vec,'o',color='grey',label='scenarios')
    axs[0,0].set_title(plot1_title)   
    axs[0,0].plot(namesArray[np.abs(tE_vec-tE_vec.max()).argmin()],tE_vec.max(),'o',color='blue',label='max / min')
    axs[0,0].plot(namesArray[np.abs(tE_vec-tE_vec.min()).argmin()],tE_vec.min(),'o',color='blue')
    #axs[0,0].plot(colArray[np.abs(tE_vec-tauE(reference)).argmin()],tauE(reference),"o",color='red')
    axs[0,0].axhline(y=tauE(reference,mode=modeHL),color='red',linestyle='--',label='reference setup')
    xlimits = [-0.5,len(namesArray)-0.5]#axs[0,0].get_xlim()
    # axs[0,0].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    # axs[0,0].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[0,0].set_xlim(xlimits)
    ylimits = axs[0,0].get_ylim()
    axs[0,0].set_ylim([ylimits[0],ylimits[1]*1.34])

    axs[0,0].legend()

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(colArray)): errorBar(axs[0,1],namesArray[i],t2_vec[i],d_t2_vec[i]*t2_vec[i],colour='grey')
    axs[0,1].plot(namesArray,t2_vec,'o',color='grey')
    axs[0,1].set_title(r'(b) $\Delta{t}_{cool}$ [ms]')   
    axs[0,1].plot(namesArray[np.abs(t2_vec-t2_vec.max()).argmin()],t2_vec.max(),'o',color='blue')
    axs[0,1].plot(namesArray[np.abs(t2_vec-t2_vec.min()).argmin()],t2_vec.min(),'o',color='blue')
    #axs[0,1].plot(colArray[np.abs(t2_vec-DTcool(reference)).argmin()],DTcool(reference),"o",color='red')
    axs[0,1].axhline(y=DTcool(reference)*1e3,color='red',linestyle='--')
    # axs[0,1].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    # axs[0,1].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[0,1].set_xlim(xlimits)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(namesArray)):  errorBar(axs[1,0],namesArray[i],tCQ_vec[i],d_tCQ_vec[i]*tCQ_vec[i],colour='grey')
    axs[1,0].plot(namesArray,tCQ_vec,'o',color='grey')
    axs[1,0].set_title(r'(c) $\tau_{CQ}^{lin}$ (long-CQ) [ms]')   
    axs[1,0].plot(namesArray[np.abs(tCQ_vec-tCQ_vec.max()).argmin()],tCQ_vec.max(),'o',color='blue')
    axs[1,0].plot(namesArray[np.abs(tCQ_vec-tCQ_vec.min()).argmin()],tCQ_vec.min(),'o',color='blue')
    #axs[1,0].plot(colArray[np.abs(lQ_vec-lambdaMHD_rough(reference)*1e3).argmin()],lambdaMHD_rough(reference)*1e3,"o",color='red')
    axs[1,0].axhline(y=tauCQlinmin(reference,longCQ=1)*1e3,color='red',linestyle='--')
    # axs[1,0].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    # axs[1,0].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[1,0].set_xlim(xlimits)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(colArray)): 
        axs[1,1].plot([namesArray[i],namesArray[i]],[lEich[i],lQ_vec[i]],color='grey',linewidth=0.3)
    axs[1,1].plot(namesArray,(lQ_vec+lEich)/2,'o',color='grey')
    axs[1,1].set_title(r'(d) $\lambda_{q}$ [mm]')   
    axs[1,1].plot(namesArray[np.abs((lQ_vec+lEich)/2-(lQ_vec.max()+lEich.max())/2).argmin()],(lQ_vec.max()+lEich.max())/2,'o',color='blue')
    axs[1,1].plot(namesArray[np.abs((lQ_vec+lEich)/2-(lQ_vec.min()+lEich.min())/2).argmin()],(lQ_vec.min()+lEich.min())/2,'o',color='blue')
    #axs[1,0].plot(colArray[np.abs(lQ_vec-lambdaMHD_rough(reference)*1e3).argmin()],lambdaMHD_rough(reference)*1e3,"o",color='red')
    axs[1,1].axhline(y=( lambdaMHD(reference,model='HD',MHD_turbulence_on=False) + lambdaMHD(reference,model='Eich',MHD_turbulence_on=False) )*5e2,
                     color='red',linestyle='--')
    # axs[1,1].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    # axs[1,1].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[1,1].set_xlim(xlimits)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(colArray)): errorBar(axs[2,0],namesArray[i],Wpol_vec[i],d_Wpol_vec[i]*Wpol_vec[i],colour='grey')
    axs[2,0].plot(namesArray,Wpol_vec,'o',color='grey')
    #axs[2,0].set_title(r'$W_{pol,vv} = 1.1 \times W_{pol}$ [MW]',fontsize=12)   
    axs[2,0].set_title(r'(e) $W_{pol,vv} = 1.1 \times W_{pol}$ [MJ]',fontsize=12)   
    axs[2,0].plot(namesArray[np.abs(Wpol_vec-Wpol_vec.max()).argmin()],Wpol_vec.max(),'o',color='blue')
    axs[2,0].plot(namesArray[np.abs(Wpol_vec-Wpol_vec.min()).argmin()],Wpol_vec.min(),'o',color='blue')
    # axs[1,1].plot(colArray[np.abs(Wpol_vec-Wth(reference)*1e-6).argmin()],Wth(reference)*1e-6,"o",color='red')
    axs[2,0].axhline( y=Wpol(reference,li3_betap="li3")/1e6 ,  color='red' , linestyle='--')
    # axs[2,0].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    # axs[2,0].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[2,0].set_xlim(xlimits)

    #-----------------------------------------------------------------------------------------------------------------------------------------

    for i in range(len(colArray)): errorBar(axs[2,1],namesArray[i],Wth_vec[i],d_Wth_vec[i]*Wth_vec[i],colour='grey')
    axs[2,1].plot(namesArray,Wth_vec,'o',color='grey')
    axs[2,1].set_title(r'(f) $W_{th}$ [MJ]',fontsize=12)   
    axs[2,1].plot(namesArray[np.abs(Wth_vec-Wth_vec.max()).argmin()],Wth_vec.max(),'o',color='blue')
    axs[2,1].plot(namesArray[np.abs(Wth_vec-Wth_vec.min()).argmin()],Wth_vec.min(),'o',color='blue')
    # axs[1,1].plot(colArray[np.abs(Wpol_vec-Wth(reference)*1e-6).argmin()],Wth(reference)*1e-6,"o",color='red')
    axs[2,1].axhline( y=reference["Wth"]/1e6 ,  color='red' , linestyle='--')
    # axs[2,1].axvspan(xlimits[1]-3,xlimits[1]-1,color='yellow',alpha=0.3)
    # axs[2,1].axvspan(xlimits[1]-1,xlimits[1],color='green',alpha=0.3)
    axs[2,1].set_xlim(xlimits)

    plt.subplots_adjust(hspace=0.5)
    #plt.tight_layout()
    plt.show()

def Melt1plot(scenario,SPR="SPR-69/B",PF_TQ=0,PF_CQ=0,material="W",cooling=1,Ndiv=2,rescale_a=1.1,CQ_lin_exp=1):
    """
    Produces the plot showing ratio of the incoming conducted & radiated loads during TQ and CQ to the critical melting value, for the various
    disruption types considered in the study.

    Requires that you have already called the function "Predictions" on the same scenario

        Input:
          - scenario:   name of a python library-type scenario
          - SPR:        string type input corresponding to the scenario name (goes in the title of the figure) 
          - PF_TQ:      0 --> not considering peaking factors;   1 --> considering peaking factors                      (default: 0)
          - PF_CQ:      0 --> not considering peaking factors;   1 --> considering peaking factors                      (default: 0)
          - material:   "W" --> Tungsten;                       "Be" --> Beryllium                                      (default: "W")
          - cooling:    0 --> no active cooling of walls;        1 --> cooling: divertor (20 MW/m2), other (10 MW/m2)   (default: 1)
          - Ndiv:       Number of divertors expected to take the loads of MD cases.                                     (default: 2)
          - rescale_a:  Nominal position of the conductive structure on which the magnetic energy couples               (default: 1.1)
          - CQ_lin_exp: Wave form of Ip drop used for the calculation of W_coupled
                            0 --> linear            1 --> exponential                                                   (default: 1)
    """
    Twall = 500 + 273.15
    T0con = np.ones(8) * Twall
    T0rad = np.ones(8) * Twall
    q_cool_div = 20e6
    q_cool_lim = 10e6
    q_cool_con = q_cool_lim*np.ones(8)
    q_cool_rad = q_cool_lim*np.ones(8)
    for i in (0,1,6): 
        T0con[i] += 500
        q_cool_con[i] = q_cool_div

    if cooling == 0:
        q_cool_con *= 0
        q_cool_rad *= 0

    qcritTQ1 = qmelt(time=scenario["tauTQ1"] , material=material , T0=T0con)
    qcritTQ2 = qmelt(time=scenario["tauTQ2"] , material=material , T0=T0con)
    qcritTQr = qmelt(time=scenario["tauTQ1"]+scenario["tauTQ2"] , material=material , T0=T0rad)
    qcritCQ  = qmelt(time=scenario["tauCQ"]  , material=material , T0=T0con)
    qcritCQr = qmelt(time=scenario["tauCQ"]  , material=material , T0=T0rad)

    Sdiv = scenario["S_div"]
    S_FW = scenario["S_FW"]
    Scp = scenario["S_cp"]

    disruptions = ["MD\nlikely","MD\nstrong","cold VDE\nfast CQ","cold VDE\nslow CQ","hot VDE\nfast CQ","hot VDE\nslow CQ","MD\nmitig.","VDE\nmitig."]
    # Swet_cond   = [ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    # Swet_rad    = [ Sdiv, Sdiv, S_FW, S_FW, S_FW, S_FW, Sdiv, S_FW ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]

    W_PFC(scenarioName=scenario,phase="TQ",peakingFactors=PF_TQ,Ndiv=Ndiv)
    W_PFC(scenarioName=scenario,phase="CQ",peakingFactors=PF_CQ,Ndiv=Ndiv,rescale_a=rescale_a,CQ_lin_exp=CQ_lin_exp)

    Swet_cond_1  = scenario["S_wet_cond_TQ1"] #[ Sdiv , Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_cond_2  = scenario["S_wet_cond_TQ2"] #[ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_cond_CQ = scenario["S_wet_cond_CQ"] #[ Sdiv , Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]

    q_net_con1 = [ max( (scenario["WTQ_con1"][i]/(scenario["tauTQ1"][i]*Swet_cond_1[i]) - q_cool_con[i]) , 0.0 ) for i in range(8) ]
    q_net_con2 = [ max( (scenario["WTQ_con2"][i]/(scenario["tauTQ2"][i]*Swet_cond_2[i]) - q_cool_con[i]) , 0.0 ) for i in range(8) ]
    q_net_radTQ= [ max( (scenario["WTQ_rad"][i]/((scenario["tauTQ1"][i]+scenario["tauTQ2"][i])*Swet_rad[i])-q_cool_rad[i]) , 0.0 ) for i in range(8) ]

    q_net_conCQ= [ max( (scenario["WCQ_con"][i]/(scenario["tauCQ"][i]*Swet_cond_CQ[i]) - q_cool_con[i]) , 0.0 ) for i in range(8) ]
    q_net_radCQ= [ max( (scenario["WCQ_rad"][i]/(scenario["tauCQ"][i]*Swet_rad[i]    ) - q_cool_rad[i]) , 0.0 ) for i in range(8) ]

    fig, axs = plt.subplots(1, 2, figsize=(15,5.5))

    fig.suptitle("Melting limit for tungsten ("+SPR+")",fontsize=18)

    ylimits = (1e-3,1e2)
    def grey_shade():
        return Rectangle(
            (5.5,1),                  # bottom-left corner: (x_min, y_min)
            width=2,
            height=ylimits[1] - 1,
            facecolor="grey",
            edgecolor="none",
            alpha=0.2,
            zorder=0
        )
    def cyan_shade():
        return Rectangle(
            (5.5,ylimits[0]),          # bottom-left corner: (x_min, y_min)
            width=2,
            height=1 - ylimits[0],
            facecolor="cyan",
            edgecolor="none",
            alpha=0.1,
            zorder=0
        )
    axs[0].semilogy(disruptions, q_net_con1 / qcritTQ1 , color='red'     , linewidth=1 ) # , label="rise phase" )
    axs[0].semilogy(disruptions, q_net_con2 / qcritTQ2 , color='red'     , linewidth=1 , linestyle='--' ) # , label="fall phase" )
    axs[0].semilogy(disruptions, q_net_radTQ/ qcritTQr , color='blue'    , linewidth=1 )
    axs[0].semilogy(disruptions, q_net_con1 / qcritTQ1 , 'o'             , color='red'  , label="conducted" )
    axs[0].semilogy(disruptions, q_net_con2 / qcritTQ2 , 'o'             , color='red' )
    axs[0].semilogy(disruptions, q_net_radTQ/ qcritTQr , 'o'             , color='blue' , label="radiated"  )
    limits = axs[0].get_xlim()
    axs[0].semilogy([-1,10]    ,   np.ones(2)          , color='black', linestyle=':' )
    axs[0].set_ylim(ylimits)
    axs[0].set_xlim(limits)
    axs[0].set_title("Thermal Quench",fontsize=16)
    axs[0].set_ylabel(r"$q_{wall}$ / $q_{melt}$",fontsize=16)
    axs[0].axhspan(1e0,1e10,color='black',alpha=0.1 , label="wall melting" )
    axs[0].axhspan(1e-10,1e0,color='cyan',alpha=0.1 , label="not melting" )
    axs[0].add_patch(grey_shade())
    axs[0].add_patch(cyan_shade())
    axs[0].text(0,1.5,"melting",color='black',fontsize=12)
    axs[0].text(0,5e-1,"not melting",color='black',fontsize=12)
    # axs[0].text(6.7,35,"ramp\ndown",color='red',fontsize=10)
    # axs[0].text(6.3,2e5,"ramp\nup",color='red',fontsize=10)
    axs[0].semilogy([0,0.5],[450e-5,450e-5],color='red')
    axs[0].semilogy([0,0.5],[150e-5,150e-5],color='red',linestyle='--')
    axs[0].text(0.7,450e-5,"slow TQ phase",color='red',fontsize=10)
    axs[0].text(0.7,150e-5,"fast TQ phase",color='red',fontsize=10)
    VS = 0
    for i in range(8):
        if scenario["isVSactive_con1"][i]:
            axs[0].semilogy(disruptions[i], 
                            scenario["WTQ_con1"][i]/(scenario["tauTQ1"][i]*Swet_cond_1[i]) / qcritTQ1[i] , 
                            'x'       , color='red' , ms=10 )
            VS += 1
        if scenario["isVSactive_con2"][i]:
            axs[0].semilogy(disruptions[i], 
                            scenario["WTQ_con2"][i]/(scenario["tauTQ2"][i]*Swet_cond_2[i]) / qcritTQ2[i] , 
                            'x'       , color='red' , ms=10 )
            VS += 1
    if VS > 0: 
        axs[0].semilogy(100,1e20,'rx',label="Vapour shielding active")
            

    axs[1].semilogy(disruptions, q_net_conCQ / qcritCQ , color='red'  , linewidth=1   )
    axs[1].semilogy(disruptions, q_net_radCQ / qcritCQr, color='blue' , linewidth=1   )
    axs[1].semilogy(disruptions, q_net_conCQ / qcritCQ , 'o'          , color='red'   , label="conducted" )
    axs[1].semilogy(disruptions, q_net_radCQ / qcritCQr, 'o'          , color='blue'  , label="radiated"  )
    axs[1].semilogy([-1,10]    , np.ones(2)            , color='black', linestyle=':' )
    axs[1].set_ylim(ylimits)
    axs[1].set_xlim(limits)
    axs[1].set_title("Current Quench",fontsize=16)
    axs[1].axhspan(1e0,1e10,color='black',alpha=0.1 , label="wall melting")
    axs[1].axhspan(1e-10,1e0,color='cyan',alpha=0.1 , label="not melting" )
    axs[1].text(0,1.5,"melting",color='black',fontsize=12)
    axs[1].text(0,5e-1,"not melting",color='black',fontsize=12)
    #axs[1].set_ylabel(r"$q_{wall} / q_{melt}$")
    axs[1].add_patch(grey_shade())
    axs[1].add_patch(cyan_shade())
    for i in range(8):
        if scenario["isVSactive_CQ"][i]:
            axs[1].semilogy(disruptions[i], 
                            scenario["WCQ_con"][i]/(scenario["tauCQ"][i]*Swet_cond_1[i]) / qcritCQ[i] , 
                            'x'       , color='red' , ms=10 )
    axs[1].semilogy( 0 , 0 ,'x', color='red' , ms=10 , label="Vapour Shielding active")
    axs[1].legend(loc='lower left',fontsize=12)

    plt.show()

def Melt2plot(scenario,SPR="SPR-69/B",PF_TQ=0,PF_CQ=0,cooling=0):
    """
    Produces the plot showing surface temperature increases during TQ and CQ, owing to conduction and radiation, for the various
    disruption types considered in the study.

    Requires that you have already called the function "Predictions" on the same scenario

        Input:
          - scenario:   name of a python library-type scenario
          - SPR:        string type input corresponding to the scenario name (goes in the title of the figure)  
          - PF_TQ:      0 --> not considering peaking factors;      1 --> considering peaking factors      (default: 0)
          - PF_CQ:      0 --> not considering peaking factors;      1 --> considering peaking factors      (default: 0)
          - cooling:    0 --> not considering active wall cooling;  1 --> considering active wall cooling  (default: 0)
    """
    q_cool_div = 20e6
    q_cool_lim = 5e6
    q_cool_PFC = 5e6

    q_cool_con = np.array([q_cool_div , q_cool_div , q_cool_lim , q_cool_lim , q_cool_lim , q_cool_lim , q_cool_div , q_cool_lim])
    q_cool_rad = np.ones(8) * q_cool_PFC 

    if cooling == 0:
        q_cool_rad = np.zeros(8)
        q_cool_con = np.zeros(8)

    T0_div = 1000 + 273.15
    T0_lim = 500 + 273.15
    T0_PFC = 500 + 273.15

    T0_con = np.array([T0_div , T0_div , T0_lim , T0_lim , T0_lim , T0_lim , T0_div , T0_lim])
    T0_rad = np.ones(8) * T0_PFC

    Tmelt = 3695 # [K]
    Tvap  = 6203 # [K]

    Sdiv = scenario["S_div"]
    S_FW = scenario["S_FW"]
    Scp = scenario["S_cp"]

    disruptions = ["MD\nlikely","MD\nstrong","cold VDE\nfast CQ","cold VDE\nslow CQ","hot VDE\nfast CQ","hot VDE\nslow CQ","MD\nmitig.","VDE\nmitig."]
    # Swet_rad    = [ Sdiv, Sdiv, S_FW, S_FW, S_FW, S_FW, Sdiv, S_FW ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]

    TTQcon1 = np.zeros(8)
    TTQcon2 = np.zeros(8)
    TTQrad  = np.zeros(8)
    TCQcon  = np.zeros(8)
    TCQrad  = np.zeros(8)

    W_PFC(scenarioName=scenario,phase="TQ",peakingFactors=PF_TQ)
    W_PFC(scenarioName=scenario,phase="CQ",peakingFactors=PF_CQ)

    Swet_cond_1  = scenario["S_wet_cond_TQ1"] #[ Sdiv , Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_cond_2  = scenario["S_wet_cond_TQ2"] #[ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_cond_CQ = scenario["S_wet_cond_CQ"] #[ Sdiv , Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]

    t_TQ1 = scenario["tauTQ1"]
    t_TQ2 = scenario["tauTQ2"]
    t_TQ3 = scenario["tauTQ1"]+scenario["tauTQ2"]
    
    for jj in range(8):
        print(disruptions[jj])
        # TTQcon1[jj] = Tfinal( time=t_TQ1[jj] , 
        #                       q0=scenario["WTQ_con1"][jj]/(t_TQ1[jj]*Swet_cond_1[jj]) , 
        #                       Swet=Swet_cond_1[jj] , 
        #                       T0=T0_con[jj] , 
        #                       q_cooling=q_cool_con[jj] )      - T0_con[jj]
        # if (TTQcon1[jj] >= Tvap-T0_con[jj]): TTQcon1[jj] = Tvap-T0_con[jj]
        # if scenario["isVSactive_con1"][jj] == 1: TTQcon1[jj] = Tvap-T0_con[jj]   

        # TTQcon2[jj] = Tfinal( time=t_TQ2[jj] , 
        #                       q0=scenario["WTQ_con2"][jj]/(t_TQ2[jj]*Swet_cond_2[jj]) ,
        #                       Swet=Swet_cond_2[jj] , 
        #                       T0=TTQcon1[jj]+T0_con[jj] ,
        #                       q_cooling=q_cool_con[jj] ) - (TTQcon1[jj]-T0_con[jj])
        # if (TTQcon2[jj] >= Tvap-T0_con[jj]): TTQcon2[jj] = Tvap-T0_con[jj]
        # if scenario["isVSactive_con2"][jj] == 1: TTQcon2[jj] = Tvap-T0_con[jj]

        # TTQrad[jj] = Tfinal( time=t_TQ3[jj] , 
        #                      q0=scenario["WTQ_rad"][jj]/(t_TQ3[jj]*Swet_rad[jj]) , 
        #                      Swet=Swet_rad[jj] , 
        #                      T0=T0_rad[jj] ,
        #                      q_cooling=q_cool_rad[jj] ) - T0_rad[jj]
        # if (TTQrad[jj] >= Tvap-T0_rad[jj]): TTQrad[jj] = Tvap-T0_rad[jj]

        # TCQcon[jj] = Tfinal( time=scenario["tauCQ"][jj] , 
        #                      q0=scenario["WCQ_con"][jj]/(scenario["tauCQ"][jj]*Swet_cond_CQ[jj]) , 
        #                      Swet=Swet_cond_CQ[jj] , 
        #                      T0=T0_con[jj] ,
        #                      q_cooling=q_cool_con[jj] ) - T0_con[jj]
        # if (TCQcon[jj] >= Tvap-T0_con[jj]): TCQcon[jj] = Tvap-T0_con[jj]
        # if scenario["isVSactive_CQ"][jj] == 1: TCQcon[jj] = Tvap - T0_con[jj]

        # TCQrad[jj] = Tfinal( time=scenario["tauCQ"][jj] , 
        #                      q0=scenario["WCQ_rad"][jj]/(scenario["tauCQ"][jj]*Swet_rad[jj]) , 
        #                      Swet=Swet_rad[jj] , 
        #                      T0=T0_rad[jj] ,
        #                      q_cooling=q_cool_rad[jj] ) - T0_rad[jj]
        # if (TCQrad[jj] >= Tvap-T0_rad[jj]): TCQrad[jj] = Tvap-T0_rad[jj]
        TTQcon1[jj] = Tfinal( time=t_TQ1[jj] , 
                              q0=scenario["WTQ_con1"][jj]/(t_TQ1[jj]*Swet_cond_1[jj]) , 
                              Swet=Swet_cond_1[jj] , 
                              T0=T0_con[jj] , 
                              q_cooling=q_cool_con[jj] )    
        if (TTQcon1[jj] >= Tvap): TTQcon1[jj] = Tvap
        if scenario["isVSactive_con1"][jj] == 1: TTQcon1[jj] = Tvap   

        TTQcon2[jj] = Tfinal( time=t_TQ2[jj] , 
                              q0=scenario["WTQ_con2"][jj]/(t_TQ2[jj]*Swet_cond_2[jj]) ,
                              Swet=Swet_cond_2[jj] , 
                              T0=TTQcon1[jj]+T0_con[jj] ,
                              q_cooling=q_cool_con[jj] )
        if (TTQcon2[jj] >= Tvap): TTQcon2[jj] = Tvap
        if scenario["isVSactive_con2"][jj] == 1: TTQcon2[jj] = Tvap

        TTQrad[jj] = Tfinal( time=t_TQ3[jj] , 
                             q0=scenario["WTQ_rad"][jj]/(t_TQ3[jj]*Swet_rad[jj]) , 
                             Swet=Swet_rad[jj] , 
                             T0=T0_rad[jj] ,
                             q_cooling=q_cool_rad[jj] ) 
        if (TTQrad[jj] >= Tvap): TTQrad[jj] = Tvap

        TCQcon[jj] = Tfinal( time=scenario["tauCQ"][jj] , 
                             q0=scenario["WCQ_con"][jj]/(scenario["tauCQ"][jj]*Swet_cond_CQ[jj]) , 
                             Swet=Swet_cond_CQ[jj] , 
                             T0=T0_con[jj] ,
                             q_cooling=q_cool_con[jj] )
        if (TCQcon[jj] >= Tvap): TCQcon[jj] = Tvap
        if scenario["isVSactive_CQ"][jj] == 1: TCQcon[jj] = Tvap

        TCQrad[jj] = Tfinal( time=scenario["tauCQ"][jj] , 
                             q0=scenario["WCQ_rad"][jj]/(scenario["tauCQ"][jj]*Swet_rad[jj]) , 
                             Swet=Swet_rad[jj] , 
                             T0=T0_rad[jj] ,
                             q_cooling=q_cool_rad[jj] ) 
        if (TCQrad[jj] >= Tvap): TCQrad[jj] = Tvap

        
    fig, axs = plt.subplots(1, 2, figsize=(15,5.5))

    fig.suptitle("Tungsten wall temperature raise ("+SPR+")",fontsize=18)

    T0 = 0
    ylimits = (3e0,3e4)
    red_shade = Rectangle(
        (5.5,Tvap-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=ylimits[1] - Tvap+T0,
        facecolor="red",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    orange_shade = Rectangle(
        (5.5,Tmelt-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tvap - Tmelt,
        facecolor="orange",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    blue_shade = Rectangle(
        (5.5,ylimits[0]),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tmelt-T0 - ylimits[0],
        facecolor="cyan",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    axs[0].semilogy(disruptions,   TTQcon1   , color='red'  , linewidth=1 )# , label="rise phase" )
    axs[0].semilogy(disruptions,   TTQcon2   , color='red'  , linewidth=1 , linestyle='--' ) # , label="fall phase" )
    axs[0].semilogy(disruptions[0:8],   TTQrad[0:8]    , color='blue' , linewidth=1 )
    axs[0].semilogy(disruptions,   TTQcon1   , 'o'          , color='red'  , label="conducted" )
    axs[0].semilogy(disruptions,   TTQcon2   , 'o'          , color='red' )
    axs[0].semilogy(disruptions,   TTQrad    , 'o'          , color='blue' , label="radiated"  )
    limits = axs[0].get_xlim()
    axs[0].semilogy([-1,10]    ,   np.ones(2)*Tmelt-T0      , color='black', linestyle=':' )
    axs[0].semilogy([-1,10]    ,   np.ones(2)*Tvap-T0       , color='black', linestyle=':' )
    axs[0].set_ylim(ylimits)
    axs[0].set_xlim(limits)
    axs[0].set_title("Thermal Quench",fontsize=16)
    axs[0].set_ylabel(r"$\Delta T_{wall}$ / $k_B$ [K]",fontsize=16)
    axs[0].axhspan(Tvap-T0 , 1e10 , color='red'   ,alpha=0.1 , label="vaporised wall" )
    axs[0].axhspan(Tmelt-T0, Tvap-T0 , color='orange',alpha=0.1 , label="molten wall" )
    axs[0].axhspan(0    , Tmelt-T0, color='cyan'  ,alpha=0.1 , label="solid wall" )
    axs[0].semilogy([6,6.5],[25e0,25e0],color='red')
    axs[0].semilogy([6,6.5],[8e0,8e0],color='red',linestyle='--')
    axs[0].text(6.7,5e0,"rise\nphase",color='red',fontsize=10)
    axs[0].text(6.7,18e0,"fall\nphase",color='red',fontsize=10)
    axs[0].add_patch(red_shade)
    axs[0].add_patch(orange_shade)
    axs[0].add_patch(blue_shade)

    red_shade = Rectangle(
        (5.5,Tvap-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=ylimits[1] - Tvap,
        facecolor="red",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    orange_shade = Rectangle(
        (5.5,Tmelt-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tvap - Tmelt,
        facecolor="orange",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    blue_shade = Rectangle(
        (5.5,ylimits[0]),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tmelt-T0 - ylimits[0],
        facecolor="cyan",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    axs[1].semilogy(disruptions,   TCQcon   , color='red'  , linewidth=1   )
    axs[1].semilogy(disruptions,   TCQrad   , color='blue' , linewidth=1   )
    axs[1].semilogy(disruptions,   TCQcon   , 'o'          , color='red'   , label="conducted" )
    axs[1].semilogy(disruptions,   TCQrad   , 'o'          , color='blue'  , label="radiated" )
    axs[1].semilogy([-1,10]    ,   np.ones(2)*(Tmelt-T0)        , color='black', linestyle=':' )
    axs[1].semilogy([-1,10]    ,   np.ones(2)*(Tvap-T0)         , color='black', linestyle=':' )
    axs[1].text(-.1,(Tmelt-T0)*0.65,"melting point",color='black',fontsize=12)
    axs[1].text(-.1,(Tvap-T0) *1.20,"vapour point",color='black',fontsize=12)
    axs[1].set_ylim(ylimits)
    axs[1].set_xlim(limits)
    axs[1].set_title("Current Quench",fontsize=16)
    axs[1].axhspan(Tvap-T0 , 1e10    , color='red'   , alpha=0.1 , label="vaporised wall" )
    axs[1].axhspan(Tmelt-T0, Tvap-T0 , color='orange', alpha=0.1 , label="molten wall" )
    axs[1].axhspan(0    , Tmelt-T0   , color='cyan'  , alpha=0.1 , label="solid wall" )
    axs[1].add_patch(red_shade)
    axs[1].add_patch(orange_shade)
    axs[1].add_patch(blue_shade)
    axs[0].legend(loc='lower left',fontsize=12)

    plt.show()

    return TCQrad  

def Melt3plot(scenario,SPR="SPR-69/B",PF_TQ=0,PF_CQ=0,cooling=0):
    """
    Produces the plot showing surface final temperature during TQ and CQ, owing to conduction and radiation, for the various
    disruption types considered in the study.

    Requires that you have already called the function "Predictions" or "W_PFC" on the same scenario

        Input:
          - scenario:   name of a python library-type scenario
          - SPR:        string type input corresponding to the scenario name (goes in the title of the figure)  
          - PF_TQ:      0 --> not considering peaking factors;      1 --> considering peaking factors      (default: 0)
          - PF_CQ:      0 --> not considering peaking factors;      1 --> considering peaking factors      (default: 0)
          - cooling:    0 --> not considering active wall cooling;  1 --> considering active wall cooling  (default: 0)
    """
    q_cool_div = 20e6 # [MW/m2]
    q_cool_lim = 5e6  # [MW/m2]
    q_cool_PFC = 5e6  # [MW/m2]

    q_cool_con = np.array([q_cool_div , q_cool_div , q_cool_lim , q_cool_lim , q_cool_lim , q_cool_lim , q_cool_div , q_cool_lim])
    q_cool_rad = np.ones(8) * q_cool_PFC 

    if cooling == 0:
        q_cool_rad = np.zeros(8)
        q_cool_con = np.zeros(8)

    T0_div = 1000 + 273.15 # [K]
    T0_lim = 500 + 273.15  # [K]
    T0_PFC = 500 + 273.15  # [K]

    T0_con = np.array([T0_div , T0_div , T0_lim , T0_lim , T0_lim , T0_lim , T0_div , T0_lim])
    T0_rad = np.ones(8) * T0_PFC

    Tmelt = 3695 # [K]
    Tvap  = 6203 # [K]

    Sdiv = scenario["S_div"]
    S_FW = scenario["S_FW"]
    Scp = scenario["S_cp"]

    disruptions = ["MD\nlikely","MD\nstrong","cold VDE\nfast CQ","cold VDE\nslow CQ","hot VDE\nfast CQ","hot VDE\nslow CQ","MD\nmitig.","VDE\nmitig."]
    # Swet_rad    = [ Sdiv, Sdiv, S_FW, S_FW, S_FW, S_FW, Sdiv, S_FW ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]

    TTQcon1         = np.zeros(8)
    TTQcon2         = np.zeros(8)
    TTQcon_1step    = np.zeros(8)
    TTQcon1_baffle      = np.ones(8) * T0_PFC
    TTQcon2_baffle      = np.ones(8) * T0_PFC
    TTQcon_1step_baffle = np.ones(8) * T0_PFC
    TTQrad          = T0_rad
    TTQrad_1step    = T0_rad
    TCQcon  = np.zeros(8)
    TCQrad  = np.zeros(8)

    W_PFC(scenarioName=scenario,phase="TQ",peakingFactors=PF_TQ,Ndiv=2)
    W_PFC(scenarioName=scenario,phase="CQ",peakingFactors=PF_CQ,Ndiv=2,rescale_a=1.1,CQ_lin_exp=1)

    Swet_cond_1  = scenario["S_wet_cond_TQ1"] #[ Sdiv , Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_cond_2  = scenario["S_wet_cond_TQ2"] #[ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_cond_CQ = scenario["S_wet_cond_CQ"] #[ Sdiv , Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]

    t_TQ1 = scenario["tauTQ1"]
    t_TQ2 = scenario["tauTQ2"]
    t_TQ3 = scenario["tauTQ1"]+scenario["tauTQ2"]
    
    for jj in range(8):
        print(disruptions[jj])
        #conducted loads: two-steps TQ
        TTQcon1[jj] = Tfinal( time=t_TQ1[jj] , 
                              q0=scenario["WTQ_con1"][jj]/(t_TQ1[jj]*Swet_cond_1[jj]) , 
                              Swet=Swet_cond_1[jj] , 
                              T0=T0_con[jj] , 
                              q_cooling=q_cool_con[jj] )    
        if (TTQcon1[jj] >= Tvap): TTQcon1[jj] = Tvap
        if scenario["isVSactive_con1"][jj] == 1: TTQcon1[jj] = Tvap   

        TTQcon2[jj] = Tfinal( time=t_TQ2[jj] , 
                              q0=scenario["WTQ_con2"][jj]/(t_TQ2[jj]*Swet_cond_2[jj]) ,
                              Swet=Swet_cond_2[jj] , 
                              T0=TTQcon1[jj] ,
                              q_cooling=q_cool_con[jj] )
        if (TTQcon2[jj] >= Tvap): TTQcon2[jj] = Tvap
        if scenario["isVSactive_con2"][jj] == 1: TTQcon2[jj] = Tvap

        # conducted loads: single-steps TQ
        TTQcon_1step[jj] = Tfinal( time=t_TQ3[jj] , 
                              q0=scenario["WTQ_1step_con"][jj]/(t_TQ3[jj]*Swet_cond_2[jj]) ,
                              Swet=Swet_cond_2[jj] , 
                              T0=T0_con[jj] ,
                              q_cooling=q_cool_con[jj] )
        if (TTQcon_1step[jj] >= Tvap): TTQcon_1step[jj] = Tvap
        if scenario["isVSactive_1step"][jj] == 1: TTQcon_1step[jj] = Tvap

        # radiated loads: double-step TQ
        TTQrad[jj] = Tfinal( time=t_TQ3[jj] , 
                             q0=scenario["WTQ_rad"][jj]/(t_TQ3[jj]*Swet_rad[jj]) , 
                             Swet=Swet_rad[jj] , 
                             T0=T0_rad[jj] ,
                             q_cooling=q_cool_rad[jj] ) 
        if (TTQrad[jj] >= Tvap): TTQrad[jj] = Tvap

        # radiated loads: single-step TQ
        TTQrad_1step[jj] = Tfinal( time=t_TQ3[jj] , 
                             q0=scenario["WTQ_1step_rad"][jj]/(t_TQ3[jj]*Swet_rad[jj]) , 
                             Swet=Swet_rad[jj] , 
                             T0=T0_rad[jj] ,
                             q_cooling=q_cool_rad[jj] ) 
        if (TTQrad_1step[jj] >= Tvap): TTQrad_1step[jj] = Tvap

        # conducted loads: CQ
        TCQcon[jj] = Tfinal( time=scenario["tauCQ"][jj] , 
                             q0=scenario["WCQ_con"][jj]/(scenario["tauCQ"][jj]*Swet_cond_CQ[jj]) , 
                             Swet=Swet_cond_CQ[jj] , 
                             T0=T0_con[jj] ,
                             q_cooling=q_cool_con[jj] )
        if (TCQcon[jj] >= Tvap): TCQcon[jj] = Tvap
        if scenario["isVSactive_CQ"][jj] == 1: TCQcon[jj] = Tvap

        # radiated loads: CQ
        TCQrad[jj] = Tfinal( time=scenario["tauCQ"][jj] , 
                             q0=scenario["WCQ_rad"][jj]/(scenario["tauCQ"][jj]*Swet_rad[jj]) , 
                             Swet=Swet_rad[jj] , 
                             T0=T0_rad[jj] ,
                             q_cooling=q_cool_rad[jj] ) 
        if (TCQrad[jj] >= Tvap): TCQrad[jj] = Tvap

        
    fig, axs = plt.subplots(1, 2, figsize=(15,5.5))

    fig.suptitle("Temperature on tungsten wall ("+SPR+")",fontsize=18)

    T0 = 0
    ylimits = (1e2,1e4)
    red_shade = Rectangle(
        (5.5,Tvap-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=ylimits[1] - Tvap+T0,
        facecolor="red",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    orange_shade = Rectangle(
        (5.5,Tmelt-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tvap - Tmelt,
        facecolor="orange",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    blue_shade = Rectangle(
        (5.5,ylimits[0]),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tmelt-T0 - ylimits[0],
        facecolor="cyan",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    axs[0].semilogy(disruptions,   TTQcon2      , color='red'  , linewidth=1 )# , label="rise phase" )
    axs[0].semilogy(disruptions,   TTQcon_1step , color='red'  , linewidth=1 , linestyle='--' ) # , label="fall phase" )
    axs[0].semilogy(disruptions,   TTQrad       , color='blue' , linewidth=1 )
    axs[0].semilogy(disruptions,   TTQrad_1step , color='blue' , linewidth=1 , linestyle='--' )
    axs[0].semilogy(disruptions,   TTQcon2      , 'o'          , color='red' , label="conducted" )
    axs[0].semilogy(disruptions,   TTQcon_1step , 'o'          , color='red' )
    axs[0].semilogy(disruptions,   TTQrad       , 'o'          , color='blue' , label="radiated"  )
    axs[0].semilogy(disruptions,   TTQrad_1step , 'o'          , color='blue' )
    limits = axs[0].get_xlim()
    axs[0].semilogy([-1,10]    ,   np.ones(2)*Tmelt-T0      , color='black', linestyle=':' )
    axs[0].semilogy([-1,10]    ,   np.ones(2)*Tvap-T0       , color='black', linestyle=':' )
    axs[0].set_ylim(ylimits)
    axs[0].set_xlim(limits)
    axs[0].set_title("Thermal Quench",fontsize=16)
    axs[0].set_ylabel(r"$T_{wall}$ / $k_B$ [K]",fontsize=16)
    axs[0].axhspan(Tvap-T0 , 1e10 , color='red'   ,alpha=0.1 , label="vaporised wall" )
    axs[0].axhspan(Tmelt-T0, Tvap-T0 , color='orange',alpha=0.1 , label="molten wall" )
    axs[0].axhspan(0    , Tmelt-T0, color='cyan'  ,alpha=0.1 , label="solid wall" )
    if (max(abs(TTQcon2-TTQcon_1step))>5) or (max(abs(TTQrad==TTQrad_1step))>5):
        axs[0].semilogy([6,6.5],np.ones(2)*ylimits[0]*3,color='black')
        axs[0].semilogy([6,6.5],np.ones(2)*ylimits[0]*2,color='black',linestyle='--')
        axs[0].text(6.7,ylimits[0]*3,"2-step TQ",color='black',fontsize=10)
        axs[0].text(6.7,ylimits[0]*2,"1-step TQ",color='black',fontsize=10)
    axs[0].add_patch(red_shade)
    axs[0].add_patch(orange_shade)
    axs[0].add_patch(blue_shade)

    red_shade = Rectangle(
        (5.5,Tvap-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=ylimits[1] - Tvap,
        facecolor="red",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    orange_shade = Rectangle(
        (5.5,Tmelt-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tvap - Tmelt,
        facecolor="orange",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    blue_shade = Rectangle(
        (5.5,ylimits[0]),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tmelt-T0 - ylimits[0],
        facecolor="cyan",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    axs[1].semilogy(disruptions,   TCQcon   , color='red'  , linewidth=1   )
    limits = axs[1].get_xlim()
    axs[1].semilogy(disruptions,   TCQrad   , color='blue' , linewidth=1   )
    axs[1].semilogy(disruptions,   TCQcon   , 'o'          , color='red'   , label="conducted" )
    axs[1].semilogy(disruptions,   TCQrad   , 'o'          , color='blue'  , label="radiated" )
    axs[1].semilogy([-1,10]    ,   np.ones(2)*(Tmelt-T0)        , color='black', linestyle=':' )
    axs[1].semilogy([-1,10]    ,   np.ones(2)*(Tvap-T0)         , color='black', linestyle=':' )
    axs[1].text(-.1,(Tmelt-T0)*0.65,"melting point",color='black',fontsize=12)
    axs[1].text(-.1,(Tvap-T0) *1.20,"vapour point",color='black',fontsize=12)
    axs[1].set_ylim(ylimits)
    axs[1].set_xlim(limits)
    axs[1].set_title("Current Quench",fontsize=16)
    axs[1].axhspan(Tvap-T0 , 1e10    , color='red'   , alpha=0.1 , label="vaporised wall" )
    axs[1].axhspan(Tmelt-T0, Tvap-T0 , color='orange', alpha=0.1 , label="molten wall" )
    axs[1].axhspan(0    , Tmelt-T0   , color='cyan'  , alpha=0.1 , label="solid wall" )
    axs[1].add_patch(red_shade)
    axs[1].add_patch(orange_shade)
    axs[1].add_patch(blue_shade)
    axs[0].legend(loc='lower left',fontsize=12)

    plt.show()

def Melt4plot(scenario,SPR="SPR-69/B",PF_TQ=0,PF_CQ=0,cooling=0,Ndiv=2,rescale_a=1.1,CQ_lin_exp=1):
    """
    Produces the plot showing surface final temperature during TQ and CQ, owing to conduction and radiation, for the various
    disruption types considered in the study.

    Requires that you have already called the function "Predictions" or "W_PFC" on the same scenario

        Input:
          - scenario:   name of a python library-type scenario
          - SPR:        string type input corresponding to the scenario name (goes in the title of the figure)  
          - PF_TQ:      0 --> not considering peaking factors;      1 --> considering peaking factors      (default: 0)
          - PF_CQ:      0 --> not considering peaking factors;      1 --> considering peaking factors      (default: 0)
          - cooling:    0 --> not considering active wall cooling;  1 --> considering active wall cooling  (default: 0)
          - Ndiv:       Number of divertors expected to take the loads of MD cases.                        (default: 2)
          - rescale_a:  Nominal position of the conductive structure on which the magnetic energy couples  (default: 1.1)
          - CQ_lin_exp: Wave form of Ip drop used for the calculation of W_coupled
                            0 --> linear            1 --> exponential                                      (default: 1)
    """
    q_cool_div = 20e6 # [MW/m2]
    q_cool_lim = 10e6  # [MW/m2]
    q_cool_PFC = 10e6  # [MW/m2]

    q_cool_con = np.array([q_cool_div , q_cool_div , q_cool_lim , q_cool_lim , q_cool_lim , q_cool_lim , q_cool_div , q_cool_lim])
    q_cool_rad = np.ones(8) * q_cool_PFC 

    if cooling == 0:
        q_cool_rad = np.zeros(8)
        q_cool_con = np.zeros(8)

    T0_div = 1000 + 273.15 # [K]
    T0_lim = 500 + 273.15  # [K]
    T0_PFC = 500 + 273.15  # [K]

    T0_con = np.array([T0_div , T0_div , T0_lim , T0_lim , T0_lim , T0_lim , T0_div , T0_lim])
    T0_rad = np.ones(8) * T0_PFC

    Tmelt = 3695 # [K]
    Tvap  = 6203 # [K]

    Sbaffle = scenario["S_div"]
    S_FW    = scenario["S_FW"]
    Scp     = scenario["S_cp"]

    disruptions = ["MD\nlikely","MD\nstrong","cold VDE\nfast CQ","cold VDE\nslow CQ","hot VDE\nfast CQ","hot VDE\nslow CQ","MD\nmitig.","VDE\nmitig."]
    # Swet_rad    = [ Sdiv, Sdiv, S_FW, S_FW, S_FW, S_FW, Sdiv, S_FW ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]

    TTQcon1         = np.zeros(8)
    TTQcon2         = np.zeros(8)
    TTQcon_1step    = np.zeros(8)
    TTQcon1_baffle      = np.ones(8) * T0_PFC
    TTQcon2_baffle      = np.ones(8) * T0_PFC
    TTQcon_1step_baffle = np.ones(8) * T0_PFC
    TTQrad          = T0_rad.copy()
    TTQrad_1step    = T0_rad.copy()
    TCQcon  = np.zeros(8)
    TCQrad  = np.zeros(8)
    TCQcon_baffle       = np.ones(8) * T0_PFC

    # Erosion depths:
    dXTQ2con = np.zeros(8)
    dXTQ1con = np.zeros(8)
    dXTQbaffle = np.zeros(8)
    dXTQrad  = np.zeros(8)
    dXCQcon  = np.zeros(8)
    dXCQbaffle = np.zeros(8)
    dXCQrad  = np.zeros(8)

    W_PFC(scenarioName=scenario,phase="TQ",peakingFactors=PF_TQ,Ndiv=Ndiv)
    W_PFC(scenarioName=scenario,phase="CQ",peakingFactors=PF_CQ,Ndiv=Ndiv,rescale_a=rescale_a,CQ_lin_exp=CQ_lin_exp)


    Swet_cond_1  = scenario["S_wet_cond_TQ1"] #[ Sdiv , Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_cond_2  = scenario["S_wet_cond_TQ2"] #[ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_cond_CQ = scenario["S_wet_cond_CQ"] #[ Sdiv , Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]

    t_TQ1 = scenario["tauTQ1"]
    t_TQ2 = scenario["tauTQ2"]
    t_TQ3 = scenario["tauTQ1"]+scenario["tauTQ2"]
    
    for jj in range(8):
        print(disruptions[jj])
        print("  conducted loads: pre-TQ")
        if jj == 0:
            (temp1,dX) = Tfinal( time=scenario["tauPreTQ"][0] , 
                                    q0=(scenario["WpreTQ_con"][0])/(scenario["tauPreTQ"][0]*Swet_cond_2[0]) ,
                                    Swet=Swet_cond_2[0] , 
                                    T0=T0_con[0] ,
                                    q_cooling=q_cool_con[0] ,
                                    output_erosion=True )
            if (temp1 >= Tvap): temp1 = Tvap
            if scenario["isVSactive_PreTQ"][jj] == 1: temp1 = Tvap   
        else:
            temp1 = 0
            dX = 0
        print("  conducted loads: two-steps TQ")
        (TTQcon1[jj],dXTQ2con[jj]) = Tfinal( time=t_TQ1[jj] , 
                                            q0=scenario["WTQ_con1"][jj]/(t_TQ1[jj]*Swet_cond_1[jj]) , 
                                            Swet=Swet_cond_1[jj] , 
                                            T0=(temp1 if jj==0 else T0_con[jj]) , 
                                            q_cooling=q_cool_con[jj] ,
                                            output_erosion=True )    
        if (TTQcon1[jj] >= Tvap): TTQcon1[jj] = Tvap
        if scenario["isVSactive_con1"][jj] == 1: TTQcon1[jj] = Tvap   

        dXTQ2con[jj] += dX
        dX = 0

        (TTQcon2[jj],dX) = Tfinal( time=t_TQ2[jj] , 
                                    q0=scenario["WTQ_con2"][jj]/(t_TQ2[jj]*Swet_cond_2[jj]) ,
                                    Swet=Swet_cond_2[jj] , 
                                    T0=TTQcon1[jj] ,
                                    q_cooling=q_cool_con[jj] ,
                                    output_erosion=True )
        if (TTQcon2[jj] >= Tvap): TTQcon2[jj] = Tvap
        if scenario["isVSactive_con2"][jj] == 1: TTQcon2[jj] = Tvap

        dXTQ2con[jj] += dX

        print("  conducted loads: single-steps TQ")
        (TTQcon_1step[jj],dXTQ1con[jj]) = Tfinal( time=t_TQ3[jj] , 
                                                    q0=scenario["WTQ_1step_con"][jj]/(t_TQ3[jj]*Swet_cond_2[jj]) ,
                                                    Swet=Swet_cond_2[jj] , 
                                                    T0=T0_con[jj] ,
                                                    q_cooling=q_cool_con[jj] ,
                                                    output_erosion=True )
        if (TTQcon_1step[jj] >= Tvap): TTQcon_1step[jj] = Tvap
        if scenario["isVSactive_1step"][jj] == 1: TTQcon_1step[jj] = Tvap

        print("  radiated loads: double-step TQ")
        (TTQrad[jj],dXTQrad[jj]) = Tfinal( time=t_TQ3[jj] , 
                                            q0=scenario["WTQ_rad"][jj]/(t_TQ3[jj]*Swet_rad[jj]) , 
                                            Swet=Swet_rad[jj] , 
                                            T0=T0_rad[jj] ,
                                            q_cooling=q_cool_rad[jj] ,
                                            output_erosion=True ) 
        if (TTQrad[jj] >= Tvap): TTQrad[jj] = Tvap

        print("  radiated loads: single-step TQ")
        TTQrad_1step[jj] = Tfinal( time=t_TQ3[jj] , 
                             q0=scenario["WTQ_1step_rad"][jj]/(t_TQ3[jj]*Swet_rad[jj]) , 
                             Swet=Swet_rad[jj] , 
                             T0=T0_rad[jj] ,
                             q_cooling=q_cool_rad[jj] ) 
        if (TTQrad_1step[jj] >= Tvap): TTQrad_1step[jj] = Tvap

        if jj==0: T0_con[0] = T0_div 
        print("  conducted loads: CQ")
        (TCQcon[jj],dXCQcon[jj]) = Tfinal( time=scenario["tauCQ"][jj] , 
                                            q0=scenario["WCQ_con"][jj]/(scenario["tauCQ"][jj]*Swet_cond_CQ[jj]) , 
                                            Swet=Swet_cond_CQ[jj] , 
                                            T0=T0_con[jj] ,
                                            q_cooling=q_cool_con[jj] ,
                                            output_erosion=True )
        if (TCQcon[jj] >= Tvap): TCQcon[jj] = Tvap
        if scenario["isVSactive_CQ"][jj] == 1: TCQcon[jj] = Tvap

        print("  radiated loads: CQ")
        (TCQrad[jj],dXCQrad[jj]) = Tfinal( time=scenario["tauCQ"][jj] , 
                                            q0=scenario["WCQ_rad"][jj]/(scenario["tauCQ"][jj]*Swet_rad[jj]) , 
                                            Swet=Swet_rad[jj] , 
                                            T0=T0_rad[jj] ,
                                            q_cooling=q_cool_rad[jj] ,
                                            output_erosion=True ) 
        if (TCQrad[jj] >= Tvap): TCQrad[jj] = Tvap

        # BAFFLE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if jj in (0,1,6):
            if jj == 0:
                    print("  Baffle --> preTQ conducted loads")
                    (temp,dX) = Tfinal( time=scenario["tauPreTQ"][0] , 
                                                q0=(scenario["WpreTQ_con_baffle"][0])/(scenario["tauPreTQ"][0]*Swet_cond_2[0]) ,
                                                Swet=Swet_cond_2[0] , 
                                                T0=T0_con[0] ,
                                                q_cooling=q_cool_con[0] ,
                                                output_erosion=True )
                    if (temp >= Tvap): temp = Tvap
                    if scenario["isVSactive_PreTQ_baffle"][jj] == 1: temp = Tvap   
                    
            else:
                temp = 0
                dX   = 0
            print("  Baffle --> conducted loads: two-steps TQ")
            (TTQcon1_baffle[jj],dXTQbaffle[jj]) = Tfinal( time=t_TQ1[jj] , 
                                                            q0=scenario["WTQ_con1_baffle"][jj]/(t_TQ1[jj]*Sbaffle) , 
                                                            Swet=Sbaffle , 
                                                            T0=(T0_PFC if not jj==0 else temp) , 
                                                            q_cooling=q_cool_PFC ,
                                                            output_erosion=True )    
            if (TTQcon1_baffle[jj] >= Tvap): TTQcon1_baffle[jj] = Tvap
            if scenario["isVSactive_con1_baffle"][jj] == 1: TTQcon1_baffle[jj] = Tvap   

            dXTQbaffle[jj] += dX
            dX = 0

            (TTQcon2_baffle[jj],dX) = Tfinal( time=t_TQ2[jj] , 
                                                q0=scenario["WTQ_con2_baffle"][jj]/(t_TQ2[jj]*Sbaffle) , 
                                                Swet=Sbaffle , 
                                                T0=T0_PFC , 
                                                q_cooling=q_cool_PFC ,
                                                output_erosion=True )    
            if (TTQcon2_baffle[jj] >= Tvap): TTQcon2_baffle[jj] = Tvap
            if scenario["isVSactive_con2_baffle"][jj] == 1: TTQcon2_baffle[jj] = Tvap   

            dXTQbaffle[jj] += dX
            print("  Baffle --> conducted loads: single-steps TQ")
            TTQcon_1step_baffle[jj] = Tfinal( time=t_TQ3[jj] , 
                                              q0=scenario["WTQ_1step_con_baffle"][jj]/(t_TQ3[jj]*Sbaffle) ,
                                              Swet=Sbaffle , 
                                              T0=T0_PFC ,
                                              q_cooling=q_cool_PFC )
            if (TTQcon_1step_baffle[jj] >= Tvap): TTQcon_1step_baffle[jj] = Tvap
            if scenario["isVSactive_1step_baffle"][jj] == 1: TTQcon_1step_baffle[jj] = Tvap

            print("  Baffle --> CQ conducted loads")
            (TCQcon_baffle[jj],dXCQbaffle[jj]) = Tfinal( time=scenario["tauCQ"][jj] , 
                                                            q0=scenario["WCQ_con_baffle"][jj]/(scenario["tauCQ"][jj]*Sbaffle) , 
                                                            Swet=Sbaffle , 
                                                            T0=T0_PFC , 
                                                            q_cooling=q_cool_PFC ,
                                                            output_erosion=True )    
            if (TTQcon1_baffle[jj] >= Tvap): TTQcon1_baffle[jj] = Tvap
            if scenario["isVSactive_con1_baffle"][jj] == 1: TTQcon1_baffle[jj] = Tvap   

    # convert conducted loads to divertor and limiter loads
    TTQ_div_2step = np.array([TTQcon2[0],TTQcon2[1],T0_div,T0_div,T0_div,T0_div,TTQcon2[6],T0_div])
    TTQ_div_1step = np.array([TTQcon_1step[0],TTQcon_1step[1],T0_div,T0_div,T0_div,T0_div,TTQcon_1step[6],T0_div])
    TTQ_lim_2step = np.array([T0_lim,T0_lim,TTQcon2[2],TTQcon2[3],TTQcon2[4],TTQcon2[5],T0_lim,TTQcon2[7]])
    TTQ_lim_1step = np.array([T0_lim,T0_lim,TTQcon_1step[2],TTQcon_1step[3],TTQcon_1step[4],TTQcon_1step[5],T0_lim,TTQcon_1step[7]])

    TCQ_div       = np.array([TCQcon[0],TCQcon[1],T0_div,T0_div,T0_div,T0_div,TCQcon[6],T0_div])
    TCQ_lim       = np.array([T0_lim,T0_lim,TCQcon[2],TCQcon[3],TCQcon[4],TCQcon[5],T0_lim,TCQcon[7]])

    # Idem for the erosion depths
    dXTQ2div = np.array([dXTQ2con[0],dXTQ2con[1],0,0,0,0,dXTQ2con[6],0])
    dXTQ2lim = np.array([0,0,dXTQ2con[2],dXTQ2con[3],dXTQ2con[4],dXTQ2con[5],0,dXTQ2con[7]])

    dXCQdiv  = np.array([dXCQcon[0],dXCQcon[1],0,0,0,0,dXCQcon[6],0])
    dXCQlim  = np.array([0,0,dXCQcon[2],dXCQcon[3],dXCQcon[4],dXCQcon[5],0,dXCQcon[7]])

    # FIGURE 1 - TEMPERATURES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15,5.5))

    fig.suptitle("Temperature on tungsten wall ("+SPR+")",fontsize=18)

    T0 = 0
    ylimits = (8e1,1e4)
    red_shade = Rectangle(
        (5.5,Tvap-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=ylimits[1] - Tvap+T0,
        facecolor="red",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    orange_shade = Rectangle(
        (5.5,Tmelt-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tvap - Tmelt,
        facecolor="orange",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    blue_shade = Rectangle(
        (5.5,ylimits[0]),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tmelt-T0 - ylimits[0],
        facecolor="cyan",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    axs[0].semilogy(disruptions, TTQ_div_2step  , color='red'       , linewidth=1 )
    axs[0].semilogy(disruptions, TTQ_lim_2step  , color='orange'    , linewidth=1 ) 
    axs[0].semilogy(disruptions, TTQrad         , color='blue'      , linewidth=1 ) 
    axs[0].semilogy(disruptions, TTQcon2_baffle , color='limegreen' , linewidth=1 ) 
    axs[0].semilogy(disruptions, TTQ_div_2step  , 'o'               , color='red'       , label='divertor' )
    axs[0].semilogy(disruptions, TTQ_lim_2step  , 'o'               , color='orange'    , label='limiter'  ) 
    axs[0].semilogy(disruptions, TTQrad         , 'o'               , color='blue'      , label='I/O wall' ) 
    axs[0].semilogy(disruptions, TTQcon2_baffle , 'o'               , color='limegreen' , label='baffle'   ) 
    limits = axs[0].get_xlim()
    axs[0].semilogy([-1,10]    ,   np.ones(2)*Tmelt-T0      , color='black', linestyle=':' )
    axs[0].semilogy([-1,10]    ,   np.ones(2)*Tvap-T0       , color='black', linestyle=':' )
    axs[0].set_ylim(ylimits)
    axs[0].set_xlim(limits)
    axs[0].set_title("Thermal Quench",fontsize=16)
    axs[0].set_ylabel(r"$T_{wall}$ / $k_B$ [K]",fontsize=16)
    axs[0].axhspan(Tvap-T0 , 1e10 , color='red'   ,alpha=0.1 , label="vaporised wall" )
    axs[0].axhspan(Tmelt-T0, Tvap-T0 , color='orange',alpha=0.1 , label="molten wall" )
    axs[0].axhspan(0    , Tmelt-T0, color='cyan'  ,alpha=0.1 , label="solid wall" )
    if (max(abs(TTQcon2-TTQcon_1step))>5) or (max(abs(TTQrad==TTQrad_1step))>5):
        axs[0].semilogy(disruptions, TTQ_lim_1step  , color='orange'   , linewidth=1 , linestyle='--' )
        axs[0].semilogy(disruptions, TTQ_div_1step  , color='red'      , linewidth=1 , linestyle='--' )
        axs[0].semilogy(disruptions, TTQrad_1step   , color='blue'   , linewidth=1 , linestyle='--' )
        axs[0].semilogy(disruptions, TTQcon_1step_baffle  , color='limegreen'   , linewidth=1 , linestyle='--' )
        axs[0].semilogy(disruptions, TTQ_div_1step  , 'o'               , color='red'       )
        axs[0].semilogy(disruptions, TTQ_lim_1step  , 'o'               , color='orange'    ) 
        axs[0].semilogy(disruptions, TTQrad_1step   , 'o'               , color='blue'      ) 
        axs[0].semilogy(disruptions, TTQcon_1step_baffle , 'o'          , color='limegreen' ) 

        axs[0].semilogy([6,6.5],np.ones(2)*ylimits[0]*3,color='black')
        axs[0].semilogy([6,6.5],np.ones(2)*ylimits[0]*2,color='black',linestyle='--')
        axs[0].text(6.7,ylimits[0]*3,"2-step TQ",color='black',fontsize=10)
        axs[0].text(6.7,ylimits[0]*2,"1-step TQ",color='black',fontsize=10)
    axs[0].add_patch(red_shade)
    axs[0].add_patch(orange_shade)
    axs[0].add_patch(blue_shade)

    red_shade = Rectangle(
        (5.5,Tvap-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=ylimits[1] - Tvap,
        facecolor="red",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    orange_shade = Rectangle(
        (5.5,Tmelt-T0),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tvap - Tmelt,
        facecolor="orange",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    blue_shade = Rectangle(
        (5.5,ylimits[0]),          # bottom-left corner: (x_min, y_min)
        width=2,
        height=Tmelt-T0 - ylimits[0],
        facecolor="cyan",
        edgecolor="none",
        alpha=0.1,
        zorder=0
    )
    axs[1].semilogy(disruptions, TCQ_div        , color='red'       , linewidth=1 )
    axs[1].semilogy(disruptions, TCQ_lim        , color='orange'    , linewidth=1 ) 
    axs[1].semilogy(disruptions, TCQrad         , color='blue'      , linewidth=1 ) 
    axs[1].semilogy(disruptions, TCQcon_baffle  , color='limegreen' , linewidth=1 ) 
    axs[1].semilogy(disruptions, TCQ_div        , 'o'               , color='red'       , label='divertor' )
    axs[1].semilogy(disruptions, TCQ_lim        , 'o'               , color='orange'    , label='limiter'  ) 
    axs[1].semilogy(disruptions, TCQrad         , 'o'               , color='blue'      , label='I/O wall' ) 
    axs[1].semilogy(disruptions, TCQcon_baffle  , 'o'               , color='limegreen' , label='baffle'   ) 
    # axs[1].semilogy(disruptions,   TCQcon   , color='red'  , linewidth=1   )
    limits = axs[1].get_xlim()
    # axs[1].semilogy(disruptions,   TCQrad   , color='blue' , linewidth=1   )
    # axs[1].semilogy(disruptions,   TCQcon   , 'o'          , color='red'   , label="conducted" )
    # axs[1].semilogy(disruptions,   TCQrad   , 'o'          , color='blue'  , label="radiated" )
    axs[1].semilogy([-1,10]    ,   np.ones(2)*(Tmelt-T0)        , color='black', linestyle=':' )
    axs[1].semilogy([-1,10]    ,   np.ones(2)*(Tvap-T0)         , color='black', linestyle=':' )
    axs[1].text(-.1,(Tmelt-T0)*0.75,"melting point",color='black',fontsize=12)
    axs[1].text(-.1,(Tvap-T0) *1.13,"vapour point",color='black',fontsize=12)
    axs[1].set_ylim(ylimits)
    axs[1].set_xlim(limits)
    axs[1].set_title("Current Quench",fontsize=16)
    axs[1].axhspan(Tvap-T0 , 1e10    , color='red'   , alpha=0.1 , label="vaporised wall" )
    axs[1].axhspan(Tmelt-T0, Tvap-T0 , color='orange', alpha=0.1 , label="molten wall" )
    axs[1].axhspan(0    , Tmelt-T0   , color='cyan'  , alpha=0.1 , label="solid wall" )
    axs[1].add_patch(red_shade)
    axs[1].add_patch(orange_shade)
    axs[1].add_patch(blue_shade)
    axs[0].legend(loc='lower left',fontsize=12)

    # FIGURE 1 - EROSION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def shade(color,ylimits): 
        return Rectangle(
                            (5.5,ylimits[0]),          # bottom-left corner: (x_min, y_min)
                            width=2,
                            height=Tmelt-T0 - ylimits[0],
                            facecolor=color,
                            edgecolor="none",
                            alpha=0.1,
                            zorder=0
                        )

    if dXTQrad.max() + dXCQrad.max() > 0 :
        fig2, ax = plt.subplots(nrows=4, ncols=2, figsize=(15,5.5) , sharex='all')
    else:
        fig2, ax = plt.subplots(nrows=3, ncols=2, figsize=(15,4.6) , sharex='all')

    title2 = "Erosion depth in "+SPR 
    title2 = title2 + ', at peak loads location' if PF_CQ==1 else title2 + ', considering toroidal average loads'
    fig2.suptitle(title2,fontsize=18)
    for a in ax[0, :]: a.tick_params(labelbottom=False)
    for a in ax[1, :]: a.tick_params(labelbottom=False)
    if dXTQrad.max() + dXCQrad.max() > 0 : 
        for a in ax[3, :]: a.tick_params(axis='x', labelsize=9)
        for a in ax[2, :]: a.tick_params(labelbottom=False)
    
    ax[0,0].bar(disruptions,dXTQ2div*1e3,color='red')
    ax[0,0].set_title('Thermal Quench')
    ax[0,0].set_ylabel(r'$\delta x$ [mm]')
    ylim1 = ax[0,0].get_ylim()

    ax[0,1].bar(disruptions,dXCQdiv*1e3,color='red')
    ax[0,1].set_title('Current Quench')

    if ax[0,1].get_ylim()[1] < ylim1[1]: 
        ax[0,1].set_ylim(ylim1) 
    else: 
        ax[0,0].set_ylim(0,ax[0,1].get_ylim()[1]) 
    ylim1 = ax[0,0].get_ylim()
    ax[0,0].text(-.5,(ylim1[1]-ylim1[0])*0.8,'divertor')
    xlim = ax[0,0].get_xlim()
    ax[0,0].add_patch(shade('grey',ylim1))
    ax[0,1].add_patch(shade('grey',ylim1))
    ax[0,0].set_xlim(xlim)
    ax[0,1].set_xlim(xlim)

    ax[1,0].bar(disruptions,dXTQbaffle*1e3,color='limegreen')
    ax[1,0].set_ylabel(r'$\delta x$ [mm]')
    ylim2 = ax[1,0].get_ylim()
    ax[1,0].text(-.5,(ylim2[1]-ylim2[0])*0.8,'baffle')

    ax[1,1].bar(disruptions,dXCQbaffle*1e3,color='limegreen')
    ax[1,1].set_ylim(ylim2)
    ax[1,0].add_patch(shade('grey',ylim2))
    ax[1,1].add_patch(shade('grey',ylim2))
    ax[1,0].set_xlim(xlim)
    ax[1,1].set_xlim(xlim)

    ax[2,0].bar(disruptions,dXTQ2lim*1e3,color='orange')
    ax[2,0].set_ylabel(r'$\delta x$ [mm]')
    ylim3 = ax[2,0].get_ylim()

    ax[2,1].bar(disruptions,dXCQlim*1e3,color='orange')

    if ax[2,1].get_ylim()[1] < ylim3[1]: 
        ax[2,1].set_ylim(ylim3) 
    else: 
        ax[2,0].set_ylim(0,ax[2,1].get_ylim()[1]) 
    ylim3 = ax[2,0].get_ylim()
    ax[2,0].text(-.5,(ylim3[1]-ylim3[0])*0.8,'limiters')
    ax[2,0].add_patch(shade('grey',ylim3))
    ax[2,1].add_patch(shade('grey',ylim3))
    ax[2,0].set_xlim(xlim)
    ax[2,1].set_xlim(xlim)

    if dXTQrad.max() + dXCQrad.max() > 0 : 
        ax[3,0].bar(disruptions,dXTQrad*1e3,color='blue')
        ax[3,0].set_ylabel(r'$\delta x$ [mm]')
        ylim4 = ax[3,0].get_ylim()
        ax[3,0].text(-.5,(ylim4[1]-ylim4[0])*0.8+ylim4[0],'I/O wall')

        ax[3,1].bar(disruptions,dXCQrad*1e3,color='blue')
        ax[3,1].set_ylim(ylim4)
        ax[3,0].add_patch(shade('grey',ylim4))
        ax[3,1].add_patch(shade('grey',ylim4))
        ax[3,0].set_xlim(xlim)
        ax[3,1].set_xlim(xlim)


    plt.show()
