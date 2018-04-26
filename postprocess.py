import sys
import os
import csv 
import numpy as np
import pandas as pd


#load the data frame for each files 
def loadDF(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.replace('"', '') for x in content]
    content = [x.strip() for x in content] 
    reviewer = filename.split("/")[-2]
    dicLocal = {}
    #the dislocal will be [reviewer, steptitle, start, end, duration]
    #validation step
    dicLocal['reviewer'] = reviewer;
    for i in range (len(content)-1):
        line = content[i+1].split('\t')
        if len(line) > 8:
            toStore = [line[-6],line[-4],line[-2]]
            if line[-1] not in dicLocal:
                dicLocal[line[-1]] = toStore
            else:
                upDated = []
                for k in range(len(toStore)):
                   upDated.append(toStore[k]+' '+dicLocal[line[-1]][k])
                dicLocal[line[-1]] = upDated
    #if the length of the keys is 24 (23+1)
    # store the keys
    if len(dicLocal.keys()) == 24:
        global steplist
        steplist= [ x for x in dicLocal.keys() if x !='reviewer']

    return dicLocal

def combine(alist,steplist):
    #df is in the form of 
    #reviewer1 start end duration reviewer2 start end duration intersect union
    #step1
    #step2
    df = pd.DataFrame(columns=['stepnumber','reviewer1','start1','end1','duration1',\
            'reviewer2','start2','end2','duration2','intersect','union','inter/uni']) 
    df['stepnumber'] = steplist
    for i in range(len(alist)):
        for step in steplist:
            if step in alist[i]:
                if i ==0:
                    df['reviewer1'][df.stepnumber==step] = alist[i]['reviewer']
                    df['start1'][df.stepnumber==step] = alist[i][step][0]
                    df['end1'][df.stepnumber==step] = alist[i][step][1]
                    df['duration1'][df.stepnumber==step] = alist[i][step][2]

                else:
                    df['reviewer2'][df.stepnumber==step] = alist[i]['reviewer']
                    df['start2'][df.stepnumber==step] = alist[i][step][0]
                    df['end2'][df.stepnumber==step] = alist[i][step][1]
                    df['duration2'][df.stepnumber==step] = alist[i][step][2]

    return df

def findUA (df):
    for k in range(len(df['start1'])):
        missing1 =True
        missing2 =True
        if not pd.isnull(df['start1'][k]):
            start1 = df['start1'][k].split(' ')
            missing1 = False
        if not pd.isnull(df['end1'][k]):
            end1 = df['end1'][k].split(' ')
            missing1 = False
        if not pd.isnull(df['start2'][k]):
            start2 = df['start2'][k].split(' ')
            missing2 = False
        if not pd.isnull(df['end2'][k]):
            end2 = df['end2'][k].split(' ')
            missing2 = False
        if missing1 and missing2:
            df['union'][k] =  np.nan
            df['intersect'][k] =  np.nan
            continue
        elif missing1:
            union = [] 
            for i in range(len(start2)):
                union.append(start2[i]+'->' +end2[i])
            df['union'][k] =' '.join(union)
            df['intersect'][k] =  np.nan
            df['inter/uni'][k] = 0
            continue
        elif missing2:
            union = [] 
            for i in range(len(start1)):
                union.append(start1[i]+'->' +end1[i])
            df['union'][k] =' '.join(union)
            df['intersect'][k] =  np.nan
            df['inter/uni'][k] = np.nan
            continue

        
        union = []
        intersect=[]
        ua = []
        for i in range(len(start1)):
            for j in range(len(start2)):
                interstart =  max (start1[i],start2[j])
                interend =  min (end1[i],end2[j])
                if (int(interstart) >int(interend) ):
                    interstart = 0
                    interend = 0
                unionstart = min (start1[i],start2[j])
                unionend = max (end1[i],end2[j])
                udur = float(unionend)-float(unionstart)
                adur = float(interend) -float(interstart)
                union.append(unionstart+'->'+unionend)
                intersect.append(str(interstart)+'->'+str(interend))
                ua.append(str(adur/udur))
        df['union'][k] =  ' '.join(union)
        df['intersect'][k] =  ' '.join(intersect)
        df['inter/uni'][k] = ' '.join(ua)
    return df



def main():
    dic = {}
    #walk through the directories and load the files into each dataframe
    for root, dirs, files in os.walk('raw'):
        for f in files:
            if f.split('.')[-1] =='txt':
                newdf = loadDF(os.path.join(root,f))
                if f not in dic:
                    dic[f] = [newdf]
                else:
                    dic[f].append(newdf)
    
    #write every file to a csv
    os.mkdir('processed')
    os.chdir('processed')

    for key in dic:
        dic[key] = combine(dic[key],steplist)
        #dic[key] = findUA(dic[key])
        dic[key].to_csv(key.split('.txt')[0]+'.csv', sep='\t')
if __name__=="__main__":
    main()                        
