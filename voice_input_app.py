import sys
import os
import tkinter as tk
from tkinter import messagebox
from recorder import Recorder
from transcriber import Transcriber
import utils
import threading
import json
import keyboard  # 新しくインポート

class VoiceInputApp:
    def __init__(self):
        # 設定の読み込み
        with open('config.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.hotkey = self.config.get('hotkey', 'shift+f1')  # キー指定形式を変更

        self.recorder = Recorder()
        self.transcriber = Transcriber()
        self.is_recording = False
        self.setup_gui()
        self.setup_hotkey()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Voice Input")
        # ウィンドウを小さく設定
        self.root.geometry("150x60")
        # 常に最前面に表示
        self.root.attributes('-topmost', True)
        # 背景色を設定（デフォルト状態: 薄い青）
        self.root.configure(bg='#e6f3ff')
        
        # ステータスラベルとボタンを1行に配置
        frame = tk.Frame(self.root, bg='#e6f3ff')
        frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        self.status_label = tk.Label(frame, text="待機中", bg='#e6f3ff')
        self.status_label.pack(side='left', padx=5)
        
        self.start_button = tk.Button(frame, text="録音", width=6, command=self.toggle_recording)
        self.start_button.pack(side='right', padx=5)

    def setup_hotkey(self):
        # グローバルホットキーの設定
        keyboard.add_hotkey(self.hotkey, self.toggle_recording)

    def toggle_recording(self, event=None):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        if not utils.is_input_field_active():
            messagebox.showerror("エラー", "入力欄が選択されていません。")
            return
        self.is_recording = True
        self.status_label.config(text="録音中")
        # 録音中は背景を赤く
        self.root.configure(bg='#ff9999')
        self.status_label.configure(bg='#ff9999')
        self.start_button.configure(text="停止")
        threading.Thread(target=self.recorder.start_recording).start()

    def stop_recording(self):
        self.is_recording = False
        self.status_label.config(text="処理中")
        # 処理中は背景をオレンジに
        self.root.configure(bg='#ffb366')
        self.status_label.configure(bg='#ffb366')
        self.recorder.stop_recording()
        threading.Thread(target=self.process_audio).start()

    def process_audio(self):
        try:
            audio_file = self.recorder.get_audio_file()
            text = self.transcriber.transcribe(audio_file)
            utils.insert_text_to_active_field(text)
            utils.save_backup(text)
            self.status_label.config(text="待機中")
            # 完了したら背景を薄い青に戻す
            self.root.configure(bg='#e6f3ff')
            self.status_label.configure(bg='#e6f3ff')
            self.start_button.configure(text="録音")
        except Exception as e:
            messagebox.showerror("エラー", f"処理中にエラーが発生しました：\n{e}")
            self.status_label.config(text="エラー")
        finally:
            if os.path.exists(audio_file):
                os.remove(audio_file)

    def run(self):
        try:
            # アプリケーション起動時に古いバックアップを削除
            deleted_count = utils.cleanup_old_backups()
            if deleted_count > 0:
                print(f"{deleted_count}個の古いバックアップファイルを削除しました。")
            
            self.root.mainloop()
        finally:
            # アプリケーション終了時にホットキーを解除
            keyboard.unhook_all()

if __name__ == "__main__":
    app = VoiceInputApp()
    app.run()