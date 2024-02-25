from zte_l13.util import jquery_now, password_algorithms_cookie, hex_sha256, DictToClass


def test_jquery_now():
    assert isinstance(jquery_now(), int)


def test_hex_sha256():
    assert hex_sha256('test') == '9F86D081884C7D659A2FEAA0C55AD015A3BF4F1B2B0B822CD15D6C15B0F00A08'


def test_password_algorithms_cookie():
    assert password_algorithms_cookie('test') == '9F86D081884C7D659A2FEAA0C55AD015A3BF4F1B2B0B822CD15D6C15B0F00A08'


def test_dict_to_class():
    d = {'a': '-1', 'b': '2.1', 'd': '3'}
    obj = DictToClass(d, int_items=['a'], float_items=['b'])
    assert obj.a == -1
    assert obj.b == 2.1
    assert obj.d == '3'
    assert hasattr(obj, 'a')
    assert hasattr(obj, 'b')
    assert not hasattr(obj, 'c')
    assert obj.__class__ == DictToClass
    assert obj.dictionary != d
    assert obj.dictionary['a'] == -1
    assert obj.dictionary['b'] == 2.1
    assert obj.dictionary['d'] == '3'
