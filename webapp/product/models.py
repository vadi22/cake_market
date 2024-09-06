from webapp.db import db
from sqlalchemy.orm import relationship
from datetime import datetime
from webapp.user.models import User

class Labor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hours = db.Column(db.Numeric(3,2))
    cost = db.Column(db.Numeric(7,2))

    def __repr__(self):
        return '<Labor id={} hours={} cost={}>'.format(self.id, self.hours, self.cost)
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(120), unique = True)
    
    def __repr__(self):
        return '<Image id={} link={}>'.format(self.id, self.link)
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    description = db.Column(db.String(400))
    labor_id = db.Column(db.SmallInteger, db.ForeignKey(Labor.id), index=True)
    image_id = db.Column(db.SmallInteger, db.ForeignKey(Image.id))
    
    image = relationship("Image", lazy="joined")
    product_labor = relationship("Labor", lazy="joined")
    product_component = relationship("Product_Component", lazy="joined")

    def __repr__(self):
        return '<Product= {} id={}>'.format(self.name, self.id)
    
class Component(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    description = db.Column(db.String(400))
    image_id = db.Column(db.SmallInteger, db.ForeignKey(Image.id), index=True)

    image = relationship("Image", lazy="joined")
    price = relationship("Price", lazy="joined")

    def __repr__(self):
        return '<Component {} id={}>'.format(self.name, self.id)

    
class Price(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    component_id = db.Column(db.Integer,  db.ForeignKey(Component.id), index = True)
    cost = db.Column(db.Numeric(7,2))
    discount = db.Column(db.Numeric(3,2))

    def __repr__(self):
        return '<Price id={} component_id={} cost={} discount={}>'.format(self.id, self.component_id, self.cost, self.discount)
    
class Product_Component(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), index = True, nullable = False)
    component_id = db.Column(db.Integer, db.ForeignKey(Component.id), index = True, nullable = False)

    components = relationship("Component", lazy="joined")

    def __repr__(self):
        return '<Product_Component id={}>'.format(self.id)

# class Product_Image(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     product_id = db.Column(db.Integer, db.ForeignKey(Product.id), index = True, nullable = False)
#     image_id =db.Column(db.Integer, db.ForeignKey(Image.id), index = True, nullable = False)
#     images = relationship("Image", lazy="joined")
#     def __repr__(self):
#         return '<Product_Image id={} images={}>'.format(self.id, self.images)
# class Component_Image(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     component_id = db.Column(db.Integer,db.ForeignKey(Component.id), index = True, nullable = False)
#     image_id =db.Column(db.Integer, db.ForeignKey(Image.id), index = True, nullable = False)
#     def __repr__(self):
#         return '<Component_Image id={}>'.format(self.id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'),  index=True) 
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id, ondelete='CASCADE'),  index=True)
    product = relationship('Product', backref='comments')
    user = relationship('User', backref='comments')
 



    def __repr__(self):
        return '<Comment {}>'.format(self.id)
