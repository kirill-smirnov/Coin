from flask_sqlalchemy import Model

forbidden = ['password', 'password_hash']

class CustomModel(Model):
  @property
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns if not c.name in forbidden}