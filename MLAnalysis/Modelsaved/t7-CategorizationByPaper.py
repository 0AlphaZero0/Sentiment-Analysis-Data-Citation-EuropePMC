#!/usr/bin/env python
#-*- coding: utf-8 -*-
# THOUVENIN Arthur athouvenin@outlook.fr
# 19/07/2019
########################

import pandas
import codecs
import time

################################################    Variables     #################################################

################################################    Functions     #################################################

###################################################    Main     ###################################################
start=time.time()
dataset=pandas.read_csv(
	filepath_or_buffer="Predictions.csv",
	header=0,
	sep="\t")

dicPMCID={}
for index,row in dataset.iterrows():
	if row["PMCID"] not in dicPMCID:
		dicPMCID.update({row["PMCID"]:{}})
	if row["AccessionNb"] not in dicPMCID[row["PMCID"]]:
		dicPMCID[row["PMCID"]].update({
			row["AccessionNb"]:{
				"crea-count":0,
				"crea-proba":0,
				"back-count":0,
				"back-proba":0,
				"use-count":0,
				"use-proba":0,
				"total":0,
				"sections":[]}})
	if row["Categories"]=="Creation":
		dicPMCID[row["PMCID"]][row["AccessionNb"]]["crea-count"]+=1
	elif row["Categories"]=="Background":
		dicPMCID[row["PMCID"]][row["AccessionNb"]]["back-count"]+=1
	else:
		dicPMCID[row["PMCID"]][row["AccessionNb"]]["use-count"]+=1
	dicPMCID[row["PMCID"]][row["AccessionNb"]]["crea-proba"]+=row["Creation"]
	dicPMCID[row["PMCID"]][row["AccessionNb"]]["back-proba"]+=row["Background"]
	dicPMCID[row["PMCID"]][row["AccessionNb"]]["use-proba"]+=row["Use"]
	dicPMCID[row["PMCID"]][row["AccessionNb"]]["total"]+=1
	if row["Section"] not in dicPMCID[row["PMCID"]][row["AccessionNb"]]["sections"]:
		dicPMCID[row["PMCID"]][row["AccessionNb"]]["sections"].append(row["Section"])

file=codecs.open("Resultbypaper.csv","w",encoding="utf-8")
file.write("PMCID")
file.write("\t")
file.write("AccessionNb")
file.write("\t")
file.write("Crea-Count")
file.write("\t")
file.write("Crea-Proba")
file.write("\t")
file.write("Back-Count")
file.write("\t")
file.write("Back-Proba")
file.write("\t")
file.write("Use-Count")
file.write("\t")
file.write("Use-Proba")
file.write("\t")
file.write("TOTAL")
file.write("\t")
file.write("Sections")
file.write("\n")

for PMCID,dicAccNb in dicPMCID.items():
	for AccessionNb, dicScores in dicAccNb.items():
		file.write(PMCID)
		file.write("\t")
		file.write(AccessionNb)
		file.write("\t")
		# dicScores["crea-proba"]=dicScores["crea-proba"]/dicScores["total"]
		# dicScores["back-proba"]=dicScores["back-proba"]/dicScores["total"]
		# dicScores["use-proba"]=dicScores["use-proba"]/dicScores["total"]
		file.write(str(dicScores["crea-count"]))
		file.write("\t")
		file.write(str(dicScores["crea-proba"]))
		file.write("\t")
		file.write(str(dicScores["back-count"]))
		file.write("\t")
		file.write(str(dicScores["back-proba"]))
		file.write("\t")
		file.write(str(dicScores["use-count"]))
		file.write("\t")
		file.write(str(dicScores["use-proba"]))
		file.write("\t")
		file.write(str(dicScores["total"]))
		if dicScores["total"]>1:
			file.write("\t")
			file.write(str(dicScores["sections"]))
		else:
			file.write("\t")
			file.write("")
		file.write("\n")
file.close()
end=time.time()
print("""##############################\n#####   CATEGORIZATION   #####\n##############################""")
print ("Duration : "+str(int(end-start))+" sec")
print("\n\n")