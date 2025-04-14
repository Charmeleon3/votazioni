import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd

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
nome_votante = st.text_input("Nome Votante")
personaggio = st.text_input("Personaggio")

# Input voti
memicita = st.slider("Memicità", 1, 10)
impatto = st.slider("Impatto", 1, 10)
evoluzione = st.slider("Evoluzione", 1, 10)

# Bottone per inviare il voto
if st.button("Invia voto"):
    if nome_votante.strip() == "" or personaggio.strip() == "":
        st.warning("Per favore, compila anche Nome Votante e Personaggio.")
    else:
        # Aggiungi i voti al foglio di calcolo
        data = [nome_votante, personaggio, memicita, impatto, evoluzione]
        sheet.append_row(data)
        st.success("Voto inviato con successo!")

# Mostra il numero di voti raccolti
try:
    records = sheet.get_all_records()
    num_voti = len(records)
    st.write(f"Numero di voti ricevuti finora: {num_voti}")
except Exception as e:
    st.warning("⚠️ Impossibile recuperare il numero di voti. Controlla che il foglio non contenga celle con errori.")




st.write("---")  # separatore visivo
with st.expander("📊 Visualizza Classifica"):
    # Legge i dati dal secondo foglio o da un'area specifica del foglio
    try:
        # Opzione 1: se hai messo la classifica su un secondo foglio
        classifica_sheet = client.open("votazioni").worksheet("Classifica")
        classifica_data = classifica_sheet.get_all_values()
    except:
        # Opzione 2: se la classifica è nello stesso foglio in basso (es. da riga 100 in poi)
        classifica_data = sheet.get('G:L')  # cambia intervallo se serve

    # Converti in DataFrame e imposta intestazioni
    if classifica_data and len(classifica_data) > 1:
        headers = classifica_data[0]
        rows = classifica_data[1:]

        # Pulisci i dati: rimuovi righe con errori tipo #DIV/0!
        clean_rows = [
            row for row in rows
            if all(cell != '#DIV/0!' and cell != '' for cell in row)
        ]

        df = pd.DataFrame(clean_rows, columns=headers)

        # Converti colonne numeriche per sorting
        for col in ['Media Memicità', 'Media Impatto', 'Media Evoluzione', 'Punteggio Totale']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.sort_values(by='Totale', ascending=False).reset_index(drop=True)

        # Mostra tabella
        st.dataframe(df)
    else:
        st.info("La classifica non è ancora disponibile.")
