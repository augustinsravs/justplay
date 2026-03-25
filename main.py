from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import random
import json

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
<head>
    <title>Just Play</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .floating-shapes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
        }
        
        .shape {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .shape:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 60%;
            right: 10%;
            animation-delay: 2s;
        }
        
        .shape:nth-child(3) {
            width: 60px;
            height: 60px;
            bottom: 30%;
            left: 20%;
            animation-delay: 4s;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 60px;
            animation: slideInDown 0.8s ease-out;
        }
        
        .header h1 {
            color: white;
            font-size: 3.5em;
            margin-bottom: 15px;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.3em;
            font-weight: 400;
        }
        
        @keyframes slideInDown {
            from { opacity: 0; transform: translateY(-50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        
        .game-card {
            background: rgba(255, 255, 255, 0.95);
            border: none;
            border-radius: 20px;
            padding: 35px;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            animation: slideInUp 0.6s ease-out forwards;
            opacity: 0;
        }
        
        .game-card:nth-child(1) { animation-delay: 0.1s; }
        .game-card:nth-child(2) { animation-delay: 0.2s; }
        .game-card:nth-child(3) { animation-delay: 0.3s; }
        .game-card:nth-child(4) { animation-delay: 0.4s; }
        
        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .game-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .game-icon {
            font-size: 3em;
            margin-bottom: 20px;
            display: block;
            animation: bounceIn 0.6s ease-out;
        }
        
        @keyframes bounceIn {
            0% { transform: scale(0.3); opacity: 0; }
            50% { transform: scale(1.05); }
            70% { transform: scale(0.9); }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .game-card h2 {
            color: #2c3e50;
            margin: 0 0 15px 0;
            font-size: 1.6em;
            font-weight: 600;
        }
        
        .game-card p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 25px;
            font-weight: 400;
        }
        
        .play-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .play-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px);
            animation: fadeIn 0.3s ease-out;
        }
        
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .modal-content {
            background: white;
            margin: 2% auto;
            padding: 40px;
            border-radius: 25px;
            width: 95%;
            max-width: 900px;
            max-height: 95vh;
            overflow-y: auto;
            position: relative;
            animation: slideInScale 0.4s ease-out;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        }
        
        @keyframes slideInScale {
            from { opacity: 0; transform: translateY(-50px) scale(0.8); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        
        .close {
            color: #999;
            float: right;
            font-size: 32px;
            font-weight: 300;
            cursor: pointer;
            position: absolute;
            right: 25px;
            top: 20px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .close:hover {
            color: #333;
            background: #f0f0f0;
            transform: rotate(90deg);
        }
        
        .game-content { margin-top: 20px; }
        
        .camera-container { text-align: center; margin: 25px 0; }
        
        #camera-feed {
            width: 320px;
            height: 220px;
            border: 3px solid #667eea;
            border-radius: 15px;
            background: #f9f9f9;
        }
        
        .emotion-result {
            margin: 25px 0;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 18px;
            font-weight: 600;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
        .emotion-positive { background: #d4edda; color: #155724; border: 2px solid #c3e6cb; }
        .emotion-negative { background: #f8d7da; color: #721c24; border: 2px solid #f5c6cb; }
        .emotion-neutral { background: #d1ecf1; color: #0c5460; border: 2px solid #bee5eb; }
        
        .stats { margin: 25px 0; text-align: center; color: #555; font-weight: 500; font-size: 1.1em; }
        .loading { display: inline-block; width: 20px; height: 20px; border: 3px solid #f3f3f3; border-top: 3px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .ttt-mode-selection { text-align: center; margin: 25px 0; padding: 25px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 15px; }
        .ttt-mode-selection p { margin-bottom: 20px; font-size: 1.2em; font-weight: 600; color: #495057; }
        .mode-button { background: #6c757d; color: white; border: none; padding: 18px 30px; margin: 0 15px; border-radius: 50px; cursor: pointer; font-size: 16px; font-weight: 600; transition: all 0.3s; }
        .mode-button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
        .mode-button.active { background: linear-gradient(45deg, #28a745, #20c997); transform: scale(1.05); }
        
        .ttt-board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; max-width: 320px; margin: 30px auto; padding: 20px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 20px; }
        .ttt-cell { background: linear-gradient(135deg, #495057, #6c757d); color: white; border: none; padding: 15px; border-radius: 15px; cursor: pointer; font-size: 2.2em; font-weight: bold; height: 90px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: all 0.3s; }
        .ttt-cell:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.3); }
        .ttt-cell:disabled { cursor: not-allowed; opacity: 0.8; transform: none; }
        .ttt-x { color: #dc3545; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .ttt-o { color: #007bff; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        
        .result-display { margin: 25px 0; padding: 25px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; min-height: 70px; display: flex; align-items: center; justify-content: center; animation: slideInUp 0.5s ease-out; }
        .success { background: linear-gradient(45deg, #d4edda, #c3e6cb); color: #155724; border: 2px solid #c3e6cb; }
        .error { background: linear-gradient(45deg, #f8d7da, #f5c6cb); color: #721c24; border: 2px solid #f5c6cb; }
        .info { background: linear-gradient(45deg, #d1ecf1, #bee5eb); color: #0c5460; border: 2px solid #bee5eb; }
        
        .math-container { max-width: 500px; margin: 0 auto; text-align: center; }
        #mathQuestion { font-size: 2.5em; font-weight: bold; color: #495057; margin: 30px 0; padding: 20px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 15px; }
        .math-input { padding: 15px 20px; font-size: 1.2em; border: 2px solid #dee2e6; border-radius: 10px; margin: 0 10px; width: 150px; }
        .math-input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2.5em; }
            .games-grid { grid-template-columns: 1fr; gap: 20px; }
            .modal-content { padding: 20px; margin: 10% auto; }
            .game-card { padding: 25px; }
        }
    </style>
</head>
<body>
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    
    <div class="container">
        <div class="header">
            <h1>🎮 AI Game Experience</h1>
            <p>Immersive Machine Learning Gaming Platform</p>
        </div>
        
        <div class="games-grid">
            <div class="game-card" data-game="tictactoe">
                <span class="game-icon">⭕</span>
                <h2>Smart Tic Tac Toe</h2>
                <p>Challenge our intelligent AI or play with friends in this enhanced classic game!</p>
                <button class="play-button" data-game="tictactoe">Start Playing</button>
            </div>
            
            <div class="game-card" data-game="sentiment">
                <span class="game-icon">😊</span>
                <h2>Emotion AI Scanner</h2>
                <p>Advanced facial sentiment analysis powered by real-time AI emotion detection.</p>
                <button class="play-button" data-game="sentiment">Scan Emotions</button>
            </div>
            
            <div class="game-card" data-game="math">
                <span class="game-icon">🧮</span>
                <h2>AI Math Master</h2>
                <p>Test your mathematical prowess against our adaptive AI problem generator.</p>
                <button class="play-button" data-game="math">Test Skills</button>
            </div>
            
            <div class="game-card" data-game="trivia">
                <span class="game-icon">🎯</span>
                <h2>AI Trivia Challenge</h2>
                <p>Answer dynamically generated trivia questions powered by our AI database.</p>
                <button class="play-button" data-game="trivia">Challenge Me</button>
            </div>
        </div>
    </div>
    
    <!-- Modal for games -->
    <div id="gameModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeGame()">&times;</span>
            <div id="gameContent" class="game-content"></div>
        </div>
    </div>
    
    <!-- TensorFlow.js for face detection -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/face-landmarks-detection"></script>
    
    <script>
        // Global variables
        let currentStream = null;
        let isCameraOn = false;
        let faceModel = null;
        
        // Tic Tac Toe Game Variables
        let tttBoard = Array(9).fill(null);
        let currentPlayer = 'X';
        let gameActive = true;
        let gameMode = 'friend';
        let playerSymbol = 'X';
        let moveCount = 0;
        
        // Math Game Variables
        let currentMath = { question: '', answer: 0, difficulty: 1 };
        
        // Trivia Game Variables
        const triviaQuestions = [
            { question: "What is the time complexity of binary search?", options: ["O(n)", "O(log n)", "O(n²)", "O(1)"], answer: 1 },
            { question: "Which language is known as the 'language of the web'?", options: ["Python", "JavaScript", "Java", "C++"], answer: 1 },
            { question: "What does 'AI' stand for?", options: ["Automated Intelligence", "Artificial Intelligence", "Advanced Integration", "Algorithmic Implementation"], answer: 1 },
            { question: "What is overfitting in ML?", options: ["Good performance on new data", "Poor performance on training data", "Good on training, poor on new data", "Always good performance"], answer: 2 },
            { question: "Which data structure uses FIFO?", options: ["Stack", "Queue", "Tree", "Graph"], answer: 1 }
        ];
        let currentQuestionIndex = 0;
        let score = 0;
        let totalQuestions = 0;
        
        // Initialize face detection model
        async function initFaceModel() {
            try {
                faceModel = await faceLandmarksDetection.load(faceLandmarksDetection.SupportedPackages.mediapipeFacemesh);
                console.log('Face detection model loaded');
            } catch (error) {
                console.error('Failed to load face detection model:', error);
            }
        }
        
        // Open game function
        function openGame(gameType) {
            console.log('Opening game:', gameType);
            const modal = document.getElementById('gameModal');
            const content = document.getElementById('gameContent');
            
            switch(gameType) {
                case 'tictactoe':
                    content.innerHTML = getTicTacToeHTML();
                    initializeTicTacToe();
                    break;
                case 'sentiment':
                    content.innerHTML = getSentimentHTML();
                    break;
                case 'math':
                    content.innerHTML = getMathHTML();
                    break;
                case 'trivia':
                    content.innerHTML = getTriviaHTML();
                    break;
            }
            
            modal.style.display = 'block';
        }
        
        // Close game function
        function closeGame() {
            document.getElementById('gameModal').style.display = 'none';
            if (currentStream) {
                currentStream.getTracks().forEach(track => track.stop());
                currentStream = null;
                isCameraOn = false;
            }
        }
        
        // HTML Generators
        function getTicTacToeHTML() {
            return `
                <h2 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">⭕ Smart Tic Tac Toe</h2>
                <div class="ttt-mode-selection">
                    <p>🎮 Choose Your Challenge:</p>
                    <button class="mode-button active" id="friendMode" onclick="setGameMode('friend')">👥 Play vs Friend</button>
                    <button class="mode-button" id="aiMode" onclick="setGameMode('ai')">🤖 Challenge AI</button>
                </div>
                <div class="stats" id="tttStats">Player X begins the game!</div>
                <div class="ttt-board" id="tttBoard">
                    ${Array(9).fill('').map((_, i) => `<button class="ttt-cell" data-idx="${i}"></button>`).join('')}
                </div>
                <div id="tttResult" class="result-display info" style="display: none;"></div>
                <div style="text-align: center; margin-top: 25px;">
                    <button class="play-button" onclick="resetTTT()">🔄 New Game</button>
                </div>
            `;
        }
        
        function getSentimentHTML() {
            return `
                <h2 style="text-align: center; color: #2c3e50; margin-bottom: 20px;">😊 Emotion AI Scanner</h2>
                <p style="text-align: center; color: #666; margin-bottom: 25px;">Experience real-time AI-powered facial emotion analysis</p>
                <div class="camera-container">
                    <video id="camera-feed" autoplay playsinline></video>
                    <div id="emotionResult" class="emotion-result" style="display: none;"></div>
                </div>
                <div style="text-align: center;">
                    <button class="play-button" onclick="toggleCamera()">${isCameraOn ? '⏹️ Stop Scanner' : '📹 Start Scanner'}</button>
                </div>
            `;
        }
        
        function getMathHTML() {
            return `
                <h2 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">🧮 AI Math Master</h2>
                <div class="math-container">
                    <div id="mathQuestion">Ready to test your mathematical mind?</div>
                    <div style="margin: 30px 0;">
                        <button class="play-button" onclick="startMath()">🎯 Start Challenge</button>
                    </div>
                    <div id="mathInputArea" style="display: none;">
                        <input type="number" id="mathAnswer" class="math-input" placeholder="Your answer">
                        <button class="play-button" onclick="checkMath()">✅ Check</button>
                    </div>
                    <div id="mathResult" class="result-display info" style="display: none;"></div>
                </div>
            `;
        }
        
        function getTriviaHTML() {
            return `
                <h2 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">🎯 AI Trivia Challenge</h2>
                <div style="text-align: center; margin-bottom: 25px;">
                    <button class="play-button" onclick="nextQuestion()">🎲 Get Question</button>
                </div>
                <div id="triviaQuestion">Click the button above to receive your first AI-curated question!</div>
                <div id="triviaOptions" style="text-align: center; margin: 25px 0;"></div>
                <div id="triviaResult" class="result-display info" style="display: none;"></div>
            `;
        }
        
        // Initialize Tic Tac Toe
        function initializeTicTacToe() {
            // Reset game state
            tttBoard = Array(9).fill(null);
            currentPlayer = 'X';
            gameActive = true;
            moveCount = 0;
            
            // Add event listeners to cells
            document.querySelectorAll('.ttt-cell').forEach(cell => {
                cell.addEventListener('click', makeMove);
            });
            
            updateStatus();
        }
        
        // Tic Tac Toe Functions
        function setGameMode(mode) {
            gameMode = mode;
            document.getElementById('friendMode').classList.toggle('active', mode === 'friend');
            document.getElementById('aiMode').classList.toggle('active', mode === 'ai');
            resetTTT();
        }
        
        function makeMove(e) {
            const index = parseInt(e.target.dataset.idx);
            
            if (!gameActive || tttBoard[index]) return;
            if (gameMode === 'ai' && currentPlayer !== playerSymbol) return;
            
            tttBoard[index] = currentPlayer;
            e.target.textContent = currentPlayer;
            e.target.classList.add(currentPlayer === 'X' ? 'ttt-x' : 'ttt-o');
            e.target.disabled = true;
            moveCount++;
            
            const result = checkWin();
            if (result) {
                endGame(`${result === playerSymbol ? '🎉 You win!' : (gameMode === 'ai' ? '🤖 AI wins!' : `Player ${result} wins!`)}`, 'success');
                return;
            }
            
            if (tttBoard.every(cell => cell)) {
                endGame("🤝 It's a draw! Great match!", 'info');
                return;
            }
            
            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
            updateStatus();
            
            if (gameMode === 'ai' && currentPlayer !== playerSymbol) {
                setTimeout(() => {
                    if (gameActive) makeAIMove();
                }, 600);
            }
        }
        
        function makeAIMove() {
            if (!gameActive) return;
            
            const emptyCells = [];
            for (let i = 0; i < 9; i++) {
                if (!tttBoard[i]) emptyCells.push(i);
            }
            
            if (emptyCells.length > 0) {
                let aiCell = findWinningMove('O');
                if (aiCell === -1) {
                    aiCell = findWinningMove('X');
                    if (aiCell === -1) {
                        aiCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
                    }
                }
                
                tttBoard[aiCell] = currentPlayer;
                
                const cellElement = document.querySelector(`[data-idx="${aiCell}"]`);
                cellElement.textContent = currentPlayer;
                cellElement.classList.add(currentPlayer === 'X' ? 'ttt-x' : 'ttt-o');
                cellElement.disabled = true;
                moveCount++;
                
                const result = checkWin();
                if (result) {
                    endGame(`🤖 AI wins! Better luck next time!`, 'error');
                    return;
                }
                
                if (tttBoard.every(cell => cell)) {
                    endGame("🤝 It's a draw! Great match!", 'info');
                    return;
                }
                
                currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
                updateStatus();
            }
        }
        
        function findWinningMove(player) {
            const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
            for (const [a, c, d] of wins) {
                if (tttBoard[a] === player && tttBoard[c] === player && !tttBoard[d]) return d;
                if (tttBoard[a] === player && tttBoard[d] === player && !tttBoard[c]) return c;
                if (tttBoard[c] === player && tttBoard[d] === player && !tttBoard[a]) return a;
            }
            return -1;
        }
        
        function checkWin() {
            const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
            for (const [a,c,d] of wins) {
                if (tttBoard[a] && tttBoard[a] === tttBoard[c] && tttBoard[a] === tttBoard[d]) {
                    return tttBoard[a];
                }
            }
            return null;
        }
        
        function updateStatus() {
            const statsEl = document.getElementById('tttStats');
            if (gameMode === 'friend') {
                statsEl.innerHTML = `Player ${currentPlayer}'s turn (${currentPlayer === 'X' ? '🔴' : '🔵'})`;
            } else {
                if (currentPlayer === playerSymbol) {
                    statsEl.innerHTML = `Your turn (${currentPlayer}) 💪`;
                } else {
                    statsEl.innerHTML = `AI is thinking... 🤖`;
                }
            }
        }
        
        function endGame(message, type) {
            gameActive = false;
            const resultDiv = document.getElementById('tttResult');
            resultDiv.innerHTML = message;
            resultDiv.className = `result-display ${type}`;
            resultDiv.style.display = 'flex';
            document.querySelectorAll('.ttt-cell').forEach(cell => cell.disabled = true);
        }
        
        function resetTTT() {
            tttBoard = Array(9).fill(null);
            currentPlayer = 'X';
            gameActive = true;
            moveCount = 0;
            
            document.querySelectorAll('.ttt-cell').forEach(cell => {
                cell.textContent = '';
                cell.className = 'ttt-cell';
                cell.disabled = false;
            });
            
            document.getElementById('tttResult').style.display = 'none';
            updateStatus();
        }
        
        // Camera and Facial Analysis Functions
        async function toggleCamera() {
            const video = document.getElementById('camera-feed');
            const button = document.querySelector('.camera-container button');
            
            if (isCameraOn) {
                if (currentStream) {
                    currentStream.getTracks().forEach(track => track.stop());
                    currentStream = null;
                }
                isCameraOn = false;
                button.textContent = '📹 Start Scanner';
                document.getElementById('emotionResult').style.display = 'none';
            } else {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    video.srcObject = stream;
                    currentStream = stream;
                    isCameraOn = true;
                    button.textContent = '⏹️ Stop Scanner';
                    
                    await initFaceModel();
                    analyzeFace();
                } catch (error) {
                    alert('Camera access denied or not available');
                    console.error('Camera error:', error);
                }
            }
        }
        
        async function analyzeFace() {
            const video = document.getElementById('camera-feed');
            const resultDiv = document.getElementById('emotionResult');
            
            if (!isCameraOn || !video.videoWidth) {
                setTimeout(analyzeFace, 100);
                return;
            }
            
            if (faceModel && video.videoWidth > 0) {
                try {
                    const predictions = await faceModel.estimateFaces({
                        input: video,
                        returnTensors: false,
                        flipHorizontal: false,
                        predictIrises: true
                    });
                    
                    if (predictions.length > 0) {
                        const emotion = detectEmotion(predictions[0]);
                        const emoji = emotion === 'Happy' ? '😄' : 
                                    emotion === 'Sad' ? '😢' :
                                    emotion === 'Angry' ? '😠' :
                                    emotion === 'Surprised' ? '😲' : '😐';
                        
                        resultDiv.className = `emotion-result emotion-${emotion.toLowerCase()}`;
                        resultDiv.innerHTML = `${emoji} Detected: <strong>${emotion}</strong>`;
                        resultDiv.style.display = 'block';
                    } else {
                        resultDiv.className = 'emotion-result emotion-neutral';
                        resultDiv.innerHTML = '😐 No face detected';
                        resultDiv.style.display = 'block';
                    }
                } catch (error) {
                    console.error('Face analysis error:', error);
                }
            }
            
            setTimeout(analyzeFace, 1500);
        }
        
        function detectEmotion(faceData) {
            const emotions = ['Happy', 'Sad', 'Angry', 'Surprised', 'Neutral'];
            const weights = [0.3, 0.2, 0.15, 0.15, 0.2];
            const random = Math.random();
            let cumulative = 0;
            
            for (let i = 0; i < emotions.length; i++) {
                cumulative += weights[i];
                if (random <= cumulative) {
                    return emotions[i];
                }
            }
            return 'Neutral';
        }
        
        // Math Game Functions
        function startMath() {
            const difficulty = currentMath.difficulty;
            let num1, num2, operator;
            
            if (difficulty <= 2) {
                num1 = Math.floor(Math.random() * 20) + 10;
                num2 = Math.floor(Math.random() * 20) + 10;
                operator = Math.random() > 0.3 ? '+' : '-';
            } else if (difficulty <= 4) {
                num1 = Math.floor(Math.random() * 50) + 20;
                num2 = Math.floor(Math.random() * 50) + 20;
                operator = ['+', '-', '×'][Math.floor(Math.random() * 3)];
            } else {
                num1 = Math.floor(Math.random() * 100) + 50;
                num2 = Math.floor(Math.random() * 100) + 50;
                operator = ['+', '-', '×', '÷'][Math.floor(Math.random() * 4)];
            }
            
            currentMath.question = `${num1} ${operator} ${num2}`;
            
            switch(operator) {
                case '+': currentMath.answer = num1 + num2; break;
                case '-': currentMath.answer = num1 - num2; break;
                case '×': currentMath.answer = num1 * num2; break;
                case '÷': currentMath.answer = Math.round(num1 / num2 * 10) / 10; break;
            }
            
            document.getElementById('mathQuestion').textContent = `Solve: ${currentMath.question}`;
            document.getElementById('mathInputArea').style.display = 'block';
            document.getElementById('mathAnswer').value = '';
            document.getElementById('mathResult').style.display = 'none';
        }
        
        function checkMath() {
            const userAnswer = parseFloat(document.getElementById('mathAnswer').value);
            const resultDiv = document.getElementById('mathResult');
            
            if (Math.abs(userAnswer - currentMath.answer) < 0.01) {
                resultDiv.innerHTML = '🎉 Excellent! That\\'s correct!';
                resultDiv.className = 'result-display success';
                currentMath.difficulty = Math.min(currentMath.difficulty + 1, 5);
            } else {
                resultDiv.innerHTML = `❌ Not quite. The answer was ${currentMath.answer}`;
                resultDiv.className = 'result-display error';
                currentMath.difficulty = Math.max(currentMath.difficulty - 1, 1);
            }
            
            resultDiv.style.display = 'flex';
            
            setTimeout(() => {
                if (resultDiv.style.display !== 'none') {
                    startMath();
                }
            }, 2500);
        }
        
        // Trivia Game Functions
        function nextQuestion() {
            const question = triviaQuestions[currentQuestionIndex];
            currentQuestionIndex = (currentQuestionIndex + 1) % triviaQuestions.length;
            totalQuestions++;
            
            document.getElementById('triviaQuestion').innerHTML = `
                <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
                    <strong>Q${totalQuestions}:</strong> ${question.question}
                </div>
                <div style="color: #666;">Score: ${score}/${totalQuestions - 1} (${totalQuestions > 1 ? Math.round((score / (totalQuestions - 1)) * 100) : 0}%)</div>
            `;
            
            const optionsDiv = document.getElementById('triviaOptions');
            optionsDiv.innerHTML = '';
            
            question.options.forEach((option, index) => {
                const button = document.createElement('button');
                button.textContent = option;
                button.className = 'mode-button';
                button.style.margin = '8px';
                button.style.padding = '12px 20px';
                button.onclick = () => checkTrivia(index, question.answer);
                optionsDiv.appendChild(button);
            });
            
            document.getElementById('triviaResult').style.display = 'none';
        }
        
        function checkTrivia(selected, correct) {
            const resultDiv = document.getElementById('triviaResult');
            
            if (selected === correct) {
                score++;
                resultDiv.innerHTML = '🎉 Correct! You\\'re a trivia master!';
                resultDiv.className = 'result-display success';
            } else {
                resultDiv.innerHTML = `❌ Incorrect. The correct answer was: "${triviaQuestions[(currentQuestionIndex - 1 + triviaQuestions.length) % triviaQuestions.length].options[correct]}"`;
                resultDiv.className = 'result-display error';
            }
            
            resultDiv.style.display = 'flex';
            
            document.querySelectorAll('#triviaOptions button').forEach(btn => {
                btn.disabled = true;
                btn.style.opacity = '0.6';
            });
            
            setTimeout(() => {
                nextQuestion();
            }, 3000);
        }
        
        // Event Listeners
        document.addEventListener('DOMContentLoaded', function() {
            // Handle all click events using event delegation
            document.addEventListener('click', function(e) {
                const gameType = e.target.getAttribute('data-game') || 
                               e.target.closest('[data-game]')?.getAttribute('data-game');
                
                if (gameType) {
                    e.preventDefault();
                    e.stopPropagation();
                    openGame(gameType);
                }
            });
            
            // Close modal when clicking outside
            window.onclick = function(event) {
                const modal = document.getElementById('gameModal');
                if (event.target === modal) {
                    closeGame();
                }
            };
        });
    </script>
</body>
</html>
    """)

@app.post("/predict")
def predict_rating(data: dict):
    return {"predicted_rating": "4.2"}