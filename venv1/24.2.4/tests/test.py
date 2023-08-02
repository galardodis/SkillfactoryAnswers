import pytest
from app.calc import Calculator


class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply(self):
        assert self.calc.multiply(self, 5, 5) == 25

    def test_dividion(self):
        assert self.calc.division(self, 25, 5) == 5

    def test_subtraction(self):
        assert self.calc.subtraction(self, 9, 8) == 1

    def test_adding_success(self):
        assert self.calc.adding(self, 1, 1) == 2

    def test_zero_dividion(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.division(self, 1, 0)

    def teardown(self):
        print('Выполнение метода Teardown')
