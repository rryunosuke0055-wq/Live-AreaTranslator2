import cv2
import numpy as np
import Quartz
import Vision
from deep_translator import GoogleTranslator


class TextExtractor:
    def __init__(self):
        # Mac ネイティブOCR用のリクエストを作成
        self.req = Vision.VNRecognizeTextRequest.alloc().init()
        # Fast モードに変更（Accurate よりも大幅に高速、リアルタイム向き）
        self.req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelFast)
        # 認識言語を英語と日本語に指定
        self.req.setRecognitionLanguages_(["en-US", "ja-JP"])

    def extract_text(self, image_bgr: np.ndarray) -> str:
        """
        OpenCVの画像(BGR)を受け取り、MacネイティブのVision Frameworkでテキストを抽出する。
        ファイル書き出しを経由せず、メモリ上で直接処理することで高速化。
        """
        try:
            # BGR → RGB に変換してからCGImageを生成（ファイルI/O不要）
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            h, w, c = image_rgb.shape
            bytes_per_row = c * w

            # CGImageをメモリ上で直接生成
            provider = Quartz.CGDataProviderCreateWithData(
                None, image_rgb.tobytes(), h * bytes_per_row, None
            )
            cg_image = Quartz.CGImageCreate(
                w, h, 8, 8 * c, bytes_per_row,
                Quartz.CGColorSpaceCreateDeviceRGB(),
                Quartz.kCGBitmapByteOrderDefault,
                provider, None, False,
                Quartz.kCGRenderingIntentDefault,
            )

            handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(
                cg_image, None
            )
            success, error = handler.performRequests_error_([self.req], None)
            if success:
                results = self.req.results()
                text = "\n".join(
                    [res.topCandidates_(1)[0].string() for res in results]
                )
                return text.strip()
        except Exception as e:
            print(f"OCR Error: {e}")
        return ""


class TranslatorAPI:
    def __init__(self):
        # 無料で使える Google Translator (deep-translator) を使用
        self._source = 'auto'
        self._target = 'ja'

    def translate(self, text: str) -> str:
        """
        APIを用いて、与えられたテキストを日本語に翻訳する。
        毎回新しい Translator インスタンスを使うことで、HTTP 接続エラーを回避しつつ高速化。
        """
        if not text:
            return ""

        try:
            translator = GoogleTranslator(source=self._source, target=self._target)
            translated = translator.translate(text)
            return translated
        except Exception as e:
            print(f"Translation Error: {e}")
            return f"[翻訳エラー] {e}"
