import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.models import MovieInfo, db
from . import views
from . import movies_dp

# movies_dp = Blueprint('movies_dp', __name__, url_prefix='/movieLibrary')

api = Api(movies_dp)


class moviesView(Resource):
    # 查看所有电影
    def get(self):
        movies_list = MovieInfo.query.all()     # 获取所有对象
        movies_all = []
        for movie in movies_list:
            data = {
                'id': movie.id,
                'name': movie.name,
                'releaseTime': movie.releaseTime,
                'director': movie.director,
                'majorActors': movie.majorActors,
                'img': movie.img,
                'averageScore': movie.averageScore,
                'numberOfParticipants': movie.numberOfParticipants,
                'desc': movie.desc,
                'movieType': movie.movieType,
            }
            movies_all.append(data)
        return jsonify({
                            'code': 200, 
                            'msg': '电影列表获取成功',
                            'data': movies_all
                        })
    # 添加
    def post(self):
        args = request.json
        name = args.get('name')
        releaseTime = args.get('releaseTime')
        director = args.get('director')
        majorActors = args.get('majorActors')
        img = args.get('img')
        averageScore = args.get('averageScore')
        numberOfParticipants = args.get('numberOfParticipants')
        desc = args.get('desc')
        movieType = args.get('movieType')

        if not all([name, releaseTime, director, majorActors, img, averageScore, numberOfParticipants,desc, movieType]):
            return jsonify({
                                'code': 400, 
                                'msg': '参数不完整'
                            })
        movie = MovieInfo(name=name, releaseTime=releaseTime, director=director, majorActors=majorActors, img=img, 
                        averageScore=averageScore, numberOfParticipants=numberOfParticipants, desc=desc, movieType=movieType)
        db.session.add(movie)
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '添加成功'
                        })


class moviesInfoView(Resource):
    # 获取一条对象
    def get(self, id):
        movies_info = MovieInfo.query.get(id)   
        if not movies_info:
            return jsonify({
                                'code': 400, 
                                'msg': '电影不存在'
                            })
        return jsonify({
            'code': 200,
            'msg': '电影获取成功',
            'data': {
                'id': movies_info.id,
                'name': movies_info.name,
                'releaseTime': movies_info.releaseTime,
                'director': movies_info.director,
                'majorActors': movies_info.majorActors,
                'img': movies_info.img,
                'averageScore': movies_info.averageScore,
                'numberOfParticipants': movies_info.numberOfParticipants,
                'desc': movies_info.desc,
                'movieType': movies_info.movieType,
            }
        })
    # 修改一条电影
    def put(self, id):
        
        args = request.json
        name = args.get('name')
        releaseTime = args.get('releaseTime')
        director = args.get('director')
        majorActors = args.get('majorActors')
        img = args.get('img')
        averageScore = args.get('averageScore')
        numberOfParticipants = args.get('numberOfParticipants')
        desc = args.get('desc')
        movieType = args.get('movieType')

        movies_info = MovieInfo.query.get(id)
        
        if not movies_info:
            return jsonify({
                                'code': 400, 
                                'msg': '电影不存在'
                           })
        
         # 字段值不为空,且修改后的值发生改变 才进行修改
        if name and name != movies_info.name:    
            movies_info.name = name
        if releaseTime and releaseTime != movies_info.releaseTime:
            movies_info.releaseTime = releaseTime
        if director and director != movies_info.director:
            movies_info.director = director
        if majorActors and majorActors != movies_info.majorActors:
            movies_info.majorActors = majorActors
        if img and img != movies_info.img:
            movies_info.img = img
        if averageScore and averageScore != movies_info.averageScore:
            movies_info.averageScore = averageScore
        if numberOfParticipants and numberOfParticipants != movies_info.numberOfParticipants:
            movies_info.numberOfParticipants = numberOfParticipants
        if desc and desc != movies_info.desc:
            movies_info.desc = desc
        if movieType and movieType != movies_info.movieType:
            movies_info.movieType = movieType

        
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '修改成功'
                        })
    # 删除一条数据
    def delete(self, id):
        
        movies_info = MovieInfo.query.get(id)
        
        if not movies_info:
            return jsonify({    
                                'code': 400, 
                                'msg': '电影不存在'
                            })
        MovieInfo.query.filter(movies_info.id == id).delete()
        
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '删除成功'
                        })
 
api.add_resource(moviesView, '/movies')
api.add_resource(moviesInfoView, '/movies/<int:id>')

