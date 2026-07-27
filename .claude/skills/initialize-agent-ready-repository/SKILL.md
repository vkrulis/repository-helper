---
name: initialize-agent-ready-repository
description: Založí nový repozitář nebo doplní dosud prázdný projekt o platformně nezávislou strukturu README.md, AGENTS.md, docs/agent-context, .agents/profiles, .agents/skills, jednotný toolkit a resources. Použijte při vytváření nového projektu, nového konfiguračního repozitáře nebo při zavádění agent-ready organizace do prázdného repa. Nepoužívejte pro reorganizaci obsahově rozvinutého repozitáře; tam nejprve použijte audit-repository-structure.
compatibility: Vyžaduje přístup k souborům repozitáře. Git a Python 3 jsou doporučené, ale strukturu lze vytvořit i ručně.
metadata:
  version: "1.1"
---

# Inicializace agent-ready repozitáře

## Cíl

Vytvořit čistý a srozumitelný základ, který je nezávislý na poskytovateli modelu a připravený pro tenké platformní konektory.

## Vstupy

Zjistěte nebo rozumně odvoďte:

- název projektu,
- jednovětý účel,
- typ repozitáře,
- primární jazyk a hlavní build/test příkazy,
- zda už existuje obsah,
- zda je vůbec požadován platformní konektor a pro kterou platformu; při práci v Codexu lze bez jiné preference odvodit Codex, jinak se zeptejte.

Ptejte se pouze na informace, které nelze bezpečně odvodit a které zásadně ovlivní výsledek. Menší mezery vyplňte viditelnými `TODO` položkami.

## Bezpečnostní kontrola

Pokud repozitář obsahuje významný stávající obsah, nepokračujte jako s novým repozitářem. Aktivujte `audit-repository-structure`.

Nevytvářejte nebo nepřepisujte:

- secrets,
- deployment credentials,
- uživatelské globální konfigurace,
- aplikační soubory mimo cílovou agentní strukturu.

## Postup

Inicializace musí automaticky distribuovat schopnosti `work-log` a `decision-records`, jejich kanonické skills, `.logs/`, `docs/agent-context/decisions/` a odpovídající pravidla v `AGENTS.md`. Použijte kanonický příkaz `repository_architecture.py init`; nevytvářejte ruční kopie těchto souborů.

1. Přečtěte `docs/agent-context/repository-architecture.md` z této kolekce nebo ekvivalentní přiloženou referenci.
2. Zkontrolujte stav Git repozitáře a existující kořenové soubory.
3. Vytvořte minimálně:

```text
README.md
AGENTS.md
docs/agent-context/README.md
.agents/README.md
.agents/profiles/README.md
.agents/skills/README.md
toolkit/README.md
resources/README.md
```

4. Do `README.md` vložte skutečné známé informace a zřetelná `TODO` pro neznámé údaje.
5. Do `AGENTS.md` vložte pouze společná pravidla a odkazy na budoucí zdroje pravdy.
6. V `docs/agent-context/README.md` popište plánované kontextové dokumenty.
7. Přidejte první profil jen tehdy, existuje-li skutečná specializovaná role. Nevytvářejte dekorativní profily.
8. Ponechte standardní repository skills `maintain-work-log` a `maintain-decision-records`; další skill přidejte jen tehdy, existuje-li opakovatelný projektový postup.
9. Založte `toolkit/README.md` jako jediný kořen všech exaktních nástrojů. Nevytvářejte `.agents/tools`, kořenové `tools`, kořenové `scripts` ani skillové `scripts`.
10. Založte `resources/README.md` s pravidly původu, licence, aktualizace a autoritativnosti. Samotné zdroje přidejte jen když jsou známé; nevymýšlejte dekorativní data.
11. Platformní konektor přidejte jen na přání. Pokud práce probíhá v Codexu a není uvedena jiná preference, lze zvolit Codex; v jiném nebo neznámém prostředí se zeptejte a připusťte variantu bez konektoru.
12. Spusťte `validate-repository-architecture`.

## Doporučený nástroj

Je-li dostupný, použijte bezpečný scaffold:

```bash
python toolkit/agent-infrastructure/repository_architecture.py init <target> --name "<project name>"
```

Nástroj standardně nepřepisuje existující soubory.

## Výstup

Uveďte:

- vytvořený strom,
- soubory obsahující `TODO`,
- zvolený platformní konektor nebo informaci, že nebyl požadován,
- vynechané volitelné části a důvod,
- provedené validační příkazy.

## Akceptační kritéria

Načtěte `references/acceptance-checklist.md` před finálním předáním a projděte všechny body.
