import glob as gb
import os
import warnings
import pandas as pd
import xlwings as xw # Xlwings is a Python library that makes it easy to call Python from Excel
import numpy as np

warnings.filterwarnings("ignore")

def get_conditionedAboveArea(sva_df):
    conditionedAbove_Area = 0
    sys = sva_df['SYSTEM_TYPE'].to_list()
    for i in range(0, len(sva_df['SYSTEM_TYPE'])):
        if(sys[i] != 'SUM'):
            conditionedAbove_Area = conditionedAbove_Area + sva_df['FLOOR_AREA'][i]
        # else:
        #     UnconditionedAbove_Area = UnconditionedAbove_Area + sva_df['FLOOR_AREA'][i]
    return conditionedAbove_Area

def get_UnconditionedAboveArea(sva_df):
    UnconditionedAbove_Area = 0
    sys = sva_df['SYSTEM_TYPE'].to_list()
    for i in range(0, len(sva_df['SYSTEM_TYPE'])):
        if(sys[i] == 'SUM'):
            UnconditionedAbove_Area = UnconditionedAbove_Area + sva_df['FLOOR_AREA'][i]
        # else:
        #     UnconditionedAbove_Area = UnconditionedAbove_Area + sva_df['FLOOR_AREA'][i]
    return UnconditionedAbove_Area

def get_SVA_report(name, path):
    with open(name) as f:
        flist = f.readlines()

        sva_count = [] 
        for num, line in enumerate(flist, 0):
            if 'SV-A' in line:
                sva_count.append(num)
            if 'SS-D' in line:
                numend = num
        numstart = sva_count[0] 
        sva_rpt = flist[numstart:numend]
        
        sva_str = []
        for line in sva_rpt:
            if (('SUM' in line and '.' in line) or ('PTAC' in line and '.' in line and 'WEATHER' not in line) or
                ('VAVS' in line and '.' in line) or ('PIU' in line and '.' in line) or 
                ('FC' in line and 'zn' not in line and 'Zn' not in line and '.' in line) or 
                ('UVT' in line and '.' in line) or
                ('PSZ' in line and '.' in line) or ('PMZS' in line and '.' in line)):
                sva_str.append(line)

        result = []  
        for line in sva_str:
            sva_list = []
            splitter = line.split()
            space_name = " ".join(splitter[:-10])
            sva_list=splitter[-10:]
            sva_list.insert(0,space_name)
            result.append(sva_list)

        sva_df = pd.DataFrame(result)
        sva_df.columns = ['SYSTEM_TYPE', 'ALTITUDE_FACTOR', 'FLOOR_AREA',
                        'MAX_PEOPLE', 'OUTSIDE_AIR_RATIO', 'COOLING_CAPACITY',
                        'SENSIBLE', 'HEATING_CAPACITY', 'COOLING_EIR', 'HEATING_EIR', 'HEAT_PUMP(SUPP_HEAT)']
        sva_df['FLOOR_AREA'] = pd.to_numeric(sva_df['FLOOR_AREA'])
        sva_df.index.name = name
        value_before_backslash = ''.join(reversed(name)).split("\\")[0]
        name1 = ''.join(reversed(value_before_backslash))
        name = name1.rsplit(".", 1)[0]
        sva_df.insert(0, 'RUNNAME', name)
        # print(sva_df)  
        
        # print("\nConditioned Area")
        # CArea = get_conditionedAboveArea(sva_df)
        # print(round(CArea,2))

        # print("UnConditioned Area")
        # UArea = get_UnconditionedAboveArea(sva_df)
        # print(round(UArea,2))
     
    return sva_df