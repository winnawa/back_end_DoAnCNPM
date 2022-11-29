from dbm import dumb
import os
import json
from time import time
from flask import Flask
from cfg.config import Config
from flask import Blueprint
#from .extension import mongo
from flask import  jsonify
from flask import request,send_file
import json
from bson import json_util
import base64
import pandas
from flask_pymongo import PyMongo
from flask_cors import CORS

mongo = PyMongo()
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
mongo.init_app(app)



class Error:
    def __init__(self, name, status):
        self.name = name
        self.status = status
#class to handle success
class Success:
    def __init__(self, name, status):
        self.name = name
        self.status = status




@app.route('/')
def index():
    user_collection = mongo.db.posts.find({})
    data = [d for d in user_collection]
    print('this is a', data)
    #return "hi"
    # posts = db.posts
    # result = posts.find({})
    return json_util.dumps(data)


# @app.route('/createCollection')
# def createCollection():
#     #mongo.db.create_collection("user")
#     print(mongo.db.list_collection_names())
#     return "<h1>success</h1>"
#     # data = [d for d in user_collection]
#     # print('this is a', data)
#     # #return "hi"
#     # # posts = db.posts
#     # # result = posts.find({})
#     # return json_util.dumps(data)


@app.route('/deleteDocuments')
def deleteDocuments():
    mongo.db.posts.delete_many({"user_id":""})
    mongo.db.posts.delete_many({"user_id":"user_id"})
    # print(mongo.db.list_collection_names())
    return "<h1>success</h1>"
    # data = [d for d in user_collection]
    # print('this is a', data)
    # #return "hi"
    # # posts = db.posts
    # # result = posts.find({})
    # return json_util.dumps(data)



@app.route('/login/authenticate', methods=['POST'])
def login_authentication():
    
    # singleUser = mongo.db.user.find({})
    # array = [d for d in singleUser]
    # print("current array",array)

    data = request.get_json()

    userName = ""
    userAccount = ""
    userPassword = ""
    for key,value in data.items():
        if key ==  "userAccount":
            userAccount = value
        if key == "userPassword":
            userPassword = value
    singleUser = mongo.db.user.find({})
    data = [d for d in singleUser]
    # print(data)
    singleUser = mongo.db.user.find({"account":userAccount ,"password" : userPassword})
    data = [d for d in singleUser]
    # print(data)


    if (len(data) > 0):
        return json_util.dumps({
                                    "data": {
                                        "_id" : data[0]["_id"],
                                        "user_name" : data[0]["username"]    
                                    },
                                    #data[0]
                                    "status":True
                                })
    else:
        error = Error("error",False)
        return json.dumps(error.__dict__)

@app.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    signupName = ""
    signupAccount = ""
    signupPassword = ""
    for key,value in data.items():
        print(key,value,"hi")
        if key ==  "signupAccount":
            signupAccount = value
        if key == "signupPassword":
            signupPassword = value
        if key == "signupName":
            signupName = value

    singleUser = mongo.db.user.find({"account": signupAccount, "password" : signupPassword})
    single_user_array = [d for d in singleUser]
    if (len(single_user_array)>0):
        error = Error("user exists",False)
        return json.dumps(error.__dict__)
    
    new_user = {    'account' : signupAccount, 
                    'password' : signupPassword,
                    'username' : signupName,
                }
    print(new_user)    
    try:
        mongo.db.user.insert_one(new_user)
    except:
        error = Error("Fail to add", False)
        return(error.__dict__)
    success = Success("Sucess", True)
    return(success.__dict__)  



@app.route('/posts/total_view', methods=['GET', 'POST'])
def show_total_view():

    
    total_post_collection = mongo.db.posts.find({})
    total_posts = [d for d in total_post_collection]
    num_of_total_post = len(total_posts)

    auto_post_collection = mongo.db.posts.find({'is_auto': True})
    auto_posts = [d for d in auto_post_collection]
    num_of_auto_post = len(auto_posts)


    fakenew_post_collection = mongo.db.posts.find({'is_fakenew': True})
    fakenew_posts = [d for d in fakenew_post_collection]
    num_of_fakenew_post = len(fakenew_posts)


    medical_post_collection = mongo.db.posts.find({'is_medical': True})
    medical_posts = [d for d in medical_post_collection]
    num_of_medical_post = len(medical_posts)


    verify_fakenew_post_collection = mongo.db.posts.find({'is_verify_fakenew': True})
    verify_fakenew_posts = [d for d in verify_fakenew_post_collection]
    num_of_verify_fakenew_post = len(verify_fakenew_posts)

    data = {
        "total_post" : num_of_total_post,
        "auto_post" : num_of_auto_post,
        "fake_new_post" : num_of_fakenew_post,
        "medical_post" : num_of_medical_post,
        "verify_fakenew_post" : num_of_verify_fakenew_post
    }
    return json_util.dumps(data)


@app.route('/posts/page/<int:page_num>', methods=['GET', 'POST'])
def show_pages(page_num):

    limit= 10
    offset= page_num*limit
    
    post_collection = mongo.db.posts.find({}).skip(offset).limit(limit)
    data = [d for d in post_collection]
    return json_util.dumps(data)

@app.route('/posts/single_post/<ObjectId:postID>', methods=['GET', 'POST'])
def get_single_post(postID):
    singlePost = mongo.db.posts.find_one({"_id": postID})
    if (singlePost):
        return json_util.dumps(singlePost)
    else:
        error = Error("Cant find the post", False)
        return(error.__dict__)


@app.route('/posts/related/<ObjectId:postID>', methods=['GET', 'POST'])
def get_related_post(postID):
    
    relationships = mongo.db["post-evidence"].find({"post_id": postID})
    # evidences = mongo.db["post-evidence"].find({})
    data = [d for d in relationships]
    # print("this is data",data)


    # single_evidence = mongo.db["evidences"].find({})
    # data1 = [d for d in single_evidence]
    # print('this is  evidence',data1)

    array_of_evidence = []
    for element in data:
        single_evidence = mongo.db["evidences"].find({"_id": element["evidence_id"]})
        single_evidence_toArray = [d for d in single_evidence]
        if len(single_evidence_toArray)==1:
            array_of_evidence.append(single_evidence_toArray[0])
        
    if len(array_of_evidence) >0:
        return json_util.dumps(array_of_evidence)
    # if (len(data)>0):
    #     return json_util.dumps(data)
    else:
        error = Error("Cant find the post", False)
        return(error.__dict__)



@app.route('/posts/update/<ObjectId:postID>', methods=['POST'])
def update_post(postID):
    
    data = request.get_json()

    verifyNews = False
    verifyNewsTouch = False

    medicalNews = False
    medicalNewsTouch = False

    fakeNews = False
    fakeNewsTouch = False

    AI_Check = False


    for key,value in data.items():
        # print(key,value,"hi")
        if key ==  "verifyNews":
            verifyNewsTouch = True
            if value == "true":
                verifyNews = True
        if key == "medicalNews":
            medicalNewsTouch = True
            if value == "true":
                medicalNews = True
        if key == "fakeNews":
            fakeNewsTouch = True
            if value == "true":
                fakeNews = True

    # post = {
    #     "is_medical":medicalNews,
    #     "is_auto" : AI_Check,
    #     "is_fakenew" :fakeNews,
    #     "is_verify_fakenew" : verifyNews,
    # }
    #print(post)

    cursorPost = mongo.db.posts.find({"_id":postID})
    array = [d for d in cursorPost]
    if (len(array) > 0):
        mongo.db.posts.update_one({"_id":postID},{
            "$set": {
                "is_medical":medicalNews,
                "is_auto" : AI_Check,
                "is_fakenew" :fakeNews,
                "is_verify_fakenew": verifyNews
            }
        })
        success = Success("Modify post Successfully", True)
        return(success.__dict__)
    else:
        error = Error("ID not found", False)
        return(error.__dict__)
    
    




@app.route('/posts/download_as_csv', methods=['GET', 'POST'])
def downloadCSV():

    posts_collection = mongo.db.posts.find({})
    data = [d for d in posts_collection]
    docs = pandas.DataFrame(columns=[])


    my_items = list()
    for num,doc in enumerate(data):
        doc["_id"] = str(doc["_id"])
        doc_id = doc["_id"]
        series_obj = pandas.Series(doc, name=doc_id)
        my_items.append(series_obj)

        #print(len(docs))
        # if num % 10 == 0:
        #     print (type(doc))
        #     print (type(doc["_id"]))
        #     print (num, "--", doc, "\n")
    #docs.to_csv("post.csv", ",")
    #print(my_items)
    docs = pandas.DataFrame(my_items)
    docs.to_csv("post.csv", ",")
    # return "hi"

    BASE_DIR = os.path.dirname(os.path.abspath(__name__))
    file = os.path.join(BASE_DIR, 'post.csv')
    return send_file(file, as_attachment=True)

@app.route('/posts/download_as_json', methods=['GET', 'POST'])
def downloadJSON():

    posts_collection = mongo.db.posts.find({})
    data = [d for d in posts_collection]
    docs = pandas.DataFrame(columns=[])

    my_items = list()
    for num,doc in enumerate(data):
        doc["_id"] = str(doc["_id"])
        doc_id = doc["_id"]
        series_obj = pandas.Series(doc, name=doc_id)
        #print(series_obj)
        #docs.concat(series_obj)
        my_items.append(series_obj)

    #print(my_items)
    docs = pandas.DataFrame(my_items)
    docs.to_csv("post.json")

    BASE_DIR = os.path.dirname(os.path.abspath(__name__))
    file = os.path.join(BASE_DIR, 'post.json')
    return send_file(file, as_attachment=True)


    
@app.route('/posts/upload_single_post/', methods=['POST'])
def upload_single_post():

    postData = request.get_json()

    comments_full = []
    #fetched_time = ""
    images = []
    is_auto = True
    is_fakenew = False
    is_medical = False
    is_verify_fakenew = False
    page_id = ""
    post_id = ""
    post_url = ""
    text = ""
    user_id = ""
    username = ""


    for key,value in postData.items():
        if key ==  "comments_full":
            comments_full = value
        if key == "iamges":
            images = value
        if key == "is_auto":
            is_auto = value
        if key == "is_fakenew":
            is_fakenew = value
        if key == "is_medical":
            is_medical = value
        if key == "is_verify_fakenew":
            is_verify_fakenew = value
        if key == "page_id":
            page_id = value
        if key == "post_id":
            post_id = value
        if key == "post_url":
            post_url = value
        if key == "text":
            text = value
        if key == "user_id":
            user_id = value
        if key == "username":
            username = value
    
    new_post = {    'comments_full' : comments_full, 
                    'images' : images,
                    'is_auto': is_auto,
                    'is_fakenew' : is_fakenew,
                    'is_medical' : is_medical,
                    'is_verify_fakenew' : is_verify_fakenew,
                    'page_id' : page_id,
                    'post_id' : post_id,
                    'post_url' : post_url,
                    'text' : text,
                    'user_id' : user_id,
                    'username' : username}
    try:
        mongo.db.posts.insert_one(new_post)
    except:
        error = Error("Fail to add", False)
        return(error.__dict__)
    success = Success("Sucess", True)
    return(success.__dict__)    


@app.route('/posts/upload_file_posts/', methods=['POST'])
def upload_file_post():

    file = request.form.get("file")
    csv = base64.b64decode(file).decode('utf-8').split('\n')

    
    for single_line in csv:
        comments_full = []   #must upload in seperate table
        #fetched_time = ""
        images = [] #must upload in seperate table
        is_auto = True
        is_fakenew = False
        is_medical = False
        is_verify_fakenew = False
        page_id = ""
        post_id = ""
        post_url = ""
        text = ""
        user_id = ""
        username = ""

        element=0
        tempString = ""
        for single_char in single_line:
            if single_char == "," or single_char=="\n":
                if (element == 0):
                    if (tempString == "false"):
                        is_auto = False
                if (element == 1):
                    if (tempString == "true"):
                        is_fakenew = True
                if (element == 2):
                    if (tempString == "true"):
                        is_medical = True
                if (element == 3):
                    if (tempString == "true"):
                        is_verify_fakenew = True
                if (element == 4):  
                    if (tempString != "page_id"):
                        page_id = tempString
                if (element == 5):
                    if (tempString != "post_id"):
                        post_id = tempString
                if (element == 6):
                    if (tempString != "post_url"):
                        post_url = tempString
                if (element == 7):
                    if (tempString != "text"):
                    #group_name, NOT the comments because cmt will be export in another file
                        text = tempString
                if (element == 8):
                    if (tempString != "user_id"):
                        user_id = tempString
                if (element == 9):
                    if (tempString != "username"):
                        username = tempString
                element += 1
                print(tempString)
                tempString = ""
            else:
                tempString += single_char

        # special case because  python doest loop over the last word
        if (tempString != "username"):
            username = tempString
        # special case because  python doest loop over the last word




        # print("tempstringnow",tempString)
        # print("this is username",username)
        if (username != ''):
            new_post = {    'comments_full' : comments_full, 
                            'images' : images,
                            'is_auto': is_auto,
                            'is_fakenew' : is_fakenew,
                            'is_medical' : is_medical,
                            'is_verify_fakenew' : is_verify_fakenew,
                            'page_id' : page_id,
                            'post_id' : post_id,
                            'post_url' : post_url,
                            'text' : text,
                            'user_id' : user_id,
                            'username' : username
                        }
            # print(new_post)
            try:        
                mongo.db.posts.insert_one(new_post)
            except:
                error = Error("Fail to add", False)
                return(error.__dict__)
    success = Success("Sucess", True)
    return(success.__dict__)    


