QUERY_CONTEXT = """ Dato il seguente testo estratto da documenti relativi a una gara d'appalto:
            \n --------------------------- \n
            {context}
            \n --------------------------- \n
            estrai con precisione le seguenti informazioni:
            • ente_appaltante: l'ente o l'amministrazione che ha pubblicato la gara, si tratta di una Regione Italiana, quindi se ne leggi una sarà sicuramente quella.
            • tipologia di offerta: il tipo di offerta, solitamente 'Aperta'
            • importo_base_asta: l'importo complessivo a base d'asta, in euro.
            • cig: il codice identificativo della gara.
            • oggetto: la descrizione generale dell'oggetto della gara.
            • lotti: un elenco dei lotti, se presenti. Per ciascun lotto includi numero, descrizione, importo. Se non ci sono lotti, restituisci una lista vuota.
            • scadenza_contratto: la data e la durata di scadenza del contratto, se specificata.
            
            Se una di esse non è presente restituisci una stringa vuota o una lista vuota.
            Restituisci l'output in formato JSON come mostrato nel system prompt. Non aggiungere altro testo.
            """


QUERY_SEARCH = """Voglio estrarre informazioni strutturate da una gara d'appalto.
                Trova nei documenti le parti che contengono riferimenti espliciti a:
                - L'ente o l'amministazione che ha pubblicato la gara
                - Tipologia di offerta, solitamente 'Aperta'
                - L'importo a base d'asta
                - Il codice CIG
                - L'oggetto della gara
                - Eventuali lotti con numero, descrizione e importo
                - La durata o la data di scadenza del contratto
                
                Restituisci solo i testi che contengono queste informazioni, o che sono strettamente legati ad essi"""

SYS_PROMPT = """Sei un assistente intelligente specializzato nell’analisi di documenti relativi a gare d’appalto.
        Il tuo compito è leggere con attenzione il contenuto fornito (estratto da uno o più documenti) e estrarre con precisione le seguenti informazioni, restituendole esclusivamente in formato JSON, nel seguente schema:

        {
        "tipologia_offerta": "",
        "ente_appaltante": "",
        "importo_base_asta": "",
        "cig": "",
        "oggetto": "",
        "lotti": [
            {
            "numero": "",
            "descrizione": "",
            "importo": ""
            }
        ],
        "scadenza_contratto": ""
        }

        • Se una delle informazioni richieste non è presente, lascia il campo corrispondente come stringa vuota ("") o, nel caso di lotti, come lista vuota ([]).
        • Riporta i valori esattamente come appaiono nei documenti, senza modificarli o riformularli.
        • Non aggiungere commenti, spiegazioni o testo al di fuori del JSON.
        • Considera che il contenuto fornito potrebbe provenire da più documenti della stessa gara, quindi potresti trovare informazioni duplicate o frammentate: riuniscile nel modo più preciso possibile.
        """



SYS_PROMPT_META = """
    Sei un assistente intelligente specializzato nell'analisi di documenti relativi a gare d'appalto.
    Il tuo compito è leggere attentamente il testo fornito e restituire esclusivamente un JSON che rispetti esattamente il seguente schema:
    {
    "tipologia_offerta": "",
    "ente_appaltante": "",
    "importo_base_asta": "",
    "cig": "",
    "oggetto": "",
    "lotti": [
        {
            "numero": "",
            "descrizione": "",
            "importo": ""
        }
    ],
    "scadenza_contratto": "",
    "scadenza_chiarimenti": ""
    }
    Se un campo non è presente, restituisci una stringa vuota ("") oppure, per il campo "lotti", una lista vuota ([]).
    Non aggiungere alcun testo extra o spiegazioni.
    """


QUERY_CONTEXT_META = """
    Dato il seguente testo estratto da documenti relativi a una gara d'appalto:
    ---------------------------
    {context}
    ---------------------------
    Estrarre con precisione le seguenti informazioni:
    - tipologia_offerta: il tipo di offerta (es. 'Aperta').
    - ente_appaltante: l'ente o l'amministrazione che ha pubblicato la gara (si tratta di una Regione Italiana).
    - importo_base_asta: l'importo complessivo a base d'asta, in euro.
    - cig: il codice identificativo della gara.
    - oggetto: la descrizione generale dell'oggetto della gara.
    - lotti: un elenco dei lotti, se presenti. Per ciascun lotto, includi numero, descrizione ed importo.
    - scadenza_contratto: la data o la durata di scadenza del contratto.
    - scadenza_chiarimenti: la data entro cui devono essere presentate le offerte.
    Se un campo non è presente, restituisci una stringa vuota o, per "lotti", una lista vuota.
    Restituisci l'output esclusivamente in formato JSON esattamente secondo lo schema indicato.
    """


QUERY_SEARCH_META = """
    Voglio estrarre informazioni strutturate da una gara d'appalto.
    Trova nei documenti le sezioni contenenti riferimenti a:
    - La tipologia dell'offerta (es. 'Aperta').
    - L'ente o l'amministrazione che ha pubblicato la gara.
    - L'importo a base d'asta.
    - Il codice CIG.
    - L'oggetto della gara.
    - Eventuali lotti (numero, descrizione, importo).
    - La data del documento.
    - La scadenza del contratto e la data di presentazione delle offerte.
    Restituisci solo i testi che contengono queste informazioni o che sono strettamente correlati.
    """