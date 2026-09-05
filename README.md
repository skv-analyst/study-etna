# study-etna

Книжный клуб по библиотеке [ETNA](https://github.com/etna-team/etna) — фреймворку для прогнозирования временных рядов.

## Материалы

- Официальная [документация библиотеки](https://docs.etna.ai/stable/index.html).
- Маршрут изучения — книга Артема Груздева **«Пособие по библиотеке временных рядов ETNA»**. На Boosty автора можно
  посмотреть [оглавление](https://boosty.to/drains/posts/26582567-a30c-41d0-915d-0ddbadcca714) и приобрести книгу
  за [1500руб](https://boosty.to/drains/posts/8b02f186-b785-403b-a371-7581b8929eab?share=post_link).

## Настройка окружения

- Проект использует [uv](https://docs.astral.sh/uv/) для управления зависимостями.
- Так как библиотека заблокирована в PyPI, то ставим из GitHub-репозитория разработчиков.

### macOS (Apple Silicon: M1/M2/M3/M4)

Зависимости `numba`/`llvmlite` для этой архитектуры не имеют прекомпилированных колёс и собираются из исходников — нужен
компилятор LLVM:

```bash
brew install llvm
uv init --python 3.11
LLVM_CONFIG="$(brew --prefix llvm)/bin/llvm-config" uv add "etna[all]@git+https://github.com/etna-team/etna.git@3.0.0"
```

### macOS (Intel) и Linux

Для этих платформ у `numba`/`llvmlite` есть готовые колёса на PyPI, компилятор не нужен:

```bash
uv init --python 3.11
uv add "etna[all]@git+https://github.com/etna-team/etna.git@3.0.0"
```

### Windows

Установи uv (PowerShell):

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Затем в терминале проекта:

```powershell
uv init --python 3.11
uv add "etna[all]@git+https://github.com/etna-team/etna.git@3.0.0"
```

Как и в случае с macOS Intel/Linux, готовые колёса `numba`/`llvmlite` под Windows есть на PyPI, поэтому дополнительный
компилятор не требуется.

### Если репозиторий уже склонирован (pyproject.toml и uv.lock уже в git)

Достаточно один раз выполнить:

```bash
uv sync
```

### Проверка установки

```bash
uv run python -c "
from importlib.metadata import version
print('etna version:', version('etna'))
from etna.datasets.tsdataset import TSDataset
from etna.models import NaiveModel
print('OK: TSDataset and NaiveModel imported successfully')
"
```

Ожидаемый вывод:

```
etna version: 3.0.0
OK: TSDataset and NaiveModel imported successfully
```
