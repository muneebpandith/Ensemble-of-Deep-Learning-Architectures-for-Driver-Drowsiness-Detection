import os
import glob
import fnmatch
def main():
	
	mainpath= "/home/muneeb/Desktop/MTECHMINORLINUX/DATA"
	##STEP 1: FIND SUBJECTS e.g., '001','002', etc & COMBINATION TYPES e.g., 'glasses' etc. AND TYPES e.g., nonsleepyCombination etc.
	#Give the paths respectively than manually typing 001 etc glasses etc, and sleepyComb... etc
	readingpath= mainpath+"/NTHU_Distracted_Driver_Dataset/Training_Dataset"
	savingpath=mainpath+"/newsubjectwise"





	subjectspath = mainpath+"/NTHU_Distracted_Driver_Dataset/Training_Dataset"
	typespath= subjectspath+"/001"	
	combspath= typespath+"/glasses"
	ext=".avi"


	subjects=os.listdir(subjectspath)
	#['001', '002', '005', '006', '008', '009', '012', '013', '015', '020', '023', '024', '031', '032', '033', '034', '035', '036'] 
	
	types   =os.listdir(typespath)
	#['glasses', 'nightglasses', 'night_noglasses', 'noglasses', 'sunglasses']
	

	combs=list()

	for file in os.listdir(combspath):
		if fnmatch.fnmatch(file, '*.avi'):
			combs.append(file.split(".")[0])
	
	#combs ['nonsleepyCombination.avi', 'sleepyCombination.avi', 'slowBlinkWithNodding.avi', 'yawning.avi']

	
	print(subjects,combs,types)
	#subjects=list(['005'])


	#doffmpeg()
	#saveindir ="I:/DDD"
	
	#ffmpeg -i "sleepyCombination.avi" -vf fps=30 "I:\DDD\001\sleepyCombination\glasses\001_nonsleepyCombination_%d.jpg"
	
	

	for eachsubject in subjects:
		for eachtype in types:
			
			frameno=0
			for eachcomb in combs:

				readingfrom= readingpath +"/"+eachsubject+"/"+eachtype+"/"+eachcomb+ext
				#annotation lateron
				#allinfo=open(readingpath +"/"+eachsubject+"/"+eachtype+"/"+eachsubject+"_"+eachcomb+"_drowsiness.txt", "r")
				#if allinfo.mode == 'r':
				#	drowsycontents =allinfo.read()
				#allinfo.close()
				
				#subjectwise ordering
				savingto=savingpath+"/"+ eachsubject +"/" +eachtype+"/"+eachcomb

				savingas= savingto+"/"+eachsubject+".ALL."+eachtype+"."+eachcomb
				print(savingas)
				

				#ORIGINALLY as: 
				#savingas= savingto+"/"+eachsubject+"_"+eachcomb+ "_%d.jpg"
								

				if not os.path.exists(savingto):
					print("Creating Path for "+eachsubject)
					os.system("mkdir -p "+savingto)	

				if(eachtype=='night_noglasses' or eachtype=='nightglasses'):
					fps=15
				else:
					fps=30
				
				print("Reading From: "+ readingfrom)	
				#saveindir + "/" + eachsubject + "/" +eachcomb+ "/" +eachtype + "/" +eachsubject+ "_"+eachcomb+"%d"
				os.system("ffmpeg -i " + readingfrom + " -vf fps="+ str(fps) + " "+ savingas+".N."+"%d.jpg")
				
if __name__== "__main__":
	main()