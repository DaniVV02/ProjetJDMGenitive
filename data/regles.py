RULES_DATABASE = [
    {
        "name": "DET_NOUN_TO_GN",
        "pattern": [
            {"label": "Det:", "type": "POS"},
            {"label": "Nom:", "type": "POS"}
        ],
        "action": "CREATE_GN"
    },
    {
        "name": "DET_ADJ_NOUN_TO_GN",
        "pattern": [
            {"label": "Det:", "type": "POS"},
            {"label": "Adj:", "type": "POS"},
            {"label": "Nom:", "type": "POS"}
        ],
        "action": "CREATE_GN"
    },
    {
        "name": "DISAMBIG_DET_NOUN",
        "pattern": [
            {"label": "Det:", "type": "POS"},
            {"label": "Nom:", "type": "POS"} 
        ],
        "action": "NEGATE_VERB_IF_PRESENT"
    }
    # Ajoute ici tes autres règles en respectant bien la clé "pattern"
]