import flet as ft
from src.ui_manager import UIManager

def main():
    """アプリケーションのメインエントリーポイント"""
    def init_app(page: ft.Page):
        # ページ設定
        page.title = "統計処理アプリケーション"
        page.window_width = 700
        page.window_height = 600
        page.window_resizable = False
        page.padding = 20
        page.theme_mode = ft.ThemeMode.LIGHT
        
        # UIManagerのインスタンス化とレイアウト作成
        ui_manager = UIManager()
        layout = ui_manager.create_layout()
        
        # キーボードイベントハンドラーを設定
        page.on_keyboard_event = ui_manager._on_keyboard_event
        
        # レイアウトをページに追加
        page.add(layout)
        page.update()

    # fletアプリケーションの起動
    ft.app(target=init_app)

if __name__ == "__main__":
    main()