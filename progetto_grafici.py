from mcp.server.fastmcp import FastMCP
import matplotlib.pyplot as plt
import os
import webbrowser
import time

# Definiamo il secondo server dedicato solo alla Visualizzazione ####SERVER GRAFICI
mcp = FastMCP("Generatore di grafici")

### TOOL 1:Grafico Profilo Giocatore
@mcp.tool()
def plot_profile_chart(player_name: str, skill: list[str], 
                       values: list[int], ovr: int) -> str:
    """Genera un grafico a barre orizzontali per il profilo di un singolo giocatore.
       Ideale per visualizzare le skill (PAC, SHO, PAS) ricevute dal server principale."""
       
    start_time = time.time()
    
    # Percorso del file 
    script_dir = os.path.dirname(__file__)
    folder_path = os.path.join(script_dir,"Grafici")
    os.makedirs(folder_path, exist_ok=True)
    filename = "profilo.png"
    fullpath = os.path.join(folder_path, filename)

    # Configurazione Grafico
    plt.figure(figsize=(8, 6))
    # Colori diversi per ogni barra per renderlo più leggibile
    colors = ['#FF5733', '#28B463', '#F1C40F', '#3498DB', '#8E44AD', '#7F9C8D']
    # Grafico a barre orizzontali
    plt.barh(skill, values, color=colors)
    
    # Stile
    plt.title(f"Profilo Tecnico: {player_name} (Rating: {ovr})", fontsize=14)
    plt.xlim(0, 100) # Scala fissa 0-100
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    
    plt.tight_layout()

    # SALVA E APRI
    try:
        # Rimuovi il vecchio file se esiste
        if os.path.exists(fullpath):
            try:
                os.remove(fullpath)
            except:
                pass

        plt.savefig(fullpath)
        plt.close()
        
        webbrowser.open(f"file://{fullpath}")
        
        end_time = time.time() 
        durata = (end_time - start_time)*1000  
        return f"Grafico del profilo di {player_name} generato e aperto in {durata:.0f} ms."
    except Exception as e:
        return f"Errore generazione grafico profilo: {e}"
    
    
### TOOL 2:Grafico Comparazione giocatori    
@mcp.tool()
def plot_comparison_chart(skill: list[str], player1_name: str, player1_values: list[int], 
                          player2_name: str, player2_values: list[int]) -> str:
    """Genera un grafico comparativo e lo apre nel browser."""
    start_time = time.time()
    # Percorso del file 
    script_dir = os.path.dirname(__file__)
    folder_path = os.path.join(script_dir,"Grafici")
    filename = "confronto.png"
    fullpath = os.path.join(folder_path, filename)

    # Configurazione Grafico
    x = range(len(skill))
    width = 0.35
    plt.figure(figsize=(10, 6))
    
    # Barre affiancate (Blu vs Rosso)
    plt.bar([i - width/2 for i in x], player1_values, width, label=player1_name, color='#3498db')
    plt.bar([i + width/2 for i in x], player2_values, width, label=player2_name, color='#e74c3c')

    # Stile e Decorazioni
    plt.title(f"Confronto Diretto: {player1_name} vs {player2_name}", fontsize=14)
    plt.ylabel('Valore Skill (0-100)')
    plt.ylim(0, 100)
    plt.xticks(x, skill)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    # SALVA E APRI
    try:
        # Se esiste già, prova a rimuoverlo
        if os.path.exists(fullpath):
            try:
                os.remove(fullpath)
            except:
                pass

        plt.savefig(fullpath)
        plt.close() # Libera la memoria
        
        webbrowser.open(f"file://{fullpath}")
        
        end_time = time.time()
        durata = (end_time - start_time)*1000
        
        return (f"Ho generato il confronto tra {player1_name} e {player2_name}.\n"
                f"Il grafico è stato aperto sul tuo schermo in {durata:.0f} ms.")
        
    except Exception as e:
        return f"Errore nella generazione del grafico: {e}"
    

if __name__ == "__main__":
    mcp.run()