import os,sys
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)               # 创建程序实例
app.config['SECRET_KEY'] = 'dev'

# 数据库配置
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)        # 生成扩展对象

# 登录管理
login_manager = LoginManager(app)
@login_manager.user_loader      # 没有括号
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user
login_manager.login_view = 'login'

@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

from watchlist import views,errors,commands