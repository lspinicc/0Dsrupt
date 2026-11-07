<img width="490" height="325" alt="image" src="https://github.com/user-attachments/assets/f1c43ed8-5eb4-48ef-bcda-8def62504e0c" />


0Dsrupt is a 0-dimensional code for the computation of heat loads on walls during a disruption.

A publication is underway, containing a detailed description of its physical model, along with a validation against JET data and a showcase of its capabilities.
For the time being, please refer to the Pinboard version:
https://pinboard.euro-fusion.org/repository/pinboard/EFDA-JET/journal/126629_manuscript_soft2026_externaluse.pdf 

The code needs to be downloaded on a device with a Python compiler and install the requirements from "Requirements.md".

1) Make a copy of the TemplateRun directory and open it
2) Fill in the "Inputs_template.xlsx" file with the flat-top quantities of the plasma equilibrium whose possible disruptions you intend to study.
3) Open "run.py" and choose what you want 0Dsrupt to do. 
4) Run 0Dsrupt opening a terminal in the directory and simply typing "python run.py" (or a python interactive / ipython terminal and launch "run run").

Every run.py file must contain at least one between:
1) Predictions()  -->  runs the model across the three phases (pre-TQ, TQ, CQ) of all eight disruption types
2) W_PFC()        -->  runs the model through the one phase specified when calling it, either for all disruption types or just for one.
                           (if you use W_PFC instead of Predictions, you need to call it once for each phase of the disruption)

At the moment there are 3 possible outcomes of one run of 0Dsrupt (not mutually exclusive):
1) writeToXls()   -->  writes a detailed output in the form of a new Excel file.
                             WARNING: if you run it multiple times, you need to close the output file while the 0Dsrupt is running!
2) Melt1plot()    -->  plots the conducted and radiated heat fluxes, normalised to the tungsten-wall-melting critical heat flux
                             (if q/q_melt > 1, some part of the wall is melting. If marked with an "X", it is vaporising).
3) Melt4plot()    -->  plots the final temperature and erosion depth of four PFCs (divertor strike points, baffles, limiters, inboard/outboard wall)
                             at the end of TQ and of CQ. TQ plots include melting & temperature rise of pre-TQ phase when this phase is present and when
                             an estimate of its duration is available within the 0Dsrupt model (mitigated disruptions and "likely MD" types)
