import urllib2
import json
import codecs

out = codecs.open('outoccur.txt', 'w','utf-8')
infile = codecs.open('gbif/1_subset.csv', 'r','utf-8')
delim="$"
idx=0;

#http://api.gbif.org/v0.9/occurrence/search?decimalLongitude=-180,-179&limit=300&offset=300

for line in infile:
	lineArr=line.strip().split(delim)	
	url = "http://api.gbif.org/v1/occurrence/"+lineArr[0]
	#print(url)
	responseOccr = urllib2.urlopen(url)
	data = json.load(responseOccr)
	errorMsg = ""
	
	if data.has_key("scientificName"):
                sciVal= data['scientificName']
		keyVal =  data['taxonKey']
		if sciVal!=lineArr[1]:
			errorMsg=errorMsg+";"+lineArr[0]+" -- scientificName: not matching (GBIF|KU) -- "+sciVal+delim+lineArr[1]
		if str(keyVal) != lineArr[2]:
			errorMsg=errorMsg+";"+lineArr[0]+" -- taxonKey: not matching (GBIF|KU) -- "+str(keyVal)+delim+lineArr[2]
        else:
                errorMsg=""+lineArr[0]+" -- Missing: GBIF scientificName"


	idx=idx+1
	#if (idx/100000)%1==0:
		#print (errorMsg)
	out.write(errorMsg)

out.close()
infile.close()
