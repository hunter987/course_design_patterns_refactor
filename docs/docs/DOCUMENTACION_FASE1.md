Proyecto de Software – Fase 1
1. Introducción

Esta documentación presenta el desarrollo de la Fase 1 del proyecto de software, cuyo objetivo es extender el sistema previamente refactorizado mediante la creación de un nuevo módulo. Dicho módulo incorpora patrones de diseño que mejoran la reutilización, escalabilidad y mantenibilidad del software, alineándose con las buenas prácticas de ingeniería propuestas en la actividad.

El nuevo módulo implementado —Gestión de Usuarios— complementa el sistema de autenticación existente (AuthService y AuthenticatedResource) y permite administrar el ciclo de vida de los usuarios dentro de la aplicación. Su diseño se fundamenta en principios sólidos de arquitectura y patrones de diseño reconocidos en la industria.

2. Modalidad de trabajo y roles

Aunque la actividad fue diseñada para trabajo colaborativo, esta fase fue desarrollada de manera individual. Para cumplir con los requerimientos, se asumieron simultáneamente los siguientes roles:

Líder del proyecto: definición del alcance funcional del módulo.

Diseñador de software: elaboración de arquitectura, identificación de patrones y definición de interfaces.

Desarrollador: implementación del módulo e integración con el sistema existente.

Tester: creación y ejecución de pruebas unitarias e integración.

Documentador: elaboración de la documentación técnica, diagramas UML y justificación del diseño.

El desarrollo se organizó siguiendo prácticas ágiles adaptadas a un contribuyente único.

3. Metodología ágil y roadmap

Se utilizó una versión adaptada de Scrum, estructurada en un sprint único dedicado al diseño, implementación e integración del módulo.

3.1 Roles Scrum (adaptados)

Product Owner: desarrollador

Scrum Master: desarrollador

Development Team: desarrollador

3.2 Product Backlog del módulo
ID	Historia de usuario	Prioridad
HU1	Registrar nuevos usuarios para gestionar accesos	Alta
HU2	Actualizar información de usuarios existentes	Media
HU3	Desactivar usuarios para revocar acceso	Media
HU4	Listar usuarios filtrados por estado	Media
HU5	Garantizar que las reglas de validación sean extensibles mediante patrones	Alta
3.3 Sprint Backlog (1 semana)

Diseño UML del módulo

Implementación de clases principales

Aplicación de patrones (Service, Strategy, Repository)

Integración con autenticación

Pruebas unitarias

Actualización de documentación técnica

4. Definición del nuevo módulo
4.1 Problema identificado

El sistema actual dispone de autenticación centralizada mediante AuthService, pero carece de un módulo para gestionar el ciclo de vida de los usuarios, lo que dificulta futuras expansiones relacionadas con seguridad, permisos o auditoría.

4.2 Objetivo del módulo

El Módulo de Gestión de Usuarios tiene como propósito:

Centralizar operaciones CRUD de usuarios.

Separar responsabilidades mediante patrones de diseño adecuados.

Facilitar escalabilidad y mantenimiento.

Integrarse de forma limpia con el sistema de autenticación existente.

4.3 Alcance funcional

Crear usuarios con validación previa.

Actualizar datos de usuarios.

Desactivar usuarios sin eliminarlos.

Listar usuarios con filtros básicos.

4.4 Patrones de diseño aplicados

Service Layer: UserService concentra reglas de negocio.

Strategy: validador intercambiable (UserValidatorStrategy, BasicUserValidator).

Repository: abstracción del acceso a datos (UserRepository e InMemoryUserRepository).

5. Diseño del módulo (UML y arquitectura)
5.1 Diagrama de clases
classDiagram
    class User {
        +id
        +username
        +email
        +isActive
        +to_dict()
    }

    class UserService {
        +create_user(data)
        +update_user(id, data)
        +deactivate_user(id)
        +list_users(filter)
        +get_user(id)
    }

    class UserValidatorStrategy {
        <<interface>>
        +validate(data)
    }

    class BasicUserValidator {
        +validate(data)
    }

    class UserRepository {
        <<interface>>
        +save(user)
        +update(user)
        +deactivate(id)
        +find_by_id(id)
        +find_all(filter)
    }

    class InMemoryUserRepository {
        +save(user)
        +update(user)
        +deactivate(id)
        +find_by_id(id)
        +find_all(filter)
    }

    UserService --> UserRepository
    UserService --> UserValidatorStrategy
    BasicUserValidator ..|> UserValidatorStrategy
    InMemoryUserRepository ..|> UserRepository

5.2 Integración con el sistema existente
flowchart LR
    Client --> UsersResource
    UsersResource --> AuthenticatedResource
    AuthenticatedResource --> AuthService
    UsersResource --> UserService
    UserService --> UserRepository
    UserService --> UserValidatorStrategy

6. Implementación

La implementación del módulo se llevó a cabo mediante los siguientes componentes:

Entidad User: representación de un usuario dentro del sistema.

UserService: capa de negocio encargada de validar datos, aplicar reglas y coordinar interacciones con el repositorio.

UserRepository + InMemoryUserRepository: abstracción e implementación concreta del almacenamiento.

UserValidatorStrategy: permite intercambiar reglas de validación sin modificar la lógica central.

UsersResource: recurso REST que expone las funciones del módulo mediante Flask-RESTful, integrándose con el mecanismo de autenticación.

El módulo fue registrado en la API principal mediante:

api.add_resource(UsersResource, "/users", "/users/<int:user_id>")


Asegurando operación autenticada y consistente.

7. Pruebas (unitarias e integración)
7.1 Pruebas unitarias

Se desarrollaron pruebas unitarias utilizando PyTest, validando:

Creación de usuarios con datos válidos.

Manejo adecuado de datos inválidos (correo incorrecto).

Desactivación de usuarios.

Consulta y filtrado básico.

Resultado de ejecución:

3 passed in 0.04s

7.2 Pruebas de integración

Las pruebas verificaron:

Que AuthenticatedResource permite/bloquea acceso según token.

Que los endpoints del módulo invocan correctamente UserService.

Que la integración entre repositorio, servicio y recurso funciona de extremo a extremo.

8. Conclusiones

La implementación del Módulo de Gestión de Usuarios permitió extender el sistema de manera estructurada, manteniendo bajo acoplamiento y alta cohesión. La adopción de patrones de diseño como Service Layer, Repository y Strategy facilitó un diseño flexible, escalable y orientado a mantenibilidad.

La integración con el sistema de autenticación reafirmó la consistencia del flujo de acceso.
El uso de prácticas ágiles, incluso en un proyecto individual, permitió organizar y ejecutar el desarrollo de forma clara, incremental y verificable.

9. Referencias

Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.
Refactoring Guru. (s.f.). Design patterns in different programming languages. https://refactoring.guru/design-patterns

Sommerville, I. (2011). Ingeniería de Software (9a ed.). Pearson.
Schwaber, K., & Sutherland, J. (2017). The Scrum Guide. https://scrumguides.org

Universidad Tecnológica de Bolívar. (2023). Recursos de la actividad 2.