# Карта библиотеки ETNA


![map](weeks/src/etna-map.png)



## Уровень 0 — Инфраструктура

Пронизывает всю библиотеку

- [Core](https://docs.etna.ai/stable/api_reference/core.html) — Общие миксины: сохранение/загрузка, базовые интерфейсы. Именно отсюда «единый интерфейс» — каждый Transform/Model/Pipeline его наследует.
- [Settings](https://docs.etna.ai/stable/api_reference/settings.html) — Флаги наличия опциональных зависимостей (torch, prophet, catboost и т.д.).
- [Loggers](https://docs.etna.ai/stable/api_reference/loggers.html) — Не просто логирование, а интеграции с трекерами экспериментов (WandB, ClearML, S3).

## Уровень 1 — Три базовые абстракции

- [Datasets](https://docs.etna.ai/stable/api_reference/datasets.html) — Основа основ - TSDataset с темпоральной индексацией + генераторы синтетики + утилиты выравнивания/загрузки данных.
- [Transforms](https://docs.etna.ai/stable/api_reference/transforms.html) — Фичи и препроцессинг: декомпозиция, кодирование, эмбеддинги, отбор признаков, пропуски/выбросы, календарь, лаги/окна, скейлеры, матфункции. Единый интерфейс fit/transform/inverse_transform.
- [Models](https://docs.etna.ai/stable/api_reference/models.html) — Адаптер с единым интерфейсом fit/forecast над: наивными, статистическими (SARIMAX/ETS/Prophet/TBATS/StatsForecast), ML (CatBoost/ElasticNet/sklearn) и нейросетевыми (свои + предобученные Chronos/TimesFM) моделями.

## Уровень 2 — Оркестрация (объединяет три абстракции в рабочий процесс)

- [Pipelines](https://docs.etna.ai/stable/api_reference/pipeline.html) — Склеивает Transforms + Model в единый объект (Pipeline). 
- [Ensembles](https://docs.etna.ai/stable/api_reference/ensembles.html) — Комбинирует прогнозы нескольких Pipeline в один.
- [Prediction Intervals](https://docs.etna.ai/stable/api_reference/prediction_intervals.html) — Надстройка над Pipeline/Model, добавляет доверительные интервалы к точечному прогнозу. Все методы работают через один и тот же принцип: гоняют бэктест, чтобы набрать историю ошибок (residuals), и на основе их разброса строят границы интервала для будущего прогноза
- [Reconciliation](https://docs.etna.ai/stable/api_reference/reconciliation.html) — Для иерархических рядов (например, продажи по сети → по регионам → по магазинам). Прогнозы на разных уровнях иерархии, построенные независимо, обычно не согласованы (сумма прогнозов по магазинам ≠ прогноз по региону). Reconciliation "выравнивает" прогнозы между source_level (уровень, на котором реально строили прогноз) и target_level (уровень, для которого нужен согласованный результат)

## Уровень 3 — Автоподбор (работает над Pipeline)
 
- [Distributions](https://docs.etna.ai/stable/api_reference/distributions.html) — Задает пространство поиска для гиперпараметров, которые перебирает модуль Auto (Auto/Tune) при автоподборе. По сути, это обёртка над типами Optuna-подобных распределений: "выбери одно из списка" / "любое вещественное число в диапазоне" / "любое целое в диапазоне".
- [Auto](https://docs.etna.ai/stable/api_reference/auto.html) — Автоподбор. Либо выбрать лучший пайплайн целиком из пула кандидатов (Auto), либо подобрать гиперпараметры внутри одного конкретного пайплайна (Tune). Использует пространства поиска из Distributions и оценивает качество по target_metric через бэктест.

## Уровень 4 — Анализ и интерпретация (потребляют TSDataset/Model/Pipeline, отдают инсайт человеку)

- [Analysis](https://docs.etna.ai/stable/api_reference/analysis.html) — "Глаза" библиотеки — то, чем смотрим на TSDataset, на результат Model/Pipeline и решаем, что делать дальше. Набор функций для визуализации, диагностики, расчета статистики. Условно распадается на пять тем.
- [Metrics](https://docs.etna.ai/stable/api_reference/metrics.html) — Численная оценка качества прогноза относительно факта. Все скалярные метрики (Metric) наследуют один базовый класс с двумя общими настройками: режим агрегации. `macro` - усреднить по сегментам. `per-segment` - оставить по каждому сегменту отдельно.
- [Clustering](https://docs.etna.ai/stable/api_reference/clustering.html) — Кластеризация похожих временные рядав (сегментов) внутри TSDataset между собой, без учёта таргета(будущего). Считается по форме самого ряда. 

## Уровень 5 — Пользовательский интерфейс

- [CLI commands](https://docs.etna.ai/stable/api_reference/commands.html) — Обёртка над Pipeline для запуска прогноза/бэктеста из терминала, вообще без Python-кода. Пайплайн целиком описывается YAML-конфигом, а не собирается программно классами.

## Песочница

- [Experimental](https://docs.etna.ai/stable/api_reference/experimental.html) — Песочница. То, что ещё не стабилизировано как основной API и может измениться/переехать в будущих версиях

