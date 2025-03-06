import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App Titel
st.title("📊 Amazon Lagerbestands-Analyse Tool")
st.write("Lade die Lagerbestandsdatei hoch und erhalte umfassende Analysen zu Umsatz, Verkäufen, Lagerbewegungen und Retouren.")

# Datei-Upload
uploaded_file = st.file_uploader("📂 Lade deine Amazon Lagerbestands-Datei hoch (CSV oder Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Datei einlesen
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
    else:
        df = pd.read_excel(uploaded_file)
    
    st.subheader("🔍 Vorschau der Daten")
    st.dataframe(df.head())
    
    # Zeiträume auswählen
    zeitraum = st.selectbox("📅 Wähle den Zeitraum für die Analyse", [
        "Letzter Tag (gestern)", "In den letzten 3 Tagen", "In den letzten 7 Tagen", "In den letzten 14 Tagen",
        "Letzte 30 Tage", "In den letzten 90 Tagen", "In den letzten 180 Tagen", "In den letzten 365 Tagen"])
    
    # Umsatz- und Verkaufsanalyse
    st.subheader("💰 Umsatz- und Verkaufsanalyse")
    if "SKU" in df.columns and "quantity" in df.columns and "price" in df.columns:
        df['Gesamtumsatz'] = df['quantity'] * df['price']
        umsatz_sku = df.groupby("SKU")["Gesamtumsatz"].sum().sort_values(ascending=False)
        
        st.write("### Top 10 Produkte nach Umsatz")
        st.dataframe(umsatz_sku.head(10))
        
        # Umsatz-Visualisierung
        fig, ax = plt.subplots()
        umsatz_sku.head(10).plot(kind='bar', ax=ax)
        plt.xticks(rotation=45)
        plt.ylabel("Umsatz (€)")
        st.pyplot(fig)
    else:
        st.warning("Die Datei scheint nicht die erwarteten Spalten zu enthalten. Stelle sicher, dass die Spalten `SKU`, `quantity` und `price` vorhanden sind.")
    
    # Lagerbestandsanalyse
    st.subheader("📦 Lagerbestandsanalyse")
    if "SKU" in df.columns and "quantity" in df.columns:
        bestand_sku = df.groupby("SKU")["quantity"].sum().sort_values(ascending=False)
        st.write("### Lagerbestand pro Produkt")
        st.dataframe(bestand_sku.head(10))
        
        # Lagerbestand-Visualisierung
        fig, ax = plt.subplots()
        bestand_sku.head(10).plot(kind='bar', ax=ax)
        plt.xticks(rotation=45)
        plt.ylabel("Bestand (Einheiten)")
        st.pyplot(fig)
    
    # Retourenanalyse
    st.subheader("🔄 Retouren-Analyse")
    if "event_type" in df.columns and "quantity" in df.columns:
        retouren = df[df["event_type"].str.contains("Return", na=False)]
        retouren_sku = retouren.groupby("SKU")["quantity"].sum().sort_values(ascending=False)
        
        st.write("### Top 10 Produkte mit den meisten Retouren")
        st.dataframe(retouren_sku.head(10))
        
        # Retouren-Visualisierung
        fig, ax = plt.subplots()
        retouren_sku.head(10).plot(kind='bar', ax=ax)
        plt.xticks(rotation=45)
        plt.ylabel("Retouren (Einheiten)")
        st.pyplot(fig)
    else:
        st.warning("Keine Retouren-Daten gefunden.")
    
    # Export der Ergebnisse
    st.subheader("📤 Export")
    if st.button("Export als CSV"):
        df.to_csv("amazon_analysen_export.csv", index=False)
        st.success("Datei erfolgreich gespeichert: amazon_analysen_export.csv")

# GitHub Dateien erstellen
with open("requirements.txt", "w") as req_file:
    req_file.write("streamlit\npandas\nmatplotlib")

with open(".gitignore", "w") as gitignore:
    gitignore.write("__pycache__/\n*.csv\n*.xlsx\n.env")

with open("README.md", "w") as readme:
    readme.write("""
# Amazon Lagerbestands-Analyse Tool

Dieses Tool analysiert Amazon-Lagerbestandsberichte und bietet umfassende Einblicke in Verkäufe, Umsatz, Retouren und Lagerbestände.

## Installation
1. Python 3 installieren
2. Benötigte Pakete installieren:
   ```
   pip install -r requirements.txt
   ```
3. Das Tool starten:
   ```
   streamlit run app.py
   ```

## Nutzung
1. Amazon-Lagerbestandsbericht hochladen (CSV/Excel)
2. Analysezeitraum auswählen
3. Statistiken & Visualisierungen erhalten
4. Ergebnisse exportieren

""")
