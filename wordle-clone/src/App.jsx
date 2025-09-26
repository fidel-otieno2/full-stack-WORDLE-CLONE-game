import React, { useState, useEffect, useRef } from 'react';
import './styles/App.css';
import WordleBoard from './components/WordleBoard';
import Keyboard from './components/Keyboard';
import Landing from './components/Landing';
import Ending from './components/Ending';
import Login from './components/Login';
import { authAPI, gameAPI, apiUtils } from './services/api';
import { authService } from './services/auth';

function App() {
  const [user, setUser] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [solution, setSolution] = useState(null);
  const [wordId, setWordId] = useState(null);
  const [guesses, setGuesses] = useState([]);
  const [currentGuess, setCurrentGuess] = useState('');
  const [gameStatus, setGameStatus] = useState('playing');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [timer, setTimer] = useState(0);
  const timerRef = useRef(null);

  useEffect(() => {
    // Check if user is already authenticated
    const savedUsername = apiUtils.getStoredUsername();
    if (savedUsername && apiUtils.isAuthenticated()) {
      setUser(savedUsername);
    }
  }, []);

  useEffect(() => {
    if (gameStarted && gameStatus === 'playing') {
      timerRef.current = setInterval(() => setTimer(t => t + 1), 1000);
    } else {
      clearInterval(timerRef.current);
    }
    return () => clearInterval(timerRef.current);
  }, [gameStarted, gameStatus]);

  // Fetch daily word when game starts
  useEffect(() => {
    const fetchDailyWord = async () => {
      if (gameStarted && !solution) {
        setLoading(true);
        try {
          const wordData = await gameAPI.getDailyWord();
          setSolution(wordData.word.toUpperCase());
          setWordId(wordData.wordId);
          setError('');
        } catch (error) {
          setError('Failed to load daily word. Please try again.');
          console.error('Error fetching daily word:', error);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchDailyWord();
  }, [gameStarted, solution]);

  useEffect(() => {
    if (!gameStarted || gameStatus !== 'playing') return;
    const handleKeyDown = (e) => {
      if (e.key === 'Enter') onEnter();
      else if (e.key === 'Backspace') onDelete();
      else if (/^[a-zA-Z]$/.test(e.key)) onChar(e.key.toUpperCase());
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentGuess, guesses, gameStatus, gameStarted]);

  const onLogin = async (username, password) => {
    setLoading(true);
    try {
      const response = await authAPI.login(username, password);
      authService.setAuthData(response.token, username);
      setUser(username);
      setError('');
    } catch (error) {
      setError('Login failed. Please check your credentials.');
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRegister = async (username, password) => {
    setLoading(true);
    try {
      const response = await authAPI.register(username, password);
      authService.setAuthData(response.token, username);
      setUser(username);
      setError('');
    } catch (error) {
      setError('Registration failed. Please try again.');
      console.error('Registration error:', error);
    } finally {
      setLoading(false);
    }
  };

  const onLogout = () => {
    authService.logout();
    setUser(null);
    setGameStarted(false);
    onRestart();
  };

  const onChar = (char) => {
    if (currentGuess.length < 5 && gameStatus === 'playing') {
      setCurrentGuess(prev => prev + char);
      setError('');
    }
  };

  const onDelete = () => {
    if (gameStatus === 'playing') {
      setCurrentGuess(prev => prev.slice(0, -1));
    }
  };

  const onEnter = async () => {
    if (gameStatus !== 'playing' || loading) return;

    if (currentGuess.length !== 5) {
      setError('Not enough letters');
      return;
    }

    if (!solution || !wordId) {
      setError('Game not ready. Please wait for the daily word to load.');
      return;
    }

    setLoading(true);
    try {
      const upperGuess = currentGuess.toUpperCase();
      const validationResult = await gameAPI.validateGuess(upperGuess, wordId);

      const newGuesses = [...guesses, {
        word: upperGuess,
        result: validationResult.result,
        isCorrect: validationResult.isCorrect
      }];
      setGuesses(newGuesses);
      setCurrentGuess('');
      setError('');

      if (validationResult.isCorrect) {
        setGameStatus('won');
        // Submit game result
        await gameAPI.submitGameResult({
          wordId,
          guesses: newGuesses.length,
          time: timer,
          won: true
        });
      } else if (newGuesses.length >= 6) {
        setGameStatus('lost');
        // Submit game result
        await gameAPI.submitGameResult({
          wordId,
          guesses: newGuesses.length,
          time: timer,
          won: false
        });
      }
    } catch (error) {
      setError('Failed to validate guess. Please try again.');
      console.error('Guess validation error:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRestart = () => {
    setSolution(null);
    setWordId(null);
    setGuesses([]);
    setCurrentGuess('');
    setGameStatus('playing');
    setTimer(0);
    setError('');
    setGameStarted(false);
  };

  // Screens
  if (!user) return <Login onLogin={onLogin} onRegister={onRegister} />;
  if (!gameStarted) return <Landing onStart={() => setGameStarted(true)} />;
  if (gameStatus !== 'playing') {
    return (
      <Ending
        won={gameStatus === 'won'}
        guesses={guesses}
        time={timer}
        solution={solution}
        onRestart={onRestart}
      />
    );
  }

  // Main Game UI
  if (loading) {
    return (
      <div className="app-container">
        <header className="title">Wordle</header>
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '200px',
          color: '#b59f3b',
          fontSize: '1.2rem',
        }}>
          Loading daily word...
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="title">Wordle</header>

      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        color: '#b59f3b',
        marginBottom: '0.5rem',
        fontSize: '1rem',
      }}>
        <span>👋 Hello, <strong>{user}</strong></span>
        <span>⏱️ Time: {Math.floor(timer / 60)}:{(timer % 60).toString().padStart(2, '0')}</span>
      </div>

      <WordleBoard
        guesses={guesses}
        currentGuess={currentGuess}
        solution={solution}
      />

      <Keyboard
        onChar={onChar}
        onDelete={onDelete}
        onEnter={onEnter}
        guesses={guesses}
        solution={solution}
        disabled={loading}
      />

      {error && <div className="error">{error}</div>}

      <button
        onClick={onLogout}
        className="restart-btn"
        style={{ marginTop: '1.5rem', background: '#8b0000' }}
        disabled={loading}
      >
        Logout
      </button>
    </div>
  );
}

export default App;
