import sys
import numpy as np
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.cell import coordinate_to_tuple
from tempfile import TemporaryDirectory
import shutil
import os
import pandas as pd
from disruption_scenarios import *
from copy import deepcopy

pm = "±"
xx = "×"

def toSubscript(text):
    translation = str.maketrans({
        "0": "₀",
        "1": "₁",
        "2": "₂",
        "3": "₃",
        "4": "₄",
        "5": "₅",
        "6": "₆",
        "7": "₇",
        "8": "₈",
        "9": "₉",
        "a": "ₐ",
        "c": "꜀",
        "e": "ₑ",
        "h": "ₕ",
        "i": "ᵢ",
        "j": "ⱼ",
        "k": "ₖ",
        "l": "ₗ",
        "m": "ₘ",
        "n": "ₙ",
        "o": "ₒ",
        "p": "ₚ",
        "r": "ᵣ",
        "s": "ₛ",
        "t": "ₜ",
        "x": "ₓ",
    })

    return str(text).translate(translation)

def readFromXls(cc='D',scenarioLabel=None,filename="Inputs_template.xlsx"):
    """
    Builds a scenario dictionary, shaped ater SCENARIO, automatically reading the data from the local copy of the input file spreadsheed

        Input:
            - cc:            corresponding column on Francis's spreadsheet, according to Excel nomenclature: 'A','B'...'Z','AA','AB'
            - scenarioLabel: name of the dictionary containing the new scenario, if not specified it is read from the input file.

        Output:
            - scenarioOut:   new dictionary, shaped after SCENARIO, containing the new data reported on the input sreadsheet   
    """

    path = Path(filename).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    def read_excel_file():
        """
        Reads the workbook using the following sequence:

        1. Try reading the original file directly.
        2. Try copying the saved file to a temporary location.
        3. Ask the running Excel application to create a snapshot.

        The aim of this passage is that the input file is still readable even if kept open.
        """

        # First attempt: read the original workbook normally.
        try:
            return pd.read_excel(path, engine="openpyxl")

        except (PermissionError, OSError):
            pass

        with TemporaryDirectory() as temporary_directory:
            temporary_path = (
                Path(temporary_directory)
                / f"{path.stem}_snapshot{path.suffix}"
            )

            # Second attempt: copy the last saved version of the workbook.
            try:
                shutil.copy2(path, temporary_path)

            except (PermissionError, OSError):
                # Third attempt: ask Excel to create the copy.
                try:
                    import win32com.client
                except ImportError as error:
                    raise PermissionError(
                        f"The workbook is locked by Excel:\n{path}\n\n"
                        "Install pywin32 to read a snapshot of an open workbook:\n"
                        "    pip install pywin32"
                    ) from error

                try:
                    excel = win32com.client.GetActiveObject(
                        "Excel.Application"
                    )
                except Exception as error:
                    raise PermissionError(
                        f"The workbook is locked, but no running Excel "
                        f"application could be accessed:\n{path}"
                    ) from error

                workbook = None

                # Look for the requested file among the workbooks open in Excel.
                for candidate in excel.Workbooks:
                    candidate_path = Path(candidate.FullName).resolve()

                    if os.path.normcase(str(candidate_path)) == os.path.normcase(
                        str(path)
                    ):
                        workbook = candidate
                        break

                if workbook is None:
                    raise PermissionError(
                        f"The workbook could not be read directly and was not "
                        f"found in the detected Excel instance:\n{path}"
                    )

                # SaveCopyAs creates a snapshot without closing or renaming
                # the workbook that the user currently has open.
                workbook.SaveCopyAs(str(temporary_path))

            # Read either the filesystem copy or the Excel-created snapshot.
            return pd.read_excel(
                temporary_path,
                engine="openpyxl"
            )

    file = read_excel_file()

    def col(colName):
        """
        Converts an Excel column name to a zero-based pandas column index.

        Examples:
            A  -> 0
            D  -> 3
            Z  -> 25
            AA -> 26
        """
        colName = colName.strip().upper()

        if not colName.isalpha():
            raise ValueError(
                f"Invalid Excel column name: {colName!r}"
            )

        column_number = 0

        for char in colName:
            column_number = (
                column_number * 26
                + ord(char)
                - ord('A')
                + 1
            )

        return column_number - 1

    def row(rowName):
        """
        Converts an Excel row number to a zero-based pandas row index.

        This assumes that the first spreadsheet row is used as the
        DataFrame header by pandas.
        """
        return rowName - 2

    # A shallow copy preserves the behaviour of your original function.
    scenarioOut = deepcopy(SCENARIO)

    if scenarioLabel is not None:
        scenarioOut["name"] = scenarioLabel
    else:
        scenarioOut["name"] = str(file.iloc[row(2), col(cc)])

    scenarioOut["R0"]     = file.iloc[row(3),  col(cc)]
    scenarioOut["a"]      = file.iloc[row(4),  col(cc)]
    scenarioOut["kappa"]  = file.iloc[row(5),  col(cc)]
    scenarioOut["delta"]  = file.iloc[row(6),  col(cc)]
    scenarioOut["Volume"] = file.iloc[row(7),  col(cc)]
    scenarioOut["Csect"]  = scenarioOut["Volume"] / (2.0 * np.pi * scenarioOut["R0"])
    scenarioOut["B0"]     = file.iloc[row(8),  col(cc)]
    scenarioOut["Ip"]     = file.iloc[row(9),  col(cc)] * 1e6
    scenarioOut["q95"]    = file.iloc[row(10), col(cc)]
    scenarioOut["li3"]    = file.iloc[row(11), col(cc)]
    scenarioOut["ne"]     = file.iloc[row(12), col(cc)] * 1e20
    scenarioOut["Tsep"]   = file.iloc[row(13), col(cc)] * 1e3
    scenarioOut["Tcore"]  = file.iloc[row(14), col(cc)] * 1e3
    scenarioOut["p_sep"]  = file.iloc[row(15), col(cc)] * 1e3
    scenarioOut["betap"]  = file.iloc[row(16), col(cc)]
    scenarioOut["P_SOL"]  = file.iloc[row(17), col(cc)] * 1e6
    scenarioOut["Psep"]   = file.iloc[row(18), col(cc)] * 1e6
    scenarioOut["Wth"]    = file.iloc[row(19), col(cc)] * 1e6
    scenarioOut["Mion"]   = file.iloc[row(20), col(cc)]
    scenarioOut["Zeff"]   = file.iloc[row(21), col(cc)]
    scenarioOut["tauW"]   = file.iloc[row(22), col(cc)]
    scenarioOut["S_FW"]   = file.iloc[row(23), col(cc)]
    scenarioOut["S_div"]  = file.iloc[row(24), col(cc)]
    scenarioOut["S_cp"]   = file.iloc[row(25), col(cc)]
    scenarioOut["WthCQ"]  = file.iloc[row(26), col(cc)]*1e6 

    return scenarioOut

def writeToXls(scenarioName, errors, filename=None, overwriteSheet=True):
    """
    Writes the entries of a scenario dictionary to an Excel workbook.

    Input:
      - scenarioName :   dictionary containing the calculated.
      - filename :       Path to the destination Excel workbook. If it does not exist, a new workbook is created.
      - overwriteSheet : bool
                            True   ->  removes existing content from the destination worksheet.
                            False  ->  preserves the existing worksheet content.

    Outputs
      - path:            Absolute path of the saved Excel workbook.
    """
    if filename == None:
        filename = scenarioName["name"] + "_output.xlsx"

    Sdiv = scenarioName["S_div"]
    S_FW = scenarioName["S_FW"]
    Scp = scenarioName["S_cp"]
    Swet_cond   = [ Sdiv, Sdiv, Scp,  Scp,  Scp,  Scp,  Sdiv, Scp  ]
    Swet_rad    = [ S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW, S_FW ]
    disruptions = ["MD likely","MD strong","cold VDE fast CQ","cold VDE slow CQ","hot VDE fast CQ","hot VDE slow CQ","Mitigated MD","Mitigated VDE"]

    ColumnNames_pTQ= ["Duration [s]"," ",                           "Conducted ","W "+toSubscript("th")+" [MJ]",
                      "Radiated ","W "+toSubscript("th")+" [MJ]",   "SOL ","width [mm]",    
                      "Radiation ","peak tor/pol"]

    ColumnNames_TQ = ["Rise time on ","target [ms]",                "Fall time on"," target [ms]", 
                      "Rise phase","tᵥₛ [ms]",                      "Fall phase","tᵥₛ [ms]",
                      "Conducted ","W "+toSubscript("loss")+" [MJ]","Radiated ","W "+toSubscript("loss")+" [MJ]",
                      "Conducted ","Wpꜰᴄ [MJ]",                     "Radiated ","Wpꜰᴄ [MJ]",
                      "SOL ","width [mm]",                          "Radiation ","peak tor/pol"]

    ColumnNames_CQ = ["Duration ","(linear) [ms]",                  "Time const. ","(exp.) [ms]",
                      "Conducted","tᵥₛ [ms]",                        "Conducted ","W "+toSubscript("loss")+" [MJ]",
                      "Coupled","W"+toSubscript("c")+" [MJ]",
                      "Radiated","W"+toSubscript("loss")+" [MJ]",   "Conducted ","Wpꜰᴄ [MJ]",
                      "Radiated ","Wpꜰᴄ [MJ]",                      "SOL width","[mm]",              
                      "TPF/HCF"," ",                                "Radiation peak"," tor/pol"]

    startCell="A1"

    path = Path(filename).expanduser().resolve()

    # Sheet 1. Results for the pre-TQ
    sheetName = "pre-TQ" 

    # Open the existing workbook or create a new one.
    if path.exists():
        workbook = load_workbook(path)
    else:
        workbook = Workbook()

        # Rename the initially created worksheet.
        worksheet = workbook.active
        worksheet.title = sheetName

    # Select or create the requested worksheet.
    if sheetName in workbook.sheetnames:
        worksheet = workbook[sheetName]

        if overwriteSheet:
            worksheet.delete_rows(1, worksheet.max_row)
    else:
        worksheet = workbook.create_sheet(title=sheetName)

    # Convert the starting cell, such as "D5", into row and column numbers.
    startRow, startColumn = coordinate_to_tuple(startCell)

    # Header styling.
    ShadedFill = PatternFill(
        fill_type="solid",
        fgColor="EEECE1"
    )

    MD_VDE_titleFont = Font(
        color="000000",
        bold=True
    )

    Scenario_titleFont = Font(
        color="FF0000",
        bold=True
    )

    WarningFont = Font(
        color="0000FF",
        bold=True
    )

    Numbers_Font = Font(
        color='FF0000'
    )

    Text_Font = Font(
        color='000000'
    )

    thinBorderTop = Border(
        left=Side(style="medium", color="B7B7B7"),
        right=Side(style="medium", color="B7B7B7"),
        top=Side(style="medium", color="B7B7B7"),
    )

    thinBorderBottom = Border(
        left=Side(style="medium", color="B7B7B7"),
        right=Side(style="medium", color="B7B7B7"),
        bottom=Side(style="medium", color="B7B7B7")
    )

    thinBorder = Border(
        left=Side(style="medium", color="B7B7B7"),
        right=Side(style="medium", color="B7B7B7"),
        top=Side(style="medium", color="B7B7B7"),
        bottom=Side(style="medium", color="B7B7B7")
    )

    borders = [thinBorderTop,thinBorderBottom]
    fonts   = [Numbers_Font,Text_Font]

    def printHeaders(columnTitles):
        # Write the table headers.
        TQ_CQ_Header = worksheet.cell(
            row=startRow,
            column=startColumn,
            value=scenarioName["name"]
        )

        ScenariosHeader = [ worksheet.cell(
            row=startRow,
            column=startColumn + i+1,
            value=disruptions[i]
        ) for i in range(len(disruptions)) ]

        TQ_CQ_Header.font=Scenario_titleFont
        TQ_CQ_Header.font=Scenario_titleFont
        for i in range(len(disruptions)): 
            ScenariosHeader[i].font=MD_VDE_titleFont
            ScenariosHeader[i].border=thinBorder

        Columns = [ worksheet.cell(
            row  = startRow + 1 + i,
            column= startColumn,
            value = columnTitles[i]
        ) for i in range(len(columnTitles)) ]

        for i in range(len(columnTitles)): 
            Columns[i].border=borders[i%2]

    # -------------------------------------------------------------------
    # Pre-TQ

    printHeaders(ColumnNames_pTQ)

    L = len(ColumnNames_pTQ)

    MDlikely = [ worksheet.cell(
        row = startRow + 1 + i,
        column= startColumn + 1,
        value=["{tpTQ:.2f}±16%".format(tpTQ=scenarioName["tauPreTQ"][0]), "τ"+toSubscript("e")+" L-mode", 
               scenarioName["Wth"]/2e6, "(0.5×Wₜₕ)", 
               0.00, " " , 
               "{Eich:.2f}/{Goldson:.2f}".format(Eich=lambdaEich(scenarioName)*1e3,Goldson=lambdaMHD(scenarioName)*1e3) , "Eich/HD", 
               "", ""][i]
    ) for i in range(L)]

    for i in range(L):  
        MDlikely[i].border=borders[i%2]
        MDlikely[i].font=fonts[i%2]

    blanks = [[ worksheet.cell(
        row = startRow + 1 + i,
        column= startColumn + 2 + j,
    ) for i in range(L)] for j in(0,3,4)]

    for j in range(3):
        for i in range(L):  
            blanks[j][i].border=borders[i%2]
            blanks[j][i].fill=ShadedFill

    VDEs = [[ worksheet.cell(
        row   = startRow + 1 + i,
        column= startColumn + 3 + j,
        value = [
            "Vertical",     "motion",
            scenarioName["Wth"]/2e6, "(0.5×Wₜₕ)", 
            0.00, " " , 
            "{Eich:.2f}/{Goldson:.2f}".format(Eich=lambdaEich(scenarioName)*1e3,Goldson=lambdaMHD(scenarioName)*1e3) , "Eich/HD", 
            " ", " "][i]
    ) for i in range(L)] for j in (0,1)]

    for j in (0,1):
        for i in range(L):  
            VDEs[j][i].border=borders[i%2]
            VDEs[j][i].font=fonts[i%2]
            if i == 1: VDEs[j][i].font=fonts[0] 

    Mitigated = [[ worksheet.cell(
        row = startRow + 1 + i,
        column= startColumn + 7 + j,
        value=["{tpTQ:.2f}±30%".format(tpTQ=scenarioName["tauPreTQ"][7]), "(0.6 a q"+toSubscript("95")+")", 
               0.00, " " , 
               scenarioName["Wth"]/5e6, "(0.2×Wₜₕ)", 
               "{Eich:.2f}/{Goldson:.2f}".format(Eich=lambdaEich(scenarioName)*1e3,Goldson=lambdaMHD(scenarioName)*1e3) , "Eich/HD", 
               "2.0/0.2", ""][i]
    ) for i in range(L)] for j in range(2)]

    for j in range(2):
        for i in range(L):  
            Mitigated[j][i].border=borders[i%2]
            Mitigated[j][i].font=fonts[i%2]

    WARNING = worksheet.cell(
        value  = "WARNING: OUTPUT FILE MUST BE CLOSED TO RUN AGAIN 0Dsrupt.",
        row    = startRow + 1,
        column = startColumn + 10
    )

    WARNING.font = WarningFont

    # -------------------------------------------------------------------
    # TQ
    C_cond  = [ 0.5 , 1.0 , 0.5 , 0.5 , 1.0 , 1.0 , 0.16, 0.16 ]
    C_rad   = [ 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.64, 0.64 ]

    # Select or create the requested worksheet.
    if "TQ" in workbook.sheetnames:
        worksheet = workbook["TQ"]
    else:
        worksheet = workbook.create_sheet(title="TQ")

    # Convert the starting cell, such as "D5", into row and column numbers.
    startRow, startColumn = coordinate_to_tuple(startCell)

    printHeaders(ColumnNames_TQ)

    TableTQ = [
        # Rise phase duration
        [worksheet.cell(
            row   = startRow + 1,
            column= startColumn + 1 + j,
            value = "{tauTQ:.2f}±{err:d}%".format(tauTQ=scenarioName["tauTQ"][j]*1e3,err=int(errors["tauTQ"][j]*100))
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 2,
            column= startColumn + 1 + j,
            value = "30% loss"
        ) for j in range(len(disruptions))],
        # Fall phase duration
        [worksheet.cell(
            row   = startRow + 3,
            column= startColumn + 1 + j,
            value = "{tauTQ:.2f}±{err}%".format(tauTQ=3*scenarioName["tauTQ"][j]*1e3,err=int(errors["tauTQ"][j]*1e2))
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 4,
            column= startColumn + 1 + j,
            value = "70% loss"
        ) for j in range(len(disruptions))],
        # VS activation threshold time - Rise phase
        [worksheet.cell(
            row   = startRow + 5,
            column= startColumn + 1 + j,
            value = "{tvs:.3f}".format(tvs=scenarioName["tvs_TQ_con1"][j]*1e3)
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 6,
            column= startColumn + 1 + j,
            value = ["No VS","VS active"][int(scenarioName["isVSactive_con2"][j])]
        ) for j in range(len(disruptions))],
        # VS activation threshold time - Fall phase
        [worksheet.cell(
            row   = startRow + 7,
            column= startColumn + 1 + j,
            value = "{tvs:.3f}".format(tvs=scenarioName["tvs_TQ_con2"][j]*1e3)
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 8,
            column= startColumn + 1 + j,
            value = ["No VS","VS active"][int(scenarioName["isVSactive_con2"][j])]
        ) for j in range(len(disruptions))],
        # Conducted W_loss from plasma 
        [worksheet.cell(
            row   = startRow + 9,
            column= startColumn + 1 + j,
            value = "{Wth:.3f}".format(Wth=scenarioName["Wth"]*1e-6*C_cond[j])
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 10,
            column= startColumn + 1 + j,
            value = "({C:.2f}×Wₜₕ)".format(C=C_cond[j])
        ) for j in range(len(disruptions))],
        # Radiated W_loss from plasma 
        [worksheet.cell(
            row   = startRow + 11,
            column= startColumn + 1 + j,
            value = "{Wth:.1f}".format(Wth=scenarioName["Wth"]*1e-6*C_rad[j])
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 12,
            column= startColumn + 1 + j,
            value = "({C:.2f}×Wₜₕ)".format(C=C_rad[j])
        ) for j in range(len(disruptions))],
        # Conducted W_PFC deposited on walls
        [worksheet.cell(
            row   = startRow + 13,
            column= startColumn + 1 + j,
            value = "{Wc:.1f}".format(Wc=(scenarioName["WTQ_con1"][j]+scenarioName["WTQ_con2"][j])*1e-6)
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 14,
            column= startColumn + 1 + j,
            value =  ["(finite λq)","VS effect"][int(scenarioName["isVSactive_con1"][j])]
        ) for j in range(len(disruptions))],
        # Radiated W_PFC deposited on walls
        [worksheet.cell(
            row   = startRow + 15,
            column= startColumn + 1 + j,
            value = "{Wth:.1f}".format(Wth=scenarioName["WTQ_rad"][j]*1e-6)
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 16,
            column= startColumn + 1 + j,
            value = ["({C:.2f}×Wₜₕ)".format(C=C_rad[j]),"VS effect"][int(scenarioName["isVSactive_con1"][j])]
        ) for j in range(len(disruptions))],
        # SOL width
        [worksheet.cell(
            row   = startRow + 17,
            column= startColumn + 1 + j,
            value = "{Eich:.2f}/{Gold:.2f}".format(Eich=scenarioName["lamEich"]*1e3,Gold=scenarioName["lamGoldston"]*1e3)
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 18,
            column= startColumn + 1 + j,
            value = "Eich/HD"
        ) for j in range(len(disruptions))],
        # Radiation Peaking
        [worksheet.cell(
            row   = startRow + 19,
            column= startColumn + 1 + j,
            value = "2.0/0.2"
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 20,
            column= startColumn + 1 + j,
            value = " "
        ) for j in range(len(disruptions))],
        ]

    for j in range(len(disruptions)):
        for i in (8,9,10,11):
            TableTQ[i][j].fill=ShadedFill
        for i in range(len(TableTQ)):
            TableTQ[i][j].border=borders[i%2]
            TableTQ[i][j].font=fonts[i%2]
        
    WARNING = worksheet.cell(
        value  = "WARNING: OUTPUT FILE MUST BE CLOSED TO RUN AGAIN 0Dsrupt.",
        row    = startRow + 1,
        column = startColumn + 10
    )

    WARNING.font = WarningFont

    # -------------------------------------------------------------------
    # CQ
    C_cond  = [ 1.0 , 1.0 , 1.0 , 0.7 , 1.0 , 0.7 , 0.2 , 0.2  ]
    C_rad   = [ 0.0 , 0.0 , 0.0 , 0.3 , 0.0 , 0.3 , 0.8 , 0.8  ]
    Ctq     = [ 1.4 , 0.7 , 0.7 , 3.0 , 0.7 , 3.0 , 0.5 , 0.5  ]
    HCF     = [0.075, 0.075, 0.12, 0.2, 0.12, 0.2 , 0.05, 0.1  ]  
    TPF     = [ 2.0 , 2.0 , 2.0 , 2.0 , 2.0 , 2.0 , 1.0 , 1.0  ]   
    errorWCQ= ["±10%", "±10%", "±10%", "±22%", "±10%", "±22%", "±22%", "±22%"]         

    # Select or create the requested worksheet.
    if "CQ" in workbook.sheetnames:
        worksheet = workbook["CQ"]
    else:
        worksheet = workbook.create_sheet(title="CQ")

    # Convert the starting cell, such as "D5", into row and column numbers.
    startRow, startColumn = coordinate_to_tuple(startCell)

    printHeaders(ColumnNames_CQ)

    TableCQ = [
        # Duration (linear)
        [worksheet.cell(
            row   = startRow + 1,
            column= startColumn + 1 + j,
            value = "≤{tauCQ:.2f}±{err:d}%".format(tauCQ=scenarioName["tauCQ"][j]*1e3,err=int(errors["tauCQ"][j]*100))
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 2,
            column= startColumn + 1 + j,
            value = "{C:.1f}×Cₛₑ꜀L*".format(C=Ctq[j])
        ) for j in range(len(disruptions))],
        # Exponential tauCQ
        [worksheet.cell(
            row   = startRow + 3,
            column= startColumn + 1 + j,
            value = "≤{tauCQ:.2f}±{err:d}%".format(tauCQ=scenarioName["tauCQ"][j]*1e3*0.6/np.log(4),err=int(errors["tauCQ"][j]*100))
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 4,
            column= startColumn + 1 + j,
            value = "0.6 τ"+toSubscript("lin")+"/log4"
        ) for j in range(len(disruptions))],
        # VS activation threshold time - Fall phase
        [worksheet.cell(
            row   = startRow + 5,
            column= startColumn + 1 + j,
            value = "{tvs:.3f}".format(tvs=scenarioName["tvs_CQ_con"][j]*1e3)
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 6,
            column= startColumn + 1 + j,
            value = ["No VS","VS active"][int(scenarioName["isVSactive_CQ"][j])]
        ) for j in range(len(disruptions))],
        # Coupled magnetic energy W_coup
        [worksheet.cell(
            row   = startRow + 7,
            column= startColumn + 1 + j,
            value = "{Wc:.1f}±{err:d}%".format(Wc=scenarioName["WcoupCQ"][j]*1e-6*C_cond[j],err=int(errors["WcoupCQ"][j]*1e2))
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 8,
            column= startColumn + 1 + j,
            value = " "
        ) for j in range(len(disruptions))],
        # Conducted W_loss from plasma
        [worksheet.cell(
            row   = startRow + 9,
            column= startColumn + 1 + j,
            value = "{Wc:.1f}±{err:d}%".format(Wc=scenarioName["WlossCQ"][j]*1e-6*C_cond[j],err=int(errors["WlossCQ"][j]*1e2))
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 10,
            column= startColumn + 1 + j,
            value = "{C:.1f}(Wₚ-W꜀)".format(C=C_cond[j])
        ) for j in range(len(disruptions))],
        # Radiated W_loss from plasma
        [worksheet.cell(
            row   = startRow + 11,
            column= startColumn + 1 + j,
            value = "{Wc:.1f}".format(Wc=scenarioName["WlossCQ"][j]*1e-6*C_rad[j])+errorWCQ[j]
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 12,
            column= startColumn + 1 + j,
            value = "{C:.1f}(Wₚ-W꜀)".format(C=C_rad[j])
        ) for j in range(len(disruptions))],
        # Conducted W_PFC from plasma 
        [worksheet.cell(
            row   = startRow + 13,
            column= startColumn + 1 + j,
            value = "{Wc:.1f}".format(Wc=scenarioName["WCQ_con"][j]*1e-6) + [errorWCQ[j] , "±30%"][int(scenarioName["isVSactive_CQ"][j])]
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 14,
            column= startColumn + 1 + j,
            value = [" ", "VS effect"][int(scenarioName["isVSactive_CQ"][j])]
        ) for j in range(len(disruptions))],
        # Radiated W_PFC from plasma 
        [worksheet.cell(
            row   = startRow + 15,
            column= startColumn + 1 + j,
            value = "{Wr:.1f}".format(Wr=scenarioName["WCQ_rad"][j]*1e-6) + errorWCQ[j]
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 16,
            column= startColumn + 1 + j,
            value = [" ", "VS effect"][int(scenarioName["isVSactive_CQ"][j])]
        ) for j in range(len(disruptions))],
        # SOL width
        [worksheet.cell(
            row   = startRow + 17,
            column= startColumn + 1 + j,
            value = "{Eich:.2f}/{Gold:.2f}".format(Eich=scenarioName["lamEich"]*1e3,Gold=scenarioName["lamGoldston"]*1e3)
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 18,
            column= startColumn + 1 + j,
            value = "Eich/HD"
        ) for j in range(len(disruptions))],
        # TPF & HCF
        [worksheet.cell(
            row   = startRow + 19,
            column= startColumn + 1 + j,
            value = "{TPF:.1f}/{HCF:.3f}".format(TPF=TPF[j], HCF=HCF[j])
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 20,
            column= startColumn + 1 + j,
            value = " "
        ) for j in range(len(disruptions))],
        # Radiation Peaking
        [worksheet.cell(
            row   = startRow + 21,
            column= startColumn + 1 + j,
            value = "2.0/0.2"
        ) for j in range(len(disruptions))],
        [worksheet.cell(
            row   = startRow + 22,
            column= startColumn + 1 + j,
            value = " "
        ) for j in range(len(disruptions))],
        ]

    for j in range(len(disruptions)):
        for i in (6,7,8,9,10,11):
            TableCQ[i][j].fill=ShadedFill
        for i in range(len(TableCQ)):
            TableCQ[i][j].border=borders[i%2]
            TableCQ[i][j].font=fonts[i%2]
        
    WARNING = worksheet.cell(
        value  = "WARNING: OUTPUT FILE MUST BE CLOSED TO RUN AGAIN 0Dsrupt.",
        row    = startRow + 1,
        column = startColumn + 10
    )

    WARNING.font = WarningFont

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SAVE OUTPUT FILE
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    try:
        workbook.save(path)
    except PermissionError as error:
        raise PermissionError(
            f"Could not save the workbook:\n{path}\n\n"
            "The destination workbook may currently be open in Excel. "
            "Close it and run the function again, or save the output "
            "to a different filename."
        ) from error
    finally:
        workbook.close()

    return str(path)

