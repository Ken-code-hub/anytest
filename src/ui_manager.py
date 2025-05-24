import flet as ft
from typing import Callable, Dict, List
import pyperclip
from .validator import DataValidator
from .analyzer import StatisticalAnalyzer

class UIManager:
    def __init__(self):
        """UIコンポーネントの初期化"""
        # 変数入力フィールド
        # 共通のテキストフィールドスタイル
        text_field_style = {
            "width": 400,
            "text_size": 16
        }

        self.variable_input = ft.TextField(
            label="変数名",
            hint_text="カンマ区切りで変数名を入力 (例: x,y,z)",
            on_focus=self._on_text_field_focus,
            **text_field_style
        )
        
        self.value_input = ft.TextField(
            label="変数の値",
            hint_text="カンマ区切りで値を入力 (例: 10,20,30)",
            on_focus=self._on_text_field_focus,
            **text_field_style
        )
        
        self.error_input = ft.TextField(
            label="誤差",
            hint_text="カンマ区切りで誤差を入力 (例: 0.1,0.2,0.3)",
            on_focus=self._on_text_field_focus,
            **text_field_style
        )
        
        self.function_input = ft.TextField(
            label="関数",
            hint_text="計算する関数を入力 (例: x + y * z)",
            on_focus=self._on_text_field_focus,
            **text_field_style
        )

        self.data_input = ft.TextField(
            label="データを入力",
            multiline=True,
            min_lines=3,
            max_lines=5,
            hint_text="スペースまたは改行で区切って数値を入力してください",
            on_focus=self._on_text_field_focus,
            **text_field_style
        )
        
        # 結果表示のスタイル設定
        self.result_text = ft.Text(
            value="",
            size=14,
            weight=ft.FontWeight.W_400,
            color=ft.colors.BLACK,
            selectable=True
        )
        
        # エラー表示のコンテナ作成
        self.error_container = ft.Row(
            controls=[
                ft.Icon(
                    name=ft.icons.ERROR_OUTLINE,
                    color=ft.colors.RED_400,
                    size=20
                ),
                ft.Text(
                    value="",
                    color=ft.colors.RED_400,
                    size=14,
                    weight=ft.FontWeight.W_500
                )
            ],
            spacing=8
        )
        self.error_container.visible = False
        self.error_text = self.error_container.controls[1]  # エラーテキストへの参照を保持

        self.qtest_button = ft.ElevatedButton(
            text="Q検定実行",
            on_click=lambda _: self.handle_test_click("qtest")
        )

        self.confidence_interval_button = ft.ElevatedButton(
            text="信頼区間計算",
            on_click=lambda _: self.handle_test_click("confidence_interval")
        )

        self.error_propagation_button = ft.ElevatedButton(
            text="誤差伝播計算",
            on_click=lambda _: self.handle_test_click("error_propagation")
        )

        # UIコンポーネントの参照を保持
        self._validator = DataValidator()
        self._analyzer = StatisticalAnalyzer()
        
        # 現在フォーカスされているテキストフィールドを保持
        self.focused_text_field = None

    def _on_text_field_focus(self, e):
        """テキストフィールドがフォーカスされた時の処理"""
        self.focused_text_field = e.control

    def _on_keyboard_event(self, e: ft.KeyboardEvent):
        """キーボードイベントを処理する"""
        # Ctrl+V または Cmd+V でペースト
        if (e.key == "v" and e.ctrl) or (e.key == "v" and e.meta):
            self._paste_from_clipboard()
        # Ctrl+C または Cmd+C でコピー（テキストが選択されている場合）
        elif (e.key == "c" and e.ctrl) or (e.key == "c" and e.meta):
            self._copy_to_clipboard()

    def _paste_from_clipboard(self):
        """クリップボードから内容をペーストする"""
        if self.focused_text_field:
            try:
                clipboard_content = pyperclip.paste()
                if clipboard_content:
                    current_value = self.focused_text_field.value or ""
                    # カーソル位置が取得できない場合は末尾に追加
                    self.focused_text_field.value = current_value + clipboard_content
                    self.focused_text_field.update()
            except Exception as e:
                print(f"ペーストエラー: {e}")

    def _copy_to_clipboard(self):
        """選択されたテキストをクリップボードにコピーする"""
        if self.focused_text_field and self.focused_text_field.value:
            try:
                # テキストフィールドの全内容をコピー（選択範囲の取得は困難なため）
                pyperclip.copy(self.focused_text_field.value)
            except Exception as e:
                print(f"コピーエラー: {e}")

    def _paste_to_field(self, text_field: ft.TextField):
        """指定されたテキストフィールドにクリップボードの内容をペーストする"""
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content:
                # 現在の値に追加するか、置き換えるかを選択（今回は置き換え）
                text_field.value = clipboard_content
                text_field.update()
        except Exception as e:
            print(f"ペーストエラー: {e}")

    def create_layout(self) -> ft.Container:
        """UIレイアウトを作成する

        Returns:
            ft.Container: UIコンポーネントを含むコンテナ
        """
        # スタイル設定
        # Flet公式APIではButtonStyleのshape/side/bgcolorはサポートされていないため削除
        # ボタン色はElevatedButtonの引数で指定
        self.qtest_button.bgcolor = ft.colors.GREY_50
        self.qtest_button.color = ft.colors.BLACK
        self.confidence_interval_button.bgcolor = ft.colors.GREY_50
        self.confidence_interval_button.color = ft.colors.BLACK
        self.error_propagation_button.bgcolor = ft.colors.BLUE_700
        self.error_propagation_button.color = ft.colors.WHITE

        # 基本統計タブのコンテンツ
        basic_stats_content = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.data_input,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="📋 ペースト",
                            on_click=lambda _: self._paste_to_field(self.data_input),
                            bgcolor=ft.colors.GREEN_50,
                            color=ft.colors.GREEN_700,
                            width=100
                        ),
                        padding=ft.padding.only(left=10, top=25)
                    )
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=20),  # スペーシング
                ft.Row(
                    controls=[
                        self.qtest_button,
                        self.confidence_interval_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12
                )
            ]),
            padding=ft.padding.symmetric(horizontal=24, vertical=16)
        )

        # 誤差伝播タブのコンテンツ
        error_prop_content = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.function_input,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="📋",
                            on_click=lambda _: self._paste_to_field(self.function_input),
                            bgcolor=ft.colors.GREEN_50,
                            color=ft.colors.GREEN_700,
                            width=50
                        ),
                        padding=ft.padding.only(left=10, top=25)
                    )
                ], alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    self.variable_input,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="📋",
                            on_click=lambda _: self._paste_to_field(self.variable_input),
                            bgcolor=ft.colors.GREEN_50,
                            color=ft.colors.GREEN_700,
                            width=50
                        ),
                        padding=ft.padding.only(left=10, top=25)
                    )
                ], alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    self.value_input,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="📋",
                            on_click=lambda _: self._paste_to_field(self.value_input),
                            bgcolor=ft.colors.GREEN_50,
                            color=ft.colors.GREEN_700,
                            width=50
                        ),
                        padding=ft.padding.only(left=10, top=25)
                    )
                ], alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    self.error_input,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="📋",
                            on_click=lambda _: self._paste_to_field(self.error_input),
                            bgcolor=ft.colors.GREEN_50,
                            color=ft.colors.GREEN_700,
                            width=50
                        ),
                        padding=ft.padding.only(left=10, top=25)
                    )
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=20),  # スペーシング
                ft.Row(
                    controls=[self.error_propagation_button],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ], spacing=12),
            padding=ft.padding.symmetric(horizontal=24, vertical=16)
        )

        # タブの作成
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            indicator_color=ft.colors.BLUE_700,
            label_color=ft.colors.BLUE_700,
            unselected_label_color=ft.colors.GREY_600,
            tabs=[
                ft.Tab(
                    text="基本統計",
                    content=basic_stats_content
                ),
                ft.Tab(
                    text="誤差伝播",
                    content=error_prop_content
                )
            ],
            width=600,
            height=400
        )

        # 結果表示エリアのスタイリング
        self.results_area = ft.Container(
            content=ft.Column([
                self.error_container,
                ft.Container(
                    content=ft.Column(
                        [self.result_text],
                        scroll=ft.ScrollMode.AUTO,
                        height=200,
                    ),
                    bgcolor=ft.colors.GREY_50,
                    padding=16,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=8,
                )
            ]),
            bgcolor=ft.colors.GREY_50,
            padding=16,
            border=ft.border.only(top=ft.BorderSide(1, ft.colors.GREY_300)),
            visible=False
        )

        # メインコンテンツの作成
        main_content = ft.Column(
            controls=[
                ft.Text("統計処理アプリケーション", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=16),  # スペーシング
                tabs,
                self.results_area
            ],
            spacing=0,
            width=600
        )

        return ft.Container(
            content=main_content,
            alignment=ft.alignment.top_center,
            expand=True,
            padding=ft.padding.all(24)
        )

    def _paste_to_field(self, text_field: ft.TextField):
        """指定されたテキストフィールドにクリップボードの内容をペーストする"""
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content:
                # 現在の値に追加するか、置き換えるかを選択（今回は置き換え）
                text_field.value = clipboard_content
                text_field.update()
        except Exception as e:
            print(f"ペーストエラー: {e}")

    def handle_test_click(self, test_type: str) -> None:
        """統計テストの実行を処理する

        Args:
            test_type (str): テストの種類 ('ttest', 'qtest', 'confidence_interval', 'error_propagation')
        """
        # エラーと結果表示をクリア
        self.clear_messages()

        try:
            if test_type == "error_propagation":
                # 誤差伝播計算の処理
                try:
                    variables = [x.strip() for x in self.variable_input.value.split(",")]
                    values = [float(x.strip()) for x in self.value_input.value.split(",")]
                    errors = [float(x.strip()) for x in self.error_input.value.split(",")]
                    function_str = self.function_input.value.strip()
                except ValueError:
                    self.show_error("数値の入力が不正です。値と誤差には数値を入力してください。")
                    return

                # 誤差伝播の入力値を検証
                is_valid, error_msg = DataValidator.validate_error_propagation_inputs(
                    variables, values, errors, function_str
                )
                if not is_valid:
                    self.show_error(error_msg)
                    return

                results = StatisticalAnalyzer.calculate_error_propagation(
                    variables, values, errors, function_str
                )
            else:
                # 基本統計処理の入力データの検証
                is_valid, numbers, error_msg = DataValidator.validate_input(self.data_input.value)
                if not is_valid:
                    self.show_error(error_msg)
                    return

                # データ要件の確認
                if test_type != "confidence_interval":
                    is_valid, error_msg = DataValidator.check_data_requirements(numbers, test_type)
                    if not is_valid:
                        self.show_error(error_msg)
                        return
                elif len(numbers) < 1:
                    self.show_error("信頼区間の計算には最低1つのデータが必要です。")
                    return

                # 統計テストの実行
                if test_type == "qtest":
                    results = StatisticalAnalyzer.perform_qtest(numbers)
                else:  # confidence_interval
                    results = StatisticalAnalyzer.calculate_confidence_interval(numbers)

            # 結果の表示
            formatted_result = StatisticalAnalyzer.format_results(results, test_type)
            self.show_result(formatted_result)

        except ValueError as ve:
            self.show_error(f"入力値のエラー: {str(ve)}")
        except Exception as e:
            self.show_error(f"計算中にエラーが発生しました: {str(e)}")

    def show_error(self, message: str) -> None:
        """エラーメッセージを表示する

        Args:
            message (str): 表示するエラーメッセージ
        """
        self.error_text.value = message
        self.error_container.visible = True
        self.error_container.update()

    def show_result(self, message: str) -> None:
        """結果メッセージを表示する

        Args:
            message (str): 表示する結果メッセージ
        """
        # 結果表示エリアを表示
        self.results_area.visible = True
        self.results_area.update()
        
        # 重要な数値を強調表示
        parts = message.split(": ")
        if len(parts) > 1:
            self.result_text.spans = [
                ft.TextSpan(
                    parts[0] + ": ",
                    style=ft.TextStyle(
                        size=14,
                        weight=ft.FontWeight.W_400
                    )
                ),
                ft.TextSpan(
                    parts[1],
                    style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_500
                    )
                )
            ]
        else:
            self.result_text.value = message
        self.result_text.update()

    def clear_messages(self) -> None:
        """エラーと結果表示をクリアする"""
        self.error_text.value = ""
        self.error_container.visible = False
        self.result_text.spans = None
        self.result_text.value = ""
        self.results_area.visible = False
        self.error_container.update()
        self.result_text.update()
        self.results_area.update()