from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Estrutura para armazenar o estado do jogo
game_state = {
    'board': [' ' for _ in range(9)],
    'current_player': 'X',
    'winner': None,
    'draw': False,
}

def check_winner():
    board = game_state['board']
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

@socketio.on('make_move')
def handle_make_move(json):
    global game_state
    index = json['position']
    player = json['player']
    
    if game_state['board'][index] == ' ' and (game_state['winner'] is None and not game_state['draw']):
        game_state['board'][index] = player
        winner = check_winner()
        if winner:
            game_state['winner'] = winner
        else:
            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
        emit('game_state', game_state, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
