import pytest
import sys
import os
import math
from io import StringIO
import datetime

# Импорт функций из файлов решений
from fact import fact_rec, fact_it
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list_comp, process_list_gen
from my_sum import my_sum
from my_sum_argv import my_sum_argv
from files_sort import sort_files
from file_search import search_file
from email_validation import fun, filter_mail
from fibonacci import fibonacci, cube
from average_scores import compute_average_scores
from plane_angle import Point, plane_angle
from phone_number import sort_phone
from people_sort import name_format
from complex_numbers import Complex
from circle_square_mk import circle_square_mk
from log_decorator import function_logger

# Группируем тесты по классам для наглядного вывода (имя файла -> тесты)

class TestFact:
    """Тесты для файла fact.py (Факториал)"""
    
    @pytest.mark.parametrize("n,expected", [(0, 1), (1, 1), (5, 120), (10, 3628800)])
    def test_fact_rec(self, n, expected):
        assert fact_rec(n) == expected

    @pytest.mark.parametrize("n,expected", [(0, 1), (1, 1), (5, 120), (10, 3628800)])
    def test_fact_it(self, n, expected):
        assert fact_it(n) == expected

class TestShowEmployee:
    """Тесты для show_employee.py"""
    def test_default(self):
        assert show_employee("Ivan") == "Ivan: 100000 ₽"
    def test_custom(self):
        assert show_employee("Ivan", 50000) == "Ivan: 50000 ₽"

class TestSumAndSub:
    """Тесты для sum_and_sub.py"""
    def test_basic(self):
        assert sum_and_sub(10, 5) == (15, 5)

class TestProcessList:
    """Тесты для process_list.py"""
    def test_comp(self):
        assert process_list_comp([1, 2, 3, 4]) == [4, 16]
    def test_gen(self):
        assert list(process_list_gen([1, 2, 3, 4])) == [4, 16]

class TestMySum:
    """Тесты для my_sum.py"""
    def test_sum(self):
        assert my_sum(1, 2, 3) == 6

class TestMySumArgv:
    """Тесты для my_sum_argv.py"""
    def test_output(self, capsys):
        sys.argv = ['script', '1', '2', '3']
        my_sum_argv()
        assert capsys.readouterr().out.strip() == "6"

class TestSortFiles:
    """Тесты для files_sort.py"""
    def test_sort(self, capsys, tmp_path):
        p = tmp_path
        (p / "b.txt").write_text("c")
        (p / "a.py").write_text("c")
        sort_files(str(p))
        out = capsys.readouterr().out
        assert "a.py" in out and "b.txt" in out

class TestFileSearch:
    """Тесты для file_search.py"""
    def test_found(self, capsys, tmp_path):
        (tmp_path / "t.txt").write_text("content")
        search_file("t.txt", str(tmp_path))
        assert "Found in" in capsys.readouterr().out

class TestEmailValidation:
    """Тесты для email_validation.py"""
    def test_valid(self):
        assert fun("a@b.c") is True
    def test_invalid(self):
        assert fun("invalid") is False

class TestFibonacci:
    """Тесты для fibonacci.py"""
    def test_fib(self):
        assert fibonacci(5) == [0, 1, 1, 2, 3]
    def test_cube(self):
        assert cube(3) == 27

class TestAverageScores:
    """Тесты для average_scores.py"""
    def test_avg(self):
        scores = [(10, 20), (20, 30)]
        assert compute_average_scores(scores) == (15.0, 25.0)

class TestPlaneAngle:
    """Тесты для plane_angle.py"""
    def test_90_degrees(self):
        # A, B, C, D для 90 градусов (ABxBC=Z, BCxCD=X)
        # B-A=(1,0,0), B-C=(0,1,0) -> C=B-(0,1,0)=(1,-1,0). CD=D-C=(0,0,1) -> D=(1,-1,1)
        angle = plane_angle(Point(0,0,0), Point(1,0,0), Point(1,-1,0), Point(1,-1,1))
        assert abs(angle - 90.0) < 1e-5

class TestPhoneNumber:
    """Тесты для phone_number.py"""
    def test_sort(self):
        res = sort_phone(["81234567890"])
        assert res[0] == "+7 (123) 456-78-90"

class TestPeopleSort:
    """Тесты для people_sort.py"""
    def test_sort(self):
        p = [["A", "B", "20", "M"], ["C", "D", "10", "F"]]
        res = list(name_format(p))
        assert res[0] == "Ms. C D" # 10 лет
        assert res[1] == "Mr. A B" # 20 лет

class TestComplexNumbers:
    """Тесты для complex_numbers.py"""
    def test_add(self):
        assert str(Complex(1, 1) + Complex(2, 2)) == "3.00+3.00i"

class TestCircleSquareMK:
    """Тесты для circle_square_mk.py"""
    def test_area(self):
        assert 3.0 < circle_square_mk(1, 10000) < 3.3

class TestLogDecorator:
    """Тесты для log_decorator.py"""
    def test_log(self, tmp_path):
        f = tmp_path / "log.txt"
        @function_logger(str(f))
        def foo(): pass
        foo()
        assert "foo" in f.read_text("utf-8")

if __name__ == "__main__":
    # Запуск pytest с аргументами:
    # -v : подробно (verbose)
    # -rA : показать отчет (report)
    # test.py : явно указываем файл
    sys.exit(pytest.main(["-v", "test.py"]))
