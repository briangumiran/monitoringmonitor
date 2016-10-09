"""
SENSLOPE monitoring scheduler

by Brian Gumiran
sets schedule once number of shifts are sent

"""
import pandas as pd
import numpy as np

fname = "monthcount\September 2016.xlsx"

#randomlist located in an excel file:
randomlist = pd.read_excel('randomlist.xlsx')

#update shift count
allshiftcount = pd.read_excel('moncount.xlsx')
shiftcountpara = ['DATE','NAME','TECH','COMM']
"""
part 1:

update total monitoring stats (saved in moncount.xlsx) based on previous months stat:
15 previous month - 15 current month

prerequisites:
save an edited excel file in folder .\montcount\
"""
#readmonthly stats
monthcount = pd.read_excel(fname)
monthnum = monthcount.index.values

#clean stuff: filled values, upparcase all, fill event indicator,remove non-events
monthcount['DATE'].fillna(method = 'pad',inplace = True)
monthcount['TECH'].fillna("NONE",inplace = True)
monthcount['COMM'].fillna("NONE",inplace = True)
monthcount['EVENT'].fillna(0, inplace = True)
monthcount['TECH'] = monthcount['TECH'].str.upper()
monthcount['COMM'] = monthcount['COMM'].str.upper()
monthcount = monthcount[monthcount['EVENT'] == 1]

#update allshiftcount
temp = pd.DataFrame(columns = ['DATE','SHIFT','TECH','COMM','EVENT'])

#count number of shifts per person, will update moncount.xlsx
for staffcnt in np.arange(len(randomlist.index)):
	#process by staff name, tech
	tempTECH = monthcount[monthcount['TECH'].str.contains(randomlist['STAFF'].values[staffcnt])]
	tempTECH.reset_index(drop=True,inplace=True)
	for techcnt in np.arange(len(tempTECH.index)):
		temp2 = [{
			'DATE' : tempTECH['DATE'].values[techcnt],
			'NAME' : randomlist['STAFF'].values[staffcnt],
			'TECH' : 1,
			'COMM' : 0
		}]
		temp2df = pd.DataFrame(temp2,columns = shiftcountpara)
		allshiftcount = allshiftcount.append(temp2df, ignore_index = True)
	
	#process by staff name, comm
	tempCOMM = monthcount[monthcount['COMM'].str.contains(randomlist['STAFF'].values[staffcnt])]
	tempCOMM.reset_index(drop=True,inplace=True)
	for commcnt in np.arange(len(tempCOMM.index)):
		temp2 = [{
			'DATE' : tempCOMM['DATE'].values[commcnt],
			'NAME' : randomlist['STAFF'].values[staffcnt],
			'TECH' : 0,
			'COMM' : 1
		}]
		temp2df = pd.DataFrame(temp2,columns = shiftcountpara)
		allshiftcount = allshiftcount.append(temp2df, ignore_index = True)
	
#print allshiftcount
allshiftcount.to_excel('moncount.xlsx', index = False)

#check duplicates
temp2df = pd.read_excel('moncount.xlsx')
temp2df.drop_duplicates(inplace = True)
temp2df.reset_index(drop=True,inplace = True)

#print temp2df
#final save to moncount
temp2df.to_excel('moncount.xlsx', index = False)

"""
part 3: Assign number of shifts per personnel
-start with CT oriented staff (tech transfer)
ASSIGNING methodology
	-then randomly assign MT and CT shifts to all staff, evenly distributed
	-then adjust for previous iterations
"""

staffshift = pd.DataFrame(columns = ['STAFF','COMM','TECH','TOTAL'])
temp3df = pd.DataFrame(columns = ['STAFF','COMM','TECH','TOTAL'])
allshiftcount = temp2df

#count number of total shifts per staff (since epoch)
for staffcnt in np.arange(len(randomlist.index)):
	tempCOUNT = allshiftcount[allshiftcount['NAME']==randomlist['STAFF'].values[staffcnt]]
	tempCOUNT.reset_index(drop=True,inplace=True)
	temp3 = [{
		'STAFF' : randomlist['STAFF'].values[staffcnt],
		'COMM' : tempCOUNT['COMM'].sum(),
		'TECH' : tempCOUNT['TECH'].sum(),
		'TOTAL' : tempCOUNT['TECH'].sum()+tempCOUNT['COMM'].sum()
	}]
	temp3df = pd.DataFrame(temp3, columns =['STAFF','COMM','TECH','TOTAL'])
	staffshift = staffshift.append(temp3df,ignore_index = True)

print staffshift
"""
part 4: record files for next shifting weights
-update a file for 

"""