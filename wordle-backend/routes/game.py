import os
import random
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Game
from werkzeug.exceptions import BadRequest

game_bp = Blueprint('game', __name__)

# Load words
words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.txt')
with open(words_file, 'r') as f:
    WORDS = [line.strip().lower() for line in f if len(line.strip()) == 5]

def get_feedback(target, guess):
    feedback = []
    target_list = list(target)
    guess_list = list(guess)
    for i in range(5):
        if guess_list[i] == target_list[i]:
            feedback.append('green')
            target_list[i] = None  # Mark as used
        else:
            feedback.append(None)
    for i in range(5):
        if feedback[i] is None:
            if guess_list[i] in target_list:
                feedback[i] = 'yellow'
                target_list[target_list.index(guess_list[i])] = None
            else:
                feedback[i] = 'gray'
    return feedback

@game_bp.route('/start', methods=['POST'])
@jwt_required()
def start_game():
    user_id = get_jwt_identity()
    target_word = random.choice(WORDS)
    game = Game(user_id=user_id, target_word=target_word)
    db.session.add(game)
    db.session.commit()
    return jsonify({'game_id': game.id, 'word_length': 5}), 201

@game_bp.route('/guess', methods=['POST'])
@jwt_required()
def submit_guess():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or 'game_id' not in data or 'guess' not in data:
        raise BadRequest('Missing game_id or guess')
    game_id = data['game_id']
    guess = data['guess'].lower().strip()
    if len(guess) != 5 or not guess.isalpha():
        return jsonify({'message': 'Guess must be a 5-letter word'}), 400

    game = Game.query.filter_by(id=game_id, user_id=user_id).first()
    if not game:
        return jsonify({'message': 'Game not found'}), 404
    if game.completed:
        return jsonify({'message': 'Game already completed'}), 400

    feedback = get_feedback(game.target_word, guess)
    guesses = json.loads(game.guesses) if game.guesses else []
    guesses.append({'guess': guess, 'feedback': feedback})
    game.guesses = json.dumps(guesses)
    game.score = len(guesses)

    if guess == game.target_word:
        game.completed = True
        game.won = True
    elif len(guesses) >= 6:
        game.completed = True
        game.won = False

    db.session.commit()
    return jsonify({
        'feedback': feedback,
        'completed': game.completed,
        'won': game.won if game.completed else None,
        'target_word': game.target_word if game.completed else None
    }), 200

@game_bp.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    user_id = get_jwt_identity()
    games = Game.query.filter_by(user_id=user_id).all()
    games_list = []
    for game in games:
        guesses = json.loads(game.guesses) if game.guesses else []
        games_list.append({
            'id': game.id,
            'target_word': game.target_word,
            'guesses': guesses,
            'completed': game.completed,
            'won': game.won,
            'score': game.score,
            'created_at': game.created_at.isoformat()
        })
    return jsonify(games_list), 200
