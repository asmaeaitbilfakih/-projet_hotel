import sqlite3

try:
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # 1. Table Hotel
    cursor.execute('''
    create table Hotel (
        idHotel INT primary key ,
        ville varchar(50) ,
        pays varchar(50),
        codePostal INT
    )
    ''')

    # 2. Table Client
    cursor.execute('''
    CREATE TABLE Client (
        idClient INT PRIMARY KEY,
        ville VARCHAR(50),
        adresse VARCHAR(100),
        codePostal INT,
        email VARCHAR(100),
        numTelephone VARCHAR(15),
        nomComplet VARCHAR(100)
    )
    ''')

    # 3. Table TypeChambre
    cursor.execute('''
    CREATE TABLE TypeChambre (
        idType INT PRIMARY KEY,
        nomType VARCHAR(50),
        Tarif FLOAT
    )
    ''')

    # 4. Table Chambre
    cursor.execute('''
    CREATE TABLE Chambre (
        idChambre INT PRIMARY KEY,
        numero INT,
        etage INT,
        fumeurs BOOLEAN,
        idHotel INT,
        idType INT,
        FOREIGN KEY (idHotel) REFERENCES Hotel(idHotel),
        FOREIGN KEY (idType) REFERENCES TypeChambre(idType)
    )
    ''')

    # 5. Table Reservation
    cursor.execute('''
    CREATE TABLE Reservation (
        idReservation INT PRIMARY KEY,
        dateDarrive DATE,
        dateDepare DATE,
        idClient INT,
        FOREIGN KEY (idClient) REFERENCES Client(idClient)
    )
    ''')

    # 7. Table Evaluation
    cursor.execute('''
    CREATE TABLE Evaluation (
        idEvaluation INT PRIMARY KEY,
        dateEvaluation DATE,
        note INT,
        texteDescriptif TEXT,
        idClient INT,
        idHotel INT,
        FOREIGN KEY (idClient) REFERENCES Client(idClient),
        FOREIGN KEY (idHotel) REFERENCES Chambre(idHotel)
    )
    ''')

    # 6. Table Hotel_Prestation
    cursor.execute('''
    CREATE TABLE Prestation (
          idHotel INT,
          idPrestation INT,
           description VARCHAR
    )
    ''')

    # 6. (doublon) Table Hotel_Prestation encore une fois
    cursor.execute('''
    CREATE TABLE Hotel_Prestation (
        idHotel INT,
        idPrestation INT,
        PRIMARY KEY (idHotel, idPrestation),
        FOREIGN KEY (idHotel) REFERENCES Hotel(idHotel),
        FOREIGN KEY (idPrestation) REFERENCES Prestation(idPrestation)
    )
    ''')

    # Table Reservation_TypeChambre
    cursor.execute('''
    CREATE TABLE Reservation_TypeChambre (
        idReservation INT,
        idType INT,
        PRIMARY KEY (idReservation, idType),
        FOREIGN KEY (idReservation) REFERENCES Reservation(idReservation),
        FOREIGN KEY (idType) REFERENCES TypeChambre(idType)
    )
    ''')

    # Enregistrer les modifications
    conn.commit()
    print("Base de données et tables créées avec succès.")

except Exception as e:
    print(f"Une erreur est survenue : {e}")

finally:
    # Fermer la connexion même en cas d'erreur
    conn.close()
