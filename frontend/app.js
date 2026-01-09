class GameApp {
    constructor() {
        this.gameId = null;
        this.timerInterval = null;
        this.startTime = null;
        this.attempts = 0;
        this.maxAttempts = 10;

        // DOM 元素
        this.timerElement = document.getElementById('timer');
        this.bestAttemptsElement = document.getElementById('best-attempts');
        this.bestTimeElement = document.getElementById('best-time');
        this.digitInputs = [
            document.getElementById('digit1'),
            document.getElementById('digit2'),
            document.getElementById('digit3'),
            document.getElementById('digit4')
        ];
        this.errorElement = document.getElementById('input-error');
        this.historyElement = document.getElementById('history');
        this.newGameBtn = document.getElementById('new-game-btn');
        this.messageElement = document.getElementById('game-message');

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadRecords();
        this.startNewGame();
    }

    setupEventListeners() {
        // 輸入框事件
        this.digitInputs.forEach((input, index) => {
            input.addEventListener('input', (e) => this.handleInput(e, index));
            input.addEventListener('keydown', (e) => this.handleKeydown(e, index));
            input.addEventListener('focus', () => this.clearError());
        });

        // 新遊戲按鈕
        this.newGameBtn.addEventListener('click', () => this.startNewGame());
    }

    handleInput(event, index) {
        const input = event.target;
        const value = input.value;

        // 只允許數字
        if (!/^\d*$/.test(value)) {
            input.value = '';
            return;
        }

        // 自動跳到下一個輸入框
        if (value.length === 1 && index < 3) {
            this.digitInputs[index + 1].focus();
        }

        // 檢查重複數字
        this.validateInput();
    }

    handleKeydown(event, index) {
        const input = event.target;

        if (event.key === 'Backspace' && input.value === '' && index > 0) {
            // 退格鍵跳到上一個輸入框
            this.digitInputs[index - 1].focus();
        } else if (event.key === 'Enter') {
            // Enter 鍵送出猜測
            this.submitGuess();
        } else if (event.key === 'ArrowLeft' && index > 0) {
            this.digitInputs[index - 1].focus();
        } else if (event.key === 'ArrowRight' && index < 3) {
            this.digitInputs[index + 1].focus();
        }
    }

    validateInput() {
        const values = this.digitInputs.map(input => input.value);
        const filledValues = values.filter(v => v !== '');
        const uniqueValues = new Set(filledValues);

        // 檢查重複
        if (filledValues.length !== uniqueValues.size) {
            this.showError('數字不能重複');
            return false;
        }

        this.clearError();
        return true;
    }

    showError(message) {
        this.errorElement.textContent = message;
        this.digitInputs.forEach(input => input.classList.add('error'));
    }

    clearError() {
        this.errorElement.textContent = '';
        this.digitInputs.forEach(input => input.classList.remove('error'));
    }

    getGuess() {
        const guess = this.digitInputs.map(input => input.value).join('');
        return guess.length === 4 ? guess : null;
    }

    async submitGuess() {
        if (!this.gameId) {
            this.showMessage('請先開始新遊戲', 'error');
            return;
        }

        const guess = this.getGuess();
        if (!guess) {
            this.showError('請輸入完整的 4 位數字');
            return;
        }

        if (!this.validateInput()) {
            return;
        }

        try {
            const response = await fetch('/api/game/guess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    game_id: this.gameId,
                    guess: guess
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || '猜測失敗');
            }

            this.attempts = result.attempts;
            this.addHistoryItem(guess, result.result.A, result.result.B);

            // 清空輸入框
            this.clearInputs();

            if (result.is_correct) {
                this.gameWin();
            } else if (this.attempts >= this.maxAttempts) {
                this.gameLose();
            }

        } catch (error) {
            this.showMessage(`猜測失敗: ${error.message}`, 'error');
        }
    }

    addHistoryItem(guess, aCount, bCount) {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';

        const guessSpan = document.createElement('span');
        guessSpan.className = 'history-guess';
        guessSpan.textContent = guess;

        const resultSpan = document.createElement('span');
        resultSpan.className = 'history-result';

        const aSpan = document.createElement('span');
        aSpan.className = 'a-count';
        aSpan.textContent = `${aCount}A`;

        const bSpan = document.createElement('span');
        bSpan.className = 'b-count';
        bSpan.textContent = `${bCount}B`;

        resultSpan.appendChild(aSpan);
        resultSpan.appendChild(document.createTextNode(' '));
        resultSpan.appendChild(bSpan);

        historyItem.appendChild(guessSpan);
        historyItem.appendChild(resultSpan);

        // 新記錄插入到最上方
        this.historyElement.insertBefore(historyItem, this.historyElement.firstChild);
    }

    clearInputs() {
        this.digitInputs.forEach(input => {
            input.value = '';
        });
        this.digitInputs[0].focus();
    }

    startTimer() {
        this.startTime = Date.now();
        this.timerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
            this.updateTimer(elapsed);
        }, 1000);
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    updateTimer(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        this.timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    async startNewGame() {
        try {
            this.stopTimer();
            this.clearInputs();
            this.clearHistory();
            this.clearMessage();

            const response = await fetch('/api/game/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || '無法開始新遊戲');
            }

            this.gameId = result.game_id;
            this.attempts = 0;
            this.startTimer();
            this.showMessage('新遊戲開始！請輸入 4 個不重複的數字。', 'success');

            // 聚焦到第一個輸入框
            this.digitInputs[0].focus();

        } catch (error) {
            this.showMessage(`開始遊戲失敗: ${error.message}`, 'error');
        }
    }

    gameWin() {
        this.stopTimer();
        const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
        this.showMessage(`恭喜猜對了！用時 ${this.formatTime(elapsed)}，猜了 ${this.attempts} 次。`, 'success');

        // 儲存成績
        this.saveRecord(this.attempts, elapsed);
    }

    gameLose() {
        this.stopTimer();
        this.showMessage(`遊戲結束！您已經猜了 ${this.maxAttempts} 次卻還沒猜對。`, 'error');
    }

    async saveRecord(attempts, timeSeconds) {
        try {
            await fetch('/api/records', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    attempts: attempts,
                    time: timeSeconds
                })
            });
            // 重新載入最佳成績
            this.loadRecords();
        } catch (error) {
            console.error('儲存成績失敗:', error);
        }
    }

    async loadRecords() {
        try {
            const response = await fetch('/api/records');
            const records = await response.json();

            this.bestAttemptsElement.textContent = records.best_attempts || '-';
            this.bestTimeElement.textContent = records.best_time ? this.formatTime(records.best_time) : '-';
        } catch (error) {
            console.error('載入成績失敗:', error);
        }
    }

    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    clearHistory() {
        this.historyElement.innerHTML = '';
    }

    showMessage(message, type = '') {
        this.messageElement.textContent = message;
        this.messageElement.className = `game-message ${type}`;
    }

    clearMessage() {
        this.messageElement.textContent = '';
        this.messageElement.className = 'game-message';
    }
}

// 應用程式初始化
document.addEventListener('DOMContentLoaded', () => {
    new GameApp();
});