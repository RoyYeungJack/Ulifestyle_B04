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



selected_type_id = form.type_id.data
selected_type = BlogType.query.get(selected_type_id)
description = selected_type.description
----------------------------------

#USE the test_blog.py to test the db
#DON'T USE THE test_data.py or tests.py