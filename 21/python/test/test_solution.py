from solution import main
from unittest import TestCase


class TestSolution(TestCase):

    def test_example_input(self):
        num_safe, allergens, elapsed_time = main(infile="test_input")
        assert num_safe == 5
        assert allergens == "mxmxvkd,sqjhc,fvjkl"

    def test_input(self):
        num_safe, allergens, elapsed_time = main(infile="input")
        assert num_safe == 2428
        assert allergens == "bjq,jznhvh,klplr,dtvhzt,sbzd,tlgjzx,ctmbr,kqms"
