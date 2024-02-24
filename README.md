# ZTE L13 Python Package

## 概要

ZTE L13 Pythonパッケージは、ZTE L13デバイスから情報を取得したりコントロールするためのユーティリティです。

## インストール

```bash
pip install git+https://github.com/bugcity/zte_l13.git
```

## 使用法

```python
from zte_l13 import ZTEL13

# インスタンスを作成
# IPアドレスとパスワードを指定する
zl = ZTEL13('192.168.0.1', 'password')

# ログイン
zl.login()

# 情報を取得
info = zl.get_signal_info()
print(info.lte_rssi)
print(info.lte_rsrp)
print(info.lte_snr)
print(info.Z5g_rsrp)
print(info.Z5g_rsrq)
print(info.Z5g_SINR)

# デバイスを制御
# 例: デバイスの再起動
zl.reboot()
```

## ライセンス

このプロジェクトはMITライセンスのもとで提供されています。
