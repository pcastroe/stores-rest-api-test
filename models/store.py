from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # lazy = 'dynamic' means that when you want to use the items, you have to fetch them
    # if lazy = 'dynamic' then calling the method is slower but creating the object is faster
    # if we remove lazy = 'dynamic', it fetches them when you create the object
    # back_populates="store" evita error
    items = db.relationship('ItemModel', lazy='dynamic', back_populates="store")
    #items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
