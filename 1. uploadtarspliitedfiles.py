import http.client
import os
import dropbox

def complete0():
        conn = http.client.HTTPSConnection("api.msg91.com")
        payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Starting:Uploading of tarred (splitted files-newsubjectwise) process is starting\", \"to\": [ \"9149429559\" ] }] }"
        headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
        conn.request("POST", "/api/v2/sendsms", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
      
def complete():
	conn = http.client.HTTPSConnection("api.msg91.com")
	payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Complete: Uploading of tarred (splitted files-newsubjectwise) process is COMPLETE\", \"to\": [ \"9149429559\"] }] }"
	headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
	conn.request("POST", "/api/v2/sendsms", payload, headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))

def upload_file(file_from, file_to,access_token):
	dbx = dropbox.Dropbox(access_token)
	f = open(file_from, 'rb')
	dbx.files_upload(f.read(), file_to)

def main():
	#this excludes subject 005
	
	access_token = 'pf60SIufNzAAAAAAAAAAQzR_9Az9uueqBoo5ueYoErVq-SQ_U1iKYnpHcoBPfTDf'
	file_from = '../../MTECHMONORLINUX/DATA/newsubjectwise.tar.gz'  
	file_to = '/Nexus/newsubjectwise.tar.gz' 
	upload_file(file_from,file_to,access_token)
	return 1
if __name__== "__main__":
	complete0()
	if(main()==1):
		complete()
