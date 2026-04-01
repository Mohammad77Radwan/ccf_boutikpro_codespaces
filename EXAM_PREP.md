# EXAM PREP - BoutikPro

## 1) Architecture Summary (Elevator Pitch)

- DB-API ([src/dbapi/main.py](src/dbapi/main.py)): Python talks directly to MySQL with mysql.connector and SQL strings. You manually manage cursor, parameters, commit, and close.
- SQLAlchemy Core ([src/core/main.py](src/core/main.py)): You still write SQL, but through SQLAlchemy engine + text(), with named parameters (:param) and cleaner transaction handling.
- SQLAlchemy ORM ([src/orm/main.py](src/orm/main.py)): You manipulate Python objects/classes mapped to tables, and SQLAlchemy builds SQL for you via Session and relationships.

## 2) Modification Blueprint (Step-by-Step)

### A) Add a New Table

Copy-paste checklist:

- [ ] Add CREATE TABLE in [sql/01_schema.sql](sql/01_schema.sql)
- [ ] If required by exam evolution, add ALTER/extra data in [sql/student_upgrade.sql](sql/student_upgrade.sql)
- [ ] Add seed/demo rows in [sql/02_seed.sql](sql/02_seed.sql) (if needed)
- [ ] DB-API mode: add SQL CRUD functions in [src/dbapi/main.py](src/dbapi/main.py)
- [ ] Core mode: add text() SQL CRUD functions in [src/core/main.py](src/core/main.py)
- [ ] ORM mode: add model class + columns in [src/orm/main.py](src/orm/main.py)
- [ ] Add menu option(s) in each main.py if professor asks to expose the feature in UI

### B) Add a New Relationship

Copy-paste checklist:

- [ ] SQL first: add FK (or association table for N:M) in [sql/01_schema.sql](sql/01_schema.sql)
- [ ] DB-API/Core: update JOIN queries and INSERT/UPDATE logic in [src/dbapi/main.py](src/dbapi/main.py) and [src/core/main.py](src/core/main.py)
- [ ] ORM 1:N:
  - [ ] Child gets ForeignKey column
  - [ ] Parent gets relationship(..., back_populates=...)
  - [ ] Child gets relationship(..., back_populates=...)
- [ ] ORM N:M:
  - [ ] Create association_table = Table(...)
  - [ ] Use relationship(secondary=association_table, back_populates=...)
- [ ] ORM self-reference (if asked): set foreign_keys + primaryjoin/secondaryjoin explicitly

### C) Add a New Menu Option

Copy-paste checklist:

- [ ] Write a new function (ex: report_xxx()) in target file:
  - [ ] [src/dbapi/main.py](src/dbapi/main.py)
  - [ ] [src/core/main.py](src/core/main.py)
  - [ ] [src/orm/main.py](src/orm/main.py)
- [ ] In main_menu(), add the printed option line
- [ ] In main_menu(), add the if/elif branch to call the function
- [ ] Keep input("Appuyez sur Entrée pour continuer...") behavior
- [ ] Smoke test quickly with piped input (example):
  - [ ] python -m src.core.main

## 3) Core vs ORM Cheat Sheet

```python
# DB-API (mysql.connector)
cur.execute("SELECT id_client, nom FROM client ORDER BY id_client")
cur.execute(
    "INSERT INTO client(nom, prenom, email) VALUES (%s, %s, %s)",
    (nom, prenom, email)
)
conn.commit()

# SQLAlchemy Core
rows = conn.execute(text("SELECT id_client, nom FROM client ORDER BY id_client"))
conn.execute(
    text("INSERT INTO client(nom, prenom, email) VALUES (:nom, :prenom, :email)"),
    {"nom": nom, "prenom": prenom, "email": email}
)
conn.commit()

# SQLAlchemy ORM
clients = session.query(Client).order_by(Client.id_client).all()
session.add(Client(nom=nom, prenom=prenom, email=email))
session.commit()
```

## 4) Common Traps & Instant Fixes

1. Write works but nothing saved
- Cause: forgot commit
- Instant fix:
  - DB-API: conn.commit()
  - Core: conn.commit()
  - ORM: session.commit()

2. App crashes after a DB error, then all next writes fail
- Cause: transaction left in failed state
- Instant fix:
  - Core: in except SQLAlchemyError -> conn.rollback()
  - ORM: in except SQLAlchemyError -> session.rollback()

3. Wrong totals in aggregation by category
- Cause: summing commande.montant_total after joining lines duplicates totals
- Instant fix: compute line-level revenue only
  - SQL: SUM(produit.prix * contient.quantite)
  - Already applied in:
    - [src/core/main.py](src/core/main.py)
    - [src/orm/main.py](src/orm/main.py)
