from flask import Flask, request, redirect, jsonify, render_template, session
from sqlalchemy import create_engine
import numpy as np
from Levenshtein import distance as LD
import pandas as pd

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def welcome():
	return render_template("index.html")

@app.route('/survey', methods=['POST'])
def survey():
    survey_result = request.form
    session['survey_result'] = survey_result
    return redirect(url_for('index'))
@app.route('/recommended')
def recommend():
    breed_info = pd.read_csv("breed_info.csv")
    apartment = float(survey_result['apartment'])
    experience = float(survey_result['experience'])
    alone = float(survey_result['alone'])
    children = float(survey_result['children'])
    social = float(survey_result['social'])
    shedding = float(survey_result['shedding'])
    groom = float(survey_result['groom'])
    size = float(survey_result['size'])
    intelligence = float(survey_result['intelligence'])
    barking = float(survey_result['barking'])
    exercise = float(survey_result['exercise'])
    x0 = np.array([apartment, experience, alone, children, social, shedding, groom, size, intelligence, barking, exercise])


    #breed_info = pd.read_csv("breed_info.csv")
    breed_info = breed_info.drop(208)
    breed_list = [l.lower() for l in breed_info["Dog Breed"]]
    breed_info_trunc = breed_info[["Dog Breed",
           "Adapts Well to Apartment Living",
           "Good For Novice Owners",
           "Tolerates Being Alone",
           "Incredibly Kid Friendly Dogs",
           "Friendly Toward Strangers",
           "Amount Of Shedding",
           "Easy To Groom",
           "Size",
           "Intelligence",
           "Tendency To Bark Or Howl",
           "Exercise Needs"] ]
    breed_info_trunc["Dog Breed"] = breed_info_trunc["Dog Breed"].map(lambda x: x.lower())

    dog_inventory = pd.read_csv("found_list.csv", index_col=0)
    dog_inventory = dog_inventory.reset_index()
    dog_inventory = dog_inventory.drop(["index"],axis=1)
    breed_inventory = dog_inventory["Breed"]

    def breed_preprocess(s):
        breed = s.lower()
        if "pit bull" in breed:
            breed = "american pit bull terrirer"
        breed = breed.replace("germ sh ", "german shorthaired ")
        breed = {True: "west highland white terrier", False: breed}[breed == "west highland"]
        breed = {True: "poodle", False: breed}["poodle" in breed]
        breed_split = breed.split()
        for i in range(len(breed_split)):
            breed_split[i] = {True: "american", False: breed_split[i] }[breed_split[i] == "am" ]
            breed_split[i] = {True: "terrier", False: breed_split[i] }[breed_split[i] == "ter" ]
            breed_split[i] = {True: "terrier", False: breed_split[i] }[breed_split[i] == "terr" ]
            breed_split[i] = {True: "german", False: breed_split[i] }[breed_split[i] == "germ" ]
            breed_split[i] = {True: "miniature", False: breed_split[i] }[breed_split[i] == "min" ]
            breed_split[i] = {True: "saint", False: breed_split[i] }[breed_split[i] == "st" ]
            breed_split[i] = {True: "", False: breed_split[i] }[breed_split[i] == "mix" ]
            breed_split[i] = {True: "australian", False: breed_split[i] }[breed_split[i] == "aust" ]
            breed_split[i] = {True: "retriever", False: breed_split[i] }[breed_split[i] == "retr" ]
        if "miniature" in breed_split:
            breed_split.insert(0, breed_split.pop( breed_split.index("miniature") ))
        ret_string = breed_split[0]
        for j in range(1,len(breed_split)):
            ret_string = ret_string + " " + breed_split[j]
        return ret_string

    def breed_fix(s):
        s_new = breed_preprocess(s)
        min_dist = 10000000
        current_breed = ""
        for breed in breed_list:
            if LD(s_new, breed) < min_dist:
                min_dist = LD(s_new, breed)
                current_breed = breed
            return current_breed

    dog_inventory["Mapped_Breed"] = breed_inventory.map(breed_fix)

    user_breed_dist = []
    for dog in dog_inventory["Mapped_Breed"]:
        user_breed_dist.append((np.linalg.norm(breed_info_trunc.loc[breed_info_trunc["Dog Breed"] == dog ].as_matrix()[0][1:12] - x0, 3)))

    dog_inventory["Recommendation Score"] =  user_breed_dist
    inventory_ret = dog_inventory.sort_values(by = "Recommendation Score", ascending=False).head(5)
    #return redirect('/')
    return inventory_ret.to_json()


"""
@app.route('/survey', methods=['POST'])
def survey():
    breed_info = pd.read_csv("breed_info.csv")
    apartment = float(request.form['apartment'])
    experience = float(request.form['experience'])
    alone = float(request.form['alone'])
    children = float(request.form['children'])
    social = float(request.form['social'])
    shedding = float(request.form['shedding'])
    groom = float(request.form['groom'])
    size = float(request.form['size'])
    intelligence = float(request.form['intelligence'])
    barking = float(request.form['barking'])
    exercise = float(request.form['exercise'])
    x0 = np.array([apartment, experience, alone, children, social, shedding, groom, size, intelligence, barking, exercise])


    #breed_info = pd.read_csv("breed_info.csv")
    breed_info = breed_info.drop(208)
    breed_list = [l.lower() for l in breed_info["Dog Breed"]]
    breed_info_trunc = breed_info[["Dog Breed",
           "Adapts Well to Apartment Living",
           "Good For Novice Owners",
           "Tolerates Being Alone",
           "Incredibly Kid Friendly Dogs",
           "Friendly Toward Strangers",
           "Amount Of Shedding",
           "Easy To Groom",
           "Size",
           "Intelligence",
           "Tendency To Bark Or Howl",
           "Exercise Needs"] ]
    breed_info_trunc["Dog Breed"] = breed_info_trunc["Dog Breed"].map(lambda x: x.lower())

    dog_inventory = pd.read_csv("found_list.csv", index_col=0)
    dog_inventory = dog_inventory.reset_index()
    dog_inventory = dog_inventory.drop(["index"],axis=1)
    breed_inventory = dog_inventory["Breed"]

    def breed_preprocess(s):
        breed = s.lower()
        if "pit bull" in breed:
            breed = "american pit bull terrirer"
        breed = breed.replace("germ sh ", "german shorthaired ")
        breed = {True: "west highland white terrier", False: breed}[breed == "west highland"]
        breed = {True: "poodle", False: breed}["poodle" in breed]
        breed_split = breed.split()
        for i in range(len(breed_split)):
            breed_split[i] = {True: "american", False: breed_split[i] }[breed_split[i] == "am" ]
            breed_split[i] = {True: "terrier", False: breed_split[i] }[breed_split[i] == "ter" ]
            breed_split[i] = {True: "terrier", False: breed_split[i] }[breed_split[i] == "terr" ]
            breed_split[i] = {True: "german", False: breed_split[i] }[breed_split[i] == "germ" ]
            breed_split[i] = {True: "miniature", False: breed_split[i] }[breed_split[i] == "min" ]
            breed_split[i] = {True: "saint", False: breed_split[i] }[breed_split[i] == "st" ]
            breed_split[i] = {True: "", False: breed_split[i] }[breed_split[i] == "mix" ]
            breed_split[i] = {True: "australian", False: breed_split[i] }[breed_split[i] == "aust" ]
            breed_split[i] = {True: "retriever", False: breed_split[i] }[breed_split[i] == "retr" ]
        if "miniature" in breed_split:
            breed_split.insert(0, breed_split.pop( breed_split.index("miniature") ))
        ret_string = breed_split[0]
        for j in range(1,len(breed_split)):
            ret_string = ret_string + " " + breed_split[j]
        return ret_string

    def breed_fix(s):
    	s_new = breed_preprocess(s)
    	min_dist = 10000000
    	current_breed = ""
    	for breed in breed_list:
            if LD(s_new, breed) < min_dist:
                min_dist = LD(s_new, breed)
                current_breed = breed
            return current_breed

    dog_inventory["Mapped_Breed"] = breed_inventory.map(breed_fix)

    user_breed_dist = []
    for dog in dog_inventory["Mapped_Breed"]:
    	user_breed_dist.append((np.linalg.norm(breed_info_trunc.loc[breed_info_trunc["Dog Breed"] == dog ].as_matrix()[0][1:12] - x0, 3)))

    dog_inventory["Recommendation Score"] =  user_breed_dist
    inventory_ret = dog_inventory.sort_values(by = "Recommendation Score", ascending=False).head(5)
    #return redirect('/')
    return inventory_ret.to_json()

if __name__ == "__main__":
    app.debug = True
    app.run()
"""













