# ADR-0010: Přenositelná capability projektové dokumentace

- Stav: accepted
- Datum: 2026-10-28
- Vlastník: správci Repository-helper
- Scope: shared
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Project Memory po ADR-0065 Orchestrátoru odděluje analytický životní cyklus epiků od sdílené
dokumentace aplikace v `docs/`. Současně Flexideo používá definition-driven architekturu:
XDS/FDT/DAD tvoří datový základ, intranetové x-item/settings skládají aplikační funkce a COMEX
je promítá do uživatelského rozhraní. Klientské repozitáře potřebují jednotný přenositelný
postup, který tyto vrstvy propojí bez vzniku druhého zdroje pravdy.

Původní ADR-0009 dovolovalo do Project Memory instalovat pouze orientační client-project skill.
Nová capability musí být užitečná i v Memory, ale nesmí převzít provisioning ani sémantické
operace MCP.

## Zvažované možnosti

- Udržovat projektovou dokumentaci ad hoc v každém repozitáři: rychle vzniknou rozdílné
  struktury a kopie analytiky.
- Generovat kompletní dokumentaci přímo z XDS/intranetu: ztratí se business význam a vznikne
  falešný dojem úplnosti runtime/UI.
- Zavést přenositelný skill s detailní referencí a read-only validátorem, který respektuje
  autority jednotlivých vrstev.

## Rozhodnutí

Přijímá se třetí varianta jako capability `project-documentation` a skill
`maintain-project-documentation`.

V Project Memory se capability smí instalovat, protože přidává pouze:

- skill;
- jeho přenositelnou referenci;
- read-only validační/inventory nástroj pod `toolkit/skills/`.

Installer v tomto režimu nemění AGENTS, `project/epics/`, `context/`,
`.project-memory/`, D1 metadata ani stav projektu.

Kurátorovaný dokumentační strom je `docs/`; generovaná FDT reference zůstává pod
`docs/reference/fdt/`. Budoucí reference intranetu nebo COMEXu vyžadují samostatného
producenta/manifest a tato capability je sama nevyrábí.

## Důsledky

Repository-helper získává první explicitně povolenou obsahovou capability pro Project Memory,
ale jen v oblasti již vlastněné kontraktem jako sdílená dokumentace. ADR-0009 zůstává platné
pro provisioning a analytickou strukturu; jeho věta o jediné povolené orientační capability je
tímto rozhodnutím rozšířena o `project-documentation`.

Datová a UI pravda se nadále neodvozuje z Markdownu: XDS/Replicator/Intranet/COMEX si ponechávají
vlastnictví. Dokumentace propojuje jejich potvrzené výstupy a explicitně uvádí neověřené mezery.
