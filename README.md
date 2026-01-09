# 1A2B 猜數字遊戲

一個完整的 Web 版本 1A2B 猜數字遊戲，包含前端介面和後端 API。

## 功能特色

- 🎯 4 位數 1A2B 猜數字遊戲
- ⌨️ 智能輸入框自動跳轉
- 🚫 即時數字重複驗證
- ⏱️ 遊戲計時器
- 📊 成績記錄系統
- 📱 響應式設計
- 🎨 大自然綠色主題

## 技術架構

- **前端**: Vanilla JavaScript + HTML5 + CSS3
- **後端**: FastAPI (Python)
- **環境管理**: uv (Python 3.13)
- **資料儲存**: JSON 檔案

## 快速開始

### 環境需求

- Python 3.13+
- uv 套件管理器

### 安裝與運行

1. **複製專案**
   ```bash
   git clone <repository-url>
   cd demo
   ```

2. **安裝依賴**
   ```bash
   uv sync
   ```

3. **啟動伺服器**
   ```bash
   uv run python backend/main.py
   ```

4. **開啟瀏覽器**

   訪問 `http://localhost:8000` 開始遊戲

## 遊戲規則

1. 系統會隨機生成一個 4 位不重複的數字
2. 玩家需要在輸入框中猜測這個數字
3. 輸入完 4 個數字後按 Enter 送出猜測
4. 系統會回應幾 A 幾 B：
   - **A**: 數字和位置都正確
   - **B**: 數字正確但位置錯誤
5. 最多可以猜 10 次
6. 猜對或用完 10 次機會即結束遊戲

## API 端點

### 遊戲相關
- `POST /api/game/new` - 開始新遊戲
- `POST /api/game/guess` - 提交猜測

### 成績相關
- `GET /api/records` - 獲取最佳成績
- `POST /api/records` - 儲存成績

### 系統
- `GET /health` - 健康檢查

## 專案結構

```
demo/
├── backend/
│   ├── main.py          # FastAPI 主程式
│   ├── game_logic.py    # 遊戲邏輯
│   └── records.py       # 成績管理
├── frontend/
│   ├── index.html       # 主頁面
│   ├── style.css        # 樣式表
│   └── app.js           # 前端邏輯
├── data/
│   └── records.json     # 成績記錄
├── pyproject.toml       # 專案配置
└── README.md            # 說明文件
```

## 開發說明

### 環境建置

使用 uv 管理 Python 環境：

```bash
# 初始化專案
uv init --python 3.13

# 安裝依賴
uv add fastapi uvicorn

# 運行程式
uv run python backend/main.py
```

### 設計特色

- **響應式設計**: 支援桌面和手機裝置
- **無障礙設計**: 使用語意化 HTML 和鍵盤導航
- **即時驗證**: 輸入時立即檢查錯誤
- **優化體驗**: 自動跳轉和智能提示

## 授權

本專案僅供學習和個人使用。