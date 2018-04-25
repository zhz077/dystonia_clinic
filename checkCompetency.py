import sys
import os
import csv 
import numpy as np
import pandas as pd

def main():
    #use abs path to read the file. Doesnt work on othe config expect zz local
    xfilename = "/Users/apple/Developer/salk/clinic/dystonia_clinic/assignment.xlsx"
    df = pd.read_excel(xfilename)
    df = df.set_index('Patient')
    df['actualreviwerA'] = np.nan 
    df['actualreviwerB'] = np.nan 
    df['actualreviwerC'] = np.nan
    #load filename for each reviewer
    for root, dirs, files in os.walk('raw'):
        for f in files:
            if f.split('.')[-1] =='txt':
                filename = 'Dys'+f.split('.')[0]
                reviewer = os.path.join(root,f).split("/")[-2]
                if pd.isnull(df.loc[filename]["actualreviwerA"]) :
                    df.loc[filename, "actualreviwerA"] = reviewer
                elif pd.isnull(df.loc[filename]["actualreviwerB"]):
                    df.loc[filename, "actualreviwerB"] = reviewer
                else:
                    df.loc[filename, "actualreviwerC"] = reviewer
    
    dc = {}
    dc["ZZ"]=[]
    dc["EC"]=[]
    dc["CB"]=[]
    dc["JV"]=[]
    dc["QC"]=[]
    for index, row in df.iterrows():
        for i in ["A","B"]:
            if row["Annot %s"%(i)] not in [row["actualreviwerA"],row["actualreviwerB"],row["actualreviwerC"]]:
                dc[row["Annot %s"%(i)]].append(index)
    with open("Competency.csv",'w') as csvf:
        field = ["reviewer","Patient List"]
        writer = csv.DictWriter(csvf,fieldnames = field)
        writer.writeheader()
        for key in dc:
            writer.writerow({field[0]:key,field[1]:",".join(dc[key])})
        

                
if __name__=="__main__":
    main()   
