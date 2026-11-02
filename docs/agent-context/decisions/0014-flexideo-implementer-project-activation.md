# ADR-0014: Projektový zavaděč externího Flexideo Implementátora

- Stav: accepted
- Datum: 2026-11-02
- Scope: shared
- Vlastník: Repository-helper
- Nahrazuje: —
- Nahrazeno: —

## Kontext a problém

Vlastník schválil capability helperu, kterou lze nakopírovat do libovolného
klientského repozitáře včetně Project Memory a aktivovat z něj lokální FCL produkt.
Umístění instalace se může lišit mezi počítači a klientské repozitáře neleží
nutně vedle produktů. ADR-0013 nadále vymezuje neanalytický klientský obal.

## Rozhodovací kritéria

Přenositelnost klientských repozitářů, jediné vlastnictví FCL mapy a dovedností,
zachování projektových pravidel a sémantiky Memory, řízená aktualizace zavaděče.
Rozhodovací brána: skutečné alternativy, dlouhodobý kontrakt, více konzumentů
a riziko opačné změny bez znalosti důvodu (4 ze 4).

## Zvažované možnosti

### Kopírovat odborné skills a absolutní cestu do projektů

Duplikuje produkt, váže repozitář na počítač a vyžaduje aktualizaci všech projektů.

### Instalovat tenký zavaděč a používat uživatelský registr umístění

Oddělí přenositelné projektové vybavení od lokální konfigurace a verzované sestavy.

## Rozhodnutí a důvody

Přijímá se druhá možnost: capability `flexideo-implementer`, projektová skill
`activate-flexideo-implementer`, přenositelný nástroj pod `toolkit/skills/` a
spravovaný instalační manifest pod `.agents/capabilities/`. Instalace je dostupná
samostatně a automaticky s klientským balíkem. Známá Memory 0.1/0.2 je explicitně
povolena; neznámá nebo neúplná se odmítne před zápisem.

Umístění produktu registruje uživatel jednou pro svůj počítač, mimo repozitáře.
Aktivace ověří sestavu jejím FCL verifierem a vrátí explicitní cesty k instrukcím
a bootstrapu, které musí agent přečíst. FCL rozhoduje o vrstvách a schopnostech,
Orchestrátor produkty sestavuje; helper nic z této logiky nepřebírá.

## Důsledky

Samostatná instalace nemění pravidla, obsah ani sémantiku klientského projektu.
Součty a rollback chrání řízené soubory, lokální změny se nepřepisují ani s force.
Produkt se nekopíruje do projektu. Registr není secrets store ani povolení k práci
s instancí. Host musí mít skutečný přístup do externí instalace. Změna sestavy
vyžaduje obnovení bootstrapu v novém chatu; aktivace sama není načtení ani implementace.

## Navazující práce

Ověřit v samostatném klientském sezení vybraného VS Code agenta. Automatické testy
ověřují instalaci a aktivaci, nikoli nezávislé porozumění zadání modelem.
