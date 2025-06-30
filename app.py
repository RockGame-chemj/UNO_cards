from flask import Flask
from flask_socketio import SocketIO, emit
import random
import request

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 游戏状态
players = {}
deck = []
discard_pile = []
current_player_index = 0

# 初始化卡牌
def init_deck():
    colors = ["red", "blue", "green", "yellow"]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "跳过", "反转", "+2"]
    specials = ["+4", "换色"] * 4  # 黑牌

    deck.clear()
    for color in colors:
        for value in values:
            deck.append({"color": color, "value": str(value)})
            if value != 0:  # 0牌只有一张
                deck.append({"color": color, "value": str(value)})
    deck.extend([{"color": "black", "value": v} for v in specials])
    random.shuffle(deck)

# Socket.io事件
@socketio.on("connect")
def handle_connect():
    player_id = request.sid
    players[player_id] = {"hand": [], "name": f"玩家{len(players)+1}"}
    emit("update-game", get_game_state(), room=player_id)
    print(f"Player connected: {player_id}")

@socketio.on("disconnect")
def handle_disconnect():
    player_id = request.sid
    players.pop(player_id, None)
    broadcast_game_state()

@socketio.on("play-card")
def handle_play_card(data):
    player_id = request.sid
    if player_id == list(players.keys())[current_player_index]:
        card = data["card"]
        discard_pile.append(card)
        players[player_id]["hand"].remove(card)
        next_turn()
        broadcast_game_state()

@socketio.on("call-uno")
def handle_call_uno():
    player_id = request.sid
    if len(players[player_id]["hand"]) == 1:
        print(f"{player_id} 喊了UNO!")

# 辅助函数
def next_turn():
    global current_player_index
    current_player_index = (current_player_index + 1) % len(players)

def get_game_state():
    return {
        "hand": players.get(request.sid, {}).get("hand", []),
        "currentPlayer": list(players.keys())[current_player_index],
        "playerCount": len(players),
        "discardPile": discard_pile
    }

def broadcast_game_state():
    for player_id in players:
        emit("update-game", get_game_state(), room=player_id)

# 启动游戏
if __name__ == "__main__":
    init_deck()
    socketio.run(app, debug=True)