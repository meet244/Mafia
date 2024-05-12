from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pymongo
import random
import os
from dotenv import load_dotenv


load_dotenv()

uri = os.getenv("MONGO_URI")
client = pymongo.MongoClient(uri)
db = client['db']
coll = db['coll']



app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify("Hello")

@app.route('/room/<string:code>/<string:name>', methods=['GET'])
def join_or_create_room(code, name):

    if code == None or code == 'null':
        coll.delete_many({})
        
        # Create a new room
        # create player object
        player = {'name': name, 'role': '', 'alive': True, 'is_pranked': False, 'is_killed': False, 'is_saved': False, 'is_suspected': False, 'vote_out_count': 0, 'is_host': True, 'host_code': 'host123'}
        # create room object
        room = {'_id': '1234', 'players': [player], 'mafias_cnt':0, 'game_started': False, 'roles': ['prankster','mafia', 'doctor', 'police']}
        # insert room object into collection
        coll.insert_one(room)
        return jsonify({"status":"Created a new room","host_code":"host123"})
    else:
        # Join a room
        # create player object
        player = {'name': name, 'role': '', 'alive': True, 'is_pranked': False, 'is_killed': False, 'is_saved': False, 'is_suspected': False, 'vote_out_count': 0, 'is_host': False}
        # get game_started from room object
        print(code)
        print(type(code))
        game_started = coll.find_one({'_id': code})['game_started']
        # check if game has already started
        if game_started == True:
            return jsonify("Game has already started")
        # get players from room object
        players = coll.find_one({'_id': code})['players']
        # check if player already exists
        for p in players:
            if p['name'] == name:
                return jsonify("Name is already taken")
        # add player to players list
        players.append(player)
        # update players in room object
        coll.update_one({'_id': code}, {'$set': {'players': players}})
        return jsonify("Joined the room")
    
@app.route('/players/<code>', methods=['GET'])
def show_players(code):
    # get players from room object
    players = coll.find_one({'_id': code})['players']

    # make a list of player names
    names = []
    for p in players:
        names.append(p['name'])
    return jsonify(names)

@app.route('/start_game/<code>/<name>', methods=['GET'])
def start_game_host(code, name):
    # get players from room object
    players = coll.find_one({'_id': code})['players']
    # check if player is host
    for p in players:
        if p['name'] == name:
            if p['is_host']:
                # check if game has already started
                game_started = coll.find_one({'_id': code})['game_started']
                if game_started:
                    return jsonify("Game has already started")
                # get players from room object
                players = coll.find_one({'_id': code})['players']
                # get roles from room object
                roles = coll.find_one({'_id': code})['roles']
                # check if number of players is less than number of roles
                if len(players) < len(roles):
                    return jsonify("Not enough players")
                
                if len(players) > len(roles):
                    # add civilians to roles
                    for i in range(len(players) - len(roles)):
                        roles.append('civillian')
                # shuffle roles
                random.shuffle(roles)
                # assign roles to players
                for i in range(len(players)):
                    players[i]['role'] = roles[i]
                # update players in room object
                coll.update_one({'_id': code}, {'$set': {'players': players}})
                # set game_started to True
                coll.update_one({'_id': code}, {'$set': {'game_started': True}})
                return jsonify("Game started")
            else:
                return jsonify("You are not the host")
    return jsonify("Player not found")


if __name__ == '__main__':
    app.run(debug=True)
