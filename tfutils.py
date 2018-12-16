import csv
import os
import random
from collections import defaultdict


class MetaLoad:
        
        def __init__(self, testpercent, basedir, metafilein):
                self.TP = testpercent
                self.BASE = basedir
                self.MI = metafilein
                self.MD = "meta"
                self.ID = "images"

        def printsummary(self,labeldict):
                ####### Finding Summary ########
                dash = '-' * 67
                print (dash)
                        #123456789012345678901234567890123456789
                print (f'Finding              Total     Train(%)  Train(#)  Test(%)  Test(#)')
                print (dash)
                for label in labeldict:
                        count = 0
                        # new tldict for 
                        tldict=defaultdict(list)
                        for findingplus in labeldict[label]:
                                fpa=findingplus.split(',')
                                finding = fpa[0]
                                tl = fpa[1]
                                count+=1
                                tldict[tl].append(finding)

                        train = len(tldict["train"])
                        trainpercent = train*100/count
                        test = len(tldict["test"])
                        testpercent = test*100/count
                        print('{:<20s}{:>5s}\t{:>4.2f}\t{:>7.0f}\t{:>8.2f}{:>8.0f}'.format(label.ljust(20),str(count).rjust(6),trainpercent,train,testpercent,test))
                

        def loadmetadata(self, want = "all"):
                # Load Metadata
                labeldict=defaultdict(list)
                fhdict = {}
                with open(os.path.join(self.BASE,self.MD,self.MI),'r') as csv_file_r:
                        csv_reader = csv.DictReader(csv_file_r)
                        line_count = 0
                        
                        #ImageFilename,Finding Labels,Follow-up #,Patient ID,Patient Age,Patient Gender,View Position,OriginalImage[Width,Height],OriginalImagePixelSpacing[x,y],TensorLoad
                        for row in csv_reader:
                                for finding in row["Finding Labels"].split('|'):
                                        finding = finding.lower()
                                        #print(f'\t{row["ImageFilename"]} -> {finding} -> {row["TensorLoad"]}')
                                        loadtype="train"
                                        if (random.randint(1,100) <= self.TP):
                                                loadtype = "test"
                                        if (finding.lower() == want or want == "all"):
                                                if (finding not in labeldict):
                                                        fhdict[finding] =  open(os.path.join(self.BASE,self.MD,finding+".csv"), 'w')
                                                        fhdict[finding].write('ImageFilename,Finding Labels,TensorLoad\n')
                                                labeldict[finding].append(row["ImageFilename"]+","+loadtype)
                                                fhdict[finding].write(f'{os.path.join(self.BASE,self.ID,row["ImageFilename"])},{loadtype}\n')
                                                line_count += 1
                self.printsummary(labeldict)
