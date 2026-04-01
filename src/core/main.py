from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.common.helpers import print_menu

engine = create_engine("mysql+pymysql://student:studentpwd@db:3306/boutikpro_ccf")


def list_clients():
    try:
        with engine.connect() as conn:
            clients = conn.execute(
                text(
                    """
                    SELECT id_client, nom, prenom, email
                    FROM client
                    ORDER BY id_client
                    """
                )
            ).fetchall()
            if not clients:
                print("Aucun client trouvé.")
            else:
                print("Liste des clients :")
                for row in clients:
                    print(
                        f"ID: {row.id_client}, Nom: {row.nom}, "
                        f"Prénom: {row.prenom}, Email: {row.email}"
                    )
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def create_client():
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    email = input("Email : ")
    try:
        with engine.connect() as conn:
            try:
                conn.execute(
                    text(
                        """
                        INSERT INTO client(nom, prenom, email)
                        VALUES (:nom, :prenom, :email)
                        """
                    ),
                    {"nom": nom, "prenom": prenom, "email": email},
                )
                conn.commit()
                print("Client créé avec succès.")
            except SQLAlchemyError:
                conn.rollback()
                raise
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def update_client():
    id_client = int(input("ID du client à modifier : "))
    nom = input("Nouveau nom : ")
    prenom = input("Nouveau prénom : ")
    email = input("Nouvel email : ")
    try:
        with engine.connect() as conn:
            try:
                result = conn.execute(
                    text(
                        """
                        UPDATE client
                        SET nom = :nom, prenom = :prenom, email = :email
                        WHERE id_client = :id_client
                        """
                    ),
                    {
                        "id_client": id_client,
                        "nom": nom,
                        "prenom": prenom,
                        "email": email,
                    },
                )
                conn.commit()
                if result.rowcount > 0:
                    print("Client modifié avec succès.")
                else:
                    print("Client non trouvé.")
            except SQLAlchemyError:
                conn.rollback()
                raise
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def delete_client():
    id_client = int(input("ID du client à supprimer : "))
    try:
        with engine.connect() as conn:
            try:
                result = conn.execute(
                    text("DELETE FROM client WHERE id_client = :id_client"),
                    {"id_client": id_client},
                )
                conn.commit()
                if result.rowcount > 0:
                    print("Client supprimé avec succès.")
                else:
                    print("Client non trouvé.")
            except SQLAlchemyError:
                conn.rollback()
                raise
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def list_products():
    try:
        with engine.connect() as conn:
            products = conn.execute(
                text(
                    """
                    SELECT p.id_produit, p.libelle, p.prix, p.stock, cp.nom_categorie
                    FROM produit p
                    JOIN categorie_produit cp ON p.id_categorie_produit = cp.id_categorie_produit
                    ORDER BY p.id_produit
                    """
                )
            ).fetchall()
            if not products:
                print("Aucun produit trouvé.")
            else:
                print("Liste des produits :")
                for row in products:
                    print(
                        f"ID: {row.id_produit}, Libellé: {row.libelle}, "
                        f"Prix: {row.prix}, Stock: {row.stock}, "
                        f"Catégorie: {row.nom_categorie}"
                    )
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def create_order():
    id_client = int(input("ID du client : "))
    id_produit = int(input("ID du produit : "))
    quantite = int(input("Quantité : "))
    try:
        with engine.connect() as conn:
            try:
                client = conn.execute(
                    text("SELECT id_client FROM client WHERE id_client = :id_client"),
                    {"id_client": id_client},
                ).fetchone()
                if client is None:
                    print("Client non trouvé.")
                    return

                product = conn.execute(
                    text(
                        """
                        SELECT prix, stock
                        FROM produit
                        WHERE id_produit = :id_produit
                        """
                    ),
                    {"id_produit": id_produit},
                ).fetchone()
                if product is None:
                    print("Produit non trouvé.")
                    return

                if product.stock < quantite:
                    print("Stock insuffisant.")
                    return

                montant_total = product.prix * quantite
                conn.execute(
                    text(
                        """
                        INSERT INTO commande(date_commande, montant_total, id_client, id_etat)
                        VALUES (NOW(), :montant_total, :id_client, 2)
                        """
                    ),
                    {"montant_total": montant_total, "id_client": id_client},
                )

                id_commande = conn.execute(text("SELECT LAST_INSERT_ID() AS id_commande")).scalar_one()

                conn.execute(
                    text(
                        """
                        INSERT INTO contient(id_commande, id_produit, quantite)
                        VALUES (:id_commande, :id_produit, :quantite)
                        """
                    ),
                    {
                        "id_commande": id_commande,
                        "id_produit": id_produit,
                        "quantite": quantite,
                    },
                )

                conn.execute(
                    text(
                        """
                        UPDATE produit
                        SET stock = stock - :quantite
                        WHERE id_produit = :id_produit
                        """
                    ),
                    {"quantite": quantite, "id_produit": id_produit},
                )

                conn.commit()
                print("Commande créée avec succès.")
            except SQLAlchemyError:
                conn.rollback()
                raise
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def list_invoices():
    try:
        with engine.connect() as conn:
            invoices = conn.execute(
                text(
                    """
                    SELECT f.id_facture, f.montant_ttc, f.date_facture,
                           c.id_commande, cl.nom, cl.prenom
                    FROM facture f
                    JOIN commande c ON f.id_commande = c.id_commande
                    JOIN client cl ON c.id_client = cl.id_client
                    ORDER BY f.id_facture
                    """
                )
            ).fetchall()
            if not invoices:
                print("Aucune facture trouvée.")
            else:
                print("Liste des factures :")
                for row in invoices:
                    print(
                        f"ID: {row.id_facture}, Montant: {row.montant_ttc}, "
                        f"Date: {row.date_facture}, Commande: {row.id_commande}, "
                        f"Client: {row.nom} {row.prenom}"
                    )
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def jointure_query():
    try:
        with engine.connect() as conn:
            results = conn.execute(
                text(
                    """
                    SELECT cl.nom, cl.prenom,
                           COUNT(c.id_commande) AS nb_commandes,
                           SUM(c.montant_total) AS total
                    FROM client cl
                    LEFT JOIN commande c ON cl.id_client = c.id_client
                    GROUP BY cl.id_client, cl.nom, cl.prenom
                    ORDER BY total DESC
                    """
                )
            ).fetchall()
            print("Requête avec jointure - Clients et leurs commandes :")
            for row in results:
                print(
                    f"Client: {row.nom} {row.prenom}, "
                    f"Nb commandes: {row.nb_commandes}, Total: {row.total or 0}"
                )
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def aggregation_query():
    try:
        with engine.connect() as conn:
            results = conn.execute(
                text(
                    """
                    SELECT cp.nom_categorie,
                           SUM(p.prix * ct.quantite) AS total_ventes
                    FROM categorie_produit cp
                    JOIN produit p ON cp.id_categorie_produit = p.id_categorie_produit
                    JOIN contient ct ON p.id_produit = ct.id_produit
                    GROUP BY cp.id_categorie_produit, cp.nom_categorie
                    ORDER BY total_ventes DESC
                    """
                )
            ).fetchall()
            print("Requête d'agrégation - Total des ventes par catégorie :")
            for row in results:
                print(f"Catégorie: {row.nom_categorie}, Total ventes: {row.total_ventes}")
    except SQLAlchemyError as err:
        print(f"Erreur : {err}")


def main_menu():
    while True:
        print_menu("Menu principal - BoutikPro (Core)")
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
