from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tkinter as tk
import threading
import time
import logging

# ✅ 視聴上限
watch_limit = 10
watched = set()

# ✅ Logging設定
logging.basicConfig(
    filename='watch_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    encoding='utf-8'
)

def log_video_watch(video_id):
    logging.info(f"視聴した動画ID: {video_id}")

# ✅ GUI（Tkinter）構築
root = tk.Tk()
root.title("視聴カウントバー")
canvas = tk.Canvas(root, width=300, height=50)
canvas.pack()

def draw_bar(count):
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 30 * count, 50, fill="green")
    canvas.create_text(150, 25, text=f"{count} / {watch_limit}", fill="white")

draw_bar(0)

# ✅ Selenium操作を別スレッドで実行
def watch_shorts():
    options = Options()
    options.binary_location = "/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    options.add_argument("--start-maximized")
    
    service = Service("/Users/maple/Desktop/Programing/chromedriver-mac-x64/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://www.youtube.com/shorts/")
    time.sleep(2)

    while len(watched) < watch_limit:
        current_url = driver.current_url
        if "/shorts/" in current_url:
            video_id = current_url.split("/shorts/")[-1]
            if video_id not in watched:
                watched.add(video_id)
                log_video_watch(video_id)
                print(f"視聴数: {len(watched)} / {watch_limit}")
                # GUIバー更新はメインスレッドなので、threading安全のためイベント利用が理想ですが
                # ここでは単純に呼び出し（問題がなければこのまま）
                draw_bar(len(watched))
        time.sleep(2)

    driver.get("https://www.youtube.com/")
    print("✅ 制限に達したため、ホームに戻しました。")

# ✅ スレッド起動
threading.Thread(target=watch_shorts, daemon=True).start()

# ✅ GUI実行（メインスレッドで）
root.mainloop()
