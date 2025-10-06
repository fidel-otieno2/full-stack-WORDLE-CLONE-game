import React, { useState } from 'react';

export default function Login({ onLogin, onRegister }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim() && password.trim() && (!isRegistering || email.trim())) {
      if (isRegistering) {
        onRegister(username.trim(), email.trim(), password);
      } else {
        onLogin(username.trim(), password);
      }
    }
  };

  return (
    <div
      className="app-container"
      style={{
        maxWidth: 480,
        margin: '2rem auto',
        padding: '2rem',
        textAlign: 'center',
        background: 'linear-gradient(to bottom right, #191970, #0d1a2b)',
        borderRadius: '1rem',
        boxShadow: '0 0 20px rgba(0,0,0,0.4)',
      }}
    >
      <h1 className="title" style={{ color: '#fff', marginBottom: '1rem' }}>
        Wordle Game
      </h1>

      <p style={{ color: '#fff', fontSize: '1.1rem', marginBottom: '1.5rem' }}>
        {isRegistering ? 'Create an account to start playing' : 'Enter your credentials to start playing'}
      </p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          autoFocus
          style={{
            width: '100%',
            padding: '0.8rem',
            fontSize: '1.1rem',
            background: '#3a3a3c',
            border: '1px solid #565758',
            borderRadius: '0.4rem',
            color: '#fff',
            marginBottom: '1rem',
          }}
        />
        {isRegistering && (
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            style={{
              width: '100%',
              padding: '0.8rem',
              fontSize: '1.1rem',
              background: '#3a3a3c',
              border: '1px solid #565758',
              borderRadius: '0.4rem',
              color: '#fff',
              marginBottom: '1rem',
            }}
          />
        )}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          style={{
            width: '100%',
            padding: '0.8rem',
            fontSize: '1.1rem',
            background: '#3a3a3c',
            border: '1px solid #565758',
            borderRadius: '0.4rem',
            color: '#fff',
            marginBottom: '1.5rem',
          }}
        />
        <button
          type="submit"
          className="restart-btn"
          style={{
            width: '100%',
            padding: '0.8rem',
            fontSize: '1.1rem',
            background: 'linear-gradient(to right, #32cd32, #228b22)',
            color: '#fff',
            border: 'none',
            borderRadius: '0.4rem',
            cursor: 'pointer',
            marginBottom: '1rem',
          }}
        >
          {isRegistering ? 'Create Account' : "Let's Play"}
        </button>
        <button
          type="button"
          onClick={() => setIsRegistering(!isRegistering)}
          style={{
            width: '100%',
            padding: '0.8rem',
            fontSize: '1rem',
            background: 'transparent',
            color: '#b59f3b',
            border: '1px solid #b59f3b',
            borderRadius: '0.4rem',
            cursor: 'pointer',
          }}
        >
          {isRegistering ? 'Already have an account? Login' : "Don't have an account? Register"}
        </button>
      </form>
    </div>
  );
}
