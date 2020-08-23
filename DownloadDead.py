import requests

resp = requests.get('https://d2cstorage-a.akamaihd.net/wr/Gratefuldead/jamoftheweek/3_21_90_hamilton.mp3', verify=False)

f = open(r"3_21_90_hamilton.mp3", "wb")
f.write(resp.content)
f.close()