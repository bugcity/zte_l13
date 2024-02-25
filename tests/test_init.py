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


def test_get_signal_info(mocker, zte_l13):
    mocker.patch(
        'zte_l13.ZTEL13._get_cmd_process',
        return_value={'lte_rssi': '-100', 'lte_rsrp': '-110', 'lte_snr': '10.2',
                      'Z5g_rsrp': '-180', 'Z5g_rsrq': '-10', 'Z5g_SINR': '27.8',
                      'LD': 'test', 'status': '0'})
    data = zte_l13.get_signal_info()
    assert data is not None
    assert data.lte_rssi == -100
    assert data.lte_rsrp == -110
    assert data.lte_snr == 10.2
    assert data.Z5g_rsrp == -180
    assert data.Z5g_rsrq == -10
    assert data.Z5g_SINR == 27.8
    assert data.dictionary.keys() == {'lte_rssi', 'lte_rsrp', 'lte_snr',
                                      'Z5g_rsrp', 'Z5g_rsrq', 'Z5g_SINR'}


def test_reboot(zte_l13):
    zte_l13.login()
    assert zte_l13.reboot() is True
