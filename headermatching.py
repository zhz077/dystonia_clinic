import sys
import os
import csv 
import re
import numpy as np
import pandas as pd

def main():
    #load filename for each reviewer
    fields = ["px from filename","px from header","agreement","reveiwer","SI"]
    towrite = []
    for root, dirs, files in os.walk('raw'):
        for f in files:
            if f.split('.')[-1] =='txt':
                filename = f.split('.')[0]
                reviewer = os.path.join(root,f).split("/")[-2]
                with open (os.path.join(root,f)) as toread:
                    header = toread.readline()
                    if len(header.split(".mp4")) >1:
                        headerfile=header.split(".mp4")[0].split("/")[-1].split("_")[0]
                    else: 
                        headerfile=header.split(".wmv")[0].split("/")[-1].split("_")[0]
                    hfilenumber = re.split("dys",headerfile,flags=re.IGNORECASE)[-1]
                    agreement =0
                    if hfilenumber == filename:
                        agreement = 1
                    SI = re.split("ms per sample: ",header,flags=re.IGNORECASE)[-1].split('"')[0]
                    towrite.append([filename,hfilenumber,agreement,reviewer,SI])

    #write a final csv
    with open("headerBenchMarking.csv",'w') as csvf:
        writer = csv.DictWriter(csvf,fieldnames = fields)
        writer.writeheader()
        df = {}
        for row in towrite:
            for i in range(len(fields)):
                df[fields[i]] = row[i]
            writer.writerow(df)
                        
if __name__=="__main__":
    main()  
