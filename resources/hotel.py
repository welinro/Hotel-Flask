import re
from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
        {
        'hotel_id': 'alpha',
        'nome': 'Alpha hotel',
        'estrelas': 4.3,
        'diaria': 212.21,
        'cidade': 'São paulo'
         },
         {
        'hotel_id': 'palace',
        'nome': 'palace hotel',
        'estrelas': 4.5,
        'diaria': 222.3,
        'cidade':'Rio de Janeiro'
         },
         {
        'hotel_id': 'gordon',
        'nome': 'gordon hotel',
        'estrelas': 4.3,
        'diaria': 123.3,
        'cidade':'Minas Gerais'
         }
         ]

        

class Hoteis(Resource):
    def get(self):
        return{'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel (Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type= str, required= True, help=" The field 'nom' cannot be left blank" )
    argumentos.add_argument('estrelas', type=float, required= True, help =" The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    
    

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get (self, hotel_id):
       hotel = HotelModel.find_hotel(hotel_id)
       if hotel:
           return hotel.json()
            
       return {'message':' Hotel not found não encontrado'}, 404 # not found

    def post (self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400# Bad request

        dados = Hotel.argumentos.parse_args()
        hotel= HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel() 
        except:
            return {'message', 'An internal error ocurred tryng to save hotel.'}, 500 # internal server error
        return hotel.json()

       
       
    def put (self, hotel_id):
        dados = Hotel.argumentos.parse_args()       
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 
        hotel= HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message', 'An internal error ocurred tryng to save hotel.'}, 500 # internal server error
        return hotel.json(), 201 # created ttt
           

        
    def delete (self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message', 'An  error ocurred tryng to delete hotel.'}, 500 # internal server error
            return {'message': ' Hotel deleted'}
        return {"message": 'Hotel not found'}, 400

