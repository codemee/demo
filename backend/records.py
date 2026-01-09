import json
import os
from typing import Dict, Optional


class RecordsManager:
    """成績記錄管理器"""

    def __init__(self, records_file: str = "data/records.json"):
        self.records_file = records_file
        self._ensure_records_file()

    def _ensure_records_file(self):
        """確保記錄檔案存在"""
        os.makedirs(os.path.dirname(self.records_file), exist_ok=True)
        if not os.path.exists(self.records_file):
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "best_attempts": None,  # 最少猜測次數
                    "best_time": None       # 最快時間（秒）
                }, f, indent=2)

    def get_records(self) -> Dict[str, Optional[float]]:
        """獲取最佳成績記錄"""
        try:
            with open(self.records_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    "best_attempts": data.get("best_attempts"),
                    "best_time": data.get("best_time")
                }
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果檔案損壞，重新建立
            self._ensure_records_file()
            return {"best_attempts": None, "best_time": None}

    def update_records(self, attempts: int, time_seconds: float) -> bool:
        """
        更新成績記錄

        Args:
            attempts: 猜測次數
            time_seconds: 遊戲時間（秒）

        Returns:
            是否有更新記錄
        """
        current_records = self.get_records()
        updated = False

        # 檢查是否是最少猜測次數
        if (current_records["best_attempts"] is None or
            attempts < current_records["best_attempts"]):
            current_records["best_attempts"] = attempts
            updated = True

        # 檢查是否是最快時間
        if (current_records["best_time"] is None or
            time_seconds < current_records["best_time"]):
            current_records["best_time"] = time_seconds
            updated = True

        # 如果有更新，寫入檔案
        if updated:
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(current_records, f, indent=2)

        return updated

    def reset_records(self):
        """重置成績記錄（用於測試）"""
        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump({
                "best_attempts": None,
                "best_time": None
            }, f, indent=2)


# 全域成績管理器實例
records_manager = RecordsManager()