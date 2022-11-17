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








# @main.route('/login/authenticate', methods=['POST'])
# def login_authentication():
#     inputEmail = request.args.get('email')
#     inputPassword = request.args.get('password')
    
#     user_collection = mongo.db.users.find({})

#     userList = User.query.filter(User.email == inputEmail, User.password == inputPassword).all()
#     if (len(userList) >0):
#         return json.dumps([singleUser.to_dict() for singleUser in userList])
#     return json.dumps([])

# @main.route('/signup', methods=['POST'])
# def signup():

#     data = request.get_json()
   
#     # print(dir(jsonData))
#     # #print(jsonData.keys)
#     # for key, value in jsonData.items():
#     #     print(key, value)
#     #     if key== "email":
#     #         print("above is my email")
#     # print(jsonData.keys())

#     # return jsonData

#     signupEmail = ""
#     signupPassword = ""
#     for key,value in data.items():
#         if key ==  "email":
#             signupEmail = value
#         if key == "password":
#             signupPassword = value

#     userList = User.query.filter(User.email == signupEmail).all()
    
#     if (len(userList) >0):
#         error = Error("error","Email has already been used")
#         return json.dumps(error.__dict__)
    
#     newUser = User(email=signupEmail,password=signupPassword,active=True)
#     db_admin.session.add(newUser)
#     db_admin.session.commit()
#     success = Success("success","Successfully created user")
#     return json.dumps(success.__dict__)
    







@app.route('/posts/page/<int:page_num>', methods=['GET', 'POST'])
def show_pages(page_num):

    limit= 1
    offset= page_num*limit
    
    post_collection = mongo.db.posts.find({}).skip(offset).limit(limit)
    data = [d for d in post_collection]
    return json.loads(json_util.dumps(data))

@app.route('/posts/single_post/<ObjectId:postID>', methods=['GET', 'POST'])
def show_single_post(postID):
    singlePost = mongo.db.posts.find_one_or_404({"_id": postID})
    if (singlePost):
        return json.loads(json_util.dumps(singlePost))




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

        for single_char in single_line:
            if single_char == "," or single_char=="\n":
                if (element == 0):
                    if (tempString == "0"):
                        is_auto = False
                if (element == 1):
                    if (tempString == "1"):
                        is_fakenew = True
                if (element == 2):
                    if (tempString == "1"):
                        is_medical = True
                if (element == 3):
                    if (tempString == "1"):
                        is_verify_fakenew = True
                if (element == 4):  
                    page_id = tempString
                if (element == 5):
                    post_id = tempString
                if (element == 6):
                    post_url = tempString
                if (element == 7):
                    #group_name, NOT the comments because cmt will be export in another file
                    text = tempString
                if (element == 8):
                    user_id = tempString
                if (element == 9):
                    username = tempString
                element += 1
                print(tempString)
                tempString = ""
            else:
                tempString += single_char    

   
    
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


