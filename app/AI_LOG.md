# Bitacora  - Semana 3

## Entrada 1: 
* Prompt que usé: "¿Cómo configuro la base de datos en memoria para los tests de FastAPI usando SQLite sin que me tire errores de tablas no encontradas al aislar las pruebas?"
* Qué produjo la IA: Sugirió crear un motor SQLite en RAM (`sqlite:///:memory:`) utilizando `StaticPool` y `check_same_thread=False` para evitar que las conexiones de SQLAlchemy perdieran las tablas. También proporcionó el código para hacer el override de la dependencia `get_db` en la app principal, por que al querer testearlo de manera normal me generaba muchos errores.
* Acepté la mayor parte del codigo pero tuve que modificar los imports añadiendo `from sqlalchemy.orm import Session` porque Mypy arrojaba el error `Name "Session" is not defined` en el tipado del generador (`Generator[Session, None, None]`).

## Entrada 2:
* Prompt que usé: "¿Cómo agrego paginación a mis endpoints GET en la estructura de 4 capas (Router, Service, Repo)?"
* **Qué produjo la IA:** Generó el código para añadir los parámetros `skip: int = Query(0)` y `limit: int = Query(100)` en el Router, pasarlos por el `SensorService`, y aplicarlos en SQLAlchemy usando `.offset(skip).limit(limit).all()` en el Repositorio.
* El código que me otorgo era correcto, pero al pegarlo generé una duplicación de funciones. Ruff me detectó los errores `F811`  y `F821` . Modifiqué el archivo borrando la función original y cambiando `List` por el nativo `list` de Python.

## Entrada 3:
* Prompt que usé: "Mypy me marca esto: `tests/test_main.py:22: error: Function is missing a return type annotation [no-untyped-def]`"
* Qué produjo la IA: Explicó que Mypy en modo estricto requiere que absolutamente todas las funciones tengan declarado su tipo de retorno. Sugirió agregar `-> None` a todas las funciones de prueba de `pytest` (incluyendo las que usan `capsys` con el tipo `pytest.CaptureFixture[str]`) y usar `-> Any` o el esquema Pydantic correspondiente en los endpoints de FastAPI.
* Apliqué las sugerencias exactamente como las indicó la IA para los archivos de test y los constructores `__init__` (agregando `-> None`). Esto eliminó los más de 15 errores de tipado estricto que marcaba Mypy en la carpeta `/app` y `/tests`.
