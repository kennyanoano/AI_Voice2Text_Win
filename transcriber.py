import openai
import os
import logging

class TranscriptionError(Exception):
    """音声文字起こし処理中のエラーを表す例外クラス"""
    pass

class Transcriber:
    def __init__(self):
        # APIキーを環境変数から取得
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        self.client = openai.OpenAI(api_key=api_key)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def transcribe(self, audio_file):
        try:
            with open(audio_file, "rb") as file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file,
                    language="ja",
                    prompt="文字起こしのプロとして適切な文字起こしを行え"
                )
            self.logger.info("音声の文字起こしが完了しました")
            return transcript.text

        except openai.APIError as e:
            self.logger.error(f"API エラー: {str(e)}")
            raise TranscriptionError(f"文字起こし処理中にエラーが発生しました: {str(e)}")
            
        except FileNotFoundError:
            self.logger.error(f"ファイルが見つかりません: {audio_file}")
            raise TranscriptionError(f"音声ファイルが見つかりません: {audio_file}")
            
        except Exception as e:
            self.logger.error(f"予期せぬエラー: {str(e)}")
            raise TranscriptionError(f"予期せぬエラーが発生しました: {str(e)}")