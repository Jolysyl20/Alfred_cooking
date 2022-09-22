# save this as app.py
from crypt import methods
from email.errors import StartBoundaryNotFoundDefect
from operator import index
from flask import Flask, redirect, render_template, request, jsonify, url_for,flash
from core import coreMongo
app = Flask(__name__)

oVolumes = ['kg','gramme','pot','ml','dl','litre' ,'c.café','c.soupe','unité' ]


@app.route("/ajout", methods=['POST','GET'])
def AjoutAliment():

    if request.method == 'POST':
        sIp = request.remote_addr 
        print(sIp)
        sCategorie = request.form['categorie']
        sNom = request.form['nom']
        sQuantite = request.form['quantite']
        sVolume = request.form['volume']
        sDateFin = request.form['dateFin']

        coreMongo.insertAliment(sCategorie,sNom,str(sQuantite),sVolume,sDateFin)

        print(sCategorie)
        return redirect("http://localhost:3000/") 
    return "cool" 


@app.route("/delete", methods=['POST','GET'])
def deleteAliment():
    if request.method == 'POST':
        sIp = request.remote_addr 
        print(sIp)
        sCategorie = request.form['categorie']
        sNom = request.form['name_aliment_to_delete']
        coreMongo.delAliment(sCategorie,sNom)
        
        return redirect("http://localhost:3000/") 
    return "cool"   

@app.route("/modif", methods=['POST','GET'])
def modifAliment():
    sCategorie = request.form['Origine_categorie']

    sNV = request.form['nvolume']
    sON = request.form['Origine_name']
    iNQ = request.form['nqte']
    sNN = request.form['nnom']
    sDF = request.form['dateFin']
    coreMongo.modifAliment(sCategorie, sNV, sON,  iNQ, sNN,sDF)
       
    return redirect("http://localhost:3000/")  

@app.route("/",methods=['get','post'])
def Accueil():
    oAliments = coreMongo.AlimentsBase()
    return render_template("index.html", aliments=oAliments, vol = oVolumes)