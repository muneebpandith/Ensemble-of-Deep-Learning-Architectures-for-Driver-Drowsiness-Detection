import http.client
import os


def complete0():
        conn = http.client.HTTPSConnection("api.msg91.com")
        payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Tar process starting\", \"to\": [ \"9149429559\" ] }] }"
        headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
        conn.request("POST", "/api/v2/sendsms", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
      
def complete():
	conn = http.client.HTTPSConnection("api.msg91.com")
	payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Tar process FACE complete for all subjects\", \"to\": [ \"9149429559\"] }] }"
	headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
	conn.request("POST", "/api/v2/sendsms", payload, headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))
def intermsg(msg):
	conn = http.client.HTTPSConnection("api.msg91.com")
	payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \" "+str(msg)+ ".\", \"to\": [ \"9149429559\"] }] }"
	headers = {'authkey': "118364AVIfu09J5e85f50eP1",'content-type': "application/json"}
	conn.request("POST", "/api/v2/sendsms", payload, headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))

def main():
	#this excludes subject 005

	intermsg("Tar process of mouth INIT")
	os.system("tar -czvf 'croppedmouth.tar.gz' 'croppedmouth' >> tarofcroppedmouthfiles.txt")
	intermsg("Tar process of MOUTH COMPLETE")
	
	intermsg("Tar process of lefteye INIT")
	os.system("tar -czvf 'croppedlefteye.tar.gz' 'croppedlefteye' >> tarofcroppedlefteye.txt")
	intermsg("Tar process of lefteye Complete")
	
	intermsg("Tar process of righteye INIT")
	os.system("tar -czvf 'croppedrighteye.tar.gz' 'croppedrighteye' >> tarofcroppedrighteye.txt")
	intermsg("Tar process of righteye COMPLETE")
		
  return 1
if __name__== "__main__":
	complete0()
	if(main()==1):
		complete()
