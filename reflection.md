REFLECTION – Software Design Patterns & Code Refactoring
1. Project Context

This project consists of a small REST API built with Flask-RESTful.
It exposes resources for authentication, products, categories, and favorites, relying on a JSON file (db.json) as its data store.

Although functional, the original code contained several design issues that negatively affected readability, maintainability, and scalability. The purpose of this activity was to analyze the existing code, identify design problems ("code smells"), and apply appropriate software design patterns to improve the overall quality of the codebase.

2. Identified Problems (Code Smells)
2.1 Duplication of Authentication Logic

Each resource (ProductsResource, CategoriesResource, FavoritesResource) implemented its own token validation logic, including:

Repeated extraction of the Authorization header

Repeated hardcoded token comparison

Repeated error messages for missing or invalid tokens

Why this matters:

Higher maintenance cost

Risk of inconsistency

Violates DRY (Don’t Repeat Yourself)

Reduces clarity and separation of concerns

2.2 Hardcoded and Inconsistent Token Handling

AuthenticationResource generated a token (abcd12345), while the other resources validated a different token (abcd1234), causing the API to fail under normal usage.

Issues:

No single source of truth

Scattered hardcoded constants

Violates SRP (Single Responsibility Principle) and Single Source of Truth

2.3 Tight Coupling Between Resources and Authentication Logic

Each resource manually handled:

Header extraction

Token validation

Response and error management

This introduced strong coupling between authentication and business logic, making the code rigid and harder to modify.

2.4 Low Cohesion Within Endpoint Classes

Multiple responsibilities were mixed inside the same classes:

Authentication

Request validation

Business logic

Database operations with DatabaseConnection

This violated cohesion and made testing and maintenance more difficult.

3. Applied Design Patterns
3.1 Service Pattern (Singleton-like): AuthService

A new file utils/auth_service.py was created to centralize:

Token generation

Token validation

Authentication rules

Benefits:

A single source of truth for all authentication logic

Simplified maintenance

Reduced coupling

More scalable and readable code

3.2 Template Method Pattern via AuthenticatedResource

A new base class was introduced in:

endpoints/base_resource.py


This class defines the shared method _require_valid_token() used across all secured endpoints.

Pattern behavior:

The base class defines the invariant structure (authentication check)

Subclasses implement their specific logic (GET, POST, etc.)

Benefits:

Eliminates duplicate authentication code

Ensures consistency

Improves readability

Separates cross-cutting concerns from business logic

3.3 Improved Separation of Concerns

While not strictly a GoF pattern, the refactor significantly improved:

Cohesion

Readability

Component isolation

This makes the architecture cleaner, clearer, and easier to evolve.

4. Assumptions and Design Decisions
4.1 Authentication intentionally remains simple

I assumed the fixed token mechanism was intentional for academic or demonstration purposes, so I preserved it but centralized the logic in AuthService.

4.2 JSON file as required persistence

I maintained the JSON storage system (db.json) to respect the original project constraints, even though a real database would be ideal in a professional context.

4.3 Choosing a base class over decorators

Instead of creating decorators for authentication, I introduced a base class (AuthenticatedResource) because:

It fits the OOP style of Flask-RESTful

It keeps the workflow predictable

It avoids adding external dependencies

4.4 Avoiding large structural changes

I did not introduce a full repository layer or ORM because the activity focuses on design patterns and code smells, not full architecture redesign.

4.5 Preserving original API behavior

All refactoring maintained functional compatibility with the original API: endpoints, data structures, and response formats remain unchanged.

5. Impact of the Refactoring
5.1 Improved Maintainability

All authentication logic now resides in:

AuthService

AuthenticatedResource

which greatly reduces the number of files that must be modified when changes occur.

5.2 Improved Readability

Resource methods now follow a clear structure:

Validate token

Execute business logic

without clutter from repeated validation code.

5.3 Reduced Risk of Bugs

Token inconsistencies have been eliminated.
Validation is now done through a single, centralized rule.

5.4 A More Scalable Architecture

The codebase is now prepared for:

JWT or OAuth authentication

Real database repositories

Logging and monitoring

Unit testing

Middleware-based authentication

These enhancements would be difficult or risky in the original structure.

6. Version Control Strategy

I used a clean commit strategy with descriptive messages, for example:

feat(auth): add AuthService for centralized token handling

refactor(products): reuse AuthenticatedResource for token validation

chore(cleanup): remove unused imports after refactor

This approach supports maintainability, peer review, and traceability of every change.

7. Visual Evidence

Below are screenshots illustrating the problems identified and the improvements made:

7.1 Original duplicated authentication logic

(insert screenshot: screenshots/original_auth.png)

7.2 Centralized authentication using AuthService

(insert screenshot: screenshots/auth_service.png)

7.3 Base class applying Template Method (AuthenticatedResource)

(insert screenshot: screenshots/authenticated_resource.png)

7.4 Git commit history showing structured refactoring

(insert screenshot: screenshots/commit_history.png)

8. Reflection and Lessons Learned

Working on this activity provided valuable insights:

    Importance of early detection of code smells

Duplication and inconsistency grow rapidly and make systems fragile.

Power of design patterns even in small projects

Patterns like Service and Template Method significantly improve structure and clarity.

Clean architecture facilitates future evolution

Separating authentication, business logic, and data access is crucial for maintainability.

Refactoring must be incremental

Breaking changes into small commits improves safety and clarity.

Documentation and commits matter

Clear documentation and commit messages help future developers and demonstrate professional practice.

9. Conclusion

Through analysis and strategic application of design patterns, the refactored project now demonstrates:

Higher readability

Better maintainability

Lower coupling

Stronger cohesion

More scalable architecture

This activity reinforced the importance of thoughtful software design and showcased the practical value of refactoring and design patterns in real-world codebases.
