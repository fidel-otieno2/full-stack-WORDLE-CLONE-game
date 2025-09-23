# 🔠 Wordle Game Clone - React Edition 🎮

A stylish, customizable Wordle game clone built with **React** and **Vite**. Guess the 5-letter word within 6 tries. Built with love and collaboration by a team of four students from Moringa School.

> **Team Members**: Fidel Martins, Hassan, Abdiazi, Ben  
> **Institution**: Moringa School  
> **Project Type**: MVP (Minimum Viable Product)

---

## 📌 Table of Contents

- [🎯 Features](#-features)
- [📸 Screenshots](#-screenshots)
- [🧰 Technologies Used](#-technologies-used)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [🛠 Folder Structure](#-folder-structure)
- [📚 How It Works](#-how-it-works)
- [💡 Future Improvements](#-future-improvements)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍👩‍👧‍👦 Authors](#-authors)

---

## 🎯 Features

- ✅ 5-letter word guessing game
- ✅ 6 attempts per round
- ✅ Beautiful animated tiles and keyboard
- ✅ Input validation
- ✅ Random word selected from a large uppercase word list
- ✅ Word list is easily customizable via `word.js`
- ✅ Color-coded feedback (green, yellow, gray)
- ✅ Hints and toast feedback for win/loss
- ✅ Custom animations (rainbow background, twinkling stars, pop tiles)
- ✅ Mobile responsive

---

## 📸 Screenshots

> *Sample preview of the gameplay*

![Gameplay board](./screenshots/gameplay-board.png)
![Keyboard interaction](./screenshots/keyboard.png)

---

## 🧰 Technologies Used

- ⚛️ React
- ⚡ Vite
- 🎨 CSS Modules
- 🧪 React Testing Library (optional for testing)
- 🗂 LocalStorage (for future state persistence)

---

## 📦 Installation

To run the project locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/your-username/wordle-clone-react.git
cd wordle-clone-react

# Install dependencies
npm install

# Start the development server
npm run dev


##🚀 Usage

Type a 5-letter word using your keyboard or on-screen keys.

Press Enter to submit.

Colors will show feedback:

🟩 Green = correct letter in correct position

🟨 Yellow = correct letter in wrong position

⬜ Gray = incorrect letter

You win if you guess correctly within 6 tries.

A toast message appears on win/loss.

##🛠 Folder Structure

arduino
Copy
Edit
/src
├── components
│   ├── Board.js
│   ├── Tile.js
│   ├── Keyboard.js
│   └── Toast.js
├── context
│   └── GameContext.js
├── utils
│   ├── helper.js
│   └── word.js          ← ✅ You can update the word list here
├── App.js
├── index.js
├── index.css
└── ...

##📚 How It Works

On load, a random uppercase word is selected from word.js.

The game listens to keyboard events and updates the board dynamically.

After each guess:

It checks for correctness

Gives visual feedback via tile colors

Moves to next row after Enter

Once the player wins or exhausts attempts, a message is shown and the game disables input.

##💡 Future Improvements

✅ Add win streak tracking

✅ Add dark/light toggle

⏳ Add difficulty levels (hard mode, longer words)

⏳ Use API for live word validation

⏳ Share score functionality

⏳ Add mobile vibration feedback

⏳ Sound effects for keys and success/failure

##🧪 Testing
We use React Testing Library for unit tests.

To run tests:

bash
Copy
Edit
npm run test
Tests cover:

Rendering the board

Validating guesses

Input interaction

Feedback accuracy

##📄 License

MIT License © 2025 Fidel Martins and Team
Feel free to use, modify, and share — with credit.

##👨‍👩‍👧‍👦 Authors

Fidel Martins - UI/UX & Project Lead

Hassan - Game Logic & Input Handling

Abdiazi - Word List Design & Testing

Ben - Styling, Animations, and CSS polish

✨ This project was built with dedication, learning, and collaboration at Moringa School. Thank you for checking it out!

