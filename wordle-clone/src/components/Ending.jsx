import React from 'react';

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

export default function Ending({ won, guesses, time, onRestart, solution }) {
  return (
    <div className="app-container" style={{ maxWidth: 480, margin: '2rem auto', padding: '2rem', textAlign: 'center' }}>
      <h1 className="title">Game Over</h1>
      <div style={{ fontSize: '1.3rem', margin: '1rem 0' }}>
        {won ? '🎉 You Won!' : '😢 You Lost!'}
      </div>
      {!won && (
        <div style={{ fontSize: '1.1rem', margin: '0.5rem 0', color: '#b59f3b' }}>
          <b>The word was:</b> <span style={{ letterSpacing: '0.2em', fontWeight: 'bold' }}>{solution}</span>
        </div>
      )}
      <div style={{ fontSize: '1.1rem', margin: '0.5rem 0' }}>
        <b>Guesses:</b> {guesses.length}
      </div>
      <div style={{ fontSize: '1.1rem', margin: '0.5rem 0' }}>
        <b>Time:</b> {formatTime(time)}
      </div>
      <button className="restart-btn" style={{ marginTop: 32, fontSize: '1.2rem', padding: '0.8em 2em' }} onClick={onRestart}>Play Again</button>
    </div>
  );
}