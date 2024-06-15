import requests
from .util import jquery_now, password_algorithms_cookie, hex_sha256, DictToClass


class ZTEL13:
    _session = None

    def __init__(self, host: str, password: str):
        """コンストラクタ

        Args:
            host (str): L13のIPアドレス
            password (str): パスワード
        """
        self.host = host
        self.password = password
        self._session = requests.Session()

    def _get_cmd_process(self, cmd: str, with_ts: bool = False) -> dict:
        """goform_get_cmd_processを実行する

        Args:
            cmd (str): コマンド、","区切りで複数指定可能
            with_ts (bool, optional): タイムスタンプを渡すか. Defaults to False.

        Returns:
            dict: 戻り値
        """
        url = f'http://{self.host}/goform/goform_get_cmd_process'
        params = {
            'isTest': 'false',
            'cmd': cmd,
        }
        if with_ts:
            params['_'] = jquery_now()
        if ',' in cmd:
            params['multi_data'] = 1
        headers = {
            'Referer': f'http://{self.host}/',
        }
        return self._session.get(url, params=params, headers=headers, timeout=5, verify=False).json()

    def _set_cmd_process(self, cmd: str, params: dict) -> dict:
        """set_cmd_processを実行する

        Args:
            cmd (str): コマンド
            params (dict): コマンドに渡すパラメータ

        Returns:
            dict: 戻り値
        """
        url = f'http://{self.host}/goform/goform_set_cmd_process'
        headers = {
            'Origin': f'http://{self.host}',
            'Referer': f'http://{self.host}/',
        }
        data = {
            'isTest': 'false',
            'goformId': cmd,
        }
        if params:
            data.update(params)
        return self._session.post(url, headers=headers, data=data, timeout=5, verify=False).json()

    def _ld(self) -> DictToClass:
        """LDを取得する

        Returns:
            DictToClass: LDの値
        """
        res = self._get_cmd_process('LD', with_ts=True)
        return DictToClass(res)

    def _rd(self) -> DictToClass:
        """wa_inner_version,cr_version,RDを取得する

        Returns:
            DictToClass: wa_inner_version,cr_version,RDの値
        """
        res = self._get_cmd_process('wa_inner_version,cr_version,RD')
        return DictToClass(res)

    def login(self) -> bool:
        """L13にログインする

        Returns:
            bool: True: ログイン成功, False: ログイン失敗
        """
        a = self._ld()
        p1 = password_algorithms_cookie(self.password)
        pw = password_algorithms_cookie(p1 + a.LD)
        res = self._set_cmd_process('LOGIN', {'password': pw})
        res = DictToClass(res)
        return res.result == '0'

    def reboot(self) -> bool:
        """L13を再起動する

        Returns:
            bool: True: 再起動成功(常にTrueを返す)
        """
        a = self._rd()
        a1 = hex_sha256(a.wa_inner_version + a.cr_version)
        ad = hex_sha256(a1 + a.RD)
        self._set_cmd_process('REBOOT_DEVICE', {'AD': ad})
        return True

    def get_signal_info(self) -> DictToClass:
        """L13の信号情報を取得する

        Returns:
            DictToClass: 信号情報 (lte_rssi, lte_rsrp, lte_snr, Z5g_rsrp, Z5g_rsrq, Z5g_SINR, signalbar)
        """
        int_items = ['lte_rssi', 'lte_rsrp', 'Z5g_rsrp', 'Z5g_rsrq', 'signalbar']
        float_items = ['lte_snr', 'Z5g_SINR']
        items = int_items + float_items
        res = self._get_cmd_process(','.join(items))
        res = {k: res[k] for k in items}
        return DictToClass(res, int_items=int_items, float_items=float_items)

    def get_bytes(self) -> DictToClass:
        """通信量やスループットを取得する

        Returns:
            DictToClass: 通信量やスループット
                (realtime_tx_bytes, realtime_rx_bytes, realtime_time, realtime_tx_thrpt, realtime_rx_thrpt,
                 monthly_rx_bytes, monthly_tx_bytes, monthly_time, monthly_kddi_tx, monthly_kddi_rx,
                 hsplus_monthly_kddi_tx, hsplus_monthly_kddi_rx)
        """
        items = [
            'realtime_tx_bytes',
            'realtime_rx_bytes',
            'realtime_time',
            'realtime_tx_thrpt',
            'realtime_rx_thrpt',
            'monthly_rx_bytes',
            'monthly_tx_bytes',
            'monthly_time',
            'monthly_kddi_tx',
            'monthly_kddi_rx',
            'hsplus_monthly_kddi_tx',
            'hsplus_monthly_kddi_rx',
        ]
        res = self._get_cmd_process(','.join(items))
        res = {k: res[k] for k in items}
        return DictToClass(res, int_items=items)
