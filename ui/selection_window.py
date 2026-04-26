from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QGuiApplication

class SelectionWindow(QWidget):
    def __init__(self, on_selected):
        super().__init__()
        self.on_selected = on_selected
        
        # ---- キャプチャ用 (画面全体の絶対座標) ----
        self.global_start = QPoint()
        self.global_end = QPoint()

        self.init_ui()

    def init_ui(self):
        # フルスクリーンで最前面、枠なし、タスクバー非表示
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        # 背景を透明に
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 単一モニター分の表示とするため、ジオメトリの強制結合処理を削除
        # 親（OverlayManager）側で各モニターのジオメトリが直接 setGeometry されます。
        
        # カーソルを十字に変更
        self.setCursor(Qt.CursorShape.CrossCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 画面全体を半透明の暗い色で塗りつぶす
        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))

        if self.is_drawing and not self.start_point.isNull() and not self.end_point.isNull():
            # 選択中の領域を切り抜く（透明にする）ための描画
            selection_rect = QRect(self.start_point, self.end_point).normalized()
            
            # その領域のハイライト（暗い背景を消す）
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(selection_rect, Qt.GlobalColor.transparent)
            
            # 元のモードに戻して枠線を描画
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            pen = QPen(QColor(0, 255, 0), 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawRect(selection_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # キャプチャ用: ウィンドウの影響を受けない画面全体の絶対座標
            self.global_start = event.globalPosition().toPoint()
            self.global_end = self.global_start
            
            # 描画用: その絶対座標を、このウィジェット上のローカル座標へ変換
            self.start_point = self.mapFromGlobal(self.global_start)
            self.end_point = self.start_point
            
            self.is_drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            # ドラッグ中は描画用と絶対座標の両方を更新
            self.global_end = event.globalPosition().toPoint()
            self.end_point = self.mapFromGlobal(self.global_end)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_drawing:
            self.global_end = event.globalPosition().toPoint()
            self.end_point = self.mapFromGlobal(self.global_end)
            self.is_drawing = False
            self.update()
            
            capture_rect = QRect(self.global_start, self.global_end).normalized()
            # 一定サイズ以上の領域が選択された場合のみコールバックを呼ぶ
            if capture_rect.width() > 10 and capture_rect.height() > 10:
                # 完全に一致した絶対座標をコールバックに渡す
                self.on_selected(capture_rect)
            else:
                # キャンセル処理：閉じる
                self.close()

    def keyPressEvent(self, event):
        # ESCキーでキャンセル
        if event.key() == Qt.Key.Key_Escape:
            self.close()
