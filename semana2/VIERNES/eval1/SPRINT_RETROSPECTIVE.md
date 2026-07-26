# Sprint 1 Retrospectiva - Sistema de Monitoreo IoT

##  Qué salió bien 
 **Calidad del Código y TDD:** Se logramos implementar el núcleo del negocio superando la meta de Definition of Done, alcanzando un 99% de cobertura en la prueba pytest.

 **Arquitectura Limpia:** La aplicación del Principio de Inversión de Dependencias (Protocolo `AlertStrategy`) nos permitió aislar la lógica de detección de anomalías sin acoplarnos a implementaciones reales de consola o email.

**Flujo de Trabajo:** El uso de `pyproject.toml` funcionó excelente como barrera de calidad.

##  Qué se puede mejorar

 **Fricción con el entorno y sintaxis:** Se perdio mucho tiempo en reparando errores de importación en Pytest causados por nombres incorrectas (uso de guiones medios `US-01.py` en lugar de guiones bajos `us_01.py`).

 **Declaraciones:** un problema muy recurrente es olvidar declarar variables o declarar variables fantasmas (que no se usan), y con el Protocolo `AlertStrategy` al minimo error te manda error en la terminar.

##  Acción Concreta para el próximo Sprint
**Estandarizar y automatizar el linting preventivo:** A partir del Sprint 2, antes de ejecutar `pytest`, será obligatorio ejecutar `ruff check .` en la terminal. De esta manera, detectar caracteres inválido o error de nombrado de variables/archivos en milisegundos, evitando que las herramientas de testing fallen silenciosamente. Además la utilizacion estricta de  `_` exclusivamente para todos los nombres de archivos Python.