# ADR 0001: Implementación de Arquitectura en Capas y Patrón Repositorio en SensorHub

## Estado
Aceptado

## Contexto
A medida que el proyecto SensorHub ha avanzado hacia su fase de producción, la lógica de negocio comenzó a mezclarse directamente dentro de los endpoints de la API. Esto generó un alto acoplamiento que dificulta dos objetivos principales:
1. Aislar la lógica de negocio para poder testearla de forma rápida mediante pruebas unitarias sin depender de la infraestructura externa.
2. Migrar de una base de datos local (SQLite) a una base de datos en la nube (PostgreSQL) sin tener que reescribir múltiples partes del código.

## Decisión
Se decide estructurar el proyecto utilizando una **Arquitectura en Capas**, definiendo el siguiente flujo unidireccional: 
`routers` (capa de presentación HTTP) -> `services` (capa de lógica de negocio) -> `repositories` (capa de acceso a datos) -> `models` (capa de dominio).

Para conectar la capa de servicios con la capa de repositorios, aplicaremos el **Principio de Inversión de Dependencias (DIP)** de SOLID. Los servicios no dependerán de una implementación concreta de base de datos, sino de un contrato abstracto (usando `typing.Protocol`).

## Consecuencias

### Positivas (+)
* **Testing Aislado:** Habilita la creación de repositorios simulados (*Fake Repositories* en memoria) para ejecutar tests de la lógica del servicio sin requerir una conexión real a base de datos.
* **Agnosticismo de Infraestructura:** El cambio del motor de persistencia (SQLite a PostgreSQL) se realiza creando una nueva clase concreta que cumpla el contrato, dejando la lógica de negocio (`services`) intacta.
* **Mantenibilidad:** El código queda modularizado y cada capa tiene una única responsabilidad (SRP).

### Negativas (-)
* **Curva de Aprendizaje:** Requiere que todos los desarrolladores entiendan el concepto de Inyección de Dependencias.
* **Sobrecarga de Archivos:** Introduce mayor "ceremonia" y cantidad de archivos (interfaces, repositorios concretos, servicios) incluso para tareas simples como un CRUD básico.
