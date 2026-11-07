---
name: activate-flexideo-implementer
description: Aktivuje lokální Flexideo Implementátor pro implementační úkol v klientském projektu. Najde a ověří instalaci produktu a načte jeho FCL bootstrap pro výběr dovedností vrstev A–E. Použij při požadavku použít Implementátor, prověřit nebo upravit Flexideo aplikaci; FAAM analýzu ponech projektové paměti.
---

# Aktivace Flexideo Implementátora

Tato dovednost zpřístupňuje externí produkt. Klasifikaci úkolu a výběr odborných
dovedností vlastní FCL; nekopíruj sem jeho mapu ani katalogy vrstev.

1. Urči kořen klientského projektu a načti jeho platná pravidla. Z tohoto kořene spusť:

   ```powershell
   python toolkit/skills/activate-flexideo-implementer/activate.py activate --project .
   ```

   Z jiné pracovní složky použij absolutní cestu k témuž projektovému nástroji
   a `--project <kořen-klientského-projektu>`. Nástroj také umí určit kořen podle
   svého umístění v instalovaném projektovém `toolkit/`.
2. Při `READY_FOR_BOOTSTRAP` zaznamenej `assembly_id` a kořen projektu. **Explicitně
   přečti** soubory vrácené jako `instructions_path` a `bootstrap_path`. Výsledek
   nástroje sám o sobě neznamená, že agent instrukce načetl nebo vykonal úkol.
3. Předej FCL původní zadání a kontext projektu. Dále načítej jen vybrané vrstvy,
   odborné skills a jejich požadované reference. Příkazy spouštěj z produktových
   pracovních adresářů podle konkrétní skill; klientský projekt zůstává cílem práce.
4. Session a výstupy ukládej mimo instalaci podle pravidel klientského projektu.
   Přístup do Project Memory a její sémantické zápisy se řídí jejím vlastním kontraktem.
5. Před pokračováním starší relace lze znovu spustit aktivaci s
   `--expected-assembly <připnuté-id>`. Při změně sestavy začni nový chat a načti
   aktuální bootstrap. Požadavky na host, prostředí, credentials a oprávnění
   ověřují vybrané odborné dovednosti; aktivace je neposkytuje.

## Chybějící instalace nebo přístup

- `NOT_CONFIGURED`: při prvním požadavku se zeptej **přímo v chatu**, například:
  „Ve které složce máte lokální Flexideo Implementátor (obsahuje `fcl/` a
  `assembly.lock.json`)? Po ověření cestu uložím pro další projekty na tomto počítači.“
  Použij dialogový nástroj hosta, pokud je dostupný; jinak polož běžnou chatovou
  otázku na textovou cestu. Umístění již výslovně zadané v úloze znovu nevyžaduj.
  Na odpověď vyčkej; cestu neodhaduj ani uživateli nepředávej registraci jako ruční úkol.
  Získanou cestu předej stejnému nástroji: `register --root <instalační-složka>`.
  Po úspěšné registraci znovu spusť `activate` a pokračuj bodem 2. Registrace
  ověří produkt a uloží umístění do uživatelské konfigurace mimo projekt; další
  projekty stejného uživatele na tomto počítači tuto otázku již nepotřebují.
- Pro jednorázově určené umístění použij `activate --assembly <instalační-složka>`.
  Absolutní cestu nezapisuj do verzovaných projektových instrukcí.
- Neplatnou sestavu, chybějící host přístup nebo jinou chybu oznam podle výsledku.
  Nehledej náhradní instalace po disku a nenahrazuj chybějící dovednost obecnou implementací.
- Ve VS Code musí použitý agent smět číst externí instalaci a spouštět její
  ověřovací nástroj. Registrace nemění sandbox ani oprávnění; instalační složka
  zůstává čteným produktem, nikoli místem pro projektové změny.
