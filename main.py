import sys
from PySide6.QtWidgets import QApplication
from ui.overlay_manager import OverlayManager

def disable_mac_app_nap():
    try:
        # Mac環境で、ウィンドウが非アクティブになっても処理が一時停止(App Nap)されないようにする
        from Foundation import NSProcessInfo, NSActivityUserInitiated, NSActivityLatencyCritical
        activity_options = NSActivityUserInitiated | NSActivityLatencyCritical
        reason = "Realtime screen capturing and translation requires continuous background execution"
        return NSProcessInfo.processInfo().beginActivityWithOptions_reason_(activity_options, reason)
    except Exception as e:
        print(f"App Nap disabled failed: {e}")
        return None

from ui.home_window import HomeWindow

def main():
    app = QApplication(sys.argv)
    
    # App Nap の無効化を保持（ガベージコレクションされないように変数に保持）
    activity = disable_mac_app_nap()
    
    # オーバーレイ管理クラスとホーム画面の初期化
    manager = OverlayManager()
    home_window = HomeWindow(manager)
    
    # アプリケーション終了時にワーカーを停止させる
    app.aboutToQuit.connect(manager.cleanup)
    
    # ホーム画面を表示
    home_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
