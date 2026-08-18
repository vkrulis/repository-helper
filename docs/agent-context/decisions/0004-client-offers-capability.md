# ADR-0004: Volitelná capability klientských nabídek

- Stav: accepted
- Datum: 2026-08-12
- Vlastník: správci repository-helper
- Scope: shared
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Klientské projekty někdy připravují fix-price nabídky s klientsky přístupným HTML obsahem, ale jiné je vůbec nepotřebují. Nabídka má vlastní obchodní a publikační životní cyklus, který není totožný s implementačním epikem ani se zdrojovým definičním modelem.

## Rozhodovací kritéria

- Nevnucovat nabídkovou strukturu klientským projektům bez nabídek.
- Zachovat dohledatelnost od převzatého podkladu až k nabídce a případné implementaci.
- Zabránit publikaci interních vstupů a přístupových údajů.
- Umožnit izolovanou publikaci mnoha klientských repozitářů na jednom hostnamu.

## Zvažované možnosti

### Nabídka jako implementační epik

Zachovala by existující strom epiků, ale směšovala by obchodní nabídku s implementačním plánem a nutila by ji do projektů, které ji nepotřebují.

### Samostatný hosting pro každý klientský repozitář

Oddělil by nasazení, ale znásobil by provozní konfiguraci, hostname a riziko nekonzistentního zabezpečení.

### Volitelná capability s centrálním publikačním kontraktem

Udržuje nabídku v autoritativním klientském repozitáři, odděluje interní a publikovatelný obsah a publikuje jednu nabídku do sdílené infrastruktury.

## Rozhodnutí

Zavádíme volitelnou capability `client-offers`, která rozšiřuje pouze klientské projekty vytvářející nabídky. Nabídka má stabilní identitu, vlastní manifest, trasovatelnost a dva nezávislé stavy: obsah nabídky a stav publikace. Může volitelně odkazovat na implementační epik, ale není epikem.

Původní podklady zůstávají v `resources/offers/`, kurátorované závěry v `docs/project/offers/`, publikovatelný HTML obsah výhradně v `public/offers/` a odvozené reporty v `artifacts/offers/`. URL je deterministicky `https://nabidky.flexideo.cz/{project-slug}/{offer-slug}/`.

Všechny projekty používají společný hostname. Každá publikace synchronizuje jen vlastní prefix do Cloudflare R2; Worker jej obsluhuje a Cloudflare Access chrání URL. Access používá OTP spolu s explicitně povolenými e-maily, avšak seznam příjemců, Access policy a secrets jsou provozní konfigurace mimo repozitář.

## Důvody

Volitelná capability zachovává lehkost body-shopping projektů a současně nabízí opakovatelný, validovatelný model tam, kde je nabídka skutečným výstupem. Oddělení vrstev brání náhodné publikaci zdrojových souborů a izolovaný prefix dovoluje nezávislé publikace bez znalosti ostatních klientů.

## Důsledky

- Nabídkový projekt instaluje nejprve `client-project`, pak `client-offers`.
- Validace odmítá neplatný manifest, duplicitní URL identitu, odkazy mimo nabídku, chybějící assety a základní stopy secrets.
- Budoucí publikační automatizace musí před uploadem validovat a nesmí měnit Access policy při běžné aktualizaci obsahu.
- Cloudflare R2, Worker a Access nejsou v této capability implementovány ani konfigurovány.

## Navazující práce

- Založit centrální publikační infrastrukturu a její bezpečně spravovaný workflow.
- Při založení prvního nabídkového projektu ověřit manifest a publikační kontrakt na reálné nabídce.
