from flask import request, jsonify

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from time import time

from app import app, db
from models import *

@app.route('/')
def index():
  return 'Hi'

@app.route('/auth/signup', methods=['POST'])
def signup():
  username = request.json["username"]
  email = request.json["email"]
  password = request.json["password"]

  if User.query.filter((User.username == username) | \
    (User.email==email)).first():
    return jsonify({
      "error": "Already exists"
    })

  u = User(username=username, email=email)
  u.set_password(password)
  
  chain = Blockchain(user_id=u.id)
  u.blockchain = chain.id

  db.session.add(u)
  db.session.add(chain)

  db.session.commit()

  access_token = create_access_token(identity = u.id)
  refresh_token = create_refresh_token(identity = u.id)

  return jsonify({
    "message": "ok",
    'access_token': access_token,
    'refresh_token': refresh_token
  })

@app.route('/auth/login', methods=['POST'])
def login():
  username = request.json["username"]
  password = request.json["password"]

  u = User.query.filter_by(username=username).first()

  if not u:
    return jsonify({
      "error": "Username not found"
    })
  
  elif u.check_password(password):
    access_token = create_access_token(identity = u.id)
    refresh_token = create_refresh_token(identity = u.id)
    return jsonify({
      "message": "ok",
      'access_token': access_token,
      'refresh_token': refresh_token
    })

  else:
    return jsonify({
      "error": "Username or password is incorrect"
    })


@app.route('/users')
@jwt_refresh_token_required
def users():
  return jsonify([x.as_dict for x in User.query.all()])
  

@app.route('/transactions/add', methods=["POST"])
@jwt_refresh_token_required
def transactions():
  private_key = request.json["fromAddress"]
  to_address = request.json["toAddress"]
  amount = request.json["amount"]

  sender = User.query.filter_by(private_key=private_key).first()
  from_address = sender.public_key
  receiver = User.query.filter_by(public_key=to_address).first()
  
  timestamp = int(time())

  sender_blockchain = Blockchain.query.filter_by(id=sender.blockchain).first()
  t1 = Transaction(timestamp=timestamp, from_address=from_address, to_address=to_address, amount=amount)
  sender_blockchain.pending_transactions.append(t1)

  receiver_blockchain = Blockchain.query.filter_by(id=receiver.blockchain).first()
  t2 = Transaction(timestamp=timestamp, from_address=from_address, to_address=to_address, amount=amount)  
  receiver_blockchain.pending_transactions.append(t2)

  db.session.add(t1)
  db.session.add(t2)
  db.session.add(sender_blockchain)
  db.session.add(receiver_blockchain)
  db.session.commit()

  return jsonify({
    "message": "ok"
  })

@app.route('/block/add', methods=["POST"])
def block():
  previous_hash = request.json["previousHash"]
  _hash = request.json["hash"]
  timestamp = request.json["timestamp"]
  transactions = request.json["transactions"]
  address = transactions[0]["toAddress"]
  amount = 0

  for transaction in transactions:
    amount += transaction["amount"]

  u = User.query.filter_by(public_key=address).first()
  blockchain = Blockchain.query.filter_by(id=u.blockchain).first()

  block = Block(timestamp=timestamp, previous_hash=previous_hash, hash=_hash, blockchain_id=blockchain.id)

  tr = Transaction(timestamp=timestamp, amount=amount, from_address=None, to_address=address)

  db.session.add(tr)

  for transaction in Transaction.query.filter_by(blockchain_id=blockchain.id, block_id=None):
    transaction.block_id = block.id
    transaction.blockchain_id = None

    print(block.transactions)
    block.transactions.append(transaction)

    db.session.add(transaction)

  block.transactions.append(tr)

  db.session.add(block)  
  db.session.commit()

  return jsonify({
    "message": "ok"
  })
