import pyperclip
import pyautogui
import datetime
import os
import json

def is_input_field_active():
    # アクティブなウィンドウやフィールドをチェックするロジックを実装
    # 簡易的にTrueを返す
    return True

def insert_text_to_active_field(text):
    # 「ご視聴ありがとうございました。」を削除
    text = text.replace("ご視聴ありがとうございました。", "")
    text = text.replace("次の動画でお会いしましょう", "")
    # 末尾の空白を削除
    text = text.strip()
    
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')  # Windowsの場合。macOSは('command', 'v')

def save_backup(text):
    # 設定ファイルからバックアップ先を取得
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    backup_dir = config.get('backup_directory', './backups')
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_transcription.txt"
    backup_path = os.path.join(backup_dir, filename)
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(text)

def cleanup_old_backups():
    """
    設定ファイルで指定された日数より古いバックアップファイルを削除します
    """
    try:
        # 設定ファイルからバックアップディレクトリと保持期間を取得
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        backup_dir = config.get('backup_directory', './backups')
        days_to_keep = config.get('backup_retention_days', 30)
        
        if not os.path.exists(backup_dir):
            return 0  # ディレクトリが存在しない場合は0を返す
            
        current_time = datetime.datetime.now()
        deleted_count = 0
        
        for filename in os.listdir(backup_dir):
            if not filename.endswith('_transcription.txt'):
                continue
                
            file_path = os.path.join(backup_dir, filename)
            file_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            age = current_time - file_time
            
            if age.days > days_to_keep:
                os.remove(file_path)
                deleted_count += 1
                
        return deleted_count
    except Exception as e:
        print(f"バックアップファイルの削除中にエラーが発生しました: {str(e)}")
        return 0