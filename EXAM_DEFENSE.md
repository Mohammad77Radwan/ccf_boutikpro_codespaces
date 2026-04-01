# EXAM DEFENSE

## 1) The Why (Architecture & Concepts)

- DB-API (Raw SQL)
  - Why: maximum SQL control, very explicit behavior, often easiest for performance tuning query-by-query.
  - Pros: direct SQL power, minimal abstraction, predictable generated SQL (because you write it).
  - Cons: more boilerplate, manual transaction handling, higher risk of mistakes if parameters are not handled correctly.

- SQLAlchemy Core
  - Why: keep SQL style but safer and cleaner with text() + named parameters.
  - Pros: better security defaults (parameter binding), cleaner transaction API, still close to SQL.
  - Cons: still mostly SQL-centric, less object-oriented than ORM.

- SQLAlchemy ORM
  - Why: fastest feature development with Python classes/relationships instead of writing SQL everywhere.
  - Pros: developer speed, readable domain model, relationship navigation (client.commandes, etc.).
  - Cons: abstraction can hide SQL costs, requires good relationship/loading knowledge.

## 2) Top 5 Guaranteed Professor Questions & Short Answers

- Q1: How does your code prevent SQL Injection?
  - A: I always use parameterized queries, never string concatenation.
  - DB-API: placeholders with `%s` and tuple values.
  - Core: `text("... WHERE id = :id")` with dict parameters.
  - ORM: values are bound automatically through Session operations and ORM filters.

- Q2: What happens if the database crashes halfway through creating an order?
  - A: The transaction is protected by try/except. If one step fails, I call rollback(), so partial writes are canceled. Only when all steps succeed do I call commit().

- Q3: How did you map Many-to-Many relationships like Contient and Livre?
  - A: With association tables.
  - SQL level: dedicated join tables (`contient`, `livre`) with composite primary keys and foreign keys.
  - ORM level: `Table(...)` objects used as `secondary=` in `relationship(...)`.

- Q4: How does the Recommande self-referencing relationship work?
  - A: `recommande` links `client` to `client` (source -> cible). In ORM I use a self-referential association table with explicit `primaryjoin`, `secondaryjoin`, and `foreign_keys` so SQLAlchemy knows which side is source and which side is target.

- Q5: In ORM, what is the N+1 query problem and how does it relate to Lazy vs Eager loading?
  - A: N+1 means 1 query for parent rows + 1 extra query per row for children (too many queries).
  - Lazy loading can trigger this if I loop over many parents and access related fields.
  - Eager loading fetches related data earlier (often in fewer queries), which avoids the explosion.

## 3) The 60-Minute Modification Blueprint (Step-by-Step)

- Add a brand new table/entity
  - [ ] Update schema in [sql/01_schema.sql](sql/01_schema.sql)
  - [ ] If required by subject evolution, update [sql/student_upgrade.sql](sql/student_upgrade.sql)
  - [ ] Optional test data in [sql/02_seed.sql](sql/02_seed.sql)
  - [ ] Add ORM class in [src/orm/main.py](src/orm/main.py)
  - [ ] Add DB-API SQL functions in [src/dbapi/main.py](src/dbapi/main.py)
  - [ ] Add Core text() functions in [src/core/main.py](src/core/main.py)
  - [ ] If feature is user-facing, add menu option in all needed main.py files

- Add a new Many-to-Many relationship
  - [ ] Create association table + FKs in [sql/01_schema.sql](sql/01_schema.sql)
  - [ ] DB-API/Core: update INSERT/JOIN logic in [src/dbapi/main.py](src/dbapi/main.py) and [src/core/main.py](src/core/main.py)
  - [ ] ORM: define `association_table = Table(...)` in [src/orm/main.py](src/orm/main.py)
  - [ ] ORM: add `relationship(..., secondary=association_table, back_populates=...)` on both sides

- Add a new menu option for a custom JOIN query
  - [ ] Implement function in target file ([src/dbapi/main.py](src/dbapi/main.py), [src/core/main.py](src/core/main.py), or [src/orm/main.py](src/orm/main.py))
  - [ ] Add printed option line in `main_menu()`
  - [ ] Add `if/elif` branch to call function
  - [ ] Keep pause line (`Appuyez sur Entrée...`) and test with quick scripted input

## 4) Golden Rules for Live Coding

- Rule 1: Never skip transaction finalization on writes
  - DB-API/Core: commit on success, rollback in except.
  - ORM: session.commit on success, session.rollback in except.

- Rule 2: Never build SQL with f-strings/user input
  - Use `%s` (DB-API) or `:param` (Core text()) or ORM-bound values.

- Rule 3: For relationship changes, sync SQL + Python together
  - If FK/table changes in SQL but ORM/class code is not updated (or inverse), runtime errors are almost guaranteed.
