"""
測試在瀏覽器中輸入 1234
"""
import asyncio
from playwright.async_api import async_playwright


async def test_input_1234():
    async with async_playwright() as p:
        # 啟動瀏覽器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("正在開啟遊戲頁面...")
        await page.goto("http://localhost:8000")
        
        # 等待頁面載入
        await page.wait_for_selector("#digit1")
        print("頁面載入完成")
        
        # 等待新遊戲初始化
        await asyncio.sleep(1)
        
        # 在四個輸入框中輸入 1234
        print("開始輸入 1234...")
        await page.fill("#digit1", "1")
        print("輸入 1")
        await asyncio.sleep(0.3)
        
        await page.fill("#digit2", "2")
        print("輸入 2")
        await asyncio.sleep(0.3)
        
        await page.fill("#digit3", "3")
        print("輸入 3")
        await asyncio.sleep(0.3)
        
        await page.fill("#digit4", "4")
        print("輸入 4")
        await asyncio.sleep(0.5)
        
        # 檢查輸入值
        digit1_value = await page.input_value("#digit1")
        digit2_value = await page.input_value("#digit2")
        digit3_value = await page.input_value("#digit3")
        digit4_value = await page.input_value("#digit4")
        
        print(f"\n輸入結果: {digit1_value}{digit2_value}{digit3_value}{digit4_value}")
        
        # 檢查錯誤訊息
        error_element = await page.query_selector("#input-error")
        error_text = await error_element.inner_text() if error_element else ""
        
        if error_text:
            print(f"錯誤訊息: {error_text}")
        else:
            print("沒有錯誤訊息，輸入成功！")
        
        # 按 Enter 送出猜測
        print("\n按 Enter 送出猜測...")
        await page.press("#digit4", "Enter")
        await asyncio.sleep(1)
        
        # 檢查歷史記錄
        history_items = await page.query_selector_all(".history-item")
        if history_items:
            first_history = history_items[0]
            guess_text = await first_history.query_selector(".history-guess")
            result_text = await first_history.query_selector(".history-result")
            
            if guess_text and result_text:
                guess = await guess_text.inner_text()
                result = await result_text.inner_text()
                print(f"猜測記錄: {guess} -> {result}")
        
        print("\n測試完成！瀏覽器將保持開啟狀態 5 秒...")
        await asyncio.sleep(5)
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_input_1234())
