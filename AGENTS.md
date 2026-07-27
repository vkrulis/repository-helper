# Repository Skills – pracovní pravidla

## Účel repozitáře

Tento repozitář je kanonickým zdrojem přenositelných skills, profilů, dokumentace a deterministických nástrojů pro organizaci agent-ready repozitářů.

## Zdroje pravdy

- Cílová architektura: `docs/agent-context/repository-architecture.md`
- Migrační politika: `docs/agent-context/migration-policy.md`
- Platformní scénáře: `docs/agent-context/platform-connector-scenarios.md`
- Neutrální profilový formát: `docs/agent-context/profile-schema.md`
- Konvence README: `docs/agent-context/repository-readme-guidelines.md`

## Povinný pracovní postup

1. Rozlišujte znalost, pravidlo, profil, skill a nástroj.
2. Společnou znalost zapisujte pouze do `docs/agent-context/`.
3. Společná pravidla prostředí zapisujte do `AGENTS.md`.
4. Kanonické profily upravujte pouze v `.agents/profiles/`.
5. Platformní konektory a profily vytvářejte pouze pro požadovanou platformu. Pokud platforma není určena, použijte Codex jen při práci v Codexu; jinak se zeptejte a nabídněte i možnost bez konektoru.
6. Každý skill musí zůstat úzce zaměřený na jednu práci.
7. Veškeré exaktní a spustitelné nástroje ukládejte výhradně pod kořenový `toolkit/`. Týká se to skriptů (`*.py`, `*.ps1`, `*.sh`, `*.bat` a dalších), validátorů, generátorů, CLI wrapperů, spustitelných balíčků i podpůrných souborů. Agentní infrastruktura patří do `toolkit/agent-infrastructure/`, doménové nástroje do `toolkit/domain/`, vývojové nástroje do `toolkit/development/` a nástroj jediného skillu do `toolkit/skills/<skill-name>/`. Pokud již projekt `toolkit/` používá, zachovejte jej a konflikt významů řešte vhodnými podsložkami. Žádné nástroje neukládejte do `.agents/`, kořenového `tools/` ani do `scripts/` uvnitř skillu.
8. Projektové vstupy určené k hledání, čtení nebo analýze ukládejte do `resources/`; běhový kód ponechte v jeho standardní cestě a přenositelné podklady jednoho skillu v jeho `references/`.
9. U zdrojů evidujte původ, licenci, formát a zda jsou ručně spravované, převzaté nebo generované.
10. Při architektonicky významném rozhodnutí použijte konzervativní skill `maintain-decision-records`; ADR ukládejte do `docs/agent-context/decisions/` a nevytvářejte jej pro běžné lokální změny.
11. Po každé materiální změně kódu, dokumentace, konfigurace, pravidel, struktury nebo nástrojů použijte skill `maintain-work-log` a přidejte stručný záznam do `.logs/YYYY/MM/YYYY-MM-DD.md`. Vznik nebo změnu stavu ADR vždy propojte s tímto záznamem. Existující historii nepřepisujte; pozdější předělávku zachyťte novým záznamem. Aktuální autoritativní znalost patří do `docs/agent-context/`, chronologická historie do `.logs/` a fyzická historie do Gitu.
12. Před předáním práce ověřte dnešní log a spusťte validaci celé kolekce.

## Povinné kontroly

```bash
python toolkit/agent-infrastructure/validate_skill_collection.py .
python toolkit/agent-infrastructure/repository_architecture.py validate .
python toolkit/work-log/work-log.py validate .
```

## Bezpečnost a změny

- Nezapisujte credentials, tokeny, produkční data ani lokální osobní konfiguraci.
- Nepřepisujte existující soubory bez zobrazení rozdílu nebo explicitního režimu `--force`.
- Migrační nástroje nesmějí automaticky rozhodovat o nejednoznačných doménových přesunech.
- Při změně platformního scénáře uveďte datum ověření a zdroj.

## Definice hotovo

Změna je hotová pouze tehdy, když:

- odpovídá architektuře repozitáře,
- nevytváří druhý zdroj pravdy,
- všechny `SKILL.md` mají validní frontmatter,
- odkazy na soubory existují,
- všechny výslovně požadované generované konektory jsou synchronní,
- validační příkazy skončí úspěšně,
- README nebo kontextová dokumentace popisují uživatelsky významnou změnu.
- materiální změna je stručně zaznamenána v dnešním pracovním logu včetně změněných souborů, skutečně provedených validací a otevřené práce.
