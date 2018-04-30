import sys
import os
import csv 
import numpy as np
import pandas as pd
import math

#run after postprocess
def main():
    for root, dirs, files in os.walk('processed'):
        with open("numberofInstances.csv",'w') as csvf:
            with open ("repeated steps.csv", 'w') as repeated:
                with open("annotation overlap.csv",'w') as finalcsv:
                    counter =0;
                    for f in files:
                        df = pd.read_csv(os.path.join(root,f),sep='\t')
                        fields = ["patient","reviewer"]
                        for i in df.stepnumber:
                            fields.append(i)
                        writer = csv.DictWriter(csvf,fieldnames = fields)
                        writerRepeated = csv.DictWriter(repeated,fieldnames=['patient','step','reviewer1','reviewer2','R1 #repeats','R2 #repeats','interval1','interval2'])
                        writerFinal = csv.DictWriter(finalcsv,fieldnames=['patient','step','reviewer1','reviewer2','agree on # repeats','intersection ==0 ','inter/Union','Time Window'])

                        if counter == 0:
                            writer.writeheader()
                            writerRepeated.writeheader()
                            writerFinal.writeheader() 
                            counter =1              
                        dc = {}
                        dcrepeated = {}
                        dcfinal = {}
                        dc['patient'] =  f.split('.')[0]
                        dcrepeated['patient'] =  f.split('.')[0]
                        for i in range(len(df.stepnumber)):
                            #write final csv:
                            dcfinal['step'] = df.stepnumber[i]
                            dcfinal['reviewer1'] = df.reviewer1[i]
                            dcfinal['reviewer2'] = df.reviewer2[i]
                            dcfinal['patient'] =  f.split('.')[0]
                            dcfinal['Time Window'] = []
                            if ( len(str(df.start1[i]).split(" "))==len(str(df.start2[i]).split(" "))) and df.reviewer1[i] ==df.reviewer1[i] and df.reviewer2[i] ==df.reviewer2[i]:
                                dcfinal['agree on # repeats'] = 1
                            else:
                                dcfinal['agree on # repeats'] = 0
                             
                            if pd.isnull(df.start1[i]):
                                dc[df.stepnumber[i]] = 0
                            else:
                                dc['reviewer'] = df.reviewer1[i]
                                dc[df.stepnumber[i]] = len(str(df.start1[i]).split(" "))

                            dcrepeated ['reviewer1'] = df.reviewer1[i]
                            dcrepeated ['step'] = df.stepnumber[i]
                            dcrepeated ['R1 #repeats'] = len(str(df.start1[i]).split(" "))
                            dcrepeated ['reviewer2'] = df.reviewer2[i]
                            dcrepeated ['R2 #repeats'] = len(str(df.start2[i]).split(" "))
                            dcrepeated['interval1'] = []
                            dcrepeated['interval2'] = []
                            interliststart1 = str(df.start1[i]).split(" ")
                            interliststart2 = str(df.start2[i]).split(" ")
                            interlistend1 =  str(df.end1[i]).split(" ")
                            interlistend2 = str(df.end2[i]).split(" ")
                            interliststart1  = [float(x) for x in interliststart1 if str(x) != 'nan']
                            interliststart2  = [float(x) for x in interliststart2 if str(x) != 'nan']
                            interlistend1 = [float(x) for x in interlistend1 if str(x) != 'nan']
                            interlistend2 = [float(x) for x in interlistend2 if str(x) != 'nan']
                            for j in range(len(interliststart1)):
                                dcrepeated['interval1'].append('->'.join([str(int(float(interliststart1[j]))),str(int(float(interlistend1[j])))]))
                            for j in range(len(interliststart2)):
                                dcrepeated['interval2'].append('->'.join([str(int(float(interliststart2[j]))),str(int(float(interlistend2[j])))]))
                            # union: Some of the union doesnt make sense:
                            unionStartlist =interliststart1+interliststart2
                            unionStartlist =[float(x) for x in unionStartlist]
                            if len(unionStartlist) == 0:
                                unionStart = 0
                            else:
                                unionStart = min(unionStartlist)
                            unionEndlist = interlistend1+interlistend2
                            unionEndlist =[float(x) for x in unionEndlist]
                            if len(unionEndlist) == 0:
                                unionEnd = 1
                            else:
                                unionEnd = max(unionEndlist)
                            interliststart1 = sorted(interliststart1)
                            interliststart2 = sorted(interliststart2)
                            interlistend1 = sorted(interlistend1)
                            interlistend2 = sorted(interlistend2)
                            interTime = 0
                            for i in range(len(interliststart1)):
                                for j in range(len(interliststart2)):
                                    startT=max(float(interliststart1[i]),float(interliststart2[j]))
                                    endT=min(float(interlistend1[i]),float(interlistend2[j]))
                                    if (float(endT) - float(startT)) >0:
                                        interTime = interTime+float(endT) - float(startT)
                            space = 0
                            if len(interliststart1) == 2 and len(interliststart2) == 2:
                                space=min(float(interliststart1[1]),float(interliststart2[1]))-max(float(interlistend1[0]),float(interlistend2[0]))
                            elif len(interliststart1) == 2:
                                space = float(interliststart1[1]) - float(interlistend1[0])
                            elif len(interliststart2) == 2:
                                space = float(interliststart2[1]) -float(interlistend2[0])
                            
                            if dcfinal['patient'] == "380" and space != 0:
                                print(max(float(interlistend1[0]),float(interlistend2[0])),min(float(interliststart1[1]),float(interliststart2[1])))
                            dcfinal['inter/Union'] =interTime/(unionEnd-unionStart-space)
                            #exception1: == 1
                            if dcfinal['inter/Union'] >=1 or dcfinal['inter/Union'] <0 :
                                dcfinal['inter/Union'] = 0
                            dcfinal['Time Window'] =dcrepeated['interval1']+dcrepeated['interval2']
                            dcrepeated['interval1'] = ' '.join(dcrepeated['interval1'])
                            dcrepeated['interval2'] = ' '.join(dcrepeated['interval2'])
                            dcfinal['Time Window']  = ' '.join(dcfinal['Time Window'])
                            #Exception 1: file missing /step missing
                            if len(interliststart1) >1  or len(interliststart2) >1:
                                writerRepeated.writerow(dcrepeated)
                            writerFinal.writerow(dcfinal)
                        writer.writerow(dc)
                        for i in range(len(df.stepnumber)):
                            if pd.isnull(df.start2[i]):
                                dc[df.stepnumber[i]] = 0
                            else:
                                dc['reviewer'] = df.reviewer2[i]
                                dc[df.stepnumber[i]] = len(str(df.start2[i]).split(" "))
                        writer.writerow(dc)                
                
if __name__=="__main__":
    main() 
