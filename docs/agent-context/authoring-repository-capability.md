# Authoring repository capability

Capability `authoring-repository` zavádí jednotný kontrakt pro specializované i
orchestrační authoring repozitáře Flexideo.

## Zdroj pravdy a minimální strom

```text
product/
├── README.md
├── skills/
├── tools/
├── contracts/
└── tests/
```

- `product/` je jediný autoritativní zdroj publikovatelného authoring produktu.
- Produktové skills vznikají přímo v `product/skills/`; `.agents/skills/` v kořeni
  obsahuje pouze skills pro údržbu workspace, build, testování a publikaci.
- `product/tools/` obsahuje sdílené produktové nástroje, `product/contracts/` strojově
  čitelná rozhraní a registry a `product/tests/` release testy a evaly produktu.
- `public/` a `product/` se vzájemně vylučují.
- Build produktu validuje a balí obsah `product/`; Product Repository Sync pouze
  synchronizuje tuto hranici do samostatného Product repository. Registr dovedností
  spotřebovává ověřené vydání, nikoli interní kořen authoring workspace.

## Specializovaný authoring

Specialista vlastní význam, workflow, kontrakty a validace jedné vrstvy. Vydává registry
schopností s identitou, verzí, zralostí, kompatibilitou a vstupně-výstupními kontrakty.
Runtime repozitář zůstává zdrojem technických omezení; klientský projekt zůstává zdrojem
zadání, akceptace a výsledných projektových definic.

## Orchestrační authoring

Orchestrátor je nadřazená authoring entita pro změny celé aplikace. Jeho produkt vlastní:

- interpretaci záměru a plán napříč vrstvami;
- discovery a resolver registrů specializovaných authoring produktů;
- handoff kontrakty, pořadí kroků, zámky, trace a vyhodnocení výsledku.

Nevlastní a nekopíruje produktové skills specialistů. `Flexideo-orchestrator` je
referenční orchestrátor: z registrovaných authoring produktů jednotlivých vrstev si
aktualizuje dostupné schopnosti a sestavuje vlastní orchestrační produkt.

## Instalace a ověření

```bash
python toolkit/agent-infrastructure/repository_architecture.py install-capability . --name authoring-repository
python toolkit/agent-infrastructure/repository_architecture.py validate .
```

Instalace zahrnuje capability `product-repository` a `development-testing`. Nezakládá
remote repository, credentials ani publish workflow. Tyto kroky vyžadují samostatné,
explicitní rozhodnutí a konfiguraci.
