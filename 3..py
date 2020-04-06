#!/usr/bin/env python
# coding: utf-8

# In[16]:


import os
import glob
import fnmatch
import cv2
import mtcnn
import http.client

# In[17]:


from mtcnn.mtcnn import MTCNN


# In[ ]:

def complete0():
	conn = http.client.HTTPSConnection("api.msg91.com")
	payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Cropping starting\",  \"to\": [ \"9149429559\", \"9797091372\" ] }] }"
	headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
	conn.request("POST", "/api/v2/sendsms", payload, headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))


def complete():
	conn = http.client.HTTPSConnection("api.msg91.com")
	payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Cropping complete\",  \"to\": [ \"9149429559\", \"9797091372\" ] }] }"
	headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
	conn.request("POST", "/api/v2/sendsms", payload, headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))


def intercomplete(msg):
	conn = http.client.HTTPSConnection("api.msg91.com")
	payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Cropping subject - " +str(msg)+ ". \",  \"to\": [ \"9149429559\" ] }] }"
	headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
	conn.request("POST", "/api/v2/sendsms", payload, headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))


def saveifcansave(savingas,img,typeofimg,bounding_box):
	BOUNDINGBOXERROR=0
	SAVESUCCESS=0
	if bounding_box[0] < 0:
		bounding_box[0]=0
		BOUNDINGBOXERROR=1
	if bounding_box[1] < 0:
		bounding_box[1]=0
		BOUNDINGBOXERROR=1
	width=bounding_box[2]
	height=bounding_box[3]
	heightO, widthO, channels = img.shape
	if bounding_box[2] > widthO:
		bounding_box[2]=width0
	if bounding_box[3]> heightO:
		bounding_box[3]:heightO
	imgCropped=img[bounding_box[1]:bounding_box[1] + bounding_box[3],bounding_box[0]:bounding_box[0]+bounding_box[2]]
	height,width,channels= imgCropped.shape
	if height <= 0  or width <= 0:
		SAVESUCCESS=0
	else:
		cv2.imwrite(savingas,imgCropped)
		SAVESUCCESS=1
	
	if SAVESUCCESS==1:
		if BOUNDINGBOXERROR==1:
			os.system("echo "+str(savingas)+ ","+str(typeofimg)+",ERRTYPE1,SOLVED>> croppingerrorlog.txt")
		if BOUNDINGBOXERROR==2:
			os.system("echo "+str(savingas)+ ","+str(typeofimg)+",ERRTYPE2,SOLVED >> croppingerrorlog.txt")
	if SAVESUCCESS==0:
		os.system("echo " +str(savingas)+ ","+str(typeofimg)+ "ERRORTYPE3,NOTSOLVED >> croppingerrorlog.txt")
	return SAVESUCCESS,imgCropped

# In[18]:

detector = MTCNN()
def findallandsave(readingfile, writingdirectory, fileattrib):
	ERRORFLAG="ZEROERROR"
	img = cv2.imread(readingfile)
	#imgGrayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = detector.detect_faces(img)
	fileattrib['whattodo']="DISCARDED"
	#print(result)
	if faces != []:
		for person in faces:
			bounding_box = person['box']
			keypoints = person['keypoints']
			#print(keypoints)
			#print(bounding_box)            
			#cv2.rectangle(img,(bounding_box[0], bounding_box[1]),(bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),(0,155,255),0)
			#cv2.circle(img,(keypoints['left_eye']), 2, (0,255,0), 2)
			#cv2.circle(img,(keypoints['right_eye']), 2, (0,155,255), 2)
			#cv2.circle(img,(keypoints['nose']), 2, (0,155,255), 2)
			#cv2.circle(img,(keypoints['mouth_left']), 2, (0,255,0), 2)
			#cv2.circle(img,(keypoints['mouth_right']), 2, (0,155,255), 2)    
			fileattrib['whattodo']="FAC"
			#cv2.imshow("Img",img)
			#imgCroppedFace=img[bounding_box[1]:bounding_box[1] + bounding_box[3],bounding_box[0]:bounding_box[0]+bounding_box[2]]            
			savingas=   writingdirectory['face']+"/"+fileattrib['sname']+"."+ fileattrib['whattodo']+"."+fileattrib['tname']+"."+fileattrib['cname']+"."+fileattrib['annotation']+"."+fileattrib['frameno']+".jpg"
			if (os.path.exists(savingas) and os.stat(savingas).st_size> 0):
				print("Exists, So ignore: "+savingas)
			else:
				print(savingas)
				savesuccess,imgCroppedFace=saveifcansave(savingas,img,"FACE",bounding_box)
				if savesuccess==0:
					ERRORFLAG="FACEERROR"

			#SAVING EYES          
			fileattrib['whattodo']="EYES"
			#cv2.imshow("Img",img)
			bounding_box_x1new=(keypoints['left_eye'][0]+bounding_box[0])//2
			bounding_box_y1new=(keypoints['left_eye'][1]+bounding_box[1])//2

			bounding_box_x2new=(keypoints['right_eye'][0]+(bounding_box[0]+bounding_box[2]))//2
			bounding_box_y2new=(keypoints['right_eye'][1]+keypoints['nose'][1])//2
			bounding_box_wnew=bounding_box_x2new-bounding_box_x1new
			bounding_box_hnew=bounding_box_y2new- bounding_box_y1new

			bounding_box_Eyes=[bounding_box_x1new, bounding_box_y1new, bounding_box_wnew,bounding_box_hnew]           

			#imgCroppedEyes=img[bounding_box_Eyes[1]:bounding_box_Eyes[1] + bounding_box_Eyes[3],bounding_box_Eyes[0]:bounding_box_Eyes[0]+bounding_box_Eyes[2]]
			bounding_box_LEye=[0,0,(bounding_box_Eyes[2]//2),bounding_box_Eyes[3]]
			bounding_box_REye=[(bounding_box_Eyes[2]//2),0,bounding_box_Eyes[2], bounding_box_Eyes[3]]

			#imgCroppedLEye=imgCroppedEyes[0:0+bounding_box_Eyes[3], 0:0+(bounding_box_Eyes[2]//2)] 
			#imgCroppedREye=imgCroppedEyes[0:0+bounding_box_Eyes[3], (bounding_box_Eyes[2]//2):bounding_box_Eyes[2]] 

			savingas=   writingdirectory['eyes']+"/"+fileattrib['sname']+"."+ fileattrib['whattodo']+"."+fileattrib['tname']+"."+fileattrib['cname']+"."+fileattrib['annotation']+"."+fileattrib['frameno']+".jpg"
			if (os.path.exists(savingas) and os.stat(savingas).st_size> 0):
				print("Exists, So ignore: "+savingas)
			else:
				print(savingas)
				savesuccess,imgCroppedEyes=saveifcansave(savingas,img,"EYES",bounding_box_Eyes)
				if savesuccess==0:
					ERRORFLAG="EYESERROR"

			#SAVING LEFT EYES 
			#bounding_box_Leye=[bounding_box_x1new, bounding_box_y1new,(bounding_box_wnew//2), bounding_box_hnew]

			fileattrib['whattodo']="LEFT_EYE"
			#cv2.imshow("Img",img)
			savingas=   writingdirectory['leye']+"/"+fileattrib['sname']+"."+ fileattrib['whattodo']+"."+fileattrib['tname']+"."+fileattrib['cname']+"."+fileattrib['annotation']+"."+fileattrib['frameno']+".jpg"
			if (os.path.exists(savingas) and os.stat(savingas).st_size> 0):
				print("Exists, So ignore: "+savingas)
			else:
				print(savingas)
				savesuccess,imgCroppedLEye=saveifcansave(savingas,imgCroppedEyes,"LEFTEYE",bounding_box_LEye)
				if savesuccess==0:
					ERRORFLAG="LEFTEYEERROR"

			#SAVING RIGHT EYES            
			#bounding_box_Leye=[bounding_box_x1new, bounding_box_y1new,(bounding_box_wnew//2), bounding_box_hnew]

			fileattrib['whattodo']="RIGHT_EYE"
			#cv2.imshow("Img",img)
			savingas=   writingdirectory['reye']+"/"+fileattrib['sname']+"."+ fileattrib['whattodo']+"."+fileattrib['tname']+"."+fileattrib['cname']+"."+fileattrib['annotation']+"."+fileattrib['frameno']+".jpg"
			if (os.path.exists(savingas) and os.stat(savingas).st_size> 0):
				print("Exists, So ignore: "+savingas)
			else:
				print(savingas)
				savesuccess,imgCroppedREye=saveifcansave(savingas,imgCroppedEyes,"RIGHTEYE",bounding_box_REye)
				if savesuccess==0:
					ERRORFLAG="RIGHTEYEERROR"

			#SAVING MOUTH          
			fileattrib['whattodo']="MOUTH"
			#cv2.imshow("Img",img)
			bounding_box_x1new=(keypoints['mouth_left'][0]+bounding_box[0])//2
			bounding_box_y1new=(keypoints['mouth_left'][1]+keypoints['nose'][1])//2
			bounding_box_x2new=(keypoints['mouth_right'][0]+(bounding_box[0]+bounding_box[2]))//2
			bounding_box_y2new=(keypoints['mouth_right'][1]+(bounding_box[1]+bounding_box[3]))//2

			bounding_box_wnew=bounding_box_x2new-bounding_box_x1new
			bounding_box_hnew=bounding_box_y2new-bounding_box_y1new
			bounding_box_Mouth=[bounding_box_x1new, bounding_box_y1new, bounding_box_wnew,bounding_box_hnew]         
			#imgCroppedMouth=img[bounding_box_Mouth[1]:bounding_box_Mouth[1] + bounding_box_Mouth[3],bounding_box_Mouth[0]:bounding_box_Mouth[0]+bounding_box_Mouth[2]]            
			savingas=   writingdirectory['mouth']+"/"+fileattrib['sname']+"."+ fileattrib['whattodo']+"."+fileattrib['tname']+"."+fileattrib['cname']+"."+fileattrib['annotation']+"."+fileattrib['frameno']+".jpg"
			if (os.path.exists(savingas) and os.stat(savingas).st_size> 0):
				print("Exists, So ignore: "+savingas)
			else:
				print(savingas)
				savesuccess,imgCroppedMouth=saveifcansave(savingas,img,"MOUTH",bounding_box_Mouth)
				if savesuccess==0:
					ERRORFLAG="MOUTH_ERROR"

	#cv2.destroyAllWindows()
	return ERRORFLAG

# In[19]:


def main():
	mainpath= "../../MTECHMINORLINUX/DATA"
	##STEP 1: FIND SUBJECTS e.g., '001','002', etc & COMBINATION TYPES e.g., 'glasses' etc. AND TYPES e.g., nonsleepyCombination etc.
	#Give the paths respectively than manually typing 001 etc glasses etc, and sleepyComb... etc
	readingpath= mainpath+"/annotatednewsubjectwise"

	savingpathface=mainpath+"/croppedface"
	savingpatheyes=mainpath+"/croppedeyes" 
	savingpathmouth=mainpath+"/croppedmouth"
	savingpathreye=mainpath+"/croppedrighteye"
	savingpathleye=mainpath+"/croppedlefteye"
	savingpath=savingpathface
	savingto={'face':'', 'eyes':'','mouth':'','leye':'','reye':''}
	subjectspath = mainpath+"/annotatednewsubjectwise"
	#ext=".avi"
	#ext=".jpg"

	subjects=os.listdir(subjectspath)
	#['001', '002', '005', '006', '008', '009', '012', '013', '015', '020', '023', '024', '031', '032', '033', '034', '035', '036'] 
	#subjects=['023']
	#subjects=['023','024','031','032','033','034','035','036']
	print(subjects)
	for eachsubject in subjects:
		intercomplete(str(eachsubject) + "INIT. ")
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
				for eachfile in myfiles:
					readingfrom= readingpath +"/"+eachsubject+"/"+eachtype+"/"+eachcomb+"/"+eachfile
					
					#subjectwise ordering
					savingto['face']=savingpathface+"/"+ eachsubject +"/" +eachtype+"/"+eachcomb
					savingto['eyes']=savingpatheyes+"/"+ eachsubject +"/" +eachtype+"/"+eachcomb
					savingto['mouth']=savingpathmouth+"/"+ eachsubject +"/" +eachtype+"/"+eachcomb
					savingto['leye']=savingpathleye+"/"+ eachsubject +"/" +eachtype+"/"+eachcomb
					savingto['reye']=savingpathreye+"/"+ eachsubject +"/" +eachtype+"/"+eachcomb


					if not os.path.exists(savingto['face']):
						print("Creating Path for "+eachsubject)
						os.system("mkdir -p "+savingto['face'])
					if not os.path.exists(savingto['eyes']):
						print("Creating Path for "+eachsubject)
						os.system("mkdir -p "+savingto['eyes'])
					if not os.path.exists(savingto['mouth']):
						print("Creating Path for "+eachsubject)
						os.system("mkdir -p "+savingto['mouth'])
					if not os.path.exists(savingto['leye']):
						print("Creating Path for "+eachsubject)
						os.system("mkdir -p "+savingto['leye']) 
					if not os.path.exists(savingto['reye']):
						print("Creating Path for "+eachsubject)
						os.system("mkdir -p "+savingto['reye'])
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
					
					#print(sname,typeofface,tname,cname,annotation,frameno)
					

					
					#saveindir + "\\" + eachsubject + "\\" +eachcomb+ "\\" +eachtype + "\\" +eachsubject+ "_"+eachcomb+"%d"
					
					#os.system("copy " + readingfrom + "  "+ savingas)


					print(readingfrom)
					#intercomplete( str(fileattrib['sname']) + " INIT.")
					ERRORFLAG=findallandsave(readingfrom, savingto, fileattrib)
		if ERRORFLAG =="ZEROERROR":
			intercomplete( str(fileattrib['sname']) + " COMPLETE.")
		else:
			intercomplete(str(fileattrib['sname']) + " FAIL: "+str(ERRORFLAG)) 
	return 1
# In[ ]:


if __name__== "__main__":
	complete0()
	if main()==1:
		complete()

