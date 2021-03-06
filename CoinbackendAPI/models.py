from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  blockchain = db.Column(db.Integer, db.ForeignKey('blockchain.id'))
  public_key = db.Column(db.String(128))
  private_key = db.Column(db.String(128))
  password_hash = db.Column(db.String(128))

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return "User: {}".format(self.username)

class Blockchain(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  blocks = db.relationship('Block', backref='blockchain', lazy="dynamic")
  pending_transactions = db.relationship('Transaction', backref='blockchain', lazy="dynamic")

  def get_balance(self):
    balance = 0
    address = User.query.filter_by(id=self.user_id).first().public_key

    for block in self.blocks:
      #block = Block.query.filter_by(id=block_id).first()
      for transaction in block.transactions:
        #transaction = Transaction.query.filter_by(id=transaction_id).first()
        if transaction.from_address == address:
          balance -= transaction.amount
        elif transaction.to_address == address:
          balance += transaction.amount

    return balance

class Block(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.Integer)
  blockchain_id = db.Column(db.Integer, db.ForeignKey('blockchain.id'))
  transactions = db.relationship('Transaction', backref='block', lazy="dynamic")
  hash = db.Column(db.String(128))
  previous_hash = db.Column(db.String(128))


  # def add_transaction(self):
    

class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  timestamp = db.Column(db.Integer)
  block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
  blockchain_id = db.Column(db.Integer, db.ForeignKey('blockchain.id'))
  from_address = db.Column(db.String(128))
  to_address = db.Column(db.String(128))
  amount = db.Column(db.Integer)