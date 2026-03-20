-- Modifications apportées par l'étudiant
-- 1. Ajouter telephone à client
ALTER TABLE client ADD COLUMN telephone VARCHAR(20);

-- 2. Ajouter stock à produit
ALTER TABLE produit ADD COLUMN stock INT NOT NULL DEFAULT 0;

-- 3. Ajouter une structure de suivi d'état de commande
-- Créer une table pour les états de commande
DROP TABLE IF EXISTS etat_commande;
CREATE TABLE etat_commande (
  id_etat INT PRIMARY KEY AUTO_INCREMENT,
  nom_etat VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO etat_commande (nom_etat) VALUES ('brouillon'), ('validee'), ('facturee');

-- Ajouter la colonne etat à commande
ALTER TABLE commande ADD COLUMN id_etat INT NOT NULL DEFAULT 1;
ALTER TABLE commande ADD CONSTRAINT fk_commande_etat FOREIGN KEY (id_etat) REFERENCES etat_commande(id_etat);

-- Mettre à jour les données existantes
UPDATE client SET telephone = '01 23 45 67 89' WHERE id_client = 1;
UPDATE client SET telephone = '01 98 76 54 32' WHERE id_client = 2;
UPDATE client SET telephone = '01 11 22 33 44' WHERE id_client = 3;

UPDATE produit SET stock = 10 WHERE id_produit = 1;
UPDATE produit SET stock = 50 WHERE id_produit = 2;
UPDATE produit SET stock = 30 WHERE id_produit = 3;

-- Les commandes existantes sont déjà facturées, donc état 'facturee'
UPDATE commande SET id_etat = 3;

-- 4. Tester les modifications
-- Les tests seront effectués via les scripts et l'application Python
