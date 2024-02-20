from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

game_state = {
    'board': [' ' for _ in range(9)],
    'current_player': 'X',
    'players': [],
    'game_active': False
}

def check_winner(board):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Draw'
    return None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_game')
def handle_join_game():
    if len(game_state['players']) < 2:
        player_id = request.sid
        game_state['players'].append(player_id)
        player_role = 'X' if game_state['players'].index(player_id) == 0 else 'O'
        emit('player_role', {'role': player_role, 'id': player_id})
        if len(game_state['players']) == 2:
            game_state['game_active'] = True
            emit('game_start', game_state, broadcast=True)
    else:
        emit('game_full', "Game is already full.")

@socketio.on('make_move')
def handle_make_move(data):
    if not game_state['game_active']:
        return
    position = data['position']
    player = data['player']
    if game_state['board'][position] == ' ' and player == game_state['current_player']:
        game_state['board'][position] = player
        winner = check_winner(game_state['board'])
        if winner:
            game_state['game_active'] = False
            emit('game_over', {'winner': winner}, broadcast=True)
        else:
            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
        emit('update_board', game_state, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
