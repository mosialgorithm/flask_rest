from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity 
from models.item import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    # parser.add_argument('store_id', type=int, required=True, help="Every item needs a store_id")
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404
    
    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':f"An item with name '{name}' already exists"}, 400
        data = Item.parser.parse_args()
        print('item data is ----> ', data)
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message':'An error occured inserting the item'}, 500
        
        return item.json(), 201
    
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'Item deleted'}
        return {'message':'Itemnot founded'}, 404
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        
        return item.json()
    
    

class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        return {'items':list(map(lambda x:x.json(), ItemModel.query.all()))}
    
            
        
    
