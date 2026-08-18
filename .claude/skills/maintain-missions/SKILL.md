---
name: maintain-missions
description: Konzervativně navrhuje, zakládá a udržuje mise (střednědobé až dlouhodobé cíle repozitáře) v docs/missions, aktivně vybízí k jejich založení, když práce narazí na něco velkého nebo nejasného, a propojuje jejich životní cyklus s ADR a pracovním logem. Použijte, když se objeví cíl přesahující jednu materiální změnu nebo s otevřenými otázkami vůči uživateli, nebo když existující mise mění stav (revize, propojení s ADR, realizace, odložení, zamítnutí). Nepoužívejte pro izolované opravy nebo lokální vylepšení bez dlouhodobého přesahu.
---

# Maintain missions

## Kdy misi navrhnout

Misi navrhněte, jakmile je z kontextu práce zřejmé něco velkého nebo nejasného. Posuďte čtyři otázky:

1. Přesahuje cíl jednu materiální změnu nebo jedno pracovní sezení a bude vyžadovat víc navazujících kroků?
2. Je rozsah nebo přístup zatím nesladěný s uživatelem (otevřené otázky, víc možných směrů)?
3. Je pravděpodobné, že cíl dřív nebo později povede alespoň k jednomu architektonicky významnému rozhodnutí (kandidát na ADR)?
4. Jde o dlouhodobý nebo strategický cíl repozitáře, ne o izolovanou opravu či lokální vylepšení?

- 0–1 kladná odpověď: misi nezakládejte; stačí pracovní log, případně rovnou ADR, pokud je rozhodnutí už jasné.
- 2 kladné odpovědi: misi navrhněte uživateli, ale nezakládejte ji bez potvrzení.
- 3–4 kladné odpovědi: aktivně vybídněte uživatele k založení mise dřív, než se pustíte do rozsáhlé realizace.

Velikost jednorázové změny sama o sobě není důvodem pro misi.

## Postup

1. Přečtěte `docs/missions/README.md` (pokud repozitář dosud misi nemá, založte jej instalací capability) a existující související mise.
2. Určete další nepoužité monotónní dvoumístné číslo v `docs/missions/`; čísla nikdy znovu nepoužívejte.
3. Použijte `references/mission-template.md` a vytvořte jeden dokument pro jeden cíl.
4. Vyplňte `Cíl`, `Proč`, `Co už víme` (fakty odlište od domněnek a uveďte datum průzkumu), `Navrhovaný přístup`, `Závislosti`, `Otevřené otázky` a návrh `Definice hotovo`.
5. Nastavte `Stav: draft`, dokud mise neprošla revizí s uživatelem; teprve po potvrzení směru přepněte na `reviewed`.
6. Aktualizujte tabulku v `docs/missions/README.md` (mise → stav → priorita).
7. Jakmile z mise vzejde architektonicky významné rozhodnutí, aktivujte `maintain-decision-records`. Do pole `ADR:` mise vložte odkaz na vzniklý ADR a stav přepněte na `in-progress`.
8. Po dokončení, odložení nebo zamítnutí aktualizujte pole `Stav` (`done`/`deferred`/`rejected`). Existující mise obsahově nepřepisujte kvůli změně stavu — upravte jen pole `Stav` (a `ADR`, je-li relevantní); zásadní změnu cíle nebo přístupu zachyťte novou misí a vzájemně je odkažte.
9. Po založení nebo změně stavu použijte `maintain-work-log` a zápis propojte s dotčeným souborem mise.
10. Spusťte validaci architektury repozitáře.

## Hranice obsahu

- Mise není implementační návod, ADR ani pracovní log — je to podklad k projití s uživatelem, ne autoritativní zdroj.
- Nezapisujte skryté uvažování, secrets, osobní ani produkční data.
- Nevytvářejte misi pro cíl, který lze bezpečně a rychle prostě udělat a zalogovat.
- Ověřené doménové poznatky vzešlé z mise časem přesuňte do `docs/agent-context/domain/`; mise ať zůstane návrhem, ne skrytým druhým zdrojem trvalé pravdy.

## Výstup

Uveďte rozhodovací bránu (proč mise ano/ne), cestu a stav mise, propojení s ADR (pokud vzniklo), aktualizaci indexu a výsledky validací.
