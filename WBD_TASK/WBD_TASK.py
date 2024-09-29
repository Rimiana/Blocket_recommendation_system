from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String,nullable=False)
    email = Column(String, nullable=False)

# back_polulates= seller betyder att seller är namnet på relationen mellan item och user

    items = relationship('Item', back_populates='seller')


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String,nullable=False)


    items = relationship('Item', back_populates= 'category')



class Item(Base):
    __tablename__= 'items'
    item_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    seller_id = Column(Integer, ForeignKey('users.user_id'))


    category = relationship('Category', back_populates='items')
    seller = relationship('User', back_populates='items')
    bids = relationship('Bid', back_populates='item')



class Bid(Base):
    __tablename__= 'bids'
    bid_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    bid_value = Column(Float, nullable=False)


    item = relationship('Item', back_populates='bids')
    user = relationship('User')



engine = create_engine('sqlite:////Users/rt/WBD_TASK/blocket.db')
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()



def populate_db():
    mobiles = Category(category_name='Mobiles')
    tablets = Category(category_name='Tablets')
    session.add_all([mobiles,tablets])
    print('kategorierna är tillagda')


    sara = User(username= 'Sara', email='saratesfai@live.se')
    mohammed = User(username= 'Mohammed', email='mohammedbakri@live.se')
    rimiana = User(username='Rimiana', email='rimianatesfai@live.se')
    adam = User(username='Adam', email='adam@example.se')
    lina = User(username='Lina', email='lina@emaple.se')
    session.add_all([sara,mohammed,rimiana,adam,lina])
    session.commit()
    print('användarna är tillagda')


    iphone = Item(name='Iphone 15', category=mobiles, seller=sara)
    samsung = Item(name=' Samsung galaxy S10', category=mobiles, seller=mohammed)
    ipad = Item(name=' Ipad Air 2', category=tablets, seller=rimiana)
    session.add_all([iphone,samsung,ipad])
    print('produkterna är tillagda')


    bid1 = Bid(item=iphone, user=adam, bid_value=5000)
    bid2 = Bid(item=ipad, user=lina, bid_value=3000)
    session.add_all([bid1,bid2])
    session.commit()
    print('bud tillagda')


populate_db()












