
from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
import sys
from functools import lru_cache

#Configurazione, Analisi e Caricamento Dati  ###SERVER DATI
mcp = FastMCP("ai_scout_server")
print("Avvio Server....", file=sys.stderr)

#Lista delle colonne di abilità nel dataset
SKILL_COLUMNS = [
    'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY',
    'Acceleration', 'Sprint Speed', 'Positioning', 'Finishing', 'Shot Power',
    'Long Shots', 'Volleys', 'Penalties', 'Vision', 'Crossing', 
    'Free Kick Accuracy', 'Short Passing', 'Long Passing', 'Curve', 
    'Dribbling', 'Agility', 'Balance', 'Reactions', 'Ball Control', 
    'Composure', 'Interceptions', 'Heading Accuracy', 'Def Awareness', 
    'Standing Tackle', 'Sliding Tackle', 'Jumping', 'Stamina', 'Strength', 
    'Aggression', 'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes'
]

try:
    #Costruiamo il percorso sicuro per il file
    script_dir = os.path.dirname(__file__)
    

    player_stats = "data/male_players.csv" 
   
    
    DATA_FILE = os.path.join(script_dir, player_stats)
    
    print(f"Caricamento dataset da: {DATA_FILE}", file=sys.stderr)
    
    df_players = pd.read_csv(DATA_FILE, encoding='UTF-8')

    # Pulizia Dati
    print("Pulizia dati in corso...", file=sys.stderr)
    
    # Convertiamo le colonne delle abilità in numeriche, gestendo i valori mancanti
    for col in SKILL_COLUMNS:
        if col in df_players.columns:
            df_players[col] = pd.to_numeric(df_players[col], errors='coerce').fillna(0)
    
    # Puliamo gli spazi bianchi dai nomi dei giocatori
    df_players['Name'] = df_players['Name'].astype(str).str.strip()
    #oridniamo il dataset per OVR decrescente cosi da avere i migliori in cima e semplificare alcune ricerche
    df_players = df_players.sort_values(by='OVR', ascending=False).reset_index(drop=True)
    print("Dataset caricato e pulito. Server pronto.", file=sys.stderr)
    
except FileNotFoundError:
    print(f"ERRORE: File non trovato: {DATA_FILE}", file=sys.stderr) 
    exit()
except Exception as e:
    print(f"ERRORE durante il caricamento: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    exit()

#funzione HELPER
@lru_cache(maxsize=128) 
def find_player(player_name: str):
    """Cerca un giocatore nel DataFrame ignorando maiuscole/minuscole."""
    
    filtro = df_players[df_players['Name'].str.contains(player_name, case=False, na=False)] 
    
    if filtro.empty:
        return None 
    
    return filtro.iloc[0] 



# Definizione dei Tool

### TOOL 1: Profilo Giocatore
@mcp.tool()
@lru_cache(maxsize=128) #salviamo in cache 128 profili giocatori richiesti
def get_player_info(player_name: str) -> str:
    """Recupera le informazioni base di un giocatore."""
    print(f"[Tool 1] Richiesto profilo per: '{player_name}'", file=sys.stderr)
    
    player_data = find_player(player_name)
    
    if player_data is None:
        return f"Errore: Giocatore '{player_name}' non trovato."
    
    #Portiere vs Giocatore di movimento
    if player_data['Position'] == 'GK':
        # Statistiche specifiche per Portieri
        stats = (
            f"PARAMETRI DA PORTIERE:\n"
            f"DIV (Tuffo):    {player_data['GK Diving']} \t REF (Riflessi): {player_data['GK Reflexes']}\n"
            f"HAN (Presa):    {player_data['GK Handling']} \t POS (Piaz.):   {player_data['GK Positioning']}\n"
            f"KIC (Rinvio):   {player_data['GK Kicking']} \t PHY (Fisico):  {player_data['PHY']}\n"
        )
    else:
        # Statistiche standard 
        stats = (
            f"PARAMETRI TECNICI:\n"
            f"PAC (Velocità): {player_data['PAC']} \t DRI (Dribbling): {player_data['DRI']}\n"
            f"SHO (Tiro):     {player_data['SHO']} \t DEF (Difesa):    {player_data['DEF']}\n"
            f"PAS (Passaggi): {player_data['PAS']} \t PHY (Fisico):    {player_data['PHY']}\n"
        )
    #risultato
    return (f"--- SCHEDA GIOCATORE: {player_data ['Name']} ---\n"
        f"Club: {player_data['Team']}\n"
        f"Ruolo: {player_data['Position']} | Rating (OVR): {player_data['OVR']}\n"
        f"Età: {player_data['Age']} anni | Altezza: {player_data['Height']}cm | Piede: {player_data['Preferred foot']}\n"
        f"-------------------------------------------\n"
        +stats
    )  
###TOOL 2: Lista Abilità
@mcp.tool()
@lru_cache(maxsize=1) #La lista è sempre uguale, inutile ricrearla
def list_available_skills() -> str:
    """Restituisce un elenco di tutte le abilità (skill) che possono essere analizzate."""
    print(f"[Tool 2] Richiesta lista abilità", file=sys.stderr)
    
    formatted_skills = map(lambda skill: f"• {skill}", SKILL_COLUMNS)
    
    return f"Ecco tutte le abilità disponibili per l'analisi:\n" + "\n".join(formatted_skills)

### TOOL 3: Confronto Giocatori
@mcp.tool()
@lru_cache(maxsize=32) #utilizziamo 32 slot di cache per confronti ripetuti
def compare_players(player_a_name: str, player_b_name: str, skill: str) -> str:
    """Confronta due giocatori su una singola abilità (es. 'Finishing' o 'Sprint Speed')."""
    print(f"[Tool 3] Richiesta comparazione: '{player_a_name}' vs '{player_b_name}' su '{skill}'", file=sys.stderr)
     
    skill_key = None
    for s in SKILL_COLUMNS:
        if s.lower() == skill.lower():
            skill_key = s
            break
            
    if skill_key is None:
        return f"Errore: Abilità '{skill}' non valida, cerca all'interno della lista abilità quella che preferisci."

    player_a_data = find_player(player_a_name)
    player_b_data = find_player(player_b_name)
    
    if player_a_data is None:
        return f"Errore: Giocatore '{player_a_name}' non trovato."
    if player_b_data is None:
        return f"Errore: Giocatore '{player_b_name}' non trovato."
        
    skill_a = player_a_data[skill_key]
    skill_b = player_b_data[skill_key]
    
    return (f"Comparazione - {skill_key}:\n"
            f"- {player_a_data['Name']}: {skill_a}\n"
            f"- {player_b_data['Name']}: {skill_b}")

### TOOL 4: Ricerca Miglior Giocatore
@mcp.tool()
@lru_cache(maxsize=32)
def find_top_player_for_skill(skill: str, min_age: int = 0) -> str:
    """Trova il miglior giocatore per una specifica abilità, sopra una certa età."""
    print(f"[Tool 4] Richiesta top player per: '{skill}' (Età > {min_age})", file=sys.stderr)
    
    skill_key = None
    for s in SKILL_COLUMNS:
        if s.lower() == skill.lower():
            skill_key = s
            break
            
    if skill_key is None:
        return f"Errore: Abilità '{skill}' non valida, cerca all'interno della lista abilità quella che preferisci."

    #Filtra per età 
    df_filtrato = df_players[df_players['Age'] >= min_age]
    
    if df_filtrato.empty:
        return f"Nessun giocatore trovato con più di {min_age} anni."
        
    #Ordina per l'abilità richiesta e prende il migliore
    top_player = df_filtrato.sort_values(by=skill_key, ascending=False).iloc[0]
    
    return (f"Miglior giocatore per {skill_key} (sopra i {min_age} anni):\n"
            f"- Nome: {top_player['Name']}\n"
            f"- Club: {top_player['Team']}\n"
            f"- Punteggio: {top_player[skill_key]}")
    
### TOOL 5: migliori giocatori per posizione
@mcp.tool()
@lru_cache(maxsize=32) #I ruoli nel calcio sono pochi (PT, DC, CC, ATT...) con maxsize=32 li copri tutti.
def best_player_for_position(position: str, num_players: int = 1) -> str:
    """Restituisce i migliori giocatori per una posizione specifica."""
    player_data = df_players[df_players['Position'].str.contains(position, case=False, na=False)]
    
    if player_data.empty:
        return None
    
    #il DataFrame è già ordinato per OVR decrescente quindi prendiamo i primi
    top_players =player_data.head(num_players)
    
    #LIST COMPREHENSION
    lines = [ f"- {p.Name} (Club: {p.Team}) -> Rating: {p.OVR}" for p in top_players.itertuples()]
   
    return f"Top {num_players} giocatori per il ruolo '{position}':\n" + "\n".join(lines)

if __name__ == "__main__":
    mcp.run(transport="stdio")