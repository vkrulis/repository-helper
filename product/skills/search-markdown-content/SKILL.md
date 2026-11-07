---
name: search-markdown-content
description: Vyhledává a vysvětluje Markdown v dokumentační oblasti repozitáře pomocí AND/OR dotazů. Použijte pro dohledání témat a doloženou rešerši; rozsah a autoritu určuje místní dokumentační profil.
---

# Vyhledávání Markdownu

Přečtěte místní `.agents/documentation.json`, pokud existuje, a pravidla repozitáře.
Profil určuje `roots` a `generated_roots`; nepředstavuje oprávnění k zápisu ani publikaci.
Bez profilu nejprve určete dokumentační kořen z README/AGENTS. Nezaměňujte
dokumentaci aplikace, analytický stav, zdrojové definice a generovanou referenci.

Použijte `toolkit/skills/search-markdown-content/search_markdown.py` z kořene repozitáře:

```text
python toolkit/skills/search-markdown-content/search_markdown.py --root docs --query "integrace + autentizace | import" --context 1 --json
```

`+` spojuje termíny AND, `|` skupiny OR. Pro více kořenů spusťte samostatná hledání.
Dotaz, rozsah a případnou normalizaci diakritiky uveďte ve výsledku.
Úryvky slouží k výběru: před závěrem přečtěte celé relevantní stránky, metadata,
rodičovské rozcestníky a odkazované zdroje. Rozlišujte ověřený stav, návrh a neznámé.
Generovaná reference dokládá svůj zdrojový snapshot, nikoli aktuální stav nasazení.

U Project Memory respektujte layout její verze a významové operace MCP. Rešerše
nemění Current Truth, epiky ani potvrzení. Zápis a publikace vyžadují rozsah
aktuálního zadání a příslušná práva; dostupný skill je sám neuděluje.
