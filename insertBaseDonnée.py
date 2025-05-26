import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

# 1. Insertion dans la table Hotel
hotels = [
    (1, 'Paris', 'France', 75001),
    (2, 'Lyon', 'France', 69002)
]
cursor.executemany(
    "INSERT OR IGNORE INTO Hotel (idHotel, ville, pays, codePostal) VALUES (?, ?, ?, ?)",
    hotels
)

# 2. Insertion dans la table Client
clients = [
    (1, '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
    (2, '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
    (3, '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
    (4, '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
    (5, '3 Rue des Fleurs', 'Nice', 60000, 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
]
cursor.executemany(
    "INSERT OR IGNORE INTO Client (idClient, adresse, ville, codePostal, email, numTelephone, nomComplet) VALUES (?, ?, ?, ?, ?, ?, ?)",
    clients
)

# 3. Insertion dans la table Prestation
prestations = [
    (1, 15, 'Petit-déjeuner'),
    (2, 30, 'Navette aéroport'),
    (3, 0, 'Wi-Fi gratuit'),
    (4, 50, 'Spa et bien-être'),
    (5, 20, 'Parking sécurisé')
]
cursor.executemany(
    "INSERT OR IGNORE INTO Prestation (idHotel, idPrestation, description) VALUES (?, ?, ?)",
    prestations
)

# 4. Insertion dans la table TypeChambre
types = [
    (1, 'Simple', 80),
    (2, 'Double', 120)
]
cursor.executemany(
    "INSERT OR IGNORE INTO TypeChambre (idType, nomType, Tarif) VALUES (?, ?, ?)",
    types
)

# 5. Insertion dans la table Chambre
chambres = [
    (1, 201, 2, 0, 1, 1),
    (2, 502, 5, 1, 1, 2),
    (3, 305, 3, 0, 2, 1),
    (4, 410, 4, 0, 2, 2),
    (5, 104, 1, 1, 2, 2),
    (6, 202, 2, 0, 1, 1),
    (7, 307, 3, 1, 1, 2),
    (8, 101, 1, 0, 1, 1)
]
cursor.executemany(
    "INSERT OR IGNORE INTO Chambre (idChambre, numero, etage, fumeurs, idHotel, idType) VALUES (?, ?, ?, ?, ?, ?)",
    chambres
)

# 6. Insertion dans la table Reservation
reservations = [
    (1, '2025-06-15', '2025-06-18', 1),
    (2, '2025-07-01', '2025-07-05', 2),
    (7, '2025-11-12', '2025-11-14', 2),
    (10, '2026-02-01', '2026-02-05', 2),
    (3, '2025-08-10', '2025-08-14', 3),
    (4, '2025-09-05', '2025-09-07', 4),
    (9, '2026-01-15', '2026-01-18', 4),
    (5, '2025-09-20', '2025-09-25', 5)
]
cursor.executemany(
    "INSERT OR IGNORE INTO Reservation (idReservation, dateDarrive, dateDepare, idClient) VALUES (?, ?, ?, ?)",
    reservations
)

# 7. Insertion dans la table Evaluation
evaluations = [
    (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1, 1),
    (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2, 1),
    (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3, 2),
    (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4, 2),
    (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5, 2)
]
cursor.executemany(
    "INSERT OR IGNORE INTO Evaluation (idEvaluation, dateEvaluation, note, texteDescriptif, idClient, idHotel) VALUES (?, ?, ?, ?, ?, ?)",
    evaluations
)


Hotel_Prestation = [
    (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1, 1),
    (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2, 1),
    (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3, 2),
    (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4, 2),
    (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5, 2)
]
cursor.executemany(
   "INSERT OR IGNORE INTO Hotel_Prestation (idHotel, idPrestation) VALUES (?, ?, ?, ?, ?, ?)",
    evaluations
)

Reservation_TypeChambre = [
    (1,1),
    (2,2),
    (7,2),
    (10,1),
    (3,1),
    (4,1),
    (9,2),
    (5,2)
]
cursor.executemany(
    "INSERT OR IGNORE INTO Reservation_TypeChambre (idReservation,idType) VALUES (?, ?, ?, ?, ?, ?)",
    evaluations
)



# Commit des transactions et fermeture de la connexion
conn.commit()
conn.close()

print("Les données ont été insérées avec succès dans les tables.")
