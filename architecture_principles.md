# Architecture Principles

  * Applications must be built as web based application to be viewed in a browser. 
  * Applications will be composed as a backend, frontend, and database.
  * Databases are datastores only, do not implement triggers or stored procedures in them
  * Backends are API driven and authenticated using JWTs.
  * Backends should assume JWTs presented to them are valid, they do not need to check the validity of the JWT, the Gateway will perform validation
  * Backends should infer user identity from the JWT. Stored in a username parameter of the token.
  * Frontends are built in native javascript

# Tech Stack

  * Backends are to be API-Driven built in Python using FastAPI
  * Frontends are to be built in native javascript (do not use frameworks like react or vue)
  * Databases are to RDBMS built on SQLite3.
  * 

# Backends

  * API backends are to be built in Python and `FastAPI`
  * APIs should be prefixed with `/api/v1` for the first version of the API
  * Use the latest version of Python where possible
  * We use `uv` for package management.
  * Use `pytest` for generating test cases.
  * Lint all code with `black`
  * All logic and validation will be done by the backend. The backend will assume no validation on the frontend.

# Databases

  * Databases are RDBMS and relation
  * Use only SQLite3 Databases
  * Do not use triggers or stored procedures in the database

# Frontends

  * Frontend are built with Native/Vanilla javascript
  * Frontend **might** perform validation to improve user experience.
  * Backends will still perform all required validation and verification.
  * Frontend will implement any flow required.





