import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

class Config:
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'news_db', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #MONGOALCHEMY_CONNECTION_STRING = 'mongodb+srv://edwardly1002:Ltb123%21%40%23@cluster0.lqbbu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    MONGOALCHEMY_DATABASE = 'visualize'
    MONGO_URI = 'mongodb+srv://fbfighter:fbfighter@fb-topic.ixbkp2u.mongodb.net/visualize?retryWrites=true&w=majority'
    SECRET_KEY='vnepfl'
    SECURITY_PASSWORD_SALT='hoangdzung'
    SECURITY_PASSWORD_HASH='sha512_crypt'
    SECURITY_POST_LOGIN_VIEW='fakenews'
    SECURITY_POST_LOGOUT_VIEW='fakenews'