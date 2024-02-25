import time
import hashlib


class DictToClass:
    """辞書をクラスに変換する
    """

    dictionary = {}

    def __init__(self, dictionary: dict, int_items: list = [], float_items: list = []):
        """コンストラクタ
           型変換できない場合はNoneになる

        Args:
            dictionary (dict): 変換元の辞書
            int_items (list, optional): intに変換するキー. Defaults to [].
            float_items (list, optional): floatに変換するキー. Defaults to [].
        """
        self.dictionary = {}
        for key, value in dictionary.items():
            try:
                if key in int_items:
                    value = int(value)
                elif key in float_items:
                    value = float(value)
            except ValueError:
                value = None
            setattr(self, key, value)
            self.dictionary[key] = value


def jquery_now() -> int:
    """jqueryのnow()を返す

    Returns:
        int: now()
    """
    return int(time.time() * 1000)


def hex_sha256(s: str) -> str:
    """SHA256のハッシュを16進の文字列で返す

    Args:
        s (str): 値

    Returns:
        str: SHA256のハッシュ
    """
    return hashlib.sha256(s.encode()).hexdigest().upper()


def password_algorithms_cookie(s: str) -> str:
    """パスワードのハッシュを返す

    Args:
        s (str): パスワード

    Returns:
        str: ハッシュ
    """
    return hex_sha256(s)
