#%% md

#%% md

# Données Externes

#%% md

### Trends

#%%

# Installation des Librairies
import http.client
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from datetime import datetime
from pylab import rcParams
#%matplotlib inline
import http.client
import json
import re
from datetime import date
from sklearn.preprocessing import MinMaxScaler


#%%

#Exportation du dictionnaire de mots clés sur le immobilier Français et Arabe utilisé pour l'extraction des indices Trends
#Trends= pd.read_excel('./mubawab_immo_data/alternatives_data/google_trends/google_trends_immo_keywords_list.xlsx',engine="openpyxl")

#%%

### On extrait les données trends par keyword de 2000 à aujourd'hui puis on moyenne les trends pour obtenir un indice global
START_DATE = "2021-03-01"
END_DATE = "2021-04-01"
keyword_list=['AUTO HALL', 'AUTO NEJMA', 'BALIMA', 'BANK OF AFRICA', 'BCP', 'BMCI', 'CARTIER SAADA', 'CDM', 'CENTRALE DANONE', 'CIH', 'CIMENTS DU MAROC', 'COLORADO', 'COSUMAR', 'CTM', 'DARI COUSPATE', 'DELATTRE LEVIVIER MAROC', 'DELTA HOLDING', 'DIAC SALAF', 'DISWAY', 'DOUJA PROM ADDOHA', 'ENNAKL', 'EQDOM', 'FENIE BROSSETTE', 'HPS', 'IB MAROC.COM', 'IMMORENTE INVEST', 'INVOLYS', 'ITISSALAT AL-MAGHRIB', 'JET CONTRACTORS', 'LABEL VIE', 'LAFARGEHOLCIM MAR', 'LESIEUR CRISTAL', 'LYDEC', 'M2M Group', 'MAGHREB OXYGENE', 'MAGHREBAIL', 'MANAGEM', 'MAROC LEASING', 'MED PAPER', 'MICRODATA', 'MINIERE TOUISSIT', 'MUTANDIS SCA', 'NEXANS MAROC', 'OULMES', 'PROMOPHARM S.A.', 'REALISATIONS MECANIQUES', 'REBAB COMPANY', 'RES DAR SAADA', 'RISMA', 'S.M MONETIQUE', 'SAHAM ASSURANCE', 'SALAFIN', 'SAMIR', 'SMI', 'SNEP', 'SOCIETE DES BOISSONS DU MAROC', 'SODEP-Marsa Maroc', 'SONASID', 'SOTHEMA', 'STOKVIS NORD AFRIQUE', 'STROC INDUSTRIE', 'TAQA MOROCCO', 'TIMAR', 'TOTAL MAROC', 'UNIMER', 'WAFA ASSURANCE', 'ZELLIDJA S.A']
df = pd.DataFrame()
for keyword in keyword_list :
  try :
    conn = http.client.HTTPSConnection("google-trends-smt-media.azurewebsites.net")
    headers = {'cookie': "JSESSIONID=3828F17EDF7F5AF6A3FF67971BFF24F9",
               'content-type': "application/json"}
    body = {'word': keyword, "startdate": START_DATE,  "enddate": END_DATE,"region":"MA","resolution":"country"}
    payload = json.dumps(body,ensure_ascii=False).encode("utf-8")
    conn.request("POST", "/api/google-trends?code=JdFhjPzi5Xtqm0bLr6Dy7iwNmUrwsT0RDBWvoIhZ5VqYnk063AIfpQ%3D%3D", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))["default"]["timelineData"]
    if len(data_json)>0:
      for i in range(len(data_json)):
        data_json[i][keyword] = float(data_json[i]["value"][0])
        output_df = pd.DataFrame(data_json)
        output_df = output_df[['formattedAxisTime', keyword]]
        df['DATE'] = output_df['formattedAxisTime']
        df[keyword]= output_df[keyword]
  except:
    pass

df['Average']=df.loc[:,df.columns!='DATE'].mean(axis=1)
df.head()

#%%

#Transformer le format de la date sous la forme year-month
data_trends=df.copy()
data_trends["DATE"] =[datetime.strptime(i, '%b %d, %Y').strftime('%Y-%m') for i in data_trends["DATE"]]
data_trends.tail()

#%%

#Enregistrement de la donnée Trends
#data_trends.to_csv('./mubawab_immo_data/alternatives_data/google_trends/google_trends_immo_keywords_data.csv',index=False)
