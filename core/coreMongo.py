import pymongo
import os.path
from datetime import date, datetime
from core import coreIo


oParams = coreIo.oParam()

# definition du chemin de la restoration de la base
sPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sPathBase = sPath + '/restorebdd'


def init():
    global oParams, oMongo
    try:
        pymongo.MongoClient("mongodb://" + oParams["user"] + ':' + oParams["pass"] + oParams["url"])
        print('============================================================'
                    'Mongo : Ouverture de la connexion : mongodb://' +
                    oParams["user"] + ':' + oParams["pass"] + oParams["url"])
        if not oParams["base"]:
            print("No Base Mongo ")
    except Exception as e:
        return False
    return True


# recupere un connexion
def setParam(oSetParams):
    global oParams
    oParams = oSetParams


def getConn():
    global oParams
    oMongo = None
    try:
        if oMongo == None:
            Connect = pymongo.MongoClient("mongodb://" + oParams["user"] + ':' + oParams["pass"] + oParams["url"])
            if not oParams["base"]:
                return "erreur la base n'existe"
            oMongo = Connect[oParams["base"]]

    except Exception as e:
        return 'erreur'
    return oMongo


# connexion à la base des aliments et affichage liste
def AlimentsBase():
    global oParams, oMongo
    oApp = []
    try:
        oMongo = getConn()
        oData = oMongo[oParams["aliments"]]
        for sAliment in oData.find():
            sReplaceId = str(sAliment['_id']).replace('ObjectId(','')
            oApp.append({'id' : sReplaceId,'catégorie':sAliment['categorie'],'infos': sAliment['infos']}) 
    except Exception as e:
        return (e)
    print(str(oApp))
    return oApp


# insertion d'un aliment
def insertAliment(sCategorie,sName,iQte, sVolume, sDateFin):
    oAliment = []
    oNewAliment  = []
    global oParams, oMongo
    oMongo = getConn()
    oData = oMongo[oParams["aliments"]]
    myquery = {"categorie": sCategorie}
    for x in oData.find(myquery):
        for i in x['infos']:
            oAliment.append(i)
        oAliment.append({'name':sName ,'quantite': int(iQte), 'volume': sVolume, 'dateFin': sDateFin})
        oOldValue = {"categorie": sCategorie} 
        oNewvalue = { "$set": {"infos" : oAliment}}
        oData.update_one(oOldValue,oNewvalue)
    return True


# suppression d'un aliment
def delAliment(sCategorie,sName):
    global oParams, oMongo
    oMongo = getConn()
    oData = oMongo[oParams["aliments"]]
    oData.update_one({"categorie": sCategorie},{'$pull': {'infos': {'name':sName }}})
    return True


# modifier un aliment
def modifAliment(sCategorie, sNV, sON, iNQ, sNN,sDF):
    global oParams, oMongo
    sNewName = sON
    print(sNewName)
    oAliment = []
    oMongo = getConn()
    oData = oMongo[oParams["aliments"]]
    myquery = {"categorie": sCategorie}
    for x in oData.find(myquery):
        for i in x['infos']:
            if sNewName != i['name']:
                oAliment.append(i)
                print('dmljkshfbkbqSCDHFMIKSHFNxclHFMXHFCm     '+str(oAliment))
        if sNN != "" and sNN !=sON:
            sNewName = sNN
        if int(iNQ) == 0:
            delAliment(sCategorie,sNewName)
        else:
            if delAliment(sCategorie,sNewName):
                #oData.update_one({"categorie": sCategorie},{'$pull': {'infos': {'name':sNewName }}})
                oAliment.append({'name':sNewName ,'quantite': int(iNQ), 'volume': sNV, 'dateFin': sDF})
                oOldValue = {"categorie": sCategorie} 
                oNewvalue = { "$set": {"infos" : oAliment}}
                oData.update_one(oOldValue,oNewvalue)

    return True







                        





# connexion à la base des utilisateurs
def userBase():
    global oParams, oMongo, oData
    try:
        oMongo = getConn()
        oData = oMongo[oParams["collaborater"]]
    except Exception as e:
        return (e)
    return oData

# verification de l'utilisateur connecté + gestion du token de connexion
def connectUser(email, password, AccessIp):
    global oParams, oMongo
    sFormat = "%Y-%m-%d %H:%M:%S"
    sUser = None
    oMongo = getConn()
    oData = oMongo[oParams["collaborater"]]
    
    for sUser in oData.find():
        if sUser['email'] == email:     
            if sUser['password'] == password:
                if sUser['droit'] == 'Administrateur':
                    if sUser['token'] == "" or sUser['token']== None:
                        sToken = coreIo.createToken()
                        oNewToken = {"$set":{"token": sToken, "lastAccess": datetime.now().strftime(sFormat), "lastAccessIp" : AccessIp}}
                        oFindUser = {"email":sUser['email']}
                        oData.update_one(oFindUser,oNewToken)
                    else : 
                        if coreIo.checkValiditeToken(sUser['lastAccess']):
                            sToken = coreIo.createToken()
                            oNewToken = {"$set":{"token": sToken, "lastAccess": datetime.now().strftime(sFormat), "lastAccessIp" : AccessIp}}
                            oFindUser = {"email":sUser['email']}
                            oData.update_one(oFindUser,oNewToken)
                    return True
        else:
            return False


#recherche utilisateur via mail et password
def searchUser(email, password): 
    global oParams, oMongo    
    oMongo = getConn()
    sTokenUser = ""
    oData = oMongo[oParams["collaborater"]]
    myquery = {"email": email, "password": password}
    for sUser in oData.find(myquery):
        sTokenUser = sUser['token']
        return sTokenUser  

#recherche utilisateur via mail et password
def searchTokenUser(sToken): 
    global oParams, oMongo    
    oMongo = getConn()
    sUser = None
    oData = oMongo[oParams["collaborater"]]
    myquery = {"token": sToken}
    for u in oData.find(myquery):
        sUser = {"name": u['name'],"firstname":u['firstname'], "droit":u['droit']} 
        return sUser

#recherche token
def checkToken(sToken, AccessIp):
    global oParams, oMongo 
    sUser = None
    oMongo = getConn()
    oData = oMongo[oParams["collaborater"]]
    myquery = {"token": sToken}
    for user in oData.find(myquery):
        sUser = user
    if sUser == None or sUser == "" or sUser["token"] != sToken or sUser["lastAccessIp"] != AccessIp:   
        return False
    if coreIo.checkValiditeToken(sUser["lastAccess"]):    
        return False
    return True    


# recuperation de la liste d'une application     
def checkApp(name):
    oApp =[]
    global oParams, oMongo    
    oMongo = getConn()
    oData = oMongo[oParams["app"]]
    myquery = {"name": name}  
    sApp = [] 
    for sApp in oData.find(myquery):
        oApp= {'name': sApp['name'], 'framework':sApp['framework'], 'swagger': sApp['swagger'], 'tests': sApp['tests']}
        
    return oApp 



# recperation des tests effectués en base
def searchTests(nameApp, seekApp): 
    global oParams, oMongo    
    oMongo = getConn()
    oTests = None
    oData = oMongo[oParams["test"]]
    alltests = []
    try:
        if nameApp == None :
            myquery = {"name": seekApp}
            for u in oData.find(myquery):
                for tt in u["testExectuer"]:
                    alltests.append(tt)
                oTests = alltests
        else:
            myquery = {"name": nameApp}        
            for u in oData.find(myquery):
                for tt in u["testExectuer"]:
                    if seekApp == tt['name']:
                        alltests.append(tt) 
                oTests = alltests
    except Exception as e:
            oData = {'success': False, 'message': 'error' + e}
            return oData
    return oTests  