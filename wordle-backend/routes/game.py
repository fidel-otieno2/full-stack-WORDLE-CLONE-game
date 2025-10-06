from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, GameResult
import random
import os
import datetime

game_bp = Blueprint("game", __name__)

@game_bp.route("/word", methods=["GET"])
def get_word():
    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.txt')
    with open(words_file, "r") as f:
        words = [w.strip().upper() for w in f.read().splitlines() if len(w.strip()) == 5]
    # Select daily word based on date
    today = datetime.date.today()
    day_index = today.toordinal() % len(words)
    word = words[day_index]
    return jsonify({"word": word, "wordId": word})

@game_bp.route("/guess", methods=["POST"])
def validate_guess():
    data = request.get_json()
    guess = data.get("guess", "").upper()
    word_id = data.get("wordId", "").upper()

    if len(guess) != 5 or len(word_id) != 5:
        return jsonify({"error": "Invalid guess or word"}), 400

    result = get_feedback(guess, word_id)
    is_correct = guess == word_id

    return jsonify({"result": result, "isCorrect": is_correct})

def get_feedback(guess, target):
    feedback = []
    target_letters = list(target)
    guess_letters = list(guess)

    # First pass: correct positions
    for i in range(5):
        if guess_letters[i] == target_letters[i]:
            feedback.append('correct')
            target_letters[i] = None  # Mark as used
        else:
            feedback.append(None)

    # Second pass: present letters
    for i in range(5):
        if feedback[i] is None:
            for j in range(5):
                if target_letters[j] and guess_letters[i] == target_letters[j]:
                    feedback[i] = 'present'
                    target_letters[j] = None
                    break
            else:
                feedback[i] = 'absent'

    return feedback

@game_bp.route("/result", methods=["POST"])
@jwt_required(optional=True)
def submit_game_result():
    user_id = get_jwt_identity() if get_jwt_identity() else None
    data = request.get_json()

    word = data.get("wordId")
    guesses = data.get("guesses")
    won = data.get("won")
    time_taken = data.get("timeTaken")

    # Validate data types
    if not isinstance(guesses, int) or not isinstance(time_taken, int) or not isinstance(won, bool) or not isinstance(word, str):
        return jsonify({"error": "Invalid data types"}), 400

    result = GameResult(user_id=user_id, word=word, guesses=guesses, won=won, time_taken=time_taken)
    db.session.add(result)
    db.session.commit()

    return jsonify({"message": "Game result saved"})
