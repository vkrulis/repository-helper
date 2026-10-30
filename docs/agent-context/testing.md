# Testování helperu

## Project Memory kompatibilita

Runner: standardní Python 3 `unittest`, bez sítě, credentials a klientských dat.
Regrese používají dočasné adresáře s minimálními syntetickými orientačními soubory;
nejsou to plně validní FAAM projekty. Testy ověřují ochranu proti scaffoldingu,
neměnnost sémantických souborů, klasifikaci a výslovné omezení orientační kontroly.
Nativní klientský scaffold se testuje v odděleném dočasném repozitáři.

```bash
python -m unittest discover -s toolkit/development/tests -v
```

Volitelný kontraktní smoke používá přímo aktuální generátor a validátor Orchestrátoru
v dočasném adresáři, nikoli jejich zkopírovanou implementaci. Dostupný je s parametrem:

```bash
python toolkit/development/tests/project_memory_contract_smoke.py ../Flexideo-orchestrator
```

Oba scénáře odstraňují pouze vlastní `TemporaryDirectory`, žádný klientský ani pracovní
repozitář. CI zde nepřibývá. Povinné kontroly kolekce, architektury a logu jsou v AGENTS.md.

## Dokumentační instalace

Stejný unittest runner zahrnuje `test_documentation_management.py`: neměnnost
projektového obsahu a šablony, idempotenci, aktualizaci z připnutého digestu, lokální
konflikt i s force, neznámé layouty, omezení profilu, poškozený manifest, odmítnutí
symlinků a rollback po chybě zápisu. Syntetické fixture nejsou projektové piloty.
Test vyhledávání zachovává AND/OR a normalizaci diakritiky. Žádný test nevolá cloud.
