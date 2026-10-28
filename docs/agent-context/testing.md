# Testování helperu

## Project Memory kompatibilita

Runner: standardní Python 3 `unittest`, bez sítě, credentials a klientských dat.
Regrese používají dočasné adresáře s minimálními syntetickými orientačními soubory;
nejsou to plně validní FAAM projekty. Testy ověřují ochranu proti scaffoldingu,
neměnnost sémantických souborů, klasifikaci, výslovné omezení orientační kontroly a
bezpečnou instalaci `project-documentation` bez vzniku dokumentačního nebo analytického
obsahu.
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


## Project documentation capability

Samostatný read-only validátor a inventura mají regresi v
`toolkit/development/tests/test_project_documentation_tool.py`. Testuje prázdný repozitář,
syntetickou Project Memory s FDT referencí, volitelnou explicitní klasifikaci
`data/view/pseudo`, neplatnou klasifikaci a zákaz helper-native `docs/project/` uvnitř
Project Memory.

## Revize project documentation podle XDS authoring návrhu

Regrese `test_project_documentation_tool.py` nově pokrývá:

- report proposal-stage rodiny `docs/reference/application/`;
- zachování stavu `proposal` místo tvrzení o implementaci;
- varování u kurátorované věcné stránky bez `## Zdroje a aktuálnost`;
- průchod stránky s uvedenou provenance sekcí.

Project Memory instalační regrese zároveň ověřuje distribuci obou přenositelných referencí
skillu bez vytvoření `docs/` nebo zásahu do analytické struktury.
