from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PAx_!@ZRlb*blgwc9vu?7w%P0&Fqq=Y_'
app.config['MYSQL_DATABASE_DB'] = 'gallery'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)