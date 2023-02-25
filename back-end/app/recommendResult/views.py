import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.models import RecommendResult, db
from . import views
from . import recommend_dp

# recommend_dp = Blueprint('recommend_dp', __name__, url_prefix='/movieLibrary')

api = Api(recommend_dp)


class recommendView(Resource):
    # 查看所有推荐
    def get(self):
        recommend_list = RecommendResult.query.all()     # 获取所有对象
        recommend_all = []
        for movie in recommend_list:
            data = {
                'id': movie.id,
                'name': movie.name,
                'releaseTime': movie.releaseTime,
                'img': movie.img,
                'averageScore': movie.averageScore,
                'numberOfParticipants': movie.numberOfParticipants,
                'desc': movie.desc,
                'movieType': movie.movieType,
            }
            recommend_all.append(data)
        return jsonify({
                            'code': 200, 
                            'msg': '推荐列表获取成功',
                            'data': recommend_all
                        })
    # 添加
    def post(self):
        args = request.json
        name = args.get('name')
        releaseTime = args.get('releaseTime')
        img = args.get('img')
        averageScore = args.get('averageScore')
        numberOfParticipants = args.get('numberOfParticipants')
        desc = args.get('desc')
        movieType = args.get('movieType')

        if not all([name, releaseTime, img, averageScore, numberOfParticipants,desc, movieType]):
            return jsonify({
                                'code': 400, 
                                'msg': '参数不完整'
                            })
        movie = RecommendResult(name=name, releaseTime=releaseTime, img=img, averageScore=averageScore,
                             numberOfParticipants=numberOfParticipants, desc=desc, movieType=movieType)
        db.session.add(movie)
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '添加成功'
                        })


class recommendInfoView(Resource):
    # 获取一条对象
    def get(self, id):
        recommend_info = RecommendResult.query.get(id)   
        if not recommend_info:
            return jsonify({
                                'code': 400, 
                                'msg': '推荐电影不存在'
                            })
        return jsonify({
            'code': 200,
            'msg': '推荐电影获取成功',
            'data': {
                'id': recommend_info.id,
                'name': recommend_info.name,
                'releaseTime': recommend_info.releaseTime,
                'img': recommend_info.img,
                'averageScore': recommend_info.averageScore,
                'numberOfParticipants': recommend_info.numberOfParticipants,
                'desc': recommend_info.desc,
                'movieType': recommend_info.movieType,
            }
        })
    # 修改一条推荐
    def put(self, id):
        
        args = request.json
        name = args.get('name')
        releaseTime = args.get('releaseTime')
        img = args.get('img')
        averageScore = args.get('averageScore')
        numberOfParticipants = args.get('numberOfParticipants')
        desc = args.get('desc')
        movieType = args.get('movieType')

        recommend_info = RecommendResult.query.get(id)
        
        if not recommend_info:
            return jsonify({
                                'code': 400, 
                                'msg': '推荐电影不存在'
                           })
        
         # 字段值不为空,且修改后的值发生改变 才进行修改
        if name and name != recommend_info.name:    
            recommend_info.name = name
        if releaseTime and releaseTime != recommend_info.releaseTime:
            recommend_info.releaseTime = releaseTime
        if img and img != recommend_info.img:
            recommend_info.img = img
        if averageScore and averageScore != recommend_info.averageScore:
            recommend_info.averageScore = averageScore
        if numberOfParticipants and numberOfParticipants != recommend_info.numberOfParticipants:
            recommend_info.numberOfParticipants = numberOfParticipants
        if desc and desc != recommend_info.desc:
            recommend_info.desc = desc
        if movieType and movieType != recommend_info.movieType:
            recommend_info.movieType = movieType

        
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '修改成功'
                        })
    # 删除一条数据
    def delete(self, id):
        
        recommend_info = RecommendResult.query.get(id)
        
        if not recommend_info:
            return jsonify({    
                                'code': 400, 
                                'msg': '推荐电影不存在'
                            })
        RecommendResult.query.filter(recommend_info.id == id).delete()
        
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '删除成功'
                        })

class getRecommendByNameView(Resource):
    
    def post(self, name):
        f = open("./data.txt","r",encoding="utf-8") 
        string = f.read()
        recommend_info = findmovie(name)
        name = recommend_info.get('name')
        releaseTime = recommend_info.get('releaseTime')
        img = recommend_info.get('img')
        averageScore = recommend_info.get('averageScore')
        numberOfParticipants = recommend_info.get('numberOfParticipants')
        desc = recommend_info.get('desc')
        movieType = recommend_info.get('movieType')

        if not all([name, releaseTime, img, averageScore, numberOfParticipants,desc, movieType]):
            return jsonify({
                                'code': 400, 
                                'msg': '参数不完整'
                            })
        movie = RecommendResult(name=name, releaseTime=releaseTime, img=img, averageScore=averageScore,
                             numberOfParticipants=numberOfParticipants, desc=desc, movieType=movieType)
        db.session.add(movie)
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '添加成功'
                        })

    def findmovie(name):
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
        i = string.find("doubanVoters",i)
        i += 16
        j = i
        while string[j] != '\'':
            j += 1
        doubanVoters = string[i:j]
        res['numberOfParticipants'] = doubanVoters
        i = string.find("dateReleased",i)
        i += 16
        j = i
        while string[j] != '\'':
            j += 1
        dateReleased = string[i:j]
        res['releaseTime'] = dateReleased
        return res


api.add_resource(recommendView, '/recommend')
api.add_resource(recommendInfoView, '/recommend/<int:id>')
api.add_resource(getRecommendByNameView, '/recommend/<string:name>')
