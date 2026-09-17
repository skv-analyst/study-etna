from pathlib import Path
from typing import Dict, Optional

import mlflow
import pandas as pd

# src/custom_logger.py -> parents[1] это корень репозитория (study-etna/)
_TRACKING_DIR = Path(__file__).resolve().parents[1] / "local" / "mlruns"
_TRACKING_DIR.mkdir(parents=True, exist_ok=True)

# Начиная с mlflow 3.x чистый "file://" filestore в maintenance mode и требует
# явного опт-аута, поэтому используем sqlite (тоже полностью локально, файл на диске)
mlflow.set_tracking_uri(f"sqlite:///{_TRACKING_DIR}/mlflow.db")
mlflow.set_experiment("study-etna")


def log_to_mlflow(
    model_name: str,
    model_params: dict,
    metrics: dict,
    run_name_suffix: str = "",
    metrics_per_segment: Optional[Dict[str, dict]] = None,
    segment_table: Optional[pd.DataFrame] = None,
    tags: Optional[dict] = None,
):
    """
    model_name, model_params, metrics, run_name_suffix — как раньше (агрегированные значения).
    metrics_per_segment: {имя_метрики: {segment: значение}}, например
        {"smape": {...}, "wape": {...}}. Каждая логируется как metrics/<имя_метрики>/<segment>,
        чтобы можно было сравнивать конкретный юнит по конкретной метрике между запусками.
    segment_table: датафрейм с разбивкой по юнитам (segment, unit_size, pick_reason, smape, ...) —
        сохраняется как артефакт, видно в UI целиком, с любыми доп. колонками.
    tags: произвольные тэги запуска (chapter, units_scope и т.п.) — по ним удобно фильтровать
        список запусков в UI, в отличие от run_name, который только читается глазами.
    """
    run_name = f"{model_name}_{run_name_suffix}" if run_name_suffix else model_name
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("model", model_name)
        mlflow.log_params(model_params)
        mlflow.log_metrics(metrics)

        if tags:
            mlflow.set_tags(tags)

        if metrics_per_segment:
            for metric_name, per_segment in metrics_per_segment.items():
                mlflow.log_metrics({f"{metric_name}/{segment}": value for segment, value in per_segment.items()})

        if segment_table is not None:
            mlflow.log_table(data=segment_table, artifact_file="metrics_by_segment.json")
