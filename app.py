import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Autenticazione con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_info = json.loads(st.secrets["GCP_CREDENTIALS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
client = gspread.authorize(creds)
sheet = client.open("votazioni").sheet1

# Titolo dell'app
st.title("Votazione Anonima")

st.write("Inserisci i seguenti dati per votare:")

# Nuovi campi testuali
nome = st.text_input("Nome")
personaggio = st.text_input("Personaggio")

# Input voti
memicita = st.slider("Memicità", 1, 10)
impatto = st.slider("Impatto", 1, 10)
evoluzione = st.slider("Evoluzione", 1, 10)

# Bottone per inviare il voto
if st.button("Invia voto"):
    if nome.strip() == "" or personaggio.strip() == "":
        st.warning("Per favore, compila anche Nome e Personaggio.")
    else:
        # Aggiungi i voti al foglio di calcolo
        data = [nome, personaggio, memicita, impatto, evoluzione]
        sheet.append_row(data)
        st.success("Voto inviato con successo!")

# Mostra il numero di voti raccolti
num_voti = len(sheet.get_all_records())
st.write(f"Numero di voti ricevuti finora: {num_voti}")
