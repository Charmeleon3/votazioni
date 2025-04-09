import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autenticazione con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\LucarioNervi\\Desktop\\progetto2 API\\credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("votazioni").sheet1

# Titolo dell'app
st.title("Votazione Anonima")

st.write("Vota su questi tre parametri da 1 a 10:")

# Input voti
memicita = st.slider("Memicità", 1, 10)
impatto = st.slider("Impatto", 1, 10)
evoluzione = st.slider("Evoluzione", 1, 10)

# Bottone per inviare il voto
if st.button("Invia voto"):
    # Aggiungi i voti al foglio di calcolo
    data = [memicita, impatto, evoluzione]
    sheet.append_row(data)
    st.success("Voto inviato con successo!")

# Mostra il numero di voti raccolti
num_voti = len(sheet.get_all_records())
st.write(f"Numero di voti ricevuti finora: {num_voti}")
