import sys
from pathlib import Path

path = (Path(__file__).resolve()).parent

sys.path.append('..')
from disruption_scenarios import *
from InputOutput import readFromXls, writeToXls

if __name__ == "__main__":
    column = 'D' #SPR-68A
    column = 'E' #SPR-68B
    column = 'F' #SPR-69A
    column = 'G' #SPR-69B
    column = 'H' #SPR-70
    SCENARIO = readFromXls(filename=str(path / "Inputs_SPR-68A.xlsx"),cc='D')

    Predictions(SCENARIO)

    writeToXls(scenarioName=SCENARIO)