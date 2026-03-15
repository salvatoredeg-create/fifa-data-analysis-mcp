# fifa-data-analysis-mcp
Analisi dati FIFA e sviluppo di server MCP (Model Context Protocol) per l'interrogazione e la visualizzazione statistica.
# ⚽ Sports Data Analytics: FIFA/FC25 & MCP Framework

Questo progetto implementa una soluzione avanzata di **Data Analytics** applicata al dataset di EA Sports FC 25 (16.000+ giocatori). L'obiettivo principale è risolvere il problema delle "allucinazioni numeriche" nei Large Language Models (LLM), garantendo risposte basate su dati certi tramite il protocollo **MCP (Model Context Protocol)**.

## Il Problema: LLM e Allucinazioni
I modelli AI generalisti (come ChatGPT o Claude) spesso generano statistiche plausibili ma errate perché non hanno accesso diretto a database strutturati. Questo sistema obbliga l'AI a recuperare il dato esatto dal file sorgente prima di rispondere all'utente.

## Architettura della Soluzione
Il sistema è strutturato come un ecosistema a microservizi coordinato da un **Agente AI (Middleware Intelligente)**:

1.  **Client (L'Intelligenza):** Claude Desktop interpreta l'intento semantico dell'utente.
2.  **Server Dati (`progetto.py`):** Esecutore logico che utilizza **Pandas** per il recupero, filtraggio e analisi dei KPI (OVR, Skill tecniche, Anagrafica).
3.  **Server Grafico (`progetto_grafici.py`):** Modulo specializzato nel rendering visivo tramite **Matplotlib**, capace di generare asset PNG dinamici.
4.  **Data Layer:** Dataset strutturato (`male_players.csv`) con 58 variabili tecniche per ogni osservazione.

## Flusso di Lavoro
1. **Query:** L'utente chiede in linguaggio naturale (es. *"Confronta il potenziale di Di Lorenzo con quello di Theo Hernandez"*).
2. **Orchestrazione:** L'LLM seleziona il tool appropriato dal Server Dati.
3. **Analisi:** Il server elabora il file CSV e restituisce i vettori numerici.
4. **Visualizzazione:** L'AI decide autonomamente di invocare il Server Grafico per mostrare il confronto visivo.
5. **Risposta:** L'utente riceve dati certificati e grafici pronti all'uso.

## Stack Tecnologico
* **Linguaggio:** Python 3.x
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Matplotlib
* **AI Framework:** Model Context Protocol (MCP), Claude Desktop

## Contenuto della Repository
* `progetto.py`: Logica del server di analisi dati.
* `progetto_grafici.py`: Logica del server di rendering grafico.
* `male_players.csv`: Database sorgente (Kaggle).
* `Relazione progetto.pdf`: Documentazione tecnica dettagliata (12 pagine).
* `Presentazione_Risultati.pdf`: Slide di sintesi dell'architettura e dei risultati.

---
*Progetto realizzato per l'esame di **Programmazione per la Data Science**.*
