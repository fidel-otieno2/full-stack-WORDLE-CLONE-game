import React from 'react';
import "../styles/Keyboard.css";

const KEYS = [
  ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
  ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
  ["Enter", "Z", "X", "C", "V", "B", "N", "M", "Del"],
];

// Determine key status from guesses
function getKeyStatus(guesses, solution) {
  const status = {};

  guesses.forEach((guessObj) => {
    const word = guessObj.word.toUpperCase();
    const guessArr = word.split("");
    const solArr = solution.toUpperCase().split("");
    const solUsed = Array(5).fill(false);

    // If we have API result, use it for key status
    if (guessObj.result) {
      guessArr.forEach((letter, i) => {
        const result = guessObj.result[i];
        if (result === "correct") {
          status[letter] = "correct";
        } else if (result === "present" && status[letter] !== "correct") {
          status[letter] = "present";
        } else if (result === "absent" && !status[letter]) {
          status[letter] = "absent";
        }
      });
    } else {
      // Fallback to client-side calculation
      // First pass: correct letters
      for (let i = 0; i < 5; i++) {
        if (guessArr[i] === solArr[i]) {
          status[guessArr[i]] = "correct";
          solUsed[i] = true;
        }
      }

      // Second pass: present or absent
      for (let i = 0; i < 5; i++) {
        const letter = guessArr[i];
        if (status[letter] === "correct") continue;

        let found = false;
        for (let j = 0; j < 5; j++) {
          if (!solUsed[j] && letter === solArr[j]) {
            found = true;
            solUsed[j] = true;
            break;
          }
        }

        if (found) {
          // Only upgrade to present if it's not already correct
          if (status[letter] !== "correct") {
            status[letter] = "present";
          }
        } else {
          if (!status[letter]) {
            status[letter] = "absent";
          }
        }
      }
    }
  });

  return status;
}

function Keyboard({ onChar, onDelete, onEnter, guesses, solution, disabled = false }) {
  const keyStatus = getKeyStatus(guesses, solution);

  return (
    <div className="keyboard">
      {KEYS.map((row, rowIndex) => (
        <div className="keyboard-row" key={rowIndex}>
          {row.map((key) => {
            const upperKey = key.toUpperCase();
            const status = keyStatus[upperKey] || "";
            const isSpecial = key === "Enter" || key === "Del";

            const handleClick = () => {
              if (disabled) return;
              if (key === "Enter") onEnter();
              else if (key === "Del") onDelete();
              else onChar(upperKey);
            };

            return (
              <button
                key={key}
                className={`key ${status.toLowerCase()} ${isSpecial ? 'special' : ''} ${disabled ? 'disabled' : ''}`}
                onClick={handleClick}
                disabled={disabled}
                aria-label={`Key ${key}`}
              >
                {key}
              </button>
            );
          })}
        </div>
      ))}
    </div>
  );
}

export default Keyboard;
