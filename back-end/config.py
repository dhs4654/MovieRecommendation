import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:  # 基本配置类
    SECRET_KEY = os.getenv('SECRET_KEY', 'some secret words')
    ITEMS_PER_PAGE = 10


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(BaseConfig):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

class DatabaseConfig(BaseConfig):
    SECRET_KEY = 'network2022'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:network2022@localhost:3306/MovieRecommendation'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # 是否追踪数据库发生的变化
    SQLALCHEMY_ECHO = True    # 是否在控制台打印输出sql语句
    JSON_AS_ASCII = False    # 返回JSON的时候不转义中文

configs = {
    'database': DatabaseConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}