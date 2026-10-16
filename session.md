# Сессия №3 — отложенное повторение: создание и смена статуса

> **Правило файлов:** в `session.md` всегда только текущее задание. Завершенная сессия вместе с разбором переносится в `archive/session-NN.md`. Прошлые сессии для выполнения не нужны.

Когда: 2026-10-18–19 (повторение навыка сессии №1 через 3–4 дня). Если дата пропущена — выполнить при первой возможности и записать фактическую дату. Ревизия при подготовке: `aef4ffd`; в начале попытки записать свою (`git rev-parse HEAD` в корне исходного проекта).

## Навык и цель

Предсказать значение, тип, статус и `valid_to` объекта `PersonIdentifier` сразу после создания и после последовательности смен статуса. Фрагмент: `src/domain/aggregates/person_identifier.py`, методы `__post_init__` и `change_status` (пути — от корня `/Users/ruslanozdoev/Dev/py/meta_learning`). Номера строк брать из IDE.

Метод — тот же, что в №2 (второе применение): **для каждой точки выписать полный путь — все номера выполненных строк по порядку, включая проверенные и ложные условия**, затем выводить результат только по ним. Каждое из четырех полей записывать в свою клетку, пустых клеток не оставлять.

**Обязательно в этот раз:** проверку запускаешь сам — это одна вставка в консоль, 1 минута.

## Рамка

20 минут максимум. 1 — рамка, 10 — чтение и предсказания, 3 — проверка, 4–6 — запись. До фиксации: исходники, IDE, свои заметки; не запускать, не читать тесты, не просить объяснений. Подсказки записывать с уровнем 0–3 (0 — нет; 1 — о способе; 2 — указано место; 3 — объяснено поведение).

## Подготовка — до таймера

Python-консоль PyCharm, интерпретатор `.venv`, рабочий каталог — корень исходного проекта. Вставить блок целиком: он только определяет функции, объектов не создает.

```python
import sys; sys.dont_write_bytecode = True

from datetime import UTC, datetime
from types import SimpleNamespace
from uuid import UUID

from src.domain.aggregates.person_identifier import PersonIdentifier
from src.domain.value_objects import PK, FieldStatus, Timestamp, ValueType

KEY = PK(UUID("12345678-1234-5678-1234-567812345678"))
START = Timestamp(datetime(2026, 10, 1, tzinfo=UTC))


def make_identifier(value_type, value, normalized_value, from_data_base):
    return PersonIdentifier(
        id=None,
        person_id=KEY,
        identifier_type_id=KEY,
        identifier_type=SimpleNamespace(value_type=value_type, validation_schema=None),
        value=value,
        normalized_value=normalized_value,
        status=FieldStatus.ACTIVE,
        source_system_id=KEY,
        source_record_id=None,
        valid_from=START,
        valid_to=None,
        from_data_base=from_data_base,
    )


def describe(obj):
    if obj.valid_to is None:
        valid_to = "None"
    elif obj.valid_to == START:
        valid_to = "исходный"
    else:
        valid_to = "новый момент"
    return (
        f"value={obj.value!r} ({type(obj.value).__name__}); "
        f"normalized_value={obj.normalized_value!r} ({type(obj.normalized_value).__name__}); "
        f"status={obj.status.name}; valid_to={valid_to}"
    )


def run(label, calls, **kwargs):
    try:
        obj = make_identifier(**kwargs)
    except Exception as e:
        print(f"{label} создан: исключение {type(e).__name__}: {e}")
        return
    print(f"{label} создан: {describe(obj)}")
    for status in calls:
        try:
            obj.change_status(status)
        except Exception as e:
            print(f"{label}: исключение на change_status({status.name}): {type(e).__name__}: {e}")
            break
    print(f"{label} после вызовов: {describe(obj)}")
```

## Задание

Сценарии независимы, каждый — новый объект. У всех при создании `status=ACTIVE`, `valid_to=None`.

| Сценарий | value_type | value | normalized_value | from_data_base | Вызовы после создания, по порядку |
| --- | --- | --- | --- | --- | --- |
| Р1 | `ValueType.DECIMAL` | `"4.20"` | `"4.2"` | `False` | `change_status(FieldStatus.INACTIVE)`, `change_status(FieldStatus.ACTIVE)` |
| Р2 | `ValueType.INTEGER` | `"delta"` | `"042"` | `True` | `change_status(FieldStatus.CONFLICT)`, `change_status(FieldStatus.INACTIVE)` |
| Р3 — свой | ___ | ___ | ___ | ___ | ___ |

Р3 придумать до запуска так, чтобы результат различал два возможных объяснения (запиши оба). Если ожидаешь исключение — тип, строка остановки, создан ли объект, выполнятся ли следующие вызовы.

## Предсказания — заполнить до запуска

`valid_to`: `None`, «исходный» или «новый момент».

| Точка | Путь: выполненные строки | value / тип | normalized_value / тип | status | valid_to | Уверенность, % |
| --- | --- | --- | --- | --- | --- | --- |
| Р1: создан | ___ | ___ | ___ | ___ | ___ | ___ |
| Р1: после вызовов | ___ | ___ | ___ | ___ | ___ | ___ |
| Р2: создан | ___ | ___ | ___ | ___ | ___ | ___ |
| Р2: после вызовов | ___ | ___ | ___ | ___ | ___ | ___ |
| Р3: создан | ___ | ___ | ___ | ___ | ___ | ___ |
| Р3: после вызовов | ___ | ___ | ___ | ___ | ___ | ___ |

Два объяснения, которые различает Р3, и какое наблюдение подтвердит каждое: ___

Какие условия могут сработать одновременно и что перезаписывается: ___

Время до фиксации: ___ мин.

## Проверка — сам, одной вставкой

Для Р3 заменить `...` своими значениями (вызовы — список, например `[FieldStatus.ACTIVE]`).

```python
run("Р1", [FieldStatus.INACTIVE, FieldStatus.ACTIVE], value_type=ValueType.DECIMAL, value="4.20", normalized_value="4.2", from_data_base=False)
run("Р2", [FieldStatus.CONFLICT, FieldStatus.INACTIVE], value_type=ValueType.INTEGER, value="delta", normalized_value="042", from_data_base=True)
run("Р3", [...], value_type=..., value=..., normalized_value=..., from_data_base=...)
```

Вывод консоли вставить сюда целиком:

```text
___
```

| Точка | Совпало /4 | Расхождение и объяснение |
| --- | --- | --- |
| Р1: создан | ___ | ___ |
| Р1: после вызовов | ___ | ___ |
| Р2: создан | ___ | ___ |
| Р2: после вызовов | ___ | ___ |
| Р3: создан | ___ | ___ |
| Р3: после вызовов | ___ | ___ |

## Итог

Первоначальные предсказания не менять.

- Верно (Р1, Р2): ___/16; Р3: ___/8 (отдельно, вход свой).
- Время: до фиксации ___ мин; всего ___ мин.
- Помощь: ___ подсказок; максимальный уровень: ___.
- Проверка гипотезы (Р3), 0–3: ___ (2 — свой вход с предсказанием; 3 — различает два объяснения, вывод согласован с наблюдением).
- Полный путь строк, второе применение — точность / время / ощущение: ___.
- Что изменю в следующий раз: ___.

После заполнения: попросить разбор, затем этот файл переносится в `archive/session-03.md`, строка — в [progress.md](progress.md).
