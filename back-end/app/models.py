from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
 
db = SQLAlchemy()
class MovieInfo(db.Model):
    __tablename__ = 'movieInfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), comment = '电影名称')
    releaseTime = db.Column(db.String(128), comment = '电影上映时间')
    director = db.Column(db.String(128), comment = '电影导演')
    majorActors = db.Column(db.String(128), comment = '主要演员')
    img = db.Column(db.String(128), comment='电影宣传海报')
    averageScore = db.Column(db.Float, comment = '电影平均评分')
    numberOfParticipants = db.Column(db.Integer, comment = '参评人数')
    desc = db.Column(db.String(128), comment = '电影简介')
    movieType = db.Column(db.String(128), comment = '电影类型')
    
    def __repr__(self):
        return 'Movie : %s' % self.name


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), comment = '用户名')
    password = db.Column(db.String(128), comment = '登录密码')

    def __repr__(self):
        return 'User : %s' % self.name

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
		    for col in class_mapper(obj.__class__).mapped_table.c)	

class PersonalRatings(db.Model):
    __tablename__ = 'personalRatings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, comment = '用户id')
    movieId = db.Column(db.Integer, comment = '电影id')
    score = db.Column(db.Float, comment = '用户评分')
    scoringTime = db.Column(db.String(128), comment = '评分时间')

    def __repr__(self):
        return 'score : %s'% self.score

class RecommendResult(db.Model):
    __tablename__ = 'recommendResult'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), comment = '电影名称')
    releaseTime = db.Column(db.String(128), comment = '电影上映时间')
    img = db.Column(db.String(128), comment='电影宣传海报')
    averageScore = db.Column(db.String(128), comment = '电影平均评分')
    numberOfParticipants = db.Column(db.String(128), comment = '参评人数')
    desc = db.Column(db.String(128), comment = '电影简介')
    movieType = db.Column(db.String(128), comment = '电影类型')


    def __repr__(self):
        return 'score : %s'% self.averageScore
