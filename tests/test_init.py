from zte_l13 import ZTEL13
import pytest
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope='module')
def zte_l13():
    host = os.getenv('ZTE_L13_HOST', '192.168.0.1')
    password = os.getenv('ZTE_L13_PASSWORD')
    zte_l13 = ZTEL13(host, password)
    zte_l13.login()
    return zte_l13


@pytest.fixture
def zte_l13_mock():
    """ログイン不要なモックテスト用フィクスチャ"""
    host = os.getenv('ZTE_L13_HOST', '192.168.0.1')
    return ZTEL13(host, 'dummy')


@pytest.mark.integration
def test_login(zte_l13):
    assert zte_l13.logined is True


def test_get_signal_info(mocker, zte_l13_mock):
    mocker.patch(
        'zte_l13.ZTEL13._get_cmd_process',
        return_value={
            'network_type': 'LTE', 'wan_active_band': 'LTE BAND 3', 'nr5g_action_band': 'n77',
            'lte_rssi': '-100', 'lte_rsrp': '-110', 'lte_snr': '10.2',
            'Z5g_rsrp': '-180', 'Z5g_rsrq': '-10', 'Z5g_SINR': '27.8',
            'signalbar': '4',
        }
    )
    data = zte_l13_mock.get_signal_info()
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


@pytest.mark.integration
def test_get_signal_info_live(zte_l13):
    data = zte_l13.get_signal_info()
    assert data is not None
    assert isinstance(data.network_type, str) and data.network_type != ''
    assert isinstance(data.wan_active_band, str) and data.wan_active_band != ''
    assert isinstance(data.nr5g_action_band, str)
    assert isinstance(data.lte_rssi, int)
    assert isinstance(data.lte_rsrp, int)
    assert isinstance(data.lte_snr, float)
    assert isinstance(data.Z5g_rsrp, int)
    assert isinstance(data.Z5g_rsrq, int)
    assert isinstance(data.Z5g_SINR, float)
    assert isinstance(data.signalbar, int)


@pytest.mark.integration
def test_reboot(zte_l13):
    assert zte_l13.reboot() is True


@pytest.mark.integration
def test_set_bearer(zte_l13):
    assert zte_l13.set_bearer(ZTEL13.WAN.W4G, ZTEL13.WAN5GSA.enable) is True
    assert zte_l13.set_bearer(ZTEL13.WAN.W5G, ZTEL13.WAN5GSA.enable) is True
