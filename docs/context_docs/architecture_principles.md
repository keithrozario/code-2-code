# Architecture Principles

  * Applications must be built as web based application to be viewed in a browser. 
  * Applications will be composed as a backend, frontend, and database.
  * Databases are datastores only, do not implement triggers or stored procedures in them
  * Backends are API driven and authenticated using JWTs.
  * Backends should assume JWTs presented to them are valid, they do not need to check the validity of the JWT, the Gateway will perform validation
  * The backend will also not issue JWTs, these will be issued from a separate identity provider.
  * Backends should infer user identity from the JWT. Stored in a `sub` parameter of the id token. The JWTs are in the `Auth: Bearer` header.
  * Frontends are built in native javascript

# Tech Stack

  * Backends are to be API-Driven built in Python using FastAPI
  * Frontends are to be built in native javascript (do not use frameworks like react or vue)
  * Databases are RDBMS built on SQLite3.

# Backends

  * API backends are to be built in Python and `FastAPI`
  * APIs should be prefixed with `/api/v1` for the first version of the API
  * Use the latest version of Python where possible
  * We use `uv` for package management.
  * Use `pytest` for executing test cases.
  * Lint all code with `black`
  * All logic and validation will be done by the backend. The backend will assume no validation on the frontend.
  * The Backend implement resource level protection, using a combination of JWT claims and user name to determine if a user can access a resource
  * If no JWT is present in a request that requires authentication, respond with a 403 status. The Gateway will redirect users appropriately.
  * Backend functions should not write data to local disk or hold state in memory
  * Use SQLAlchemy as the ORM
  * Data is stored in the `SQLite3` database
  * Files or Objects are to be stored in a Google Cloud Storage (GCS) bucket.
  * The Database and GCS bucket configuration is stored in environment variables
      * The Bucket Name(s) should be stored as descriptive environment variables
      * The SQLAlchemy engine configuration should be stored as descriptive environment variables
  * When interacting with Google Cloud Infrastructure (e.g. GCS buckets, PubSub, VertexAI) use the relevant google python SDKs.
  * As much as possible use Cloud Native functionality
  

# Infrastructure

  * Backend APIs are deployed as Google Cloud Run App
  * The Cloud Run app exists in a VPC and will only allow access from the same VPC
  * There is a External facing load balancer, that routes http traffic to a API gateway (e.g. Kong)
  * The API Gateway is also hosted as a CloudRun App in the VPC. 
  * The API Gateway will then route traffic to the CloudRun App.
  * As the app runs on a single SQLite3 database, the app cannot scale beyond 1 running instance.
  * The LoadBalancer will implement the cloudarmor firewall

# Databases

  * Databases are RDBMS and relation
  * Use only SQLite3 Databases
  * Do not use triggers or stored procedures in the database

# Frontends

  * Frontend are built with Native/Vanilla javascript
  * Frontend **might** perform validation to improve user experience.
  * Backends will still perform all required validation and verification.
  * Frontend will implement any flow required.





