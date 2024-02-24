from zte_l13 import ZTEL13
import pytest


@pytest.fixture(scope='module')
def zte_l13():
    host = '192.168.0.1'
    password = 'correct_password'
    return ZTEL13(host, password)


@pytest.fixture(scope='module')
def wrong_zte_l13():
    host = '192.168.0.1'
    password = 'incorrect_password'
    return ZTEL13(host, password)


def test_login(zte_l13, wrong_zte_l13):
    assert zte_l13.login() is True
    assert wrong_zte_l13.login() is False


def test_get_signal_info(zte_l13):
    zte_l13.login()
    data = zte_l13.get_signal_info()
    assert data is not None
    assert hasattr(data, 'lte_rssi')
    assert type(data.lte_rssi) is int
    assert hasattr(data, 'lte_rsrp')
    assert type(data.lte_rsrp) is int
    assert hasattr(data, 'lte_snr')
    assert type(data.lte_snr) is float
    assert hasattr(data, 'Z5g_rsrp')
    assert type(data.Z5g_rsrp) is int
    assert hasattr(data, 'Z5g_rsrq')
    assert type(data.Z5g_rsrq) is int
    assert hasattr(data, 'Z5g_SINR')
    assert type(data.Z5g_SINR) is float


def test_reboot(zte_l13):
    zte_l13.login()
    assert zte_l13.reboot() is True
