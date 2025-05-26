import streamlit as st
import sqlite3
from datetime import date, timedelta
import pandas as pd
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/jpg;base64,{encoded}");
             background-size: cover;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Appelle cette fonction avec le nom de ton image
add_bg_from_local("image.png")

# Connexion à la base
def get_conn():
    return sqlite3.connect("hotel.db", check_same_thread=False)

conn = get_conn()
cursor = conn.cursor()

# === Fonctions utilitaires ===
def afficher_clients():
    cursor.execute("SELECT * FROM Client")
    return cursor.fetchall()

def afficher_reservations():
    cursor.execute("""
    SELECT r.idReservation, c.nomComplet, r.dateDepare, r.dateDarrive
    FROM Reservation r
    JOIN Client c ON r.idClient = c.idClient
    
    """)
    return cursor.fetchall()


def ajouter_client(ville, adresse, codePostal, email, numTelephone, nomComplet):
    cursor.execute("""
        INSERT INTO Client (ville, adresse, codePostal, email, numTelephone, nomComplet) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ville, adresse, codePostal, email, numTelephone, nomComplet))
    conn.commit()
def ajouter_reservation(idReservation, dateDarrive,dateDepare,idClient):
    cursor.execute("INSERT INTO Reservation (idReservation, dateDarrive,dateDepare,idClient) VALUES (?, ?, ?, ?)",
                   (idReservation, dateDarrive,dateDepare,idClient))
    conn.commit()



# === Ajoutez cette nouvelle fonction ===
def afficher_chambres_disponibles(date_debut, date_fin):
    cursor.execute("""
        SELECT c.*
        FROM Chambre c
        WHERE c.idChambre NOT IN (
            SELECT con.idType
            FROM reservation_typechambre con
            JOIN Reservation r ON r.idReservation =  con.idReservation
            WHERE
                r.dateDepare >= ? AND r.dateDarrive <= ?
      
        )
    """, (str(date_debut), str(date_fin)))
    return cursor.fetchall()



# === Interface Streamlit ===
st.markdown("<h1 style='color: white;'>🏨 Gestion Des Réservations Des Hôtels</h1>", unsafe_allow_html=True)


menu = st.sidebar.selectbox("🛎️ Menu", ["Liste Réservations", "Liste Clients", "Chambres Disponibles", "Ajouter Client", "Ajouter Réservation"])

if menu == "Liste Réservations":
    st.subheader("📋 Liste des Réservations")
    data = afficher_reservations()
    df = pd.DataFrame(data, columns=["idReservation", "NomClient","dateDarrive","dateDepare"])
    st.dataframe(df.style.set_properties(**{
    'background-color': '#f0f0f0',
    'color': 'black',
    'border-color': 'gray',
}))

   





elif menu == "Liste Clients":
    st.subheader("👥 Liste des Clients")
    data = afficher_clients()
    df = pd.DataFrame(data, columns=["idClient", "adresse", "ville", "codePostal", "email", "numTelephone", "nomComple"])

    st.dataframe(df.style.set_properties(**{
        'background-color': '#f0f0f0',
        'color': 'black',
        'border-color': 'gray',
    }))







elif menu == "Ajouter Client":
    st.subheader("➕ Ajouter un Client")
    
    with st.form("client_form"):
        nomComplet = st.text_input("Nom complet*")
        numTelephone = st.text_input("Téléphone*", help="Format: +212612345678")
        email = st.text_input("Email*")
        ville = st.text_input("Ville*")
        codePostal = st.text_input("Code Postal*")
        adresse = st.text_input("Adresse*")
        submitted = st.form_submit_button("Enregistrer")
        
        if submitted:
            if not all([nomComplet, numTelephone, email, ville, codePostal, adresse]):
                # ✅ Message d'erreur personnalisé avec fond blanc
                st.markdown("""
                    <div style='background-color: white; padding: 10px; border: 1px solid red; color: red; border-radius: 5px;'>
                        <strong>❌ Tous les champs marqués d'un * sont obligatoires</strong>
                    </div>
                """, unsafe_allow_html=True)
            else:
                try:
                    ajouter_client(
                        ville, 
                        adresse, 
                        int(codePostal), 
                        email, 
                        numTelephone, 
                        nomComplet
                    )
                    st.success("Client enregistré avec succès!")
                except ValueError:
                    st.error("Le code postal doit être un nombre")
                except sqlite3.IntegrityError as e:
                    st.error(f"Erreur: {str(e)}")



# === Modifiez la section "Chambres Disponibles" comme suit ===
elif menu == "Chambres Disponibles":
    st.subheader("🛌 Chambres Disponibles")
    
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input("Date de début", value=date.today())
    with col2:
        date_fin = st.date_input("Date de fin", value=date.today() + timedelta(days=1))
    
    if date_fin <= date_debut:
        st.error("La date de fin doit être après la date de début")
    else:
        chambres = afficher_chambres_disponibles(date_debut, date_fin)
        if chambres:
            st.write(f"Chambres disponibles du {date_debut} au {date_fin}:")
            df = pd.DataFrame(chambres, columns=["idChambre", "numero", "etage","fumeurs", "idType", "idHotel"])
            st.dataframe(df)
        else:
            st.warning("Aucune chambre disponible pour cette période")





elif menu == "Ajouter Réservation":
    st.subheader("➕ Ajouter une Réservation")
    with st.form("reservation_form"):
        idReservation = st.text_input("ID Réservation*")
        clients = cursor.execute("SELECT idClient, nomComplet FROM Client").fetchall()
        client = st.selectbox("Client*", clients, format_func=lambda x: f"{x[0]} - {x[1]}")
        
        col1, col2 = st.columns(2)
        with col1:
            debut = st.date_input("Date d'arrivée*", value=date.today())
        with col2:
            fin = st.date_input("Date de départ*", value=date.today() + timedelta(days=1))
            
        submitted = st.form_submit_button("Enregistrer")
        
        if submitted:
            if fin <= debut:
                # ❌ Erreur personnalisée avec fond blanc
                st.markdown("""
                    <div style='background-color: white; padding: 10px; border: 1px solid red; color: red; border-radius: 5px;'>
                        <strong>❌ La date de départ doit être après la date d'arrivée</strong>
                    </div>
                """, unsafe_allow_html=True)
            else:
                try:
                    ajouter_reservation(
                        idReservation, 
                        str(debut), 
                        str(fin),
                        client[0]
                    )
                    st.success("Réservation enregistrée!")
                except sqlite3.IntegrityError:
                    # ❌ ID de réservation déjà existant — message personnalisé
                    st.markdown("""
                        <div style='background-color: white; padding: 10px; border: 1px solid red; color: red; border-radius: 5px;'>
                            <strong>❌ Cet ID de réservation existe déjà</strong>
                        </div>
                    """, unsafe_allow_html=True)






