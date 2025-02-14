import pytest

def foo(a, b):
    return a + b

def test_foo_1():
    assert foo(2, 3) == 5

def test_foo_2():
    assert foo(-1, 2) != -1

