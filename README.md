# Jack references
pip install -r requirements.txt
flask db upgrade

set FLASK_APP=microblog.py
export FLASK_APP=microblog.py
flask shell
users = User.query.all()

db.session.add_all([bg1,bg2])
db.session.delete(xx)
db.engine.execute("DROP TABLE blogger CASCADE")



flask --debug run --host=0.0.0.0
----------------------------------