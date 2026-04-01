from datetime import date, datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    create_engine,
    func,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from src.common.helpers import print_menu

engine = create_engine("mysql+pymysql://student:studentpwd@db:3306/boutikpro_ccf")


class Base(DeclarativeBase):
    pass


contient_association_table = Table(
    "contient",
    Base.metadata,
    Column("id_commande", ForeignKey("commande.id_commande"), primary_key=True),
    Column("id_produit", ForeignKey("produit.id_produit"), primary_key=True),
    Column("quantite", Integer, nullable=False, default=1),
)


livre_association_table = Table(
    "livre",
    Base.metadata,
    Column("id_produit", ForeignKey("produit.id_produit"), primary_key=True),
    Column("id_fournisseur", ForeignKey("fournisseur.id_fournisseur"), primary_key=True),
)


recommande_association_table = Table(
    "recommande",
    Base.metadata,
    Column("id_client_source", ForeignKey("client.id_client"), primary_key=True),
    Column("id_client_cible", ForeignKey("client.id_client"), primary_key=True),
)


class Client(Base):
    __tablename__ = "client"

    id_client: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(50), nullable=False)
    prenom: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    telephone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    carte_fidelite: Mapped["Carte_fidelite"] = relationship(
        back_populates="client", uselist=False
    )
    commandes: Mapped[list["Commande"]] = relationship(back_populates="client")

    clients_recommandes: Mapped[list["Client"]] = relationship(
        "Client",
        secondary=recommande_association_table,
        primaryjoin=id_client == recommande_association_table.c.id_client_source,
        secondaryjoin=id_client == recommande_association_table.c.id_client_cible,
        foreign_keys=[
            recommande_association_table.c.id_client_source,
            recommande_association_table.c.id_client_cible,
        ],
        back_populates="recommande_par",
    )

    recommande_par: Mapped[list["Client"]] = relationship(
        "Client",
        secondary=recommande_association_table,
        primaryjoin=id_client == recommande_association_table.c.id_client_cible,
        secondaryjoin=id_client == recommande_association_table.c.id_client_source,
        foreign_keys=[
            recommande_association_table.c.id_client_cible,
            recommande_association_table.c.id_client_source,
        ],
        back_populates="clients_recommandes",
    )


class Carte_fidelite(Base):
    __tablename__ = "carte_fidelite"

    id_carte_fidelite: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_creation: Mapped[date] = mapped_column(Date, nullable=False)
    points_fidelite: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    id_client: Mapped[int] = mapped_column(
        Integer, ForeignKey("client.id_client"), nullable=False, unique=True
    )

    client: Mapped["Client"] = relationship(back_populates="carte_fidelite")


class Etat_commande(Base):
    __tablename__ = "etat_commande"

    id_etat: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_etat: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    commandes: Mapped[list["Commande"]] = relationship(back_populates="etat")


class Commande(Base):
    __tablename__ = "commande"

    id_commande: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_commande: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    montant_total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    id_client: Mapped[int] = mapped_column(
        Integer, ForeignKey("client.id_client"), nullable=False
    )
    id_etat: Mapped[int] = mapped_column(
        Integer, ForeignKey("etat_commande.id_etat"), nullable=False, default=1
    )

    client: Mapped["Client"] = relationship(back_populates="commandes")
    etat: Mapped["Etat_commande"] = relationship(back_populates="commandes")
    facture: Mapped["Facture"] = relationship(back_populates="commande", uselist=False)
    produits: Mapped[list["Produit"]] = relationship(
        secondary=contient_association_table,
        back_populates="commandes",
    )


class Facture(Base):
    __tablename__ = "facture"

    id_facture: Mapped[int] = mapped_column(Integer, primary_key=True)
    montant_ttc: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    date_facture: Mapped[date] = mapped_column(Date, nullable=False)
    id_commande: Mapped[int] = mapped_column(
        Integer, ForeignKey("commande.id_commande"), nullable=False, unique=True
    )

    commande: Mapped["Commande"] = relationship(back_populates="facture")


class Categorie_produit(Base):
    __tablename__ = "categorie_produit"

    id_categorie_produit: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_categorie: Mapped[str] = mapped_column(String(50), nullable=False)

    produits: Mapped[list["Produit"]] = relationship(back_populates="categorie_produit")


class Produit(Base):
    __tablename__ = "produit"

    id_produit: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(String(50), nullable=False)
    prix: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    id_categorie_produit: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categorie_produit.id_categorie_produit"),
        nullable=False,
    )

    categorie_produit: Mapped["Categorie_produit"] = relationship(back_populates="produits")
    commandes: Mapped[list["Commande"]] = relationship(
        secondary=contient_association_table,
        back_populates="produits",
    )
    fournisseurs: Mapped[list["Fournisseur"]] = relationship(
        secondary=livre_association_table,
        back_populates="produits",
    )


class Categorie_fournisseur(Base):
    __tablename__ = "categorie_fournisseur"

    id_categorie_fournisseur: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_categorie: Mapped[str] = mapped_column(String(50), nullable=False)

    fournisseurs: Mapped[list["Fournisseur"]] = relationship(
        back_populates="categorie_fournisseur"
    )


class Fournisseur(Base):
    __tablename__ = "fournisseur"

    id_fournisseur: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_fournisseur: Mapped[str] = mapped_column(String(50), nullable=False)
    id_categorie_fournisseur: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categorie_fournisseur.id_categorie_fournisseur"),
        nullable=False,
    )

    categorie_fournisseur: Mapped["Categorie_fournisseur"] = relationship(
        back_populates="fournisseurs"
    )
    produits: Mapped[list["Produit"]] = relationship(
        secondary=livre_association_table,
        back_populates="fournisseurs",
    )


def list_clients():
    try:
        with Session(engine) as session:
            clients = session.query(Client).order_by(Client.id_client).all()
            if not clients:
                print("Aucun client trouvé.")
            else:
                print("Liste des clients :")
                for client in clients:
                    print(
                        f"ID: {client.id_client}, Nom: {client.nom}, "
                        f"Prénom: {client.prenom}, Email: {client.email}"
                    )
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def create_client():
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    email = input("Email : ")
    try:
        with Session(engine) as session:
            try:
                client = Client(nom=nom, prenom=prenom, email=email)
                session.add(client)
                session.commit()
                print("Client créé avec succès.")
            except SQLAlchemyError:
                session.rollback()
                raise
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def update_client():
    id_client = int(input("ID du client à modifier : "))
    nom = input("Nouveau nom : ")
    prenom = input("Nouveau prénom : ")
    email = input("Nouvel email : ")
    try:
        with Session(engine) as session:
            try:
                client = session.get(Client, id_client)
                if client is None:
                    print("Client non trouvé.")
                    return
                client.nom = nom
                client.prenom = prenom
                client.email = email
                session.commit()
                print("Client modifié avec succès.")
            except SQLAlchemyError:
                session.rollback()
                raise
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def delete_client():
    id_client = int(input("ID du client à supprimer : "))
    try:
        with Session(engine) as session:
            try:
                client = session.get(Client, id_client)
                if client is None:
                    print("Client non trouvé.")
                    return
                session.delete(client)
                session.commit()
                print("Client supprimé avec succès.")
            except SQLAlchemyError:
                session.rollback()
                raise
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def list_products():
    try:
        with Session(engine) as session:
            products = (
                session.query(Produit)
                .join(Produit.categorie_produit)
                .order_by(Produit.id_produit)
                .all()
            )
            if not products:
                print("Aucun produit trouvé.")
            else:
                print("Liste des produits :")
                for product in products:
                    print(
                        f"ID: {product.id_produit}, Libellé: {product.libelle}, "
                        f"Prix: {product.prix}, Stock: {product.stock}, "
                        f"Catégorie: {product.categorie_produit.nom_categorie}"
                    )
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def create_order():
    id_client = int(input("ID du client : "))
    id_produit = int(input("ID du produit : "))
    quantite = int(input("Quantité : "))
    try:
        with Session(engine) as session:
            try:
                client = session.get(Client, id_client)
                if client is None:
                    print("Client non trouvé.")
                    return

                produit = session.get(Produit, id_produit)
                if produit is None:
                    print("Produit non trouvé.")
                    return

                if produit.stock < quantite:
                    print("Stock insuffisant.")
                    return

                montant_total = produit.prix * quantite
                commande = Commande(
                    date_commande=datetime.now(),
                    montant_total=montant_total,
                    client=client,
                    id_etat=2,
                )
                session.add(commande)
                session.flush()

                session.execute(
                    contient_association_table.insert().values(
                        id_commande=commande.id_commande,
                        id_produit=produit.id_produit,
                        quantite=quantite,
                    )
                )

                produit.stock -= quantite
                session.commit()
                print("Commande créée avec succès.")
            except SQLAlchemyError:
                session.rollback()
                raise
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def list_invoices():
    try:
        with Session(engine) as session:
            invoices = (
                session.query(Facture)
                .join(Facture.commande)
                .join(Commande.client)
                .order_by(Facture.id_facture)
                .all()
            )
            if not invoices:
                print("Aucune facture trouvée.")
            else:
                print("Liste des factures :")
                for facture in invoices:
                    commande = facture.commande
                    client = commande.client
                    print(
                        f"ID: {facture.id_facture}, Montant: {facture.montant_ttc}, "
                        f"Date: {facture.date_facture}, Commande: {commande.id_commande}, "
                        f"Client: {client.nom} {client.prenom}"
                    )
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def jointure_query():
    try:
        with Session(engine) as session:
            results = (
                session.query(
                    Client.nom,
                    Client.prenom,
                    func.count(Commande.id_commande).label("nb_commandes"),
                    func.sum(Commande.montant_total).label("total"),
                )
                .outerjoin(Client.commandes)
                .group_by(Client.id_client, Client.nom, Client.prenom)
                .order_by(func.sum(Commande.montant_total).desc())
                .all()
            )
            print("Requête avec jointure - Clients et leurs commandes :")
            for row in results:
                total = row.total if row.total is not None else 0
                print(
                    f"Client: {row.nom} {row.prenom}, "
                    f"Nb commandes: {row.nb_commandes}, Total: {total}"
                )
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def aggregation_query():
    try:
        with Session(engine) as session:
            results = (
                session.query(
                    Categorie_produit.nom_categorie,
                    func.sum(Produit.prix * contient_association_table.c.quantite).label(
                        "total_ventes"
                    ),
                )
                .join(Categorie_produit.produits)
                .join(
                    contient_association_table,
                    Produit.id_produit == contient_association_table.c.id_produit,
                )
                .group_by(
                    Categorie_produit.id_categorie_produit,
                    Categorie_produit.nom_categorie,
                )
                .order_by(
                    func.sum(Produit.prix * contient_association_table.c.quantite).desc()
                )
                .all()
            )
            print("Requête d'agrégation - Total des ventes par catégorie :")
            for row in results:
                print(f"Catégorie: {row.nom_categorie}, Total ventes: {row.total_ventes}")
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def main_menu():
    while True:
        print_menu("Menu principal - BoutikPro (ORM)")
        print("1. Lister les clients")
        print("2. Créer un client")
        print("3. Modifier un client")
        print("4. Supprimer un client")
        print("5. Lister les produits")
        print("6. Enregistrer une commande")
        print("7. Lister les factures")
        print("8. Requête avec jointure")
        print("9. Requête d'agrégation")
        print("0. Quitter")
        choice = input("Choix : ")

        if choice == "1":
            list_clients()
        elif choice == "2":
            create_client()
        elif choice == "3":
            update_client()
        elif choice == "4":
            delete_client()
        elif choice == "5":
            list_products()
        elif choice == "6":
            create_order()
        elif choice == "7":
            list_invoices()
        elif choice == "8":
            jointure_query()
        elif choice == "9":
            aggregation_query()
        elif choice == "0":
            break
        else:
            print("Choix invalide.")

        input("Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main_menu()
