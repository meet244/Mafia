from flask import Flask, render_template, request, jsonify, redirect
# from flask_cors import CORS
import pymongo
import random
import os
import time
import datetime
from dotenv import load_dotenv


load_dotenv()

uri = os.getenv("MONGO_URI")
client = pymongo.MongoClient(uri)
db = client['db']
coll = db['coll']

app = Flask(__name__, static_folder='static')
# CORS(app)

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/ui', methods=['GET'])
def ui():
    return render_template('ui.html')

@app.route('/spectate', methods=['GET'])
def spectate():
    return render_template('spectator.html')

@app.route('/join', methods=['GET'])
def join():
    return render_template('join.html')

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/createRoom', methods=['POST'])
def createRoom():
    # get params from request
    name = request.json['playerName']
    is_prankster = request.json['isPrankster']
    is_doctor = request.json['isDoctor']
    is_police = request.json['isPolice']

    # delete all rooms
    coll.delete_many({})
    # Create a new room code and host code
    roomCode = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    hostCode = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    
    # check if room code already exists
    exists = coll.find_one({'_id': roomCode})
    while True:
        if exists == None:
            break
        elif exists['mafia_won'] != None:
            break
        roomCode = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        exists = coll.find_one({'_id': roomCode})

    roomCode = '1234'
    hostCode = 'host123'

    roles = ['mafia']
    if is_prankster:
        roles.append('prankster')
    if is_doctor:
        roles.append('doctor')
    if is_police:
        roles.append('police')

    # create player object
    player = {'name': name, 'role': '', 'alive': True, 'is_pranked': False, 'is_killed': False, 'is_saved': False, 'is_suspected': False, 'vote_out_count': 0, 'is_host': True,'current_state_complete':False, 'host_code': hostCode}
    # create room object
    room = {'_id': roomCode, 'players': [player], 'game_started': False, 'roles': roles, 'game_state':'1', 'next_state_time': '0', 'last_killed': '','police_susp':False, 'voted_out': '', 'was_voted_mafia':False, 'mafia_won':None}
    # insert room object into collection
    coll.insert_one(room)
    return jsonify({"status":"created","host_code":hostCode, "code":roomCode})

@app.route('/joinRoom/<string:code>/<string:name>', methods=['GET'])
def joinRoom(code, name):
    # prevent joining
    if (name.lower() == 'nobody' or name.lower() == 'skip'):
        return jsonify({"error":"Name not allowed"})
    # Join a room
    # create player object
    player = {'name': name, 'role': '', 'alive': True, 'is_pranked': False, 'is_killed': False, 'is_saved': False, 'is_suspected': False, 'vote_out_count': 0, 'is_host': False,'current_state_complete':False}
    # get game_started from room object
    doc = coll.find_one({'_id': code})
    if doc == None:
        return jsonify({"error":"Game not found"})
    # check if game has already started
    if doc['mafia_won'] != None:
        return jsonify({"error":"Game has already ended"})
    if doc['game_started'] == True:
        return jsonify({"error":"Game has already started"})
    # get players from room object
    players = doc['players']
    # check if player already exists
    for p in players:
        if p['name'] == name:
            return jsonify({"error":"Name already taken"})
    if len(players) >= 20:
        return jsonify({"error":"Room is full"})
    # add player to players list
    doc['players'].append(player)
    # update players in room object
    coll.update_one({'_id': code}, {'$set': {'players': players}})
    return jsonify({"status":"joined"})

@app.route('/play', methods=['GET'])
def play():
    return render_template('play.html')

@app.route('/players/<string:code>', methods=['GET'])
def show_players(code):
    doc = coll.find_one({'_id': code})
    if doc == None:
        return jsonify({"stop":"Game not found"})
    # get players from room object
    players = doc['players']

    # make a list of player names
    names = []
    for p in players:
        names.append(p['name'])
    return jsonify(names)

@app.route('/start_game/<string:code>/<string:host_code>', methods=['GET'])
def start_game_host(code, host_code):
    doc = coll.find_one({'_id': code})
    if doc == None:
        return jsonify({"stop":"Game not found"})
    # get players from room object
    players = doc['players']
    # check if player is host
    for p in players:
        if p['is_host'] and p['host_code'] == host_code:
            doc = coll.find_one({'_id': code})
            # check if game has already started
            game_started = doc['game_started']
            if game_started:
                return jsonify({"error":"Game has already started"})
            
            # get players from room object
            players = doc['players']
            # get roles from room object
            roles = doc['roles']
            
            # check if number of players is less than number of roles
            if len(players) < len(roles):
                return jsonify({"error":"Number of players is less than number of roles"})
            
            if len(players) > len(roles):
                # add civillians to roles
                for i in range(len(players) - len(roles)):
                    roles.append('civillian')
            # shuffle roles
            random.shuffle(roles)
            # assign roles to players
            for i in range(len(players)):
                players[i]['role'] = roles[i]
            
            # next state time = current time epoch in ms + 7 seconds

            doc['next_state_time'] = str(int(time.time() * 1000) + 7000)
            doc['game_state'] = '2'
            
            # update room object
            coll.update_one({'_id': code}, {'$set': {'game_started': True, 'players': players, 'roles': roles, 'next_state_time': doc['next_state_time'], 'game_state': doc['game_state']}})

            return jsonify({"status":"Game started"})
        else:
            return jsonify({"error":"Player is not host"})
    return jsonify("Player not found")

@app.route('/reset_game/<string:code>/<string:host_code>', methods=['GET'])
def reset_game_host(code, host_code):
    # get the game object
    doc = coll.find_one({'_id': code})

    if doc == None:
        return jsonify({"error":"Game not found"})

    # remove all players except host
    players = doc['players']
    for p in players:
        if p['is_host']:
            host = p
            break

    if host['host_code'] != host_code:
        return jsonify({"error":"Player is not host"})

    # reset the game vars
    host['alive'] = True
    doc['players'] = [host]
    doc['game_state'] = '1'
    doc['next_state_time'] = '0'
    doc['last_killed'] = ''
    doc['police_susp'] = False
    doc['voted_out'] = ''
    doc['was_voted_mafia'] = False
    doc['mafia_won'] = None
    doc['game_started'] = False

    # update the game object
    coll.update_one({'_id': code}, {'$set': doc})

    return jsonify({"status":"Game reset"})

@app.route('/state_poll/<string:code>/<string:player_state>/<string:name>', methods=['GET'])
def status_poll(code, player_state, name):
    # get players from room object
    doc = coll.find_one({'_id': code})
    if doc == None:
        return jsonify({"stop":"Game not found"})

    if player_state == '1':
        # if game is also in state 1
        if player_state == doc['game_state']:
            players_list = []
            for p in doc['players']:
                players_list.append(p['name'])
            return jsonify({"status":"wait", 'players':players_list})
        
        # if game moved to state 2
        if doc['game_started'] == False:
            return jsonify({"status":"wait"})
        else:
            for p in doc['players']:
                if p['name'] == name:
                    return jsonify({"status":"update",'role':p['role'],'next_state_time':doc['next_state_time']})
                
    elif player_state == '2':
        # if game is also in state 2
        if player_state == doc['game_state']:
            players_list_not_done = []
            for p in doc['players']:
                if p['alive']:
                    if p['current_state_complete'] == False:
                        players_list_not_done.append(p['name'])
            return jsonify({"status":"wait", 'waiting_players':players_list_not_done})
        
        # if game moved to state 3
        alive = []
        dead = []
        for p in doc['players']:
            if p['alive']:
                alive.append(p['name'])
            else:
                dead.append(p['name'])
        return jsonify({"status":"update",'next_state_time':doc['next_state_time'],'alive':alive,'dead':dead})
    
    elif player_state == '3':
        # if game is also in state 3
        if player_state == doc['game_state']:
            players_list_not_done = []
            for p in doc['players']:
                if p['current_state_complete'] == False:
                    players_list_not_done.append(p['name'])
            return jsonify({"status":"wait", 'waiting_players':players_list_not_done})
        
        # if game moved to state 4
        alive = []
        dead = []
        for p in doc['players']:
            if p['alive']:
                alive.append(p['name'])
            else:
                dead.append(p['name'])
        
        # if game over 
        final_results = False if doc['mafia_won'] == None else True
        if final_results:
            # game has ended - show alive,role,name of players
            player_roles = []
            for p in doc['players']:
                player_roles.append({'name':p['name'],'role':p['role'],'alive':p['alive']})
            
            return jsonify({"status":"update",'next_state_time':doc['next_state_time'], 'last_killed':doc['last_killed'], 'mafia_won': doc['mafia_won'], 'final_results': final_results, 'player_roles': player_roles})


        return jsonify({"status":"update",'next_state_time':doc['next_state_time'],'last_killed': doc['last_killed'],'police_susp':doc['police_susp'], 'alive':alive,'dead':dead, 'final_results': final_results, 'mafia_won': doc['mafia_won']})
    
    elif player_state == '4':
        # if game is also in state 4
        if player_state == doc['game_state']:
            players_list_not_done = []
            for p in doc['players']:
                if p['current_state_complete'] == False:
                    if p['alive'] == True:
                        players_list_not_done.append(p['name'])
            return jsonify({"status":"wait", 'waiting_players':players_list_not_done})
        
        # if game moved to state 5
        final_results = False if doc['mafia_won'] == None else True
        if final_results:
            # game has ended - show alive,role,name of players
            player_roles = []
            for p in doc['players']:
                player_roles.append({'name':p['name'],'role':p['role'],'alive':p['alive']})
            
            return jsonify({"status":"update",'next_state_time':doc['next_state_time'], 'voted_out': doc['voted_out'], 'was_voted_mafia': doc['was_voted_mafia'], 'mafia_won': doc['mafia_won'], 'final_results': final_results, 'player_roles': player_roles})


        # send results, final results & time to next state
        return jsonify({"status":"update",'next_state_time':doc['next_state_time'], 'voted_out': doc['voted_out'], 'was_voted_mafia': doc['was_voted_mafia'], 'mafia_won': doc['mafia_won'], 'final_results': final_results})
    else:
        print(player_state)
        print(type(player_state))
        return jsonify({"status":"wait"})

@app.route('/update_state/<string:code>/<string:name>', methods=['GET'])
def update_state_complete(code, name):
    doc = coll.find_one({'_id': code})
    if doc == None:
        return jsonify({"stop":"Game not found"})
    everyones_complete = True
    # get players from room object and update current_state_complete
    for p in doc['players']:
        if p['alive']:
            if p['name'] == name:
                p['current_state_complete'] = True
                # print(f"{name} has completed work")
            if p['current_state_complete'] == False:
                everyones_complete = False
    # print("everyones_complete: ", everyones_complete)
    if everyones_complete:
        # update state after everyone has completed choosing
        if doc['game_state'] == '2':
            doc['game_state'] = '3'
            # make all players state complete False
            for p in doc['players']:
                p['current_state_complete'] = False
            # calc next state time and update
            doc['next_state_time'] = str(int(time.time() * 1000) + 7000)
            coll.update_one({'_id': code}, {'$set': {'game_state': doc['game_state'], 'next_state_time': doc['next_state_time'], 'players': doc['players']}})

            return jsonify({"status":"done"})
        if doc['game_state'] == '3':
            doc['game_state'] = '4'
            # make all players state complete False
            for p in doc['players']:
                p['current_state_complete'] = False

            # calc results of dead(killed by mafia) and suspection
            doc['last_killed'] = 'Nobody'
            for p in doc['players']:
                if p['is_pranked']:
                    if p['role'] == 'mafia':
                        for p1 in doc['players']:
                            p1['is_killed'] = False
                    elif p['role'] == 'doctor':
                        for p1 in doc['players']:
                            p1['is_saved'] = False
                    elif p['role'] == 'police':
                        for p1 in doc['players']:
                            p1['is_suspected'] = False
            for p in doc['players']:
                if p['is_killed']:
                    if p['is_saved']:
                        p['is_killed'] = False
                        p['is_saved'] = False
                    else:
                        p['alive'] = False
                        doc['last_killed'] = p['name']
                if p['is_suspected']:
                    if p['role'] == 'mafia':
                        doc['police_susp'] = True

            # FINALE RESULTS CALCULATION
            mafia_count = 0
            villager_count = 0

            # count the number of mafia and villagers
            for p in doc['players']:
                if p['role'] == 'mafia' and p['alive']:
                    mafia_count += 1
                elif p['role'] != 'mafia' and p['alive']:
                    villager_count += 1

            # check the win conditions
            if mafia_count == 0:
                doc['mafia_won'] = False
            elif mafia_count >= villager_count:
                doc['mafia_won'] = True

            # make all players state complete False
            for p in doc['players']:
                p['is_killed'] = False
                p['is_saved'] = False
                p['is_suspected'] = False
                p['is_pranked'] = False

            # calc next state time and update
            doc['next_state_time'] = str(int(time.time() * 1000) + 7000)
            
            coll.update_one({'_id': code}, {'$set': {'game_state': doc['game_state'], 'next_state_time': doc['next_state_time'], 'players': doc['players'], 'last_killed': doc['last_killed'], 'police_susp': doc['police_susp'], 'mafia_won': doc['mafia_won']}})
            
            return jsonify({"status":"done"})
        elif doc['game_state'] == '4':
            # update game_state and next_state_time when everyone has completed voting
            doc['game_state'] = '2'
            # make all players state complete False
            for p in doc['players']:
                p['current_state_complete'] = False
            
            # calc results of voting
            alive_players = 0
            skipped_cnt = 0
            max_vote = 0
            total_vote = 0
            max_voted = ''
            for p in doc['players']:
                if p['alive']:
                    alive_players += 1
                    if p['vote_out_count'] > max_vote:
                        max_vote = p['vote_out_count']
                        max_voted = p['name']
                    elif p['vote_out_count'] == max_vote:
                        max_voted = 'tie'
                    total_vote += p['vote_out_count']

            skipped_cnt = alive_players - total_vote
            if skipped_cnt > max_vote:
                max_voted = 'skip'
            if max_voted == 'skip':
                doc['voted_out'] = 'Nobody'

            if max_voted != 'tie':
                for p in doc['players']:
                    if p['name'] == max_voted:
                        p['alive'] = False
                        doc['voted_out'] = p['name']
                        if p['role'] == 'mafia':
                            doc['was_voted_mafia'] = True
                        break
            else:
                doc['voted_out'] = 'No one'
            # make all players state complete False
            for p in doc['players']:
                p['vote_out_count'] = 0

            # FINALE RESULTS CALCULATION
            mafia_count = 0
            villager_count = 0

            # count the number of mafia and villagers
            for p in doc['players']:
                if p['role'] == 'mafia' and p['alive']:
                    mafia_count += 1
                elif p['role'] != 'mafia' and p['alive']:
                    villager_count += 1

            # check the win conditions
            if mafia_count == 0:
                doc['mafia_won'] = False
            elif mafia_count >= villager_count:
                doc['mafia_won'] = True                

            # calc next state time and update
            doc['next_state_time'] = str(int(time.time() * 1000) + 7000)
            coll.update_one({'_id': code}, {'$set': {'game_state': doc['game_state'], 'next_state_time': doc['next_state_time'], 'players': doc['players'], 'voted_out': doc['voted_out'], 'was_voted_mafia': doc['was_voted_mafia'], 'mafia_won': doc['mafia_won']}})
            return jsonify({"status":"done"})

    coll.update_one({'_id': code}, {'$set': {'players': doc['players']}})
    return jsonify({"status":"done"})

@app.route('/selected_target/<string:code>/<string:player_name>/<string:target>', methods=['GET'])
def selected_target(code, player_name, target):
    doc = coll.find_one({'_id': code})
    if doc == None:
        return jsonify({"stop":"Game not found"})
    # get players from room object
    players = doc['players']
    # get player object
    for p in players:
        if p['name'] == player_name:
            player = p
    # check if player is alive
    if player['alive'] == False:
        return jsonify({"error":"Player is dead"})

    # check if player has a role
    if player['role'] == 'mafia':
        # get target player object
        for p in players:
            if p['name'] == target:
                target_player = p
        # mark target player as killed
        target_player['is_killed'] = True
    elif player['role'] == 'doctor':
        # get target player object
        for p in players:
            if p['name'] == target:
                target_player = p
        # mark target player as saved
        target_player['is_saved'] = True
    elif player['role'] == 'police':
        # get target player object
        for p in players:
            if p['name'] == target:
                target_player = p
        # mark target player as suspected
        target_player['is_suspected'] = True
    elif player['role'] == 'prankster':
        # get target player object
        for p in players:
            if p['name'] == target:
                target_player = p
        # mark target player as pranked
        target_player['is_pranked'] = True
    elif player['role'] == 'civillian':
        pass
    else:
        return jsonify({"error":"Player does not have a role"})

    # update players in room object
    coll.update_one({'_id': code}, {'$set': {'players': players}})
    update_state_complete(code,player_name)
    return jsonify({"status":"done"})

@app.route('/selected_vote/<string:code>/<string:player_name>/<string:target>', methods=['GET'])
def selected_vote(code, player_name, target):
    if target == 'skip':
        update_state_complete(code,player_name)
        return jsonify({"status":"done"})
    
    doc = coll.find_one({'_id': code})

    if doc == None:
        return jsonify({"stop":"Game not found"})
    # get players from room object
    players = doc['players']
    # get player object
    for p in players:
        if p['name'] == player_name:
            player = p
    # check if player is alive
    if player['alive'] == False:
        return jsonify({"error":"Player is dead"})

    # get target player object
    for p in players:
        if p['name'] == target:
            target_player = p
    # mark target player as voted out
    target_player['vote_out_count'] += 1

    # update players in room object
    coll.update_one({'_id': code}, {'$set': {'players': players}})
    update_state_complete(code,player_name)
    return jsonify({"status":"done"})

@app.route('/spectator/<string:code>', methods=['GET'])
def spectator(code):
    doc = coll.find_one({'_id': code})

    if doc == None:
        return jsonify({"stop":"Game not found"})
    # get players from room object
    players = doc['players']

    # get alive and dead players
    alive = []
    dead = []
    for p in players:
        if p['alive']:
            alive.append(p['name'])
        else:
            dead.append(p['name'])

    # get final results
    final_results = False if (doc['mafia_won'] == None) else True
    print("final_results: ", final_results)
    # get player roles
    player_roles = []
    if final_results:
        for p in players:
            player_roles.append({'name':p['name'],'role':p['role'],'alive':p['alive']})

    return jsonify({'alive':alive, 'dead':dead, 'final_results': final_results, 'mafia_won': doc['mafia_won'], 'player_roles': player_roles})



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
