from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager  
from app import app
from model.model import db
 
# 创建命令行对象
manage = Manager(app)
 
# 创建迁移对象
migrate = Migrate(app, db)
 
# 添加迁移命令到命令行对象
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()
