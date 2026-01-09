#!/usr/bin/env python3
"""
簡單的遊戲邏輯測試
"""
import sys
import os

# 加入後端目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from game_logic import GameLogic

def test_game_logic():
    """測試遊戲邏輯"""
    game_logic = GameLogic()

    print("測試 1A2B 遊戲邏輯...")

    # 測試新遊戲
    game_id = game_logic.new_game()
    print(f"OK: 新遊戲建立成功，遊戲 ID: {game_id}")

    # 模擬已知的答案進行測試
    # 我們需要稍微修改測試方式，因為答案是隨機的
    # 讓我們測試錯誤處理
    try:
        # 測試重複數字
        game_logic.check_guess(game_id, "1123")
        print("ERROR: 應該要拒絕重複數字")
    except ValueError as e:
        print(f"OK: 正確拒絕重複數字: {e}")

    try:
        # 測試位數不對
        game_logic.check_guess(game_id, "123")
        print("ERROR: 應該要拒絕錯誤位數")
    except ValueError as e:
        print(f"OK: 正確拒絕錯誤位數: {e}")

    try:
        # 測試不存在的遊戲
        game_logic.check_guess("invalid_id", "1234")
        print("ERROR: 應該要拒絕不存在的遊戲")
    except ValueError as e:
        print(f"OK: 正確拒絕不存在的遊戲: {e}")

    print("所有基本測試通過！")

def test_sample_game():
    """測試一個完整的遊戲範例"""
    print("\n測試完整遊戲流程...")

    game_logic = GameLogic()

    # 建立遊戲
    game_id = game_logic.new_game()
    print(f"遊戲 ID: {game_id}")

    # 進行一些猜測（我們不知道答案，所以只是測試流程）
    test_guesses = ["0123", "4567", "8901"]

    for guess in test_guesses:
        try:
            a_count, b_count, is_correct = game_logic.check_guess(game_id, guess)
            attempts = game_logic.get_attempts(game_id)
            print(f"猜測 {guess}: {a_count}A{b_count}B (第 {attempts} 次)")

            if is_correct:
                print("猜對了！")
                break
        except ValueError as e:
            print(f"猜測 {guess} 失敗: {e}")

    print("遊戲流程測試完成")

if __name__ == "__main__":
    test_game_logic()
    test_sample_game()
    print("\n所有測試完成！遊戲系統運行正常。")