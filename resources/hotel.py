from flask_restful import Resource, reqparse
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
        return{'hoteis': hoteis}

class Hotel (Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    
    

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get (self, hotel_id):
       hotel = Hotel.find_hotel(hotel_id)
       if hotel:
           return hotel
            
       return {'message':' Hotel not found não encontrado'}, 404 # not found

    def post (self, hotel_id):
       

        dados = Hotel.argumentos.parse_args()

        novo_hotel = {
            'hotel_id': hotel_id, **dados }
        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put (self, hotel_id):
        
        dados = Hotel.argumentos.parse_args()
        novo_hotel = {'hotel_id': hotel_id, **dados }

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200 
        hoteis.append(novo_hotel)
        return novo_hotel, 201 # created ttt
           

        
    def delete (self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel ['hotel_id'] != hotel_id]
        return {'message': ' Hotel deleted'}

