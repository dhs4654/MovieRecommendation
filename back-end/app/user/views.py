import random
from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
import re
from app.models import User, db
from . import views
from . import users_dp

# users_dp = Blueprint('users_dp', __name__, url_prefix='/userLibrary')

api = Api(users_dp)


class usersView(Resource):
    # 查看所有用户
    def get(self):
        users_list = User.query.all()     # 获取所有对象
        users_all = []
        for user in users_list:
            data = {
                'id': user.id,
                'name': user.name,
                'password': user.password,
            }
            users_all.append(data)
        return jsonify({
                            'code': 200, 
                            'msg': '用户列表获取成功',
                            'data': users_all
                        })
    # 添加
    def post(self):
        args = request.json
        name = args.get('name')
        password = args.get('password')
        if not all([name, password]):
            return jsonify({
                                'code': 400, 
                                'msg': '参数不完整'
                            })
        users = User(name=name, password=password)
        db.session.add(users)
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '添加成功'
                        })


class usersInfoView(Resource):
    # 获取一条对象
    def get(self, id):
        users_info = User.query.get(id)   
        if not users_info:
            return jsonify({
                                'code': 400, 
                                'msg': '用户不存在'
                            })
        return jsonify({
            'code': 200,
            'msg': '用户获取成功',
            'data': {
                'id': users_info.id,
                'name': users_info.name,
                'password': users_info.password
            }
        })
    # 修改一条用户
    def put(self, id):
        
        args = request.json
        
        name = args.get('name')
        password = args.get('password')
        users_info = User.query.get(id)
        
        if not users_info:
            return jsonify({
                                'code': 400, 
                                'msg': '用户不存在'
                           })
        
         # 字段值不为空,且修改后的值发生改变 才进行修改
        if name and name != users_info.name:    
            users_info.name = name
        if password and password != users_info.password:
            users_info.password = password

        
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '修改成功'
                        })
    # 删除一条数据
    def delete(self, id):
        
        users_info = User.query.get(id)
        
        if not users_info:
            return jsonify({    
                                'code': 400, 
                                'msg': '用户不存在'
                            })
        User.query.filter(User.id == id).delete()
        
        db.session.commit()
        return jsonify({
                            'code': 200, 
                            'msg': '删除成功'
                        })
 
class userRegisterView(Resource):
    def post(self):

        res = {
            "code": 0,
            "msg": "注册成功",
            "data": {}
        }

        name = request.form.get("name")
        password = request.form.get("password")
        users_list = User.query.all()
        users_all = []
        for user in users_list:
            print(user.name)
            data = {
                'id': user.id,
                'name': user.name,
                'password': user.password,
            }
            users_all.append(data)
        flag = False
        for user in users_all:
            if name == user['name']:
                flag = True
                break

        if not name or not password:
            res['code'] = -1
            res['msg'] = '账号密码不能为空'
            return make_response(res)
        elif len(name) >= 16 or len(password) >= 16:
            res['code'] = -2
            res['msg'] = '用户名/密码长度不能超多16位'
            return make_response(res)
        elif not re.findall(r'^[a-zA-Z0-9]+$', name):
            res['code'] = -3
            res['msg'] = '用户名存在非法字符'
            return make_response(res)
        elif not flag:
            addUser = User(name=name, password=password)
            db.session.add(addUser)
            db.session.commit()
            users = {
                'name': name,
                'password': password
            }
            res['data'] = users
            return make_response(res)
        else:
            res['code'] = -4
            res['msg'] = '该用户已经存在'
            return make_response(res)
    
            
class userLoginView(Resource):
    def post(self):

        res = {
            "code": 0,
            "msg": "登录成功",
            "data": {}
        }
        name = request.form.get("name")
        password = request.form.get("password")

        if len(name) >= 16 or len(password) >= 16:
            res['code'] = -2
            res['msg'] = '用户名/密码长度不能超多16位'
            return make_response(res)
        user = User.query.filter_by(name=name, password=password).first()
        if name == user.name and password == user.password:
            res['data']['name'] = name
            res['data']['password'] = password
            return make_response(res)
        
        res['code'] = -1
        res['msg'] = "请填写正确的账号密码"
        return make_response(res)



api.add_resource(usersView, '/users')
api.add_resource(usersInfoView, '/users/<int:id>')
api.add_resource(userRegisterView, '/register')
api.add_resource(userLoginView, '/login')

