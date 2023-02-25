import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app.models import PersonalRatings, db
from . import views
from . import pr_dp

api = Api(pr_dp)


class prsView(Resource):
    def get(self):
        prs_list = PersonalRatings.query.all()     # 获取所有对象
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
        return jsonify({
                            'code': 200, 
                            'msg': '个人评分列表获取成功',
                            'data': prs_all
                        })
    # 添加
    def post(self):
        args = request.json
        userId = args.get('userId')
        movieId = args.get('movieId')
        score = args.get('score')
        scoringTime = args.get('scoringTime')

        if not all([userId, movieId, score, scoringTime]):
            return jsonify({
                                'code': 400, 
                                'msg': '参数不完整'
                            })
        pr = PersonalRatings(userId=userId, movieId=movieId, score=score, scoringTime=scoringTime)
        db.session.add(pr)
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '添加成功'
                        })


class prsInfoView(Resource):
    # 获取一条对象
    def get(self, id):
        prs_info = PersonalRatings.query.get(id)   
        if not prs_info:
            return jsonify({
                                'code': 400, 
                                'msg': '电影不存在'
                            })
        return jsonify({
            'code': 200,
            'msg': '电影获取成功',
            'data': {
                'id': prs_info.id,
                'userId': prs_info.userId,
                'movieId': prs_info.movieId,
                'score': prs_info.score,
                'scoringTime': prs_info.scoringTime,
            }
        })
    # 修改一条电影
    def put(self, id):
        
        args = request.json
        userId = args.get('userId')
        movieId = args.get('movieId')
        score = args.get('score')
        scoringTime = args.get('scoringTime')
        print("---------------------------------------------------")
        print(args)
        prs_info = PersonalRatings.query.get(id)
        
        if not prs_info:
            return jsonify({
                                'code': 400, 
                                'msg': '电影不存在'
                           })
        
         # 字段值不为空,且修改后的值发生改变 才进行修改
        if userId and userId != prs_info.userId:    
            prs_info.userId = userId
        if movieId and movieId != prs_info.movieId:
            prs_info.movieId = movieId
        if score and score != prs_info.score:
            prs_info.score = score
        if scoringTime and scoringTime != prs_info.scoringTime:
            prs_info.scoringTime = scoringTime

        
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '修改成功'
                        })
    # 删除一条数据
    def delete(self, id):
        
        prs_info = PersonalRatings.query.get(id)
        
        if not prs_info:
            return jsonify({    
                                'code': 400, 
                                'msg': '电影不存在'
                            })
        PersonalRatings.query.filter(prs_info.id == id).delete()
        
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '删除成功'
                        })
 
api.add_resource(prsView, '/prs')
api.add_resource(prsInfoView, '/prs/<int:id>')
