from __future__ import unicode_literals
from distutils import dir_util
from pytest import fixture
import os


@fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.

    Benefits:
        - tests can't interfere with each other, as each test will have a copy of the data files.
        - This way you can run tests using multiple cores without worrying about concurrency of resources
        -
    Parameters
    ----------
    tmpdir
    request

    Returns
    -------

    """
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


"""
@pytest.fixture
um bei Klassen funktionen immer ein neues Objekt benutzt wird und nicht ein neues

@pytest.mark.parametrize("earned,spent,expected", [
    (30, 10, 20),
    (20, 2, 18),
])
def test_transactions(earned, spent, expected):
    my_wallet = Wallet()
    my_wallet.add_cash(earned)
    my_wallet.spend_cash(spent)
    assert my_wallet.balance == expected
Um mehrere Funktionen testen zukönnen
"""

"""
@pytest.fixture
def my_wallet():
    '''Returns a Wallet instance with a zero balance'''
    return Wallet()

@pytest.mark.parametrize("earned,spent,expected", [
    (30, 10, 20),
    (20, 2, 18),
])
def test_transactions(my_wallet, earned, spent, expected):
    my_wallet.add_cash(earned)
    my_wallet.spend_cash(spent)
    assert my_wallet.balance == expected
"""

"""
# Mark test so u only run specific tests
@pytest.mark.run_these_please
def test_number_two():
    assert [1] == [1]

$ pytest -v -m run_these_please /path/to/test_file.py
"""

"""
https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest
Für permanentes Testen Semaphore CI/CD
"""

import types


def freeVar(val):
    def nested():
        return val

    return nested.__closure__[0]


def nested(outer, innerName, **freeVars):
    if isinstance(outer, (types.FunctionType, types.MethodType)):
        outer = outer.__code__
    for const in outer.co_consts:
        if isinstance(const, types.CodeType) and const.co_name == innerName:
            return types.FunctionType(const,
                                      globals(),
                                      None,
                                      None,
                                      tuple(freeVar(freeVars[name]) for name in const.co_freevars)
                                      )


# Examples

def f(v1):
    v2 = 1

    def g(v3=2):
        return v1 + v2 + v3 + 4

    def h():
        return 16

    return g() + h() + 32


class C(object):
    def foo(self):
        def k(x):
            return [self, x]

        return k(3)


def m():
    vm = 1

    def n(an=2):
        vn = 4

        def o(ao=8):
            vo = 16
            return vm + an + vn + ao + vo

        return o()

    return n()


import unittest


class TestNested(unittest.TestCase):
    def runTest(self):
        nestedG = nested(f, 'g', v1=8, v2=1)
        self.assertEqual(nestedG(2), 15)
        nestedH = nested(f, 'h')
        self.assertEqual(nestedH(), 16)
        nestedK = nested(C.foo, 'k', self='mock')
        self.assertEqual(nestedK(5), ['mock', 5])
        nestedN = nested(m, 'n', vm=1)
        nestedO = nested(nestedN, 'o', vm=1, an=2, vn=4)
        self.assertEqual(nestedO(8), 31)


