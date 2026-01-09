# Python 環境建置

使用 uv 管理 Python 環境
- 以 `uv init` 初始專案使用 Python 3.13
- 套件均以 `uv add` 加入專案
- Python 程式檔均以 `uv run` 執行

## Windows 環境注意事項

- Windows 中 Python 預設會以系統的編碼輸出文字，在繁體中文版會是 Big5，也就是 CP950 編碼，請特別留意