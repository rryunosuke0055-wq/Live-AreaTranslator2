import cv2
import numpy as np
import Quartz
import Vision
from deep_translator import GoogleTranslator

class TextExtractor:
    def __init__(self):
        # Mac ネイティブOCR用のリクエストを作成
        self.req = Vision.VNRecognizeTextRequest.alloc().init()
        self.req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
        # 認識言語を英語と日本語に指定
        self.req.setRecognitionLanguages_(["en-US", "ja-JP"])

    def extract_text(self, image_bgr: np.ndarray) -> str:
        """
        OpenCVの画像(BGR)を受け取り、MacネイティブのVision Frameworkでテキストを抽出する。
        Tesseractが不要で、かつ非常に高速・高精度に動作する。
        """
        # 一時ファイルとして書き出してURL化（CGImageへの変換より安定するため）
        tmp_path = "/tmp/live_areatranslator_ocr.png"
        cv2.imwrite(tmp_path, image_bgr)
        
        url = Quartz.NSURL.fileURLWithPath_(tmp_path)
        handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
        
        success, error = handler.performRequests_error_([self.req], None)
        if success:
            results = self.req.results()
            # 抽出された結果を結合
            text = "\n".join([res.topCandidates_(1)[0].string() for res in results])
            return text.strip()
        return ""

class TranslatorAPI:
    def __init__(self):
        # 無料で使える Google Translator (deep-translator) を使用
        self.translator = GoogleTranslator(source='auto', target='ja')
        
    def translate(self, text: str) -> str:
        """
        APIを用いて、与えられたテキストを日本語に翻訳する。
        """
        if not text:
            return ""
            
        print(f"Original Text:\n{text}")
        try:
            translated = self.translator.translate(text)
            return translated
        except Exception as e:
            print(f"Translation Error: {e}")
            return f"[翻訳エラー] {e}"
