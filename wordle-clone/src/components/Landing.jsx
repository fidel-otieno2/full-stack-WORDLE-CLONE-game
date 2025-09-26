import React from 'react';

// Styles
const tileStyle = (bg, border = "none") => ({
  width: '2.5rem',
  height: '2.5rem',
  background: bg,
  border,
  color: '#fff',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontWeight: 'bold',
  fontSize: '1.3rem',
  borderRadius: '0.2rem',
});

function ExampleRow() {
  return (
    <div
      aria-label="Example row"
      style={{
        display: 'flex',
        gap: '0.5rem',
        justifyContent: 'center',
        margin: '1rem 0',
      }}
    >
      <div style={tileStyle('#538d4e')}>W</div>
      <div style={tileStyle('#b59f3b')}>O</div>
      <div style={tileStyle('#3a3a3c')}>R</div>
      <div style={tileStyle('#121213', '2px solid #3a3a3c')}>D</div>
      <div style={tileStyle('#121213', '2px solid #3a3a3c')}>S</div>
    </div>
  );
}

export default function Landing({ onStart }) {
  return (
    <div
      className="app-container"
      style={{
        maxWidth: 480,
        margin: '2rem auto',
        padding: '2rem',
        textAlign: 'center',
      }}
    >
      <h1 className="title">How to Play</h1>
      <p>
        Guess the <b>WORDLE</b> in 6 tries.
      </p>

      <ul
        style={{
          textAlign: 'left',
          maxWidth: 400,
          margin: '1rem auto',
          color: '#fff',
          fontSize: '1.1rem',
        }}
      >
        <li>Each guess must be a valid 5-letter word.</li>
        <li>
          The color of the tiles will change to show how close your guess was
          to the word.
        </li>
      </ul>

      <ExampleRow />

      <div
        style={{
          textAlign: 'left',
          maxWidth: 400,
          margin: '0 auto',
          color: '#fff',
          fontSize: '1rem',
        }}
      >
        <div>
          <b>W</b> is in the word and in the correct spot (green).
        </div>
        <div>
          <b>O</b> is in the word but in the wrong spot (yellow).
        </div>
        <div>
          <b>R</b> is not in the word in any spot (grey).
        </div>
      </div>

      <button
        className="restart-btn"
        onClick={onStart}
        style={{
          marginTop: 32,
          fontSize: '1.2rem',
          padding: '0.8em 2em',
        }}
      >
        Start Game
      </button>
    </div>
  );
}