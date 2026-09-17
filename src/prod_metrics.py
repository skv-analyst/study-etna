import numpy as np
from etna.datasets import TSDataset


def bias(y_true: TSDataset, y_pred: TSDataset) -> dict:
    """Signed WAPE, в процентах, по каждому сегменту:

        Bias = 100 * sum(pred - true) / sum(|true|)

    ETNA не имеет такой метрики из коробки. Знак задаёт направление систематической
    ошибки: >0 — модель завышает (перебор курьеров), <0 — занижает (нехватка).
    """
    df_true = y_true[:, :, "target"]
    df_pred = y_pred[:, :, "target"]
    segments = df_true.columns.get_level_values("segment").unique()
    return {
        segment: 100
        * (df_pred[segment]["target"] - df_true[segment]["target"]).sum()
        / df_true[segment]["target"].abs().sum()
        for segment in segments
    }


def pooled(y_true: TSDataset, y_pred: TSDataset, signed: bool = False) -> float:
    """WAPE/Bias, посчитанные не как среднее по юнитам (как SMAPE(mode="macro")),
    а как одно отношение — сумма ошибок по ВСЕМ юнитам и датам сразу, делённая
    на сумму факта по ВСЕМ юнитам и датам сразу:

        pooled = 100 * sum(pred - true) / sum(|true|)          (signed=True, это Bias)
        pooled = 100 * sum(|pred - true|) / sum(|true|)        (signed=False, это WAPE)

    В отличие от простого среднего по сегментам, это взвешивает юниты по объёму —
    крупный юнит влияет на итог сильнее мелкого, а не поровну с ним.
    """
    df_true = y_true[:, :, "target"].values
    df_pred = y_pred[:, :, "target"].values
    diff = df_pred - df_true
    numerator = diff.sum() if signed else np.abs(diff).sum()
    denominator = np.abs(df_true).sum()
    return 100 * numerator / denominator
