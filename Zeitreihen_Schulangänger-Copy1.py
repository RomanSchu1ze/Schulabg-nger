#!/usr/bin/env python
# coding: utf-8

# ### Erstellung Datensatz: Schulabgänger nach Schultyp & Geschlecht auf Kreisebene 1995-2019

# **Anmerkungen:** <br>
# Daten finden sich auf der Regionaldatenbank des statistischen Bundesamtes.<br>
# 
# **Tabellebezeichnung**:<br>
# 21111-02-06-4-B:<br>
# Absolventen/Abgänger allgemeinbildender Schulen nach Geschlecht und Abschlussarten - Schuljahr - regionale Ebenen <br>
# 
# **Link zur Datenquelle:**<br> https://www.regionalstatistik.de/genesis//online?operation=table&code=21111-02-06-4-B&bypass=true&levelindex=1&levelid=1631709824822#abreadcrumb

# In[63]:


# Bibliotheken importieren
import pandas as pd
import numpy as np


# In[64]:


# Dateien
files = ["21111-02-06-4-B-95-01.csv", "21111-02-06-4-B-02-08.csv", 
         "21111-02-06-4-B-09-12.csv", "21111-02-06-4-13-19.csv"]


# In[65]:


# definiere Spaltennamen
columns = ["Jahr", "Regio-Schlüssel", "Kreise und kreisfreie Stadt", 
           "Schulabgänger insgesamt", "Schulabgänger insgesamt weiblich", 
           "Schulabgänger ohne Abschluss",  "Schulabgänger ohne Abschluss weiblich", 
           "Schulabgänger Hauptschulabschluss",  "Schulabgänger Hauptschulabschluss weiblich",            
           "Schulabgänger Realschulabschluss", "Schulabgänger Realschulabschluss weiblich", 
           "dar. schulischer Teil der Fachhochschulreife", "dar. schulischer Teil der Fachhochschulreife weiblich",  
           "mit Fachhochschulreife", "mit Fachhochschulreife weiblich",
           "mit allgemeiner Hochschulreife", "mit allgemeiner Hochschulreife weiblich"]


# In[66]:


# Bereinigung der Daten 
def clean_data(df):
    # replace certain strings with NA´s
    for element in ("-", ".", "x"):
        df.replace(element, np.nan, inplace=True)
    # convert relevant columns of object dtypes to float64
    for col in df.columns:
        if col not in ["Jahr", "Regio-Schlüssel", "Kreise und kreisfreie Stadt"]:
        # convert columns of object dtype to float
            df[col] = df[col].astype("float64")
    # return final dataframe
    return df


# In[67]:


# leere Liste um Datensätze zu speichern
l=[]


# In[68]:


for file in files:
    
    # Daten einlesen
    df = pd.read_csv(f"Schulabgänger Zeitreihe/{file}", sep=";", skiprows=7, encoding= "unicode_escape")

    # Spaltennamen in dataframe einfügen
    df.columns = columns
    
    # Entferne Zeilen bei denen die Kreisschlüssel Missings enthalten
    df = df[df["Regio-Schlüssel"].notna()]
    
    # Bereinigung der Daten
    df = clean_data(df)
    
    # Aggregat (Fach-)Hochschulreife insgesamt
    df["Schulabgänger (Fach-)Hochschulreife"] =     df["mit Fachhochschulreife"].fillna(0) +     df["mit allgemeiner Hochschulreife"].fillna(0)
    
    # Aggregat (Fach-)Hochschulreife weiblich
    df["Schulabgänger (Fach-)Hochschulreife weiblich"] =     df["mit Fachhochschulreife weiblich"].fillna(0) +     df["mit allgemeiner Hochschulreife weiblich"].fillna(0)
    
    # Schulabgänger ingesamt
    df["Schulabgänger insgesamt männlich"] =     df["Schulabgänger insgesamt"] -     df["Schulabgänger insgesamt weiblich"]
    
    # Schulabgänger ohne Abschluss
    df["Schulabgänger ohne Abschluss männlich"] =     df["Schulabgänger ohne Abschluss"] -     df["Schulabgänger ohne Abschluss weiblich"]
    
    # Schulabgänger Hauptschule
    df["Schulabgänger Hauptschulabschluss männlich"] =     df["Schulabgänger Hauptschulabschluss"] -      df["Schulabgänger Hauptschulabschluss weiblich"]
    
    # Schulabgänger Realschule
    df["Schulabgänger Realschulabschluss männlich"] =     df["Schulabgänger Realschulabschluss"] -     df["Schulabgänger Realschulabschluss weiblich"]
    
    # Schulabgänger (Fach-)Hochschulreife
    df["Schulabgänger (Fach-)Hochschulreife männlich"] =    df["Schulabgänger (Fach-)Hochschulreife"] -     df["Schulabgänger (Fach-)Hochschulreife weiblich"] 
    
    # Entfernen überflüssiger Spalten
    cols = [11, 12, 13, 14, 15, 16]
    df.drop(df.columns[cols], axis=1, inplace=True)
    
    # liste mit Daten füllen
    l.append(df)                    


# In[69]:


# Individuelle Dataframes aus Liste zusammenführen (1995-2019)
data=pd.concat(l)


# In[70]:


# Spaltenanordnung anpassen
columns = ["Jahr", "Regio-Schlüssel", "Kreise und kreisfreie Stadt",
           "Schulabgänger insgesamt", "Schulabgänger insgesamt männlich", "Schulabgänger insgesamt weiblich",
           "Schulabgänger ohne Abschluss", "Schulabgänger ohne Abschluss männlich", "Schulabgänger ohne Abschluss weiblich",
           "Schulabgänger Hauptschulabschluss", "Schulabgänger Hauptschulabschluss männlich", "Schulabgänger Hauptschulabschluss weiblich",
           "Schulabgänger Realschulabschluss", "Schulabgänger Realschulabschluss männlich", "Schulabgänger Realschulabschluss weiblich",
           "Schulabgänger (Fach-)Hochschulreife", "Schulabgänger (Fach-)Hochschulreife männlich", "Schulabgänger (Fach-)Hochschulreife weiblich",
]


# In[71]:


# Saplten sortieren
data = data[columns]


# In[89]:


# erste fünf Zeilen
data.head()


# #### BA-Beschäftigtendaten aus Q3 2020 einlesen, um relevante Kreise zu identifizieren

# In[73]:


# Beschäftigten Daten von der Bundesagentur einlesen, um relevante Kreise zu identifizieren
df_ba = pd.read_csv("Schulabgänger Zeitreihe/202009_Besch_Kreise.csv", 
                    sep=";",
                    names=["Datum", "Kreis", "Berufe ID","SVB", "AGB", "X"], 
                    header=None)


# In[74]:


# Identifikation der individuellen Kreis-Schlüssel
Kreise = df_ba["Kreis"].unique()


# In[75]:


# identifiziere nur relevante Kreise
mask = data["Regio-Schlüssel"].isin(Kreise)


# In[76]:


# filtere nur relevante Kreise
df_Kreise = data[mask]


# In[77]:


# Sortierung der Daten
df_Kreise = df_Kreise.sort_values(by=["Jahr", "Regio-Schlüssel"])


# In[78]:


# Format der Daten
df_Kreise[df_Kreise["Jahr"] == "2019"].shape


# In[79]:


# Prüfung, ob Kreise fehlen
print("Unique values in Kreise that are not in the final dataframe:")
print(np.setdiff1d(np.sort(Kreise), df_Kreise["Regio-Schlüssel"].unique()))


# In[80]:


# als Excel speichern
df_Kreise.to_excel("Schulabgänger Zeitreihe/Schulabgänger_Kreise_Roh_1995-2019.xlsx", index=False)


# #### Konvertierung von Schulform-Spalten in Zeilen

# In[81]:


# Konvertiere Schulformspalten in Zeilen, Label der Spalte: Schulform
final = df_Kreise.melt(id_vars=["Jahr", "Regio-Schlüssel", "Kreise und kreisfreie Stadt"], 
        var_name="Schulform", value_name="Anzahl")


# In[82]:


# erste fünf Zeilen
final.head()


# In[83]:


# Sortierung der Daten
final = final.sort_values(by=["Jahr", "Regio-Schlüssel", "Schulform"])


# In[84]:


#final.Anzahl = final.Anzahl.replace(0, np.nan)


# In[85]:


# Anzahl der fehlenden Werte (->Göttingen 2013-2016)
final["Anzahl"].isna().sum()


# In[86]:


# Anzahl der fehlenden Werte (->Göttingen 2013-2016)
final[final["Schulform"] == "Schulabgänger insgesamt"]["Anzahl"].isna().sum()


# In[87]:


# individuelle Jahreswerte
final.Jahr.unique()


# In[88]:


# Als Excel speichern
final.to_excel("Schulabgänger Zeitreihe/Schulabgänger_Kreise_1995-2019.xlsx", index=False)

