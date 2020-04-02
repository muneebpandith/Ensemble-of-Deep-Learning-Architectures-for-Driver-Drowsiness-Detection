import os
import glob
import fnmatch
import cv2
import pandas as pd
import numpy as np
import sys

def complete0():
        conn = http.client.HTTPSConnection("api.msg91.com")
        payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Annotprocess starting\",  \"to\": [ \"9149429559\", \"9797091372\" ] }] }"
        headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
        conn.request("POST", "/api/v2/sendsms", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
       

def complete():
        conn = http.client.HTTPSConnection("api.msg91.com")
        payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Annot process complete\",  \"to\": [ \"9149429559\", \"9797091372\" ] }] }"
        headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
        conn.request("POST", "/api/v2/sendsms", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
       
def getannotation(filename):
	fileobj = open(filename,"r")
	filedata = fileobj.read()
	#print(filedata)
	return filedata

def updateannotation(annotationdata,frameno):
    length=len(annotationdata)
    if((int(frameno)+1)>length):
        return annotationdata[length-1]
    else:
        return annotationdata[int(frameno)-1]

def annotateimage(readingfile, writingdirectory, fileattrib):
	savingas=   writingdirectory+"/"+fileattrib['sname']+"."+ fileattrib['typeofface']+"."+fileattrib['tname']+"."+fileattrib['cname']+"."+fileattrib['annotation']+"."+fileattrib['frameno']+".jpg"
	#print("Reading From: "+ readingfile + "Copying to: ", savingas)
	if (os.path.exists(savingas) and os.stat(savingas).st_size> 0):
		print("Annotation done already: "+savingas)
	else:
		print(savingas)

	
	savingas=   writingdirectory+"/"+fileattrib['sname']+"."+ fileattrib['typeofface']+"."+fileattrib['tname']+"."+fileattrib['cname']+"."+fileattrib['annotation']+"."+fileattrib['frameno']+".jpg"
	#print("Reading From: "+ readingfile + "Copying to: ", savingas)
	
	if (os.path.exists(savingas) and os.stat(savingas).st_size> 0):
		print("Exists, So ignore: "+savingas)
	else:
		print(savingas)
		#cv2.imwrite(savingas,imgCroppedFace)
def main():

	
	mainpath= "../../MTECHMINORLINUX/DATA"
	##STEP 1: FIND SUBJECTS e.g., '001','002', etc & COMBINATION TYPES e.g., 'glasses' etc. AND TYPES e.g., nonsleepyCombination etc.
	#Give the paths respectively than manually typing 001 etc glasses etc, and sleepyComb... etc
	

	readingpath=mainpath+"/newsubjectwise"
		
	savingpath=mainpath+"/annotatednewsubjectwise"



	subjectspath = mainpath+"/newsubjectwise"
	annotationsmainpath=mainpath+"/NTHU_Distracted_Driver_Dataset/Training_Dataset"


	subjects=os.listdir(subjectspath)
	#['001', '002', '005', '006', '008', '009', '012', '013', '015', '020', '023', '024', '031', '032', '033', '034', '035', '036'] 
	#subjects=['023']
	#subjects=['023','024','031','032','033','034','035','036']
	print(subjects)
	


	for eachsubject in subjects:
		typespath= subjectspath+"/"+eachsubject
		types   =os.listdir(typespath)	
		#['glasses', 'nightglasses', 'night_noglasses', 'noglasses', 'sunglasses']
		#print(types)



		
		for eachtype in types:
			combspath= typespath+"/"+eachtype
			combs   =os.listdir(combspath)
			#print(combs)

			for eachcomb in combs:
				filespath=combspath+"/"+eachcomb
				myfiles=list()
				for file in os.listdir(filespath):
					if fnmatch.fnmatch(file, '*.jpg'):
					#combs.append(file.split(".")[0])
						myfiles.append(file)
				#print(myfiles)
				annotationspath= annotationsmainpath+"/"+eachsubject+"/"+eachtype+"/"+eachsubject+"_"+eachcomb+"_drowsiness.txt"
				annotationdata=getannotation(annotationspath)
				for eachfile in myfiles:
					readingfrom= readingpath +"/"+eachsubject+"/"+eachtype+"/"+eachcomb+"/"+eachfile
					
					#subjectwise ordering
					savingto=savingpath+"/"+ eachsubject +"/" +eachtype+"/"+eachcomb
					
					if not os.path.exists(savingto):
						print("Creating Path for "+eachsubject)
						os.system("mkdir -p "+savingto)	

					if(eachtype=='night_noglasses' or eachtype=='nightglasses'):
						fps=15
					else:
						fps=30
					

					
					#print(readingfileinfo)
					#readingfrom=eachfile

					fileattrib=dict()
					
					fileattrib['sname']=sname=eachfile.split(".")[0]
					fileattrib['typeofface']=typeofface=eachfile.split(".")[1]
					fileattrib['tname']=tname=eachfile.split(".")[2]
					fileattrib['cname']=cname=eachfile.split(".")[3]
					fileattrib['annotation']=annotation=eachfile.split(".")[4]
					fileattrib['frameno']=frameno=eachfile.split(".")[5]
					

					fileattrib['annotation']=updateannotation(annotationdata,fileattrib['frameno'])
					annotateimage(readingfrom, savingto, fileattrib)
	return 1
if __name__== "__main__":
        complete0()
        if main()==1 :
                complete()




