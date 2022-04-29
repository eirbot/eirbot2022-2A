import sys
import requests

response = requests.get('http://'+sys.argv[1]+':'+sys.argv[2]+'/pos_robot')
#print(response.text)

str1 = response.text.split(",")
pos=[int(str1[0]),int(str1[1])]
print(pos)