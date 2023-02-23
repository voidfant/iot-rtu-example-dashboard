import json

import pandas as pd
from typing import Union
from collections.abc import Iterator


def csv_to_df(path: str) -> Iterator:
    with open(path) as f:
        raw_data = [list(map(quick_check, x.split(';'))) for x in f.read().split('\n')]
    df_json = pd.DataFrame(raw_data, columns=['time', 'altitude']).to_json(orient='values')

    return iter(json.loads(df_json))


def quick_check(x: str) -> Union[str, float]:
    """
    При сборке пакета данных, нам необходимо конвертировать строковые значения в тип данных float.
    Однако не все строки в .csv файле представляют из себя численные значения.
    Этот метод проверяет, являются ли значения в строке числом и возвращает str или float в зависимости от того,
    что ему пришло.
    :param x: Строка, нуждающаяся в проверке.
    :return: Результат конвертации.
    """
    try:
        return float(x)
    except ValueError:
        return x