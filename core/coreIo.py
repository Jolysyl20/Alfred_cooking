import os.path, json, os, json, string, random
from datetime import datetime



sPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = None


def oParam():
    with open(sPath+ "/conf.json") as mon_fichier:
        data = json.load(mon_fichier)
    print(str(data))
    return data


oFiles2Delete =[]
# methode de comparaison

def checkValiditeToken(lastAccess):
    if lastAccess == None or lastAccess == "":
        return True
    sFormat = "%Y-%m-%d %H:%M:%S"
    dLastAccess = datetime.strptime(lastAccess, sFormat)
    dToday = datetime.now().strftime(sFormat)
    dToday  = datetime.strptime(dToday, sFormat)
    if dToday.timestamp() - dLastAccess.timestamp() > 28800:
        return True
    return False    


def createToken():
    sRandomeJeton = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(60))
    return sRandomeJeton    