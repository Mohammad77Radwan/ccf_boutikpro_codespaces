import mysql.connector
from src.common.config import DB_CONFIG
from src.common.helpers import print_menu


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


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
    id_client = int(input("ID du client à modifier : "))
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
    id_client = int(input("ID du client à supprimer : "))
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
    id_client = int(input("ID du client : "))
    # Pour simplifier, on crée une commande avec un produit
    id_produit = int(input("ID du produit : "))
    quantite = int(input("Quantité : "))
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
