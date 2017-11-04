import csv
import random
import math
from sklearn.model_selection import KFold
import sys
from sklearn import model_selection
import numpy as np

conti=[0,5,16,17,18,24,30,36]
kfold_val=10
kf = model_selection.KFold(n_splits=kfold_val,shuffle=True)



def openfile(file):
	# line=csv.reader(open(file, "rb"))
	data=list(csv.reader(open(file, "rb")))
	return data

def read_data(data):
	count=0
	input1,input2=[],[]
	for s in data:
		listval=s[-1].strip()
		s[-1]=listval
		class1='- 50000.'
		if(s[-1]==class1):
			input1.append(s)
		else:
			input2.append(s)
		count+=1
	return input1,input2

def gaussian(x,mean,stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	value=(float(1 / float(math.sqrt(2*math.pi) * stdev)) * float(exponent))
	return value

def process_data(data):
	nominal={}
	mean_list,std_list=[],[]
	for j in xrange(len(data[0])-1):
		nominal_list_prob,nominal_list_count,nominal_list_names=[],[],[]
		if(j not in conti ):
				mp={}
				for i in xrange(len(data)):
					if data[i][j] in mp.keys():
						mp[data[i][j]]+=1
					else:
						mp[data[i][j]]=1					
				for k, v in mp.items():
					mp[k]=round(float(float(v)/float(len(data))),5)
				nominal[j]=mp
			
		else:
			cont=[]
			mean=0.0
			sum_=0.0
			for i in xrange(len(data)):
				cont.append(float(data[i][j]))	
			sum_=sum(cont)
			mean=float(sum_/len(cont))
			std=np.std(cont) 
			std_list.append(std)
			mean_list.append(mean)
			mean=0.0
			sum_=0.0
		
	return mean_list,std_list,nominal



if __name__ == "__main__":
	filename = 'census-income.data'
	l=[]
	data = openfile(filename)
	for x in xrange(30):
		print "Epoch Number:", x+1,"\n"
		total_acc=[]
		for train, test in kf.split(data):
			Accuracy=0
			traindata,testdata=[],[]
			for i in train:
				traindata.append(data[i])
			input1,input2 = read_data(traindata)
			Accuracy=0
			mean_list1,std_list1,nominal1 = process_data(input1)
			testdata=[]
			mean_list2,std_list2,nominal2 = process_data(input2)
			for i in test:
				testdata.append(data[i])
			for i in xrange(len(testdata)):
				pwc1,pwc2,count=0,0,0
				for j in xrange(len(testdata[i])-1):
					if(j not in conti):
						if(testdata[i][j]!=' ?'):
							if testdata[i][j] in nominal1[j]:
								newpwc1=math.log(nominal1[j][testdata[i][j]])
								pwc1+=newpwc1
							flag=0
							if testdata[i][j] in nominal2[j]:
								newpwc2=math.log(nominal2[j][testdata[i][j]])
								pwc2+=newpwc2
					else:
						pass
				testdata[i][-1]=testdata[i][-1].strip()
				newpwc1=math.log(float(float(len(input1))/float(len(input1)+len(input2))))
				pwc1 += newpwc1
				newpwc2=math.log(float(float(len(input2))/float(len(input1)+len(input2))))
				pwc2 += newpwc2
				testprob=[]
				testprob.append(pwc1)
				testprob.append(pwc2)
				if (pwc1>pwc2 and testdata[i][-1]=='- 50000.'):
					Accuracy+=1
				if( (pwc2>pwc1 and testdata[i][-1]=='50000+.')):
					Accuracy+=1
			flag=False
			accpercent=(Accuracy/float(len(testdata))) * 100.0
			Accuracy=accpercent
			total_acc.append(Accuracy)
		mean_acc = np.mean(total_acc)
		std=np.std(total_acc)
		#printing mean
		print mean_acc
		#printing standard dev
		print std

