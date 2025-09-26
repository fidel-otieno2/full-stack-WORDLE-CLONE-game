import React from 'react';
import Tile from './Tile';
import '../styles/WordleBoard.css';

function WordleBoard({ guesses, currentGuess, solution }) {
  const maxRows = 6;

  // Only add current guess if game is still in progress
  const filledRows = [...guesses];
  if (guesses.length < maxRows) filledRows.push({ word: currentGuess, result: null, isCorrect: false });

  const emptyRows = Array(maxRows - filledRows.length).fill({ word: '', result: null, isCorrect: false });
  const rows = [...filledRows, ...emptyRows].slice(0, maxRows); // Always 6 rows

  return (
    <div className="board">
      {rows.map((guessObj, rowIndex) => (
        <div className="board-row" key={rowIndex}>
          {[...Array(5)].map((_, colIndex) => (
            <Tile
              key={colIndex}
              value={guessObj.word[colIndex] || ''}
              status={getStatus(guessObj, colIndex, solution, rowIndex < guesses.length)}
            />
          ))}
        </div>
      ))}
    </div>
  );
}

// Determines tile color for each letter
function getStatus(guessObj, idx, solution, isSubmitted) {
  if (!isSubmitted || !guessObj.word) return '';

  // If we have API result, use it
  if (guessObj.result && guessObj.result[idx]) {
    return guessObj.result[idx];
  }

  // Fallback to client-side calculation if no API result
  const word = guessObj.word.toUpperCase();
  solution = solution.toUpperCase();

  const guessArr = word.split('');
  const solArr = solution.split('');
  const statusArr = Array(5).fill('absent');
  const solUsed = Array(5).fill(false);

  // 1st pass: check for correct letters
  for (let i = 0; i < 5; i++) {
    if (guessArr[i] === solArr[i]) {
      statusArr[i] = 'correct';
      solUsed[i] = true;
    }
  }

  // 2nd pass: check for present letters
  for (let i = 0; i < 5; i++) {
    if (statusArr[i] === 'correct') continue;
    for (let j = 0; j < 5; j++) {
      if (!solUsed[j] && guessArr[i] === solArr[j]) {
        statusArr[i] = 'present';
        solUsed[j] = true;
        break;
      }
    }
  }

  return statusArr[idx];
}

export default WordleBoard;
