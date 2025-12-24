# scrapingweb
# 📊 Analisi Dati: MyDramaList BL Top Rated

Questo progetto contiene un'analisi approfondita di un dataset contenente i drama **Boys' Love (BL)** più votati su MyDramaList.
L'obiettivo è esplorare trend temporali, differenze geografiche (Thailandia vs Giappone) e previsioni di rating tramite Machine Learning.

## 📂 Struttura del Dataset

Il progetto utilizza due file principali:
1.  **`mdl_bl_top_rated.csv`**: Il file originale (grezzo).
2.  **`mdl_bl_top_rated_finale.csv`**: Il file pulito e processato.

### Processo di Pulizia (Data Cleaning)
Il dataset originale presentava una colonna `year` "sporca" contenente informazioni miste. È stato creato uno script per:
* Estrarre il **Paese** (es. Thai, Japanese).
* Estrarre il **Tipo** (es. Drama, Special).
* Estrarre l'**Anno di Rilascio**.
* Estrarre il **Numero di Episodi**.
* Reimpostare il **Rank** da 1.

Analisi Effettuate
Il progetto si divide in diverse fasi di analisi:

1. Analisi Geografica e Quantitativa
Dominio del Mercato: La Thailandia è il produttore principale per volume (quantità).

Confronto Qualità: Il Giappone, pur producendo meno titoli, mantiene una media voti (Rating) significativamente più alta e costante.

Distribuzione (KDE Plot): Analisi della densità dei voti che mostra come la produzione thailandese sia molto varia (dal mediocre al capolavoro), mentre quella giapponese è più concentrata su voti medio-alti.

2. Analisi Temporale
Il Boom del Genere: Grafici che evidenziano una crescita esponenziale del numero di produzioni a partire dal 2020.

Anni d'Oro: Identificazione degli anni con la maggiore concentrazione di "Capolavori" (Rating > 8.0).

Heatmap: Una mappa di calore che mostra l'evoluzione del dominio di mercato per Paese anno per anno.

3. Analisi Formato e Contenuto
Episodi vs Rating: Le serie brevi (8-12 episodi) tendono ad avere voti migliori rispetto a quelle molto lunghe.

Drama vs Special: Le serie complete ricevono valutazioni mediamente superiori rispetto agli episodi speciali.

Analisi Lessicale: Analisi delle parole più frequenti nei titoli. La parola "Love" è onnipresente. Curiosamente, i titoli molto lunghi mostrano una leggera correlazione positiva con voti alti.

4. Machine Learning (Random Forest)
È stato addestrato un modello Random Forest Regressor per prevedere il rating di un drama basandosi sulle sue caratteristiche.

Metriche: MAE (Mean Absolute Error) di circa 0.51.

Feature Importance: I fattori più determinanti per il voto sono risultati essere:

Numero di Episodi (~46%)

Anno di rilascio (~40%)

Paese di origine

📈 Visualizzazioni
Lo script genera diverse immagini PNG ad alta risoluzione, tra cui:

analisi_bl_grandissima.png: Panoramica generale.

analisi_confronto_kde.png: Confronto curve di densità Thai vs Japan.

analisi_anni_heatmap.png: Evoluzione temporale per paese.

ml_feature_importance.png: Grafico dei fattori predittivi del modello ML.