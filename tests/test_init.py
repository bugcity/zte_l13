from zte_l13 import ZTEL13
import pytest
import os
from dotenv import load_dotenv
load_dotenv()


@pytest.fixture(scope='module')
def zte_l13():
    host = '192.168.0.1'
    password = os.getenv('ZTE_L13_PASSWORD')
    zte_l13 = ZTEL13(host, password)
    zte_l13.login()
    return zte_l13


def test_login(zte_l13):
    assert zte_l13.logined is True


def test_get_signal_info(mocker, zte_l13):
    mocker.patch(
        'zte_l13.ZTEL13._get_cmd_process',
        return_value={
            'network_type': 'LTE', 'wan_active_band': 'LTE BAND 3', 'nr5g_action_band': 'n77',
            'lte_rssi': '-100', 'lte_rsrp': '-110', 'lte_snr': '10.2',
            'Z5g_rsrp': '-180', 'Z5g_rsrq': '-10', 'Z5g_SINR': '27.8',
            'signalbar': '4',
            'LD': 'test', 'status': '0'
        }
    )
    data = zte_l13.get_signal_info()
    assert data is not None
    assert data.network_type == 'LTE'
    assert data.wan_active_band == 'LTE BAND 3'
    assert data.nr5g_action_band == 'n77'
    assert data.lte_rssi == -100
    assert data.lte_rsrp == -110
    assert data.lte_snr == 10.2
    assert data.Z5g_rsrp == -180
    assert data.Z5g_rsrq == -10
    assert data.Z5g_SINR == 27.8
    assert data.signalbar == 4
    assert data.dictionary.keys() == {
        'network_type', 'wan_active_band', 'nr5g_action_band',
        'lte_rssi', 'lte_rsrp', 'lte_snr',
        'Z5g_rsrp', 'Z5g_rsrq', 'Z5g_SINR',
        'signalbar'
    }

    # mocker.patchを削除
    mocker.stopall()

    data = zte_l13.get_signal_info()
    assert data is not None
    assert data.network_type != ''
    assert data.wan_active_band != ''
    assert data.nr5g_action_band != ''
    assert data.lte_rssi != 0
    assert data.lte_rsrp != 0
    assert data.lte_snr != 0
    assert data.Z5g_rsrp != 0
    assert data.Z5g_rsrq != 0
    assert data.Z5g_SINR != 0
    assert data.signalbar != 0


def test_reboot(zte_l13):
    assert zte_l13.reboot() is True
