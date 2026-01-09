import random
import string
from typing import Dict, Tuple


class GameLogic:
    """1A2B 猜數字遊戲邏輯"""

    def __init__(self):
        # 儲存進行中的遊戲狀態：game_id -> (answer, attempts)
        self.games: Dict[str, Tuple[str, int]] = {}

    def generate_game_id(self) -> str:
        """生成唯一的遊戲 ID"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def generate_answer(self) -> str:
        """生成 4 位不重複的數字作為答案"""
        digits = list('0123456789')
        random.shuffle(digits)
        return ''.join(digits[:4])

    def new_game(self) -> str:
        """開始新遊戲，返回遊戲 ID"""
        game_id = self.generate_game_id()
        answer = self.generate_answer()
        self.games[game_id] = (answer, 0)
        return game_id

    def check_guess(self, game_id: str, guess: str) -> Tuple[int, int, bool]:
        """
        檢查猜測結果

        Args:
            game_id: 遊戲 ID
            guess: 猜測的 4 位數字字串

        Returns:
            Tuple[A數量, B數量, 是否猜對]
        """
        if game_id not in self.games:
            raise ValueError("遊戲不存在")

        answer, attempts = self.games[game_id]

        # 增加猜測次數
        attempts += 1
        self.games[game_id] = (answer, attempts)

        if len(guess) != 4 or not guess.isdigit():
            raise ValueError("猜測必須是 4 位數字")

        # 檢查是否有重複數字
        if len(set(guess)) != 4:
            raise ValueError("數字不能重複")

        a_count = 0
        b_count = 0

        # 計算 A（位置和數字都正確）
        for i in range(4):
            if guess[i] == answer[i]:
                a_count += 1

        # 計算 B（數字正確但位置錯誤）
        guess_digits = list(guess)
        answer_digits = list(answer)

        for g_digit in guess_digits:
            if g_digit in answer_digits:
                b_count += 1
                answer_digits.remove(g_digit)

        # B 數量不包含 A
        b_count -= a_count

        is_correct = a_count == 4

        return a_count, b_count, is_correct

    def get_attempts(self, game_id: str) -> int:
        """獲取遊戲的猜測次數"""
        if game_id not in self.games:
            raise ValueError("遊戲不存在")
        return self.games[game_id][1]

    def remove_game(self, game_id: str):
        """移除已完成的遊戲"""
        if game_id in self.games:
            del self.games[game_id]


# 全域遊戲邏輯實例
game_logic = GameLogic()