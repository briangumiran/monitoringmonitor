"""
SENSLOPE monitoring scheduler

by Brian Gumiran
sets schedule once number of shifts are sent

"""
import pandas as pd
import numpy as np

#change FNAME everytime when running this code
fname = "monthcount\June 2016.xlsx"

#randomlist located in an excel file:
randomlist = pd.read_excel('randomlist.xlsx')

#update shift count
allshiftcount = pd.read_excel('moncount.xlsx')
shiftcountpara = ['DATE','NAME','COMM','EVENTC','TECH','EVENTT']
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

#clean stuff: filled values, upparcase all, fill event indicator, do not remove non-events
monthcount['DATE'].fillna(method = 'pad',inplace = True)
monthcount['TECH'].fillna("NONE",inplace = True)
monthcount['COMM'].fillna("NONE",inplace = True)
monthcount['EVENT'].fillna(0, inplace = True)
monthcount['TECH'] = monthcount['TECH'].str.upper()
monthcount['COMM'] = monthcount['COMM'].str.upper()
#print monthcount


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
			'COMM' : 0,
			'EVENTT': tempTECH['EVENT'].values[techcnt],
			'EVENTC': 0
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
			'COMM' : 1,
			'EVENTT': 0,
			'EVENTC': tempCOMM['EVENT'].values[commcnt]
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
finalpara = ['STAFF','COMM','COMMALL','%COMM','TECH','TECHALL','%TECH','TOTAL','ALL','%ALL']
staffshift = pd.DataFrame(columns = finalpara)
temp3df = pd.DataFrame(columns = finalpara)
allshiftcount = temp2df

#count number of total shifts per staff (since epoch)
for staffcnt in np.arange(len(randomlist.index)):
	tempCOUNT = allshiftcount[allshiftcount['NAME']==randomlist['STAFF'].values[staffcnt]]
	tempCOUNT.reset_index(drop=True,inplace=True)
	#print tempCOUNT
	
	sumCOMM = tempCOUNT['EVENTC'].sum()
	allCOMM = tempCOUNT['COMM'].sum()
	sumTECH = tempCOUNT['EVENTT'].sum()
	allTECH = tempCOUNT['TECH'].sum()
	total = sumTECH+sumCOMM
	all = allCOMM+allTECH
	try:
		RATCOMM = 100*sumCOMM/allCOMM
	except ZeroDivisionError:
		RATCOMM = 0

	try:
		RATTECH	= 100*sumTECH/allTECH
	except ZeroDivisionError:
		RATTECH = 0
		
	try:
		RATALL	= 100*total/all
	except ZeroDivisionError:
		RATALL = 0

	temp3 = [{
		'STAFF' : randomlist['STAFF'].values[staffcnt],
		'COMM' : sumCOMM,
		'COMMALL' : allCOMM,
		'%COMM' : RATCOMM,
		'TECH' : sumTECH,
		'TECHALL' : allTECH,
		'%TECH' : RATTECH,
		'TOTAL' : total, 
		'ALL' : all, 
		'%ALL': RATALL
	}]
	temp3df = pd.DataFrame(temp3, columns =finalpara)
	staffshift = staffshift.append(temp3df,ignore_index = True)

print staffshift
"""
part 4: record files for next shifting weights
-update a file for 

"""