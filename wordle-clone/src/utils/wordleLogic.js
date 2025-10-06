// Client-side utilities for Wordle

export const isValidGuess = (guess) => {
  return guess.length === 5 && /^[A-Z]+$/.test(guess);
};

export const getFeedback = (guess, target) => {
  const feedback = [];
  const targetLetters = target.split('');
  const guessLetters = guess.split('');

  for (let i = 0; i < 5; i++) {
    if (guessLetters[i] === targetLetters[i]) {
      feedback.push('green');
    } else if (targetLetters.includes(guessLetters[i])) {
      feedback.push('yellow');
    } else {
      feedback.push('gray');
    }
  }
  return feedback;
};
