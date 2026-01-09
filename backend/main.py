from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import sys

# 將當前目錄加入 Python 路徑，以便匯入其他模組
sys.path.insert(0, os.path.dirname(__file__))

from game_logic import game_logic
from records import records_manager


# Pydantic 模型
class GuessRequest(BaseModel):
    game_id: str
    guess: str

class RecordRequest(BaseModel):
    attempts: int
    time: float


# 建立 FastAPI 應用程式
app = FastAPI(title="1A2B 猜數字遊戲", version="1.0.0")

# 啟用 CORS（開發用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生產環境中應該指定具體的來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/game/new")
async def new_game():
    """開始新遊戲"""
    try:
        game_id = game_logic.new_game()
        return {"game_id": game_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"無法開始新遊戲: {str(e)}")


@app.post("/api/game/guess")
async def guess(request: GuessRequest):
    """提交猜測"""
    try:
        a_count, b_count, is_correct = game_logic.check_guess(request.game_id, request.guess)
        attempts = game_logic.get_attempts(request.game_id)

        result = {
            "result": {"A": a_count, "B": b_count},
            "is_correct": is_correct,
            "attempts": attempts
        }

        # 如果猜對了，移除遊戲狀態
        if is_correct:
            game_logic.remove_game(request.game_id)

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"猜測處理失敗: {str(e)}")


@app.get("/api/records")
async def get_records():
    """獲取最佳成績"""
    try:
        records = records_manager.get_records()
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取成績失敗: {str(e)}")


@app.post("/api/records")
async def save_record(request: RecordRequest):
    """儲存新成績"""
    try:
        updated = records_manager.update_records(request.attempts, request.time)
        return {"updated": updated}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"儲存成績失敗: {str(e)}")


@app.get("/health")
async def health_check():
    """健康檢查"""
    return {"status": "ok"}


# SPA fallback - 處理前端路由
from fastapi.responses import FileResponse

@app.get("/{path:path}")
async def serve_frontend(path: str):
    """提供前端檔案"""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
    file_path = os.path.join(frontend_path, path)

    # 如果是具體檔案，直接提供
    if os.path.isfile(file_path):
        return FileResponse(file_path)

    # 否則提供 index.html（SPA 模式）
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    return {"error": "File not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)