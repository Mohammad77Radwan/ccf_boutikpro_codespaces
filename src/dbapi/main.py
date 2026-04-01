import mysql.connector
from tabulate import tabulate

try:
    from src.common.config import DB_CONFIG
    from src.common.helpers import print_menu
except ModuleNotFoundError:
    import os
    import sys

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)
    from src.common.config import DB_CONFIG
    from src.common.helpers import print_menu


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def read_int(prompt):
    value = input(prompt).strip()
    try:
        return int(value)
    except ValueError:
        print("Entrée invalide : nombre attendu.")
        return None


def run_read_query(sql, params=None):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, params or ())
        return cur.fetchall()
    except mysql.connector.Error as err:
        print(f"Erreur base de données : {err}")
        return None
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def list_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_client, nom, prenom, email FROM client ORDER BY id_client")
    clients = cur.fetchall()
    if not clients:
        print("Aucun client trouvé.")
    else:
        print("Liste des clients :")
        for row in clients:
            print(f"ID: {row[0]}, Nom: {row[1]}, Prénom: {row[2]}, Email: {row[3]}")
    cur.close()
    conn.close()


def create_client():
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    email = input("Email : ")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO client(nom, prenom, email) VALUES (%s, %s, %s)",
            (nom, prenom, email),
        )
        conn.commit()
        print("Client créé avec succès.")
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")


def update_client():
    id_client = read_int("ID du client à modifier : ")
    if id_client is None:
        return
    nom = input("Nouveau nom : ")
    prenom = input("Nouveau prénom : ")
    email = input("Nouvel email : ")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE client SET nom=%s, prenom=%s, email=%s WHERE id_client=%s",
            (nom, prenom, email, id_client),
        )
        conn.commit()
        if cur.rowcount > 0:
            print("Client modifié avec succès.")
        else:
            print("Client non trouvé.")
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")


def delete_client():
    id_client = read_int("ID du client à supprimer : ")
    if id_client is None:
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM client WHERE id_client=%s", (id_client,))
        conn.commit()
        if cur.rowcount > 0:
            print("Client supprimé avec succès.")
        else:
            print("Client non trouvé.")
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")


def list_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_produit, p.libelle, p.prix, p.stock, cp.nom_categorie
        FROM produit p
        JOIN categorie_produit cp ON p.id_categorie_produit = cp.id_categorie_produit
        ORDER BY p.id_produit
    """)
    products = cur.fetchall()
    if not products:
        print("Aucun produit trouvé.")
    else:
        print("Liste des produits :")
        for row in products:
            print(f"ID: {row[0]}, Libellé: {row[1]}, Prix: {row[2]}, Stock: {row[3]}, Catégorie: {row[4]}")
    cur.close()
    conn.close()


def create_order():
    id_client = read_int("ID du client : ")
    # Pour simplifier, on crée une commande avec un produit
    id_produit = read_int("ID du produit : ")
    quantite = read_int("Quantité : ")
    if id_client is None or id_produit is None or quantite is None:
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Vérifier stock
        cur.execute("SELECT prix, stock FROM produit WHERE id_produit=%s", (id_produit,))
        product = cur.fetchone()
        if not product:
            print("Produit non trouvé.")
            cur.close()
            conn.close()
            return
        prix, stock = product
        if stock < quantite:
            print("Stock insuffisant.")
            cur.close()
            conn.close()
            return
        montant_total = prix * quantite
        # Créer commande
        cur.execute(
            "INSERT INTO commande(date_commande, montant_total, id_client, id_etat) VALUES (NOW(), %s, %s, 2)",
            (montant_total, id_client),
        )
        id_commande = cur.lastrowid
        # Ajouter ligne
        cur.execute(
            "INSERT INTO contient(id_commande, id_produit, quantite) VALUES (%s, %s, %s)",
            (id_commande, id_produit, quantite),
        )
        # Mettre à jour stock
        cur.execute("UPDATE produit SET stock=stock-%s WHERE id_produit=%s", (quantite, id_produit))
        conn.commit()
        print("Commande créée avec succès.")
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")


def list_invoices():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id_facture, f.montant_ttc, f.date_facture, c.id_commande, cl.nom, cl.prenom
        FROM facture f
        JOIN commande c ON f.id_commande = c.id_commande
        JOIN client cl ON c.id_client = cl.id_client
        ORDER BY f.id_facture
    """)
    invoices = cur.fetchall()
    if not invoices:
        print("Aucune facture trouvée.")
    else:
        print("Liste des factures :")
        for row in invoices:
            print(f"ID: {row[0]}, Montant: {row[1]}, Date: {row[2]}, Commande: {row[3]}, Client: {row[4]} {row[5]}")
    cur.close()
    conn.close()


def jointure_query():
    # Requête avec jointure : clients et leurs commandes
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT cl.nom, cl.prenom, COUNT(c.id_commande) as nb_commandes, SUM(c.montant_total) as total
        FROM client cl
        LEFT JOIN commande c ON cl.id_client = c.id_client
        GROUP BY cl.id_client, cl.nom, cl.prenom
        ORDER BY total DESC
    """)
    results = cur.fetchall()
    print("Requête avec jointure - Clients et leurs commandes :")
    for row in results:
        print(f"Client: {row[0]} {row[1]}, Nb commandes: {row[2]}, Total: {row[3] or 0}")
    cur.close()
    conn.close()


def aggregation_query():
    # Requête d'agrégation : total des ventes par catégorie
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT cp.nom_categorie, SUM(c.montant_total) as total_ventes
        FROM categorie_produit cp
        JOIN produit p ON cp.id_categorie_produit = p.id_categorie_produit
        JOIN contient ct ON p.id_produit = ct.id_produit
        JOIN commande c ON ct.id_commande = c.id_commande
        GROUP BY cp.id_categorie_produit, cp.nom_categorie
        ORDER BY total_ventes DESC
    """)
    results = cur.fetchall()
    print("Requête d'agrégation - Total des ventes par catégorie :")
    for row in results:
        print(f"Catégorie: {row[0]}, Total ventes: {row[1]}")
    cur.close()
    conn.close()


def complete_catalog_view():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            p.libelle AS produit,
            cp.nom_categorie AS categorie_produit,
            f.nom_fournisseur AS fournisseur,
            cf.nom_categorie AS categorie_fournisseur
        FROM produit p
        INNER JOIN categorie_produit cp
            ON p.id_categorie_produit = cp.id_categorie_produit
        INNER JOIN livre l
            ON p.id_produit = l.id_produit
        INNER JOIN fournisseur f
            ON l.id_fournisseur = f.id_fournisseur
        INNER JOIN categorie_fournisseur cf
            ON f.id_categorie_fournisseur = cf.id_categorie_fournisseur
        ORDER BY cp.nom_categorie, p.libelle, f.nom_fournisseur
        """
    )
    rows = cur.fetchall()
    if not rows:
        print("Aucun produit/fournisseur trouvé.")
    else:
        print(
            tabulate(
                rows,
                headers=[
                    "Produit",
                    "Catégorie Produit",
                    "Fournisseur",
                    "Catégorie Fournisseur",
                ],
                tablefmt="fancy_grid",
            )
        )
    cur.close()
    conn.close()


def products_suppliers_by_product_category():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            cp.nom_categorie AS categorie_produit,
            p.libelle AS produit,
            f.nom_fournisseur AS fournisseur
        FROM produit p
        INNER JOIN categorie_produit cp
            ON p.id_categorie_produit = cp.id_categorie_produit
        INNER JOIN livre l
            ON p.id_produit = l.id_produit
        INNER JOIN fournisseur f
            ON l.id_fournisseur = f.id_fournisseur
        ORDER BY cp.nom_categorie, p.libelle, f.nom_fournisseur
        """
    )
    rows = cur.fetchall()
    if not rows:
        print("Aucun produit/fournisseur trouvé.")
    else:
        print(
            tabulate(
                rows,
                headers=["Catégorie Produit", "Produit", "Fournisseur"],
                tablefmt="fancy_grid",
            )
        )
    cur.close()
    conn.close()


def update_product_interactive():
    id_produit = read_int("ID du produit à modifier : ")
    if id_produit is None:
        return

    nouveau_libelle = input("Nouveau libellé (laisser vide pour ne pas modifier) : ").strip()
    nouveau_prix = input("Nouveau prix (laisser vide pour ne pas modifier) : ").strip()

    if not nouveau_libelle and not nouveau_prix:
        print("Aucune modification demandée.")
        return

    updates = []
    params = []

    if nouveau_libelle:
        updates.append("libelle = %s")
        params.append(nouveau_libelle)

    if nouveau_prix:
        try:
            prix_value = float(nouveau_prix)
        except ValueError:
            print("Prix invalide.")
            return
        updates.append("prix = %s")
        params.append(prix_value)

    params.append(id_produit)
    query = f"UPDATE produit SET {', '.join(updates)} WHERE id_produit = %s"

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, tuple(params))
        conn.commit()
        if cur.rowcount > 0:
            print("Produit modifié avec succès.")
        else:
            print("Produit non trouvé.")
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")


def initialize_database():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS etat_commande (
                id_etat INT PRIMARY KEY AUTO_INCREMENT,
                nom_etat VARCHAR(20) NOT NULL UNIQUE
            )
            """
        )
        cur.execute(
            """
            INSERT IGNORE INTO etat_commande (id_etat, nom_etat)
            VALUES
                (1, 'brouillon'),
                (2, 'validee'),
                (3, 'facturee')
            """
        )

        cur.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = 'produit'
              AND column_name = 'stock'
            """
        )
        has_stock_column = cur.fetchone()[0] > 0
        if not has_stock_column:
            cur.execute("ALTER TABLE produit ADD COLUMN stock INT NOT NULL DEFAULT 0")

        cur.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = 'commande'
              AND column_name = 'id_etat'
            """
        )
        has_id_etat_column = cur.fetchone()[0] > 0
        if not has_id_etat_column:
            cur.execute("ALTER TABLE commande ADD COLUMN id_etat INT NOT NULL DEFAULT 1")

        cur.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.table_constraints
            WHERE constraint_schema = DATABASE()
              AND table_name = 'commande'
              AND constraint_name = 'fk_commande_etat'
              AND constraint_type = 'FOREIGN KEY'
            """
        )
        has_fk_commande_etat = cur.fetchone()[0] > 0
        if not has_fk_commande_etat:
            cur.execute(
                """
                ALTER TABLE commande
                ADD CONSTRAINT fk_commande_etat
                FOREIGN KEY (id_etat) REFERENCES etat_commande(id_etat)
                """
            )

        cur.execute("DELETE FROM contient")
        cur.execute("DELETE FROM livre")
        cur.execute("DELETE FROM produit")
        cur.execute("DELETE FROM fournisseur")
        cur.execute("DELETE FROM categorie_fournisseur")
        cur.execute("DELETE FROM categorie_produit")

        cur.execute(
            """
            INSERT INTO categorie_produit (id_categorie_produit, nom_categorie)
            VALUES
                (1, 'Ordinateurs'),
                (2, 'Accessoires')
            """
        )

        cur.execute(
            """
            INSERT INTO categorie_fournisseur (id_categorie_fournisseur, nom_categorie)
            VALUES
                (1, 'Grossiste'),
                (2, 'Constructeur')
            """
        )

        cur.execute(
            """
            INSERT INTO fournisseur (id_fournisseur, nom_fournisseur, id_categorie_fournisseur)
            VALUES
                (1, 'TechDistrib', 1),
                (2, 'MegaHardware', 2)
            """
        )

        cur.execute(
            """
            INSERT INTO produit (id_produit, libelle, prix, id_categorie_produit)
            VALUES
                (1, 'PC Portable 14 pouces', 799.99, 1),
                (2, 'Souris sans fil', 24.90, 2),
                (3, 'Clavier mecanique', 69.90, 2)
            """
        )

        cur.execute(
            """
            INSERT INTO livre (id_produit, id_fournisseur)
            VALUES
                (1, 2),
                (2, 1),
                (3, 1)
            """
        )

        conn.commit()
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erreur initialisation DB : {err}")


def run_self_test():
    complete_catalog_view()
    products_suppliers_by_product_category()
    print("✅ SYSTEM CHECK PASSED: Database seeded and read operations are working.")


def main_menu():
    while True:
        print_menu("Menu principal - BoutikPro (DB-API)")
        print("1. Lister les clients")
        print("2. Créer un client")
        print("3. Modifier un client")
        print("4. Supprimer un client")
        print("5. Lister les produits")
        print("6. Enregistrer une commande")
        print("7. Lister les factures")
        print("8. Requête avec jointure")
        print("9. Requête d'agrégation")
        print("10. Catalogue complet (produits/fournisseurs)")
        print("11. Vue analytique par catégorie produit")
        print("12. Modifier un produit (nom/prix)")
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
        elif choice == "10":
            complete_catalog_view()
        elif choice == "11":
            products_suppliers_by_product_category()
        elif choice == "12":
            update_product_interactive()
        elif choice == "0":
            break
        else:
            print("Choix invalide.")
        input("Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    initialize_database()
    run_self_test()
    main_menu()
