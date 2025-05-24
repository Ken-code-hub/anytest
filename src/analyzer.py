from typing import List, Tuple, Dict
import numpy as np
from scipy import stats
from sympy import diff, symbols, sympify

class StatisticalAnalyzer:
    @staticmethod
    def perform_qtest(data: List[float], confidence_level: float = 0.95) -> Dict[str, float]:
        """Dixonのq検定（外れ値検定）を実行する

        Args:
            data (List[float]): 検定するデータ
            confidence_level (float, optional): 信頼水準. デフォルトは0.95

        Returns:
            Dict[str, float]: Q検定の結果
            - q_statistic: Q統計量
            - q_critical: 棄却限界値
            - is_outlier: 外れ値の有無（1: 外れ値あり, 0: 外れ値なし）
        """
        # データを昇順にソート
        sorted_data = sorted(data)
        n = len(sorted_data)

        # Q統計量の計算
        # n > 3の場合のQ統計量
        q_stat = abs(sorted_data[1] - sorted_data[0]) / abs(sorted_data[-1] - sorted_data[0])
        q_stat_end = abs(sorted_data[-1] - sorted_data[-2]) / abs(sorted_data[-1] - sorted_data[0])
        # 大きい方のQ統計量を採用
        q_stat = max(q_stat, q_stat_end)

        # 棄却限界値の取得（95%信頼水準の場合の値）
        q_critical_values = {
            3: 0.970, 4: 0.829, 5: 0.710, 6: 0.625,
            7: 0.568, 8: 0.526, 9: 0.493, 10: 0.466
        }
        
        # データ数に応じた棄却限界値を取得（データ数が10より大きい場合は10のものを使用）
        q_critical = q_critical_values.get(min(n, 10))

        # 外れ値の判定
        is_outlier = 1 if q_stat > q_critical else 0

        return {
            "q_statistic": float(q_stat),
            "q_critical": float(q_critical),
            "is_outlier": is_outlier
        }

    @staticmethod
    def calculate_confidence_interval(data: List[float], confidence_level: float = 0.683) -> Dict[str, float]:
        """t分布に基づく信頼区間を計算する

        Args:
            data (List[float]): データ
            confidence_level (float, optional): 信頼水準. デフォルトは0.95

        Returns:
            Dict[str, float]: 信頼区間の計算結果
            - mean: 平均値
            - std: 標準偏差
            - lower: 信頼区間下限
            - upper: 信頼区間上限
            - confidence_level: 信頼水準
        """
        n = len(data)
        mean = np.mean(data)
        std = np.std(data, ddof=1)  # 不偏標準偏差
        
        # t分布の両側パーセント点を計算
        t_value = stats.t.ppf((1 + confidence_level) / 2, n - 1)
        
        # 標準誤差
        se = std / np.sqrt(n)
        
        # 信頼区間の計算
        margin_of_error = t_value * se
        lower = mean - margin_of_error
        upper = mean + margin_of_error

        return {
            "mean": float(mean),
            "std": float(std),
            "lower": float(lower),
            "upper": float(upper),
            "confidence_level": float(confidence_level)
        }

    @staticmethod
    def calculate_error_propagation(variables: List[str], values: List[float],
                                    errors: List[float], function_str: str) -> Dict[str, any]:
        """誤差伝播法を使用して関数の誤差を計算する

        Args:
            variables (List[str]): 変数名のリスト
            values (List[float]): 変数の値のリスト
            errors (List[float]): 各変数の誤差のリスト
            function_str (str): 計算する関数の文字列表現

        Returns:
            Dict[str, any]: 誤差伝播の計算結果
            - function_value: 関数の計算値
            - propagated_error: 伝播した誤差
            - relative_error: 相対誤差（%）
            - latex_original: 元の関数のLaTeX表現
            - latex_derivatives: 各変数の偏微分のLaTeX表現のリスト
        """
        # 変数をsympy記号に変換
        symbol_list = [symbols(var) for var in variables]
        
        # 関数をパース
        func = sympify(function_str)
        
        # 変数と値の辞書を作成
        var_dict = dict(zip(symbol_list, values))
        
        # 関数値を計算
        function_value = float(func.subs(var_dict))
        
        # 元の関数のPython形式を取得
        func_str = str(func)
        
        # 誤差伝播の計算と偏微分のPython形式を格納
        total = 0
        derivatives = []
        for symbol, error in zip(symbol_list, errors):
            # 偏微分を計算
            partial_derivative = diff(func, symbol)
            # 偏微分のPython形式を保存
            derivatives.append({
                'variable': str(symbol),
                'expression': str(partial_derivative)
            })
            # 偏微分値を計算
            derivative_value = float(partial_derivative.subs(var_dict))
            # 誤差の二乗項を加算
            total += (derivative_value * error) ** 2
        
        # 誤差の平方根を計算
        propagated_error = total ** 0.5
        
        # 相対誤差を計算（%表示）
        relative_error = (propagated_error / abs(function_value)) * 100 if function_value != 0 else float('inf')
        
        return {
            "function_value": function_value,
            "propagated_error": propagated_error,
            "relative_error": relative_error,
            "original_function": func_str,
            "derivatives": derivatives
        }

    @staticmethod
    def perform_ttest(group1: List[float], group2: List[float], test_type: str = "independent") -> Dict[str, float]:
        """2集団のt検定を実行する

        Args:
            group1 (List[float]): 第1群のデータ
            group2 (List[float]): 第2群のデータ
            test_type (str): 検定の種類 ("independent": 独立2標本, "paired": 対応2標本)

        Returns:
            Dict[str, float]: t検定の結果
            - statistic: t統計量
            - pvalue: p値
            - dof: 自由度
            - mean1: 第1群の平均
            - mean2: 第2群の平均
            - test_type: 実行した検定の種類
        """
        group1_array = np.array(group1)
        group2_array = np.array(group2)
        
        mean1 = np.mean(group1_array)
        mean2 = np.mean(group2_array)
        
        if test_type == "independent":
            # 独立2標本t検定（等分散を仮定）
            statistic, pvalue = stats.ttest_ind(group1_array, group2_array)
            dof = len(group1) + len(group2) - 2
        elif test_type == "paired":
            # 対応2標本t検定
            if len(group1) != len(group2):
                raise ValueError("対応2標本t検定では、両群のデータ数が同じである必要があります")
            statistic, pvalue = stats.ttest_rel(group1_array, group2_array)
            dof = len(group1) - 1
        else:
            raise ValueError("test_typeは'independent'または'paired'である必要があります")
        
        return {
            "statistic": float(statistic),
            "pvalue": float(pvalue),
            "dof": int(dof),
            "mean1": float(mean1),
            "mean2": float(mean2),
            "test_type": test_type
        }

    @staticmethod
    def format_results(results: Dict[str, float], test_type: str) -> str:
        """統計結果を文字列にフォーマットする

        Args:
            results (Dict[str, float]): 統計結果の辞書
            test_type (str): テストの種類 ('ttest', 'qtest', 'confidence_interval', 'error_propagation')

        Returns:
            str: フォーマットされた結果
        """
        if test_type == "ttest":
            test_name = "独立2標本t検定" if results['test_type'] == "independent" else "対応2標本t検定"
            significance = "有意" if results['pvalue'] < 0.05 else "非有意"
            return (
                f"{test_name}結果:\n"
                f"第1群平均 = {results['mean1']:.4f}\n"
                f"第2群平均 = {results['mean2']:.4f}\n"
                f"検定統計量 (t値) = {results['statistic']:.4f}\n"
                f"自由度 = {results['dof']}\n"
                f"p値 = {results['pvalue']:.4f}\n"
                f"判定 (α=0.05): {significance}"
            )
        elif test_type == "qtest":
            return (
                f"Q検定結果:\n"
                f"Q統計量 = {results['q_statistic']:.4f}\n"
                f"棄却限界値 = {results['q_critical']:.4f}\n"
                f"判定: {'外れ値あり' if results['is_outlier'] else '外れ値なし'}"
            )
        elif test_type == "error_propagation":
            # 偏微分の文字列を構築
            derivatives_str = "\n".join([
                f"diff f /diff {deriv['variable']} = {deriv['expression']}"
                for deriv in results['derivatives']
            ])
            
            return (
                f"誤差伝播の計算結果:\n"
                f"元の関数: {results['original_function']}\n\n"
                f"偏微分:\n{derivatives_str}\n\n"
                f"関数値 = {results['function_value']:.6f}\n"
                f"伝播誤差 = {results['propagated_error']:.6f}\n"
                f"相対誤差 = {results['relative_error']:.2f}%"
            )
        else:  # confidence_interval
            confidence_percent = results['confidence_level'] * 100
            return (
                f"信頼区間の計算結果:\n"
                f"平均値 = {results['mean']:.4f}\n"
                f"標準偏差 = {results['std']:.4f}\n"
                f"{confidence_percent:.1f}%信頼区間:\n"
                f"下限 = {results['lower']:.4f}\n"
                f"上限 = {results['upper']:.4f}"
            )