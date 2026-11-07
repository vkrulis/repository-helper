# Zásady hlavního README

## Účel

`README.md` je první orientační bod pro člověka a podpůrný zdroj pro agenty. Nemá nahrazovat `AGENTS.md` ani podrobnou kontextovou dokumentaci.

## Povinné minimum

1. Název a jednovětý účel projektu.
2. Co repozitář obsahuje a co neobsahuje.
3. Jak projekt nainstalovat nebo otevřít.
4. Jak provést nejběžnější operaci.
5. Jak spustit build, testy nebo validaci.
6. Kde jsou architektonické a doménové podklady.
7. Kde jsou pravidla pro agenty.
8. Jak přispívat nebo komu změnu předat.

Dokumentované příkazy musí uvádět pracovní adresář a používat přenositelné relativní cesty podle cílové architektury repozitáře. Strojově nebo uživatelsky specifické absolutní cesty do README nepatří, pokud nejsou nevyhnutelným a vysvětleným vstupem externího runtime.

## Doporučená osnova

```markdown
# Project name

Jednovětý účel.

## Přehled

## Struktura repozitáře

## Rychlý start

## Vývoj a validace

## Dokumentace

## Práce s AI agenty

## Přispívání
```

## Vztah k ostatním souborům

| Soubor | Odpovídá na otázku |
|---|---|
| `README.md` | Co to je a jak začít? |
| `AGENTS.md` | Jak se zde musí pracovat? |
| `docs/agent-context/` | Jak projekt funguje a proč? |
| `.agents/profiles/` | Kdo má danou práci vykonávat? |
| `.agents/skills/` | Jak se provádí konkrétní práce? |
| `resources/` | Jaké vstupní zdroje lze prohledávat nebo analyzovat? |
| `toolkit/` | Jaké exaktní nástroje projekt poskytuje a jak jsou rozdělené do podsložek? |
| `.logs/` | Kde je chronologická pracovní historie a jak se vytváří? |

README má ve struktuře uvést také volitelné `resources/` a vysvětlit, jaké vstupní zdroje lze prohledávat nebo analyzovat.

## Zakázané duplicity

README nemá obsahovat úplné kopie:

- agentních pravidel,
- detailní architektury,
- dlouhých operačních postupů,
- platformních profilů.

Má je stručně uvést a odkázat na kanonické umístění.
