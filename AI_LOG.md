## Semana 4 · Entrada 1
Prompt: "modifica db.py para leer DATABASE_URL del entorno, con SQLite como
default local, y normaliza postgres:// / postgresql:// a postgresql+psycopg://"

La IA propuso una función get_database_url() y agregar connect_args condicional
(check_same_thread solo aplica a SQLite). Acepté la función tal cual. Modifiqué
la sugerencia inicial de connect_args = {} sin tipo: mypy marcaba error porque
disallow_untyped_defs exige anotación explícita. Cambié a
connect_args: dict[str, bool] = {} para que pasara mypy sin desactivar la regla.

## Semana 4 · Entrada 2
Prompt: "docker compose up --build falla con connection refused en api-1
aunque db-1 ya inició"

La IA diagnosticó que depends_on: [db] solo espera a que el contenedor exista,
no a que PostgreSQL acepte conexiones, y propuso un healthcheck con pg_isready
más depends_on con condition: service_healthy. Acepté la solución completa.
Verifiqué el comportamiento reiniciando con docker compose down -v para
confirmar que el healthcheck realmente bloqueaba el arranque de api hasta que
db reportara "healthy" en los logs.

## Semana 4 · Entrada 3
Prompt: "necesito inicializar Alembic para las migraciones"

La IA propuso quitar Base.metadata.create_all() de main.py y reemplazarlo por
Alembic como único responsable del esquema, argumentando que create_all() no
modifica tablas existentes y ya me había causado un error de "no such column"
en la semana. Acepté el cambio de arquitectura. Antes de aplicarlo pregunté
por qué no podían convivir ambos mecanismos en paralelo; la respuesta (evitar
que dos sistemas compitan por la misma responsabilidad, y alinear el proyecto
con el flujo de arranque que pide la guía para producción) me convenció de
aceptarlo sin modificarlo.

## Semana 4 · Entrada 4
Prompt: "una línea autogenerada por Alembic en migrations/versions supera el
límite de ruff, ¿la reescribo?"

La IA propuso dos opciones: reformatear la línea a mano, o excluir
migrations/versions del linting vía extend-exclude en pyproject.toml. Rechacé
reformatear a mano porque cada alembic revision --autogenerate futura
regeneraría el archivo con el mismo formato, obligándome a repetir el ajuste
cada vez. Acepté la exclusión: es código generado por una herramienta, no
código que yo mantengo línea por línea, y es la práctica estándar para
carpetas de migraciones autogeneradas.
