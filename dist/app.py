import collections
from re import S
from flask import Flask, render_template, url_for, jsonify, request
import os, json
import numpy as np
from pymongo import MongoClient, database
import pprint
from bson import Binary, Code, BSON
from bson.json_util import dumps
#from flask_cors import CORS, cross_origin

client = MongoClient('mongodb://rer:rer@123.56.68.67:7017/School')
db = client['School']
collection = db['Campus']

app = Flask(__name__)
@app.after_request
def after_request(response):
    '''
    Allows for Cross Origin Requests.
    '''
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
    
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/place/<id>')
def click_place_id(id):
    return dumps(collection.find_one({"id":int(id)}))

@app.route('/filter/<vals>', methods=['GET'])
def filter_submit(vals):
    averageNoiseScore = vals(0)
    averageLightScore = vals(1)
    averageSmellScore = vals(2)
    
    for x in collection.find({"average sound score": averageNoiseScore, "average light score": averageLightScore, "average smell score": averageSmellScore}):
        print(x)

    return("done")


@app.route('/survey/<results>', methods=['GET'])
def submit_survey(results):
    data = json.loads(results)
    placeID = data["score:"]["id"]
    doc = collection.find_one({"id":placeID})
  
    peopleAnswer = data["score:"]["people"]
    movementAnswer = data["score:"]["movement"]
    talkingAnswer = data["score:"]["talking"]
    noiseAnswer = data["score:"]["noise"]
    noiseTypeAnswer = data["score:"]["noiseType"]
    lightAnswer = data["score:"]["light"]
    lightBrightAnswer = data["score:"]["lightBright"]
    lightFlickeringAnswer = data["score:"]["lightFlickering"]
    lightColourPeculiarAnswer = data["score:"]["lightColourPeculiar"]
    smellsAnswer = data["score:"]["smells"]
    smellTypeAnswer = data["score:"]["smellType"]
    floorStickyAnswer = data["score:"]["floorSticky"]
    floorUnevenAnswer = data["score:"]["floorUneven"]
    seatsHardAnswer = data["score:"]["seatsHardBinary"]
    texturesAnswer = data["score:"]["texturesRoughBinary"]
    
    answersArray = [peopleAnswer, movementAnswer, talkingAnswer, noiseAnswer, lightAnswer, lightBrightAnswer, lightFlickeringAnswer, lightColourPeculiarAnswer, smellsAnswer, 
    floorStickyAnswer, floorUnevenAnswer]
   
    scoreKeys =  ['people', 'movement', 'talking', 'noise', 'light', 'lightBright', 'lightFlickering', 'lightColourPeculiar', 'smells', 'floorSticky', 'floorUneven',]
    

    count = 0
    for surveyValue in answersArray:
        key = scoreKeys[count]
        if surveyValue == '1':
            collection.update_one({"id":placeID},{"$inc": {key+".0.No": 1}})
        elif surveyValue == '2':
            collection.update_one({"id":placeID},{"$inc": {key+".1.Rarely": 1}})
        elif surveyValue == '3':
            collection.update_one({"id":placeID},{"$inc": {key+".2.Sometimes": 1}})
        elif surveyValue == '4':
            collection.update_one({"id":placeID},{"$inc": {key+".3.Yes": 1}})

        count = count + 1
    
 
    if seatsHardAnswer == '1': 
        collection.update_one({"id":placeID},{"$inc": {"seatsHard.0.Soft": 1}})
    else: 
        collection.update_one({"id":placeID},{"$inc": {"seatsHard.1.Hard": 1}})
        

    if texturesAnswer == '1': 
        collection.update_one({"id":placeID},{"$inc": {"texturesRough.0.Smooth": 1}})
    else: 
        collection.update_one({"id":placeID},{"$inc": {"texturesRough.1.Rough": 1}})

    if noiseTypeAnswer[0] == "Voices":
        collection.update_one({"id":placeID},{"$inc": {"noiseType.0.Voices": 1}})
    if noiseTypeAnswer[1] == "Cutlery/Furniture":
        collection.update_one({"id":placeID},{"$inc": {"noiseType.1.Cutlery/Furniture": 1}})
    if noiseTypeAnswer[2] == "Media/Music":
        collection.update_one({"id":placeID},{"$inc": {"noiseType.2.Media/Music": 1}})
    if noiseTypeAnswer[3] == "Traffic/Heavy machinery":
        collection.update_one({"id":placeID},{"$inc": {"noiseType.3.Traffic/Heavy machinery": 1}})
    if noiseTypeAnswer[4] == "Other":
        collection.update_one({"id":placeID},{"$inc": {"noiseType.4.Other": 1}})

    if smellTypeAnswer[0] == "Chemical":
        collection.update_one({"id":placeID},{"$inc": {"smellType.0.Chemical": 1}})
    if smellTypeAnswer[1] == "Food":
        collection.update_one({"id":placeID},{"$inc": {"smellType.1.Food": 1}})
    if smellTypeAnswer[2] == "Cosmetic":
        collection.update_one({"id":placeID},{"$inc": {"smellType.2.Cosmetic": 1}})
    if smellTypeAnswer[3] == "Natural":
        collection.update_one({"id":placeID},{"$inc": {"smellType.3.Natural": 1}})          
    if smellTypeAnswer[4] == "Other":
        collection.update_one({"id":placeID},{"$inc": {"smellType.4.Other": 1}})   

    noiseScoreNo  = doc["noise"][0]["No"]
    noiseScoreRarely  = doc["noise"][1]["Rarely"]
    noiseScoreSometimes  = doc["noise"][2]["Sometimes"]
    noiseScoreYes  = doc["noise"][3]["Yes"]            
    noiseScoreList = [noiseScoreNo, noiseScoreRarely, noiseScoreSometimes, noiseScoreYes]
    if(max(noiseScoreList) == noiseScoreNo or max(noiseScoreList) == noiseScoreRarely):
        collection.update_one({"id":placeID},{"$set": {"average sound score": 1}}) 
    if(max(noiseScoreList) == noiseScoreSometimes):
        collection.update_one({"id":placeID},{"$set": {"average sound score": 2}})    
    if(max(noiseScoreList) == noiseScoreYes):
        collection.update_one({"id":placeID},{"$set": {"average sound score": 3}})


    lightScoreNo  = doc["light"][0]["No"]
    lightScoreRarely  = doc["light"][1]["Rarely"]
    lightScoreSometimes  = doc["light"][2]["Sometimes"]
    lightScoreYes  = doc["light"][3]["Yes"]
    lightScoreList = [lightScoreNo, lightScoreRarely, lightScoreSometimes, lightScoreYes]
    if(max(lightScoreList) == lightScoreNo or max(lightScoreList) == lightScoreRarely):
        collection.update_one({"id":placeID},{"$set": {"average light score": 1}})
    if(max(lightScoreList) == lightScoreSometimes):
        collection.update_one({"id":placeID},{"$set": {"average light score": 2}})     
    if(max(lightScoreList) == lightScoreYes):
        collection.update_one({"id":placeID},{"$set": {"average light score": 3}})

    smellScoreNo  = doc["smells"][0]["No"]
    smellScoreRarely  = doc["smells"][1]["Rarely"]
    smellScoreSometimes  = doc["smells"][2]["Sometimes"]
    smellScoreYes  = doc["smells"][3]["Yes"]
    smellScoreList = [smellScoreNo, smellScoreRarely, smellScoreSometimes, smellScoreYes]
    if(max(smellScoreList) == smellScoreNo or max(smellScoreList) == smellScoreRarely):
        collection.update_one({"id":placeID},{"$set": {"average smells score": 1}})
    if(max(smellScoreList) == smellScoreSometimes):
        collection.update_one({"id":placeID},{"$set": {"average smells score": 2}})    
    if(max(smellScoreList) == smellScoreYes):
        collection.update_one({"id":placeID},{"$set": {"average smells score": 3}})
    
    return("done")

@app.route('/newLocation/<information>', methods=['GET'])
def submit_newLocation(information):
    data = json.loads(information)
    print(data)

    #generate a placeID for this new location
    #create a new space in the database for this new location

    return("done")



if __name__ == "__main__":
    app.run(debug=True)