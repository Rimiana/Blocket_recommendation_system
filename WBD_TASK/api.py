from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from WBD_TASK import User, Item, Bid, Category


app = Flask(__name__)

engine = create_engine('sqlite:///blocket.db')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/recommmendations/new_user', methods= ['GET'])
def get_new_user_recommendations():
    
    popular_items = session.query(Item.name, Item.item_id, func.count(Bid.bid_id).label('bid_count')) \
        .join(Bid) \
        .group_by(Item.item_id) \
        .order_by(func.count(Bid.bid_id).desc()) \
        .limit(10) \
        .all()

    
    recommendations = [{'name': item.name, 'bid_count': bid_count}for item, bid_count in popular_items]
    return jsonify(recommendations)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

