from app import db
from models import *

db.create_all()

u = User(username="23", email="qwggg@er.com")
u.set_password("qwerty")
chain = Blockchain(user_id=u.id)
u.blockchain = chain.id

db.session.add(u)
db.session.add(chain)
db.session.commit()
