# Základní typy repozitářů

Tento dokument je autoritativní taxonomií repozitářů spravovaných pomocí
Repository-helperu. Každý repozitář má právě jeden **primární typ**. Capability mohou
typ rozšiřovat, ale nesmějí znejasnit jeho zdroj pravdy ani odpovědnost.

## Development repository

Vyvíjí a ověřuje runtime produkt nebo technickou komponentu platformy. Zdrojový kód
zůstává ve standardní projektové cestě, interní automatizace v `toolkit/` a případná
publikovatelná projekce v jediné hranici `public/` nebo `product/`.

Development repository vlastní implementaci, build, testy, runtime kompatibilitu a
technická omezení. Nevlastní klientské zadání ani authoringový postup nad více vrstvami.

## Authoring repository

Vytváří, testuje a vydává přenositelný authoring produkt: skills, nástroje, kontrakty,
definice nebo metodiku, pomocí nichž vznikají či se mění aplikace. Jeho publikovatelný
produkt vzniká přímo a autoritativně v `product/`; kořen repozitáře je pracovní a
údržbová infrastruktura.

Authoring má dvě role:

- `specialist` vlastní authoring jedné vrstvy nebo vymezené oblasti a vydává její
  samostatně verzovaný produkt;
- `orchestrator` je nadřazená authoring entita. Překládá záměr na koordinovanou změnu
  aplikace, vybírá specialisty, řídí handoff, pořadí, lock a trasovatelnost napříč
  vrstvami. Nekopíruje jejich detailní znalost ani produkty.

`Flexideo-orchestrator` je referenční orchestration-authoring repository ekosystému.
Načítá registry produktů specializovaných authoring repozitářů, sestavuje z nich své
aktuální schopnosti a koordinuje finální tvorbu a úpravy aplikací napříč vrstvami.

## Client-project repository

Realizuje jednu konkrétní klientskou aplikaci. Vlastní zadání, projektový kontext,
akceptaci, trasovatelnost a jediný aktuální projektový definiční model v `definitions/`.
Používá produkty authoring repozitářů, ale nevydává obecný platformní authoring produkt.

## Documentation repository

Konsoliduje ověřenou technickou a doménovou dokumentaci z jednotlivých vrstev a může
vydávat uživatelskou dokumentaci. Je authoringu blízké, ale jde o samostatný primární
typ: nevlastní runtime implementaci, klientský definiční model ani autoritativní
authoring skills. Původ a revizní stav přenesených znalostí musí zůstat dohledatelný.

## Rozhodovací pravidlo

Typ určete podle toho, **co je autoritativním výstupem repozitáře**, ne podle použitého
jazyka nebo přítomnosti dokumentace:

| Autoritativní výstup | Primární typ |
| --- | --- |
| Runtime kód nebo technická komponenta | `development` |
| Přenositelný postup/nástroj pro tvorbu aplikací | `authoring` |
| Jedna klientská aplikace a její definice | `client-project` |
| Konsolidovaná technická nebo uživatelská dokumentace | `documentation` |

Pokud repozitář zdánlivě odpovídá více typům, před strukturální změnou vymezte jednu
primární odpovědnost a ostatní popište jako capability nebo závislosti. Změna primárního
typu je architektonické rozhodnutí a vyžaduje ADR.
