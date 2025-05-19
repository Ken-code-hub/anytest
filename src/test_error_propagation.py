from src.analyzer import StatisticalAnalyzer

def test_error_propagation():
    # テストケース: f(x, y) = x^2 + 2xy + y^2
    variables = ['x', 'y']
    values = [2.0, 3.0]
    errors = [0.1, 0.2]
    function_str = 'x**2 + 2*x*y + y**2'

    # 誤差伝播の計算を実行
    analyzer = StatisticalAnalyzer()
    results = analyzer.calculate_error_propagation(
        variables=variables,
        values=values,
        errors=errors,
        function_str=function_str
    )

    # 結果を表示
    print(analyzer.format_results(results, "error_propagation"))

if __name__ == "__main__":
    test_error_propagation()