from typing import List, Tuple, Optional, Dict
import numpy as np
import re

class DataValidator:
    @staticmethod
    def validate_input(text: str) -> Tuple[bool, Optional[List[float]], Optional[str]]:
        """テキスト入力を検証し、数値リストに変換する

        Args:
            text (str): 改行または空白で区切られた数値データ

        Returns:
            Tuple[bool, Optional[List[float]], Optional[str]]: 
            - 検証結果（True/False）
            - 変換された数値リスト（検証失敗時はNone）
            - エラーメッセージ（検証成功時はNone）
        """
        if not text or text.isspace():
            return False, None, "データが入力されていません。"

        # 改行とスペースで分割
        values = text.split()
        
        try:
            # 文字列を数値に変換
            numbers = [float(x) for x in values]
            
            # 数値リストが空でないことを確認
            if not numbers:
                return False, None, "有効な数値が入力されていません。"
                
            return True, numbers, None
            
        except ValueError:
            return False, None, "無効な入力があります。数値のみを入力してください。"

    @staticmethod
    def check_data_requirements(data: List[float], test_type: str) -> Tuple[bool, Optional[str]]:
        """統計テストの要件を満たしているか確認する

        Args:
            data (List[float]): 検証するデータ
            test_type (str): テストの種類 ('qtest', 'confidence_interval', 'error_propagation')

        Returns:
            Tuple[bool, Optional[str]]:
            - 検証結果（True/False）
            - エラーメッセージ（検証成功時はNone）
        """
        if test_type == "qtest":
            # Qテストには最低3つのデータが必要
            if len(data) < 3:
                return False, "Qテストには最低3つのデータが必要です。"
        elif test_type == "confidence_interval":
            if len(data) < 1:
                return False, "信頼区間の計算には最低1つのデータが必要です。"
        elif test_type == "error_propagation":
            pass  # 誤差伝播の要件は別メソッドで検証
        else:
            return False, "不正なテスト種別です。"

        return True, None

    @staticmethod
    def validate_error_propagation_inputs(variables: List[str], values: List[float],
                                        errors: List[float], function_str: str
                                        ) -> Tuple[bool, Optional[str]]:
        """誤差伝播計算の入力値を検証する

        Args:
            variables (List[str]): 変数名のリスト
            values (List[float]): 変数の値のリスト
            errors (List[float]): 誤差のリスト
            function_str (str): 関数式

        Returns:
            Tuple[bool, Optional[str]]:
            - 検証結果（True/False）
            - エラーメッセージ（検証成功時はNone）
        """
        # 空の入力をチェック
        if not variables or not values or not errors or not function_str:
            return False, "すべての入力フィールドを入力してください。"

        # リストの長さが一致することを確認
        if not (len(variables) == len(values) == len(errors)):
            return False, "変数名、値、誤差の数が一致していません。"

        # 変数名の形式を検証
        variable_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
        for var in variables:
            if not variable_pattern.match(var):
                return False, f"無効な変数名です: {var}"

        # 誤差が正の値であることを確認
        if any(error <= 0 for error in errors):
            return False, "誤差は正の値である必要があります。"

        # 関数式に使用されている変数名を検証
        function_vars = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', function_str))
        undefined_vars = function_vars - set(variables)
        if undefined_vars:
            return False, f"関数式で未定義の変数が使用されています: {', '.join(undefined_vars)}"

        # 基本的な関数式の構文を検証
        try:
            # シンプルな構文チェック（括弧の対応など）
            if function_str.count('(') != function_str.count(')'):
                return False, "関数式の括弧の対応が正しくありません。"
        except Exception as e:
            return False, f"関数式の構文が不正です: {str(e)}"

        return True, None

    @staticmethod
    def split_data_for_ttest(data: List[float]) -> Tuple[List[float], List[float]]:
        """データをt検定用に2グループに分割する

        Args:
            data (List[float]): 分割するデータ

        Returns:
            Tuple[List[float], List[float]]: 2つのグループに分けられたデータ
        """
        mid = len(data) // 2
        return data[:mid], data[mid:]