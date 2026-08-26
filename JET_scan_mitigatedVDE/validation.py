import sys
from pathlib import Path

path = (Path(__file__).resolve()).parent

sys.path.append('..')
from disruption_scenarios import *
from InputOutput import readFromXls, writeToXls

def validation(scenario) :

    tau_cool   = DTcool(scenarioName=scenario) + tauTQ(scenarioName=scenario)
    tau_CQ_min = tauCQlinmin(scenarioName=scenario,mitigatedVDE=1)
    tau_CQ_ave = tauCQlinmin(scenarioName=scenario,mitigatedVDE=1,longCQ=1)
    qcrit_Be   = qmelt(tauTQ(scenarioName=scenario),material="Be")
    qcrit_W    = qmelt(tauTQ(scenarioName=scenario),material="W")
    qcrit_Be_CQ= qmelt(tau_CQ_ave,material="Be")
    qcrit_W_CQ = qmelt(tau_CQ_ave,material="W")

    scenario["tauCQ"] = tau_CQ_ave
    scenario["WthCQ"] = Wpol(scenarioName=scenario)
    scenario["WcoupCQ"] = Wcoupled(scenarioName=scenario,lin_exp=0)*np.ones(8)
    scenario["WlossCQ"] = scenario["WthCQ"] - scenario["WcoupCQ"]

    Wrad       = scenario["Wth"] * (0.2 + 0.8**2) + scenario["WlossCQ"][0]*0.8

    errors     = RMSE(scenario)

    d_Wrad     = errors["WlossCQ"][0] #((0.1 * Wpol(scenarioName=scenario))**2 + (0.3 * Wcoupled(scenarioName=scenario,lin_exp=0))**2)**0.5 * 0.8

    print("________________________________________________________________")
    print("SCENARIO:         ",scenario["name"])
    print("________________________________________________________________")
    print("Ip [MA]:          {I:6.1f}".format(I=scenario["Ip"]/1e6))
    print("tau[preTQ]+tau1:  {t:10.5f}    [min,max]=[{min:8.5f}, {max:8.5f}]".format(t=tau_cool,   min=0.7*tau_cool,   max=1.3*tau_cool))
    print("tau[CQ] min.:     {t:10.5f}    [min,max]=[{min:8.5f}, {max:8.5f}]".format(t=tau_CQ_min, min=0.7*tau_CQ_min, max=1.3*tau_CQ_min))
    print("tau[CQ] long:     {t:10.5f}    [min,max]=[{min:8.5f}, {max:8.5f}]".format(t=tau_CQ_ave, min=0.7*tau_CQ_ave, max=1.3*tau_CQ_ave))
    # print("Wrad [MJ]:        {W:10.5f}    [min,max]=[{min:8.5f}, {max:8.5f}]".format(W=Wrad/1e6,   min=0.78e-6*Wrad,   max=1.22e-6*Wrad))
    print("Wrad [MJ]:        {W:10.5f}    [min,max]=[{min:8.5f}, {max:8.5f}]".format(W=Wrad/1e6,   
                                                                                     min=float((1-d_Wrad)*1e-6*Wrad),   
                                                                                     max=float((1+d_Wrad)*1e-6*Wrad)))
    print("qmelt TQ [MW/m2]: {q:10.5f}    with Berillium (walls)".format(q=qcrit_Be/1e6))
    print("qmelt TQ [MW/m2]: {q:10.5f}    with Tungsten (divertor)".format(q=qcrit_W/1e6))
    print("qmelt CQ [MW/m2]: {q:10.5f}    with Berillium (walls)".format(q=qcrit_Be_CQ/1e6))
    print("qmelt CQ [MW/m2]: {q:10.5f}    with Tungsten (divertor)".format(q=qcrit_W_CQ/1e6))
    print("---------------------------------------------------------------")
    print("W_TQ conduct. [MJ] ",scenario["Wth"]*0.8*0.2e-6)
    print("tauTQ [ms]:        ",tauTQ(scenario)*1e3)
    print("S_limiter [m2] ~   ",scenario["S_cp"])
    print("q_plasma [MW/m2]   ",0.2*0.8*scenario["Wth"]/(scenario["S_cp"]*tauTQ(scenario))/1e6)
    print("---------------------------------------------------------------")
    print("W_CQ conduct. [MJ] ",(Wpol(scenarioName=scenario)-Wcoupled(scenarioName=scenario,lin_exp=1))*0.2e-6)
    print("tauCQ [ms]:        ",tau_CQ_ave*1e3)
    print("S_limiter [m2] ~   ",scenario["S_cp"])
    print("q_plasma [MW/m2]   ",(Wpol(scenarioName=scenario)-Wcoupled(scenarioName=scenario,lin_exp=1))*0.2/(scenario["S_cp"]*tau_CQ_ave)/1e6)
    print("---------------------------------------------------------------")
    print("W_TQ rad [MJ]      ",scenario["Wth"] * 0.8**2 / 1e6)
    print("tauCQ [ms]:        ",tauTQ(scenario)*1e3)
    print("S_PFC [m2] ~       ",scenario["S_FW"])
    print("q_plasma [MW/m2]   ",scenario["Wth"] * 0.8**2/(scenario["S_FW"]*tauTQ(scenario))/1e6)
    print("---------------------------------------------------------------")
    print("W_CQ rad [MJ]      ",(Wpol(scenarioName=scenario)-Wcoupled(scenarioName=scenario,lin_exp=1))*0.8e-6)
    print("tauCQ [ms]:        ",tau_CQ_ave*1e3)
    print("S_PFC [m2] ~       ",scenario["S_FW"])
    print("q_plasma [MW/m2]   ",(Wpol(scenarioName=scenario)-Wcoupled(scenarioName=scenario,lin_exp=1))*0.8/(scenario["S_FW"]*tau_CQ_ave)/1e6)
    print(" ")

if __name__ == "__main__":
    JET_30e2kA = readFromXls(filename=str(path / "Inputs_JET.xlsx"),cc='D')
    JET_12e2kA = readFromXls(filename=str(path / "Inputs_JET.xlsx"),cc='E')
    JET_25e2kA = readFromXls(filename=str(path / "Inputs_JET.xlsx"),cc='F')

    validation(JET_30e2kA)
    validation(JET_12e2kA)
    validation(JET_25e2kA)


