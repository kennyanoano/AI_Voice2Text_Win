#　ツールの目的

cursorとか使っているときにボイス入力がしたい！
けどwindowsにはいい感じのボイス入力がなかったので自力で作ってみた
ツールを立ち上げた状態で　shift+F1（カスタマイズ可能）を押すと　録音開始、もう一回押すと喋った内容を文字起こしして今選択しているウィンドウに入力


## 主な機能

- **Shift-F1キーによる音声入力の開始・停止**
- **音声をテキストに変換し、アクティブな入力欄に自動挿入**
- **変換テキストのバックアップ機能**
- **エラーハンドリングとユーザーへのフィードバック**
- **設定ファイルによる柔軟なカスタマイズ**

---

## ファイル構成

- `voice_input_app.py`: メインアプリケーションのエントリーポイント
- `recorder.py`: 音声録音機能を提供
- `transcriber.py`: 音声をテキストに変換する機能を提供
- `utils.py`: ユーティリティ関数とエラーハンドリング
- `config.json`: ショートカットキーやバックアップ先などの設定

---


## 動作説明

1. **アプリケーションの起動**
   - `voice_input_app.py`を実行すると、GUIが表示されます。

2. **音声入力の開始**
   - Shift-F1キーを押すか、GUIの「録音開始」ボタンをクリックします。
   - アクティブな入力欄が選択されていない場合、エラーメッセージが表示されます。

3. **音声入力の停止とテキスト変換**
   - 再度Shift-F1キーを押すか、「録音開始」ボタンをクリックすると録音が停止します。
   - 録音された音声がOpenAI APIに送信され、テキストに変換されます。

4. **テキストの挿入とバックアップ**
   - 変換されたテキストがアクティブな入力欄に自動で挿入されます。
   - 同時に、設定したバックアップ先にテキストが保存されます。

## エラーハンドリング

- **入力欄未選択時**
  - 録音開始時にアクティブな入力欄がない場合、エラーメッセージを表示します。

- **API通信エラー**
  - 文字起こしの際にエラーが発生した場合、エラーメッセージを表示し、処理を中断します。

- **バックアップエラー**
  - テキストの保存時にエラーが発生した場合、エラーメッセージを表示します。

## セキュリティとプライバシー

- **APIキーの管理**
  - 環境変数`OPENAI_API_KEY`からAPIキーを取得します。

- **音声データの扱い**
  - 処理後、音声ファイルは削除されます。

- **録音中のインジケータ**
  - 録音中はステータスラベルに「録音中...」と表示されます。

## カスタマイズ

- **設定の変更**
  - `config.json`でショートカットキー、バックアップ先、バックアップ保持期間を変更できます。

- **バックアップの自動整理機能**
  - アプリケーション起動時に、設定された保持期間（デフォルト30日）を超えた古いバックアップファイルを自動的に削除します。
  - 保持期間は`config.json`の`backup_retention_days`で設定可能です。

## 注意点

- **アクティブな入力欄へのテキスト挿入**
  - `pyautogui`を使用していますが、場合によっては管理者権限が必要な場合があります。

- **プラットフォーム依存のコード**
  - 一部のキー操作やシステム呼び出しは、WindowsとmacOSで異なる場合がありますので調整してください。