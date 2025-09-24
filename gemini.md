# Project: Money-note rewrite

## Introduction

The project will re-write money note from Java to a new tech stack written below.

In version 1 we will retain all functionality in moneynote and only perform a technical re-write.


## Tech Stack

* The backend is API driven, written in Python using Fast API.
* The Database is a SQLite3 file named `moneynote.db`
* The Database will implement exactly the data model used in the old version.
* The frontend will be implemented react-js
* Any authentication of the user will be done by an API gateway, we will not perform authentication in code here.
* The api will write directly into the database

## Database

* Reimplement the database in SQLite3 by implementing the models in code.
* The database in `./moneynote.db` there is only one database, use this.
* The database definition is in `./technical_design/database_design/database_schema.md`

