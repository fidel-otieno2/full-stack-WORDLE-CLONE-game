import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './WordleBoard.css';

const WordleBoard = () => {
  const [game, setGame] = useState(null);
  const [currentGuess, setCurrentGuess] = useState('');
  const [guesses, setGuesses] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    startGame();
  }, [navigate]);

  const startGame = async () => {
    try {
      const response = await api.post('/game/start');
      setGame(response.data);
      setGuesses([]);
      setFeedback([]);
      setCurrentGuess('');
      setMessage('');
    } catch (err) {
      setMessage('Failed to start game');
    }
  };

  const submitGuess = async () => {
    if (currentGuess.length !== 5) return;
    try {
      const response = await api.post('/game/guess', { guess: currentGuess });
      const newFeedback = response.data.feedback;
      setGuesses([...guesses, currentGuess]);
      setFeedback([...feedback, newFeedback]);
      setCurrentGuess('');
      if (response.data.completed) {
        setMessage(response.data.message);
      }
    } catch (err) {
      setMessage('Invalid guess');
    }
  };

  const handleKeyPress = (key) => {
    if (key === 'ENTER') {
      submitGuess();
    } else if (key === 'BACKSPACE') {
      setCurrentGuess(currentGuess.slice(0, -1));
    } else if (currentGuess.length < 5) {
      setCurrentGuess(currentGuess + key);
    }
  };

  const renderGrid = () => {
    const grid = [];
    for (let i = 0; i < 6; i++) {
      const row = [];
      for (let j = 0; j < 5; j++) {
        let letter = '';
        let color = 'gray';
        if (i < guesses.length) {
          letter = guesses[i][j];
          color = feedback[i][j];
        } else if (i === guesses.length) {
          letter = currentGuess[j] || '';
        }
        row.push(
          <div key={j} className={`cell ${color}`}>
            {letter}
          </div>
        );
      }
      grid.push(<div key={i} className="row">{row}</div>);
    }
    return grid;
  };

  const renderKeyboard = () => {
    const keys = [
      ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
      ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
      ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACKSPACE']
    ];
    return keys.map((row, i) => (
      <div key={i} className="keyboard-row">
        {row.map(key => (
          <button key={key} onClick={() => handleKeyPress(key)}>
            {key}
          </button>
        ))}
      </div>
    ));
  };

  return (
    <div className="wordle-board">
      <h1>Wordle Clone</h1>
      <button onClick={startGame}>New Game</button>
      <div className="grid">{renderGrid()}</div>
      <div className="keyboard">{renderKeyboard()}</div>
      <p>{message}</p>
    </div>
  );
};

export default WordleBoard;
