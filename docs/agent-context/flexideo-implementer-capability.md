# Aktivace lokálního Flexideo Implementátora

Capability `flexideo-implementer` přidá do libovolného existujícího klientského
repozitáře tenký zavaděč externího produktu. Funguje také v rozpoznané Project
Memory 0.1/0.2. Helper vlastní pouze zavaděč a jeho instalaci; FCL vlastní mapu,
bootstrap a resolution, Orchestrátor sestavení produktů. Rozhodnutí:
[ADR-0014](decisions/0014-flexideo-implementer-project-activation.md).

## Instalace do klientského projektu

Z kořene helperu:

```powershell
python toolkit/agent-infrastructure/repository_architecture.py install-capability "<projekt>" --name flexideo-implementer
```

Stejný zavaděč se automaticky přidává při instalaci `client-project` (také v
Project Memory) a při nativní instalaci jeho závislosti pro `project-documentation`.
Samostatná instalace kopíruje pouze:

```text
.agents/skills/activate-flexideo-implementer/SKILL.md
.agents/skills/activate-flexideo-implementer/agents/openai.yaml
toolkit/skills/activate-flexideo-implementer/activate.py
```

Generuje manifest `.agents/capabilities/flexideo-implementer.json` s verzí kontraktu,
provenancí helperu a kontrolními součty. Nevyžaduje lokálně nainstalovaný produkt.
Samostatná instalace nemění `AGENTS.md`, obsah projektu, analytiku, definitions,
credentials, revize ani sémantická metadata Project Memory. Při neznámé nebo
neúplné Memory odmítne zápis. Balík `client-project` navíc zachovává svůj vlastní
neanalytický obal podle ADR-0013; tento rozsah se novou capability nerozšiřuje.

## Umístění produktu na počítači

Při prvním požadavku na Implementátor bez existující registrace se projektová
dovednost zeptá na cestu přímo v chatu VS Code. Použije dostupný dialogový nástroj
agenta, nebo běžnou textovou otázku. Zeptá se na složku obsahující `fcl/` a
`assembly.lock.json` a oznámí, že ji po ověření uloží pro další projekty na počítači.
Po odpovědi sama provede registraci a zopakuje aktivaci; uživatel nemusí psát
registrační příkaz. Již výslovně zadanou cestu nevyžaduje podruhé. Bez odpovědi
nepokračuje odhadem a neprochází disk.

Registrace je jednorázová pro uživatele na počítači. Pro ruční nebo automatizované
nastavení je nadále dostupný příkaz z helperu i ze zkopírovaného projektového nástroje:

```powershell
python toolkit/skills/activate-flexideo-implementer/activate.py register --root "C:/flexideo/local-products/flexideo-implementer"
```

Registrace nejprve ověří skutečnou sestavu. Na Windows používá
`%LOCALAPPDATA%/Flexideo/local-products.json` (fallback `~/AppData/Local/`),
na ostatních systémech `$XDG_CONFIG_HOME/Flexideo/local-products.json` nebo
`~/.config/Flexideo/local-products.json`.

```json
{
  "schema_version": 1,
  "products": {
    "flexideo-implementer": {
      "root": "C:/flexideo/local-products/flexideo-implementer"
    }
  }
}
```

Registr je uživatelská konfigurace mimo klientský repozitář. Obsahuje pouze
umístění, nikoli secrets. Ostatní registrované produkty se zachovají; změna na
jiné umístění vyžaduje `--replace`. Chybná sestava nic nezaregistruje a zápis
registru je atomický. `--registry <soubor>` umožňuje explicitní izolovanou konfiguraci.

## Aktivace v projektu nebo z jiného pracovního adresáře

Z kořene klientského projektu:

```powershell
python toolkit/skills/activate-flexideo-implementer/activate.py activate --project .
```

Při spuštění absolutní cestou z jiné složky lze `--project` vynechat: kořen se
určí podle umístění instalovaného nástroje v projektu. Explicitní `--project`
má přednost. Jednorázové `--assembly <cesta>` má přednost před registrem a registr
nemění. Nástroj neskenuje disk ani nepoužívá náhradní instalaci.

Výsledek `READY_FOR_BOOTSTRAP` obsahuje kořen projektu, `assembly_id`, cestu k
produktovému `AGENTS.md` a `fcl/skills/resolve-flexideo-authoring-request/SKILL.md`.
**Agent musí oba produktové soubory skutečně přečíst.** Nástroj pouze ověří sestavu
jejím FCL `verify`; sám neklasifikuje úkol, nenačítá všechny skills a nic neimplementuje.
Vrací `execution: NOT_STARTED` a nemění klientský projekt ani instalaci.

Ve VS Code zpřístupní kanonickou projektovou skill použitý agent/konektor. Pro
hosta s jiným discovery mechanismem použijte příslušný explicitně zvolený renderer
helperu. Nové platformní konektory se samotnou instalací nevytvářejí. Agent musí
mít oprávnění ke čtení externího produktu a běhu Python verifieru; registrace tato
oprávnění neuděluje a nepřidává zapisovatelný root produktu.

## Aktualizace a diagnostika

- Instalaci lze opakovat; řízené soubory se aktualizují jen z předchozího
  zaznamenaného obsahu. Lokální úpravy nebo cizí soubory se odmítnou i s `--force`.
- Preflight zkontroluje celý balík před zápisem, při I/O chybě obnoví předchozí
  soubory. Kontrolní součty tolerují pouze převod Git LF/CRLF.
- `repository_architecture.py validate <projekt>` kontroluje i případnou instalaci
  zavaděče, nikoli dostupnost produktu na cizím počítači. CI registr nepotřebuje.
- Chybějící registr/profil vrací `NOT_CONFIGURED`; neplatný registr `INVALID_REGISTRY`,
  nepřístupný host `BLOCKED_HOST_ACCESS`; chybějící, neplatná nebo neověřitelná
  sestava odpovídající `ASSEMBLY_*`, `INVALID_ASSEMBLY` či `VERIFICATION_FAILED`.
- `activate --expected-assembly <id>` odmítne změněnou sestavu stavem `ASSEMBLY_CHANGED`.
  Produkt aktualizujte mezi chaty. Session a výstupy patří mimo instalaci, podle
  pravidel klientského projektu a výrobce artefaktu.
- `register` a `activate` vracejí JSON, při úspěchu exit 0, při odmítnutí exit 2.
  Přístup k prostředí, účtu a instance nástrojům se ověřuje až v odborné vrstvě.
