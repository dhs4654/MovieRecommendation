from flask import *
import json
import time
from config import configs
from app.models import db, MovieInfo, User, PersonalRatings, RecommendResult
from flasgger import Swagger, swag_from
from app.user import users_dp
from app.movieInfo import movies_dp
from app.personalRatings import pr_dp
from app.recommendResult import recommend_dp
from flask_socketio import SocketIO, emit
app = Flask(__name__)
# socketio = SocketIO()
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

name_space = '/websocket'  
swagger = Swagger(app)
sockets = Sockets()


def init_settings():
    app.config.from_object(configs['database'])
    app.config.from_object(configs['development'])
    app.config.from_object(configs['testing'])
    app.config.from_object(configs['default'])
    db.init_app(app)
    app.register_blueprint(users_dp)
    app.register_blueprint(movies_dp)
    app.register_blueprint(pr_dp)
    app.register_blueprint(recommend_dp)
    sockets.init_app(app)
    

# Cross-domain
@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ 


def add_database_rules():
    with app.app_context():  
        db.drop_all()  # 删除所有表 
        db.create_all()
        movie1 = MovieInfo(name='肖申克的救赎', releaseTime = '1994-09-10',director='弗兰克·德拉邦特', majorActors='蒂姆·罗宾斯, 摩根·弗里曼, 鲍勃·冈顿, 威廉姆·赛德',
                      img='app/statics/images/xskdjs.jpeg', averageScore=9.7, numberOfParticipants=2748520,
                      desc='一场谋杀案使银行家安迪（蒂姆•罗宾斯 Tim Robbins 饰）蒙冤入狱', movieType ='剧情/犯罪')
        movie2 = MovieInfo(name = '泰坦尼克号', releaseTime = '1997-12-19',director='詹姆斯·卡梅隆', majorActors='莱昂纳多·迪卡普里奥, 凯特·温丝莱特, 比利·赞恩,凯西·贝茨',
                      img='app/static/images/2.jpg', averageScore=9.5, numberOfParticipants=2020737,
                      desc='1912年4月10日, 号称 “世界工业史上的奇迹”的豪华客轮泰坦尼克号开始了自己的处女航', movieType ='剧情/爱情')
        db.session.add_all([movie1, movie2])
        db.session.commit()
        user1 = User(name = '张三',password='12345611')
        user2 = User(name = 'admin',password='12345678')
        db.session.add_all([user1, user2])
        db.session.commit() 
        pr1 = PersonalRatings(userId=6041, movieId=318, score=0.0, scoringTime='2022-12-21')
        pr2 = PersonalRatings(userId=6041, movieId=1721, score=0.0, scoringTime='2022-12-21')
        pr3 = PersonalRatings(userId=6041, movieId=1682, score=0.0, scoringTime='2022-12-21')
        pr4 = PersonalRatings(userId=6041, movieId=2571, score=0.0, scoringTime='2022-12-21')
        pr5 = PersonalRatings(userId=6041, movieId=356, score=0.0, scoringTime='2022-12-21')
        pr6 = PersonalRatings(userId=6041, movieId=3252, score=0.0, scoringTime='2022-12-21')
        db.session.add_all([pr1, pr2, pr3, pr4, pr5, pr6])
        db.session.commit() 
        # rd1 = RecommendResult(name='肖申克的救赎', releaseTime = '1994-09-10',img='../statics/images/xskdjs.jpeg', averageScore='9.7', numberOfParticipants='2748520',desc='一场谋杀案使银行家安迪（蒂姆•罗宾斯 Tim Robbins 饰）蒙冤入狱', movieType ='剧情/犯罪')
        # rd2 = RecommendResult(userId=2, movieId=2, averageScore=10.0)
        # db.session.add_all([rd1])
        # db.session.commit() 

def findmovie(string, name):

    start_pos = string.find(name)
    res = {}
    res['name'] = name
    i = string.find("poster", start_pos)
    i += 10
    j = i
    while string[j] != '\'':
        j += 1
    poster = string[i:j]
    res['img'] = poster
    i = string.find("genre",i)
    i += 9
    j = i
    while string[j] != '\'':
        j += 1
    genre = string[i:j]
    res['movieType'] = genre
    i = string.find("description",i)
    i += 15
    j = i
    while string[j] != '\'':
        j += 1
    description = string[i:j]
    res['desc'] = description
    i = string.find("doubanRating",i)
    i += 16
    j = i
    while string[j] != '\'':
        j += 1
    doubanRating = string[i:j]
    res['averageScore'] = doubanRating
    i = string.find("doubanVoters", i)
    i += 16
    j = i
    while string[j] != '\'':
        j += 1
    doubanVoters = string[i:j]
    res['numberOfParticipants'] = doubanVoters
    i = string.find("dateReleased", i)
    i += 16
    j = i
    while string[j] != '\'':
        j += 1
    dateReleased = string[i:j]
    res['releaseTime'] = dateReleased
    return res

def postRecommendResult(name):
    f = open("./data.txt","r",encoding="utf-8") 
    string = f.read()
    recommend_info = findmovie(string, name)
    name = recommend_info['name']
    releaseTime = recommend_info['releaseTime']
    img = recommend_info['img']
    averageScore = recommend_info['averageScore']
    numberOfParticipants = recommend_info['numberOfParticipants']
    desc = recommend_info['desc']
    movieType = recommend_info['movieType']

    if not all([name, releaseTime, img, averageScore, numberOfParticipants,desc, movieType]):
        return jsonify({
                            'code': 400, 
                            'msg': '参数不完整'
                        })
    movie = RecommendResult(name=name, releaseTime=releaseTime, img=img, averageScore=averageScore, numberOfParticipants=numberOfParticipants, desc=desc, movieType=movieType)
    db.session.add(movie)
    db.session.commit()
    return jsonify({
                        'code': 200, 
                        'msg': '添加成功'
                    })



@sockets.route('/websocket')
def communicate(ws):
    while not ws.closed:
        prs_list = PersonalRatings.query.all()
        prs_all = []
        for pr in prs_list:
            data = {
                'id': pr.id,
                'userId': pr.userId,
                'movieId': pr.movieId,
                'score': pr.score,
                'scoringTime': pr.scoringTime,
            }
            prs_all.append(data)
        flag = False
        for item in prs_all:
            if item['score'] != 0.0:
                flag = True
                break
        if flag:
            string = ""
            for item in prs_all:
                string+=str(item['userId'])+'|'+str(item['movieId'])+'|'+str(int(item['score'] // 2))+','
            ws.send(str(string))
            for id in range(1,7):
                prs_info = PersonalRatings.query.get(id)
                prs_info.score = 0.0
                db.session.commit()
            msg = ws.receive()
            print("----------------------------------------------------")
            res = json.loads(msg)
            print(res)
            for key, val in res.items():
                name = val
                postRecommendResult(name)
            ws.close()
            break
        time.sleep(20)
        
        # ws.send(str("hello world")) 
    return 


@app.route('/')
def index():
    return 'hello index'

if __name__ == '__main__':
    init_settings()
    # add_database_rules()
    # socketio.run(app, host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=5000, debug = True)     
    server = pywsgi.WSGIServer(('0.0.0.0',5000), application=app, handler_class=WebSocketHandler)
    print('server started')
    server.serve_forever()
