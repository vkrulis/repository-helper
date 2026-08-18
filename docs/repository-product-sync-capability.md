# Product Repository Sync – obecné zadání schopnosti pro správce repozitářů

> **Stav dokumentu:** návrh cílové schopnosti / implementační zadání pro Codex  
> **Účel:** obecný, opakovaně použitelný mechanismus pro oddělení soukromého pracovního repozitáře od oficiálního produktového repozitáře při zachování řízené obousměrné synchronizace  
> **Klíčové slovo:** `product`  
> **Synchronizační hranice:** `product/` v pracovním repozitáři ↔ root cílového produktového repozitáře  
> **Výchozí větve:** `develop ↔ develop`, `main ↔ main`  
> **Platforma:** GitHub / GitHub Actions / GitHub App  
> **Status implementace:** tento dokument popisuje požadovanou schopnost; nepředpokládá, že již existuje

---

## 1. Cíl

Navrhnout a následně implementovat ve správci repozitářů obecnou schopnost **Product Repository Sync**, která umožní používat dva logicky oddělené GitHub repozitáře:

1. **Workspace repository** – pracovní, typicky privátní repozitář autora nebo interního týmu.
2. **Product repository** – oficiální repozitář obsahující pouze produktový kód, oficiální dokumentaci, testy a další soubory určené ke sdílení, sestavení nebo distribuci.

Pracovní repozitář může obsahovat libovolné interní vývojové podklady, například:

- `.agents/`
- `.skills/`
- `.vscode/`
- interní dokumentaci,
- analytické materiály,
- experimenty,
- lokální utility,
- pracovní poznámky,
- AI kontext,
- pomocné skripty,
- další neveřejné soubory.

V pracovním repozitáři musí existovat vyhrazená podsložka:

```text
product/
```

Obsah této složky představuje **jedinou produktovou projekci**, která se synchronizuje s oficiálním Product repository.

Základní kontrakt:

```text
Workspace repository
│
├── .agents/
├── .skills/
├── .vscode/
├── internal-docs/
├── research/
├── ...
│
└── product/
    ├── src/
    ├── tests/
    ├── docs/
    ├── README.md
    └── ...
          │
          │ synchronizace
          ▼
Product repository
│
├── src/
├── tests/
├── docs/
├── README.md
└── ...
```

Platí:

```text
Workspace/product/  ==  Product repository /
```

z hlediska synchronizovaného produktového obsahu.

---

# 2. Základní princip

Workspace repository je místem, kde vlastník může pohodlně pracovat s kompletním vývojovým kontextem.

Product repository je místem, kde se nachází pouze oficiální produktová podoba a kde mohou pracovat také další oprávnění přispěvatelé.

Mechanismus musí podporovat oba směry:

```text
Workspace A / product/
        │
        │ publish
        ▼
Product B / root
```

a:

```text
Product B / root
        │
        │ import
        ▼
Workspace A / product/
```

Nejde však o nekontrolovaný obousměrný filesystem mirror.

Jde o **řízenou Git synchronizaci se znalostí větví, původu změny, historie a bezpečnostních hranic**.

---

# 3. Terminologie

## 3.1 Workspace repository

Pracovní repozitář, v příkladech označovaný jako **Repo A**.

Typicky:

- privátní,
- plný vývojový workspace,
- obsahuje interní a neveřejné soubory,
- obsahuje `product/`,
- externí přispěvatelé do něj nemusí mít přístup.

## 3.2 Product repository

Oficiální repozitář, v příkladech označovaný jako **Repo B**.

Typicky:

- veřejný, interní nebo privátní podle potřeby produktu,
- obsahuje pouze produktový obsah,
- jeho root odpovídá `product/` ve Workspace repository,
- může přijímat Pull Requesty dalších přispěvatelů.

## 3.3 Product boundary

Adresář:

```text
product/
```

ve Workspace repository.

Je to **tvrdá synchronizační hranice**.

Synchronizační mechanismus nesmí při A → B publikaci číst, exportovat ani kopírovat soubory mimo tuto složku, pokud to není výslovně součást jiné administrativní operace.

## 3.4 Outbound sync / Publish

Směr:

```text
Workspace/product/ → Product/
```

## 3.5 Inbound sync / Import

Směr:

```text
Product/ → Workspace/product/
```

---

# 4. Hlavní invarianty

Implementace musí dodržovat následující invarianty.

## 4.1 `product/` je jediná synchronizovaná oblast Workspace repository

Z Product repository se nikdy nesynchronizuje například:

```text
Workspace/.agents/
Workspace/.skills/
Workspace/internal-docs/
Workspace/research/
```

Stejně tak se tyto adresáře nikdy nesmějí publikovat do Product repository.

## 4.2 Product repository reprezentuje root obsahu `product/`

Mapování je:

```text
Workspace/product/src/       → Product/src/
Workspace/product/docs/      → Product/docs/
Workspace/product/README.md  → Product/README.md
```

Nikoli:

```text
Product/product/src/
```

## 4.3 Synchronizace je branch-aware

Každá zdrojová větev musí být explicitně mapována na cílovou větev.

Výchozí konfigurace:

```text
Workspace/develop  ↔ Product/develop
Workspace/main     ↔ Product/main
```

Feature větve se standardně automaticky nesynchronizují.

## 4.4 Synchronizace nesmí vytvořit nekonečný cyklus

Například:

```text
A → B → A → B → A ...
```

musí být konstrukčně vyloučeno.

## 4.5 Každá automatická změna musí být dohledatelná

Musí být možné zjistit:

- odkud synchronizace vznikla,
- zdrojový repozitář,
- zdrojovou větev,
- zdrojový commit SHA,
- cílový repozitář,
- cílovou větev,
- čas synchronizace,
- výsledný commit nebo Pull Request,
- stav synchronizace.

## 4.6 Privátní Workspace repository nesmí být zpřístupněno přispěvatelům Product repository

Přispěvatel do B smí přispět do produktu, ale nesmí tím automaticky získat možnost číst jiné části A.

---

# 5. Doporučený vývojový workflow

## 5.1 Práce vlastníka ve Workspace repository

Běžná práce probíhá například:

```text
feature/*
   ↓
PR
   ↓
develop
   ↓
PR
   ↓
main
```

Vlastník může ve feature větvi současně měnit:

```text
.agents/
.skills/
internal-docs/
product/
```

Dokud ale nedojde k merge do synchronizované větve, Product repository se nemění.

### Merge do `develop`

```text
Workspace/feature-x
       ↓
Workspace/develop
       ↓
Product Sync
       ↓
Product/develop
```

### Merge do `main`

```text
Workspace/develop
       ↓
Workspace/main
       ↓
Product Sync
       ↓
Product/main
```

---

# 6. Workflow externího nebo jiného oprávněného přispěvatele

Přispěvatel nemusí znát ani vidět Workspace repository.

Pracuje standardním GitHub způsobem pouze s Product repository:

```text
Product repository
   │
   ├── branch
   │
   ├── fork
   │
   └── Pull Request
          ↓
        review
          ↓
        merge
```

Například:

```text
Product/feature-x
       ↓
PR → Product/develop
       ↓
merge
       ↓
Product Sync Import
       ↓
Workspace/sync/product-...
       ↓
PR → Workspace/develop
```

Změna se tedy může dostat zpět do pracovního repozitáře, aniž by přispěvatel dostal přístup k jeho neveřejné části.

---

# 7. Důležitý princip pro B → A

## 7.1 Výchozí režim: vždy Pull Request

Inbound synchronizace z Product repository nemá standardně zapisovat přímo do:

```text
Workspace/develop
Workspace/main
```

Místo toho má vytvořit integrační větev, například:

```text
sync/product/develop/<short-sha>
```

a Pull Request:

```text
sync/product/develop/<short-sha>
    ↓
Workspace/develop
```

Pull Request musí jasně uvádět zdroj:

```text
Source repository: owner/product-repo
Source branch: develop
Source commit: abcdef123456...
Sync direction: product → workspace
Product path: product/
```

Tím je zachováno:

- code review,
- CI,
- kontrola konfliktů,
- historie,
- dohledatelnost,
- možnost změnu odmítnout.

## 7.2 Volitelný režim do budoucna

Po dostatečném ověření může být pro vybrané repozitáře povolen:

```text
inbound.autoMerge: true
```

Auto-merge však smí proběhnout pouze tehdy, pokud:

- vznikl čistý diff,
- neexistuje konflikt,
- požadované status checks prošly,
- ruleset dovoluje merge,
- synchronizace je jednoznačně identifikovaná,
- není detekován drift nebo konkurenční změna.

Toto není požadavek pro první verzi.

---

# 8. A → B Publish

Outbound synchronizace se má spustit po úspěšném push/merge do explicitně mapované větve Workspace repository.

Výchozí mapování:

```yaml
branches:
  develop: develop
  main: main
```

Proces:

1. přijmout událost změny Workspace větve,
2. zjistit, zda je větev synchronizovaná,
3. načíst konfiguraci páru repozitářů,
4. ověřit existenci `product/`,
5. získat aktuální SHA Workspace větve,
6. získat aktuální stav odpovídající větve Product repository,
7. vypočítat projekci `product/`,
8. porovnat ji s Product root,
9. pokud není žádný rozdíl, skončit jako `NO-OP`,
10. pokud rozdíl existuje, připravit změnu,
11. provést validace,
12. zapsat změnu do odpovídající větve B podle zvoleného publikačního režimu,
13. uložit metadata synchronizace.

---

# 9. Režim publikace A → B

Podporovat dva režimy.

## 9.1 `direct`

Pro technický mirror, kde Product větev dovoluje GitHub App zapisovat přímo.

```yaml
outbound:
  mode: direct
```

Vhodné pouze tam, kde:

- jsou pravidla větve nastavena tak, že konkrétní GitHub App může bezpečně provádět synchronizační zápisy,
- publish je plně automatizovaný,
- není požadován druhý review krok.

## 9.2 `pull-request`

Preferovaný konzervativní režim:

```yaml
outbound:
  mode: pull-request
```

Mechanismus vytvoří větev v B:

```text
sync/workspace/develop/<short-sha>
```

a PR do:

```text
Product/develop
```

Po ověření lze PR mergovat ručně nebo přes auto-merge.

Správce repozitářů musí umožnit režim nastavit per repository.

---

# 10. B → A Import

Inbound synchronizace se spouští pouze nad stabilními mapovanými větvemi Product repository.

Typicky:

```text
push do Product/develop
push do Product/main
```

nebo ekvivalentní událost po merge Pull Requestu.

Proces:

1. přijmout změnu Product repository,
2. určit, zda Product repository patří k registrovanému Workspace repository,
3. určit mapovanou Workspace větev,
4. ověřit původ změny,
5. zjistit, zda nejde pouze o commit právě vytvořený outbound synchronizací,
6. získat Product root,
7. připravit jeho projekci do `Workspace/product/`,
8. získat cílovou Workspace větev,
9. vypočítat diff,
10. pokud není změna, skončit `NO-OP`,
11. detekovat konflikt nebo drift,
12. založit `sync/product/...` větev,
13. změnit pouze `product/`,
14. vytvořit commit,
15. založit PR do odpovídající Workspace větve,
16. spustit CI,
17. uložit provenance metadata.

---

# 11. Prevence synchronizačního ping-pongu

Toto je kritická součást návrhu.

Pouhé použití textu v commit message typu:

```text
[skip sync]
```

nesmí být jediným mechanismem.

Synchronizace musí pracovat s jednoznačnými metadaty.

Minimálně ukládat:

```text
sync-id
direction
source-repository
source-branch
source-sha
target-repository
target-branch
target-sha
timestamp
```

Doporučený identifikátor:

```text
product-sync:<source-owner>/<source-repo>:<source-branch>:<source-sha>
```

Při přijetí nové události správce nejprve zjistí, zda:

- daný zdrojový SHA již byl aplikován,
- aktuální commit vytvořila synchronizační aplikace,
- obsah cílové projekce již odpovídá zdroji.

Výsledkem může být:

```text
SYNCED
NO-OP
CONFLICT
FAILED
PENDING-PR
BLOCKED
```

## 11.1 Idempotence

Opakované zpracování stejné GitHub webhook delivery nebo stejného SHA nesmí vést k dalším commitům.

Platí:

```text
apply(sync X)
apply(sync X)
apply(sync X)
```

musí mít stejný výsledný stav jako:

```text
apply(sync X)
```

---

# 12. Drift

Drift znamená, že:

```text
Workspace/product/
```

a:

```text
Product/
```

se rozešly způsobem, který nelze bezpečně vysvětlit poslední známou synchronizací.

Správce musí umět drift detekovat.

Příklady:

- změna vznikla současně v A i B,
- někdo provedl přímý push do chráněné větve B,
- sync PR z B do A ještě nebyl mergnut, ale A mezitím změnilo stejný soubor,
- historie byla přepsána,
- cílová větev byla force-pushnuta.

Při driftu se nesmí slepě přepsat jedna strana.

Výchozí chování:

```text
BLOCK + vytvořit diagnostiku
```

Případně vytvořit PR s konfliktem, pokud je možné změnu reprezentovat standardním Git merge procesem.

---

# 13. Konflikty

Konflikt se má řešit standardním Git způsobem.

Synchronizační mechanismus nesmí automaticky rozhodovat významový konflikt jen podle toho, která změna je novější.

Příklad:

```text
A/product/src/file.cs
```

a:

```text
B/src/file.cs
```

byly nezávisle změněny od posledního společného synchronizačního bodu.

Výsledek:

```text
CONFLICT
```

a člověk nebo nadřazený agent rozhodne, jak má výsledný stav vypadat.

AI může konflikt:

- vysvětlit,
- navrhnout merge,
- navrhnout řešení,

ale automatická synchronizační vrstva musí zachovat kontrolu a nesmí významovou změnu svévolně vybrat.

---

# 14. Konfigurace

Ve Workspace repository zavést konfigurační soubor.

Doporučený název:

```text
.repo-manager/product-sync.yml
```

Minimální návrh:

```yaml
version: 1

product:
  path: product

target:
  provider: github
  repository: owner/product-repository

branches:
  develop: develop
  main: main

outbound:
  enabled: true
  mode: pull-request

inbound:
  enabled: true
  mode: pull-request
  autoMerge: false

sync:
  deleteRemovedFiles: true
  requireCleanProjection: true
```

## 14.1 `product.path`

Pro tuto schopnost je konvenční a výchozí hodnota vždy:

```yaml
product:
  path: product
```

Správce může interně podporovat budoucí rozšíření, ale první implementace má standardizovat právě klíčové slovo:

```text
product
```

Není cílem podporovat libovolné množství alternativních adresářů.

## 14.2 `target.repository`

Povinné nastavení cílového Product repository:

```yaml
target:
  repository: flexideo/example-product
```

## 14.3 `branches`

Explicitní mapování.

Například:

```yaml
branches:
  develop: develop
  main: main
```

Budoucí varianta může umožnit:

```yaml
branches:
  develop: integration
  main: main
```

První implementace ale musí být optimalizována na jednoduché shodné mapování.

---

# 15. Co se synchronizuje

Celý strom:

```text
Workspace/product/**
```

na:

```text
Product/**
```

a zpět.

Tím `product/` samo funguje jako allowlist.

Není vhodné koncipovat první verzi stylem:

> synchronizuj celý Workspace repository a pak blacklistem vynechej `.agents`, `.skills`, ...

To by zvyšovalo riziko zveřejnění nového interního adresáře.

Bezpečnostní model má být opačný:

```text
NIC mimo product/ není součástí produktové synchronizace.
```

---

# 16. Mazání souborů

Synchronizace musí podporovat odstranění souboru.

Pokud je v A odstraněno:

```text
product/docs/old.md
```

musí publish do B odstranit:

```text
docs/old.md
```

Stejně tak při legitimním inbound importu.

Mazání však smí proběhnout pouze v synchronizované projekci.

Synchronizační mechanismus nikdy nesmí provést obecné:

```bash
rm -rf target
```

nad pracovním repozitářem nebo jiným adresářem mimo připravený izolovaný staging prostor.

---

# 17. Bezpečnostní model

## 17.1 Preferovaná autentizace: GitHub App

Pro cross-repository automatizaci preferovat GitHub App.

Důvody:

- instalace se omezuje na zvolené repozitáře,
- oprávnění lze explicitně omezit,
- používají se krátkodobé installation access tokens,
- akce jsou identifikovatelné jako aktivita aplikace,
- řešení je vhodnější pro opakované použití na více repository pairs než osobní PAT.

Nepoužívat osobní classic PAT jako výchozí architektonický mechanismus.

## 17.2 Least privilege

GitHub App a GitHub Actions workflow mají mít pouze oprávnění nutná pro danou operaci.

Typicky může být potřeba:

```text
Contents: Read / Write
Pull requests: Read / Write
Metadata: Read
```

Přesný rozsah musí Codex odvodit podle skutečných REST/GraphQL operací implementace.

Nesmí přidat například:

```text
Administration: Write
Issues: Write
Actions: Write
Secrets: Write
```

pokud k tomu není doložená potřeba.

## 17.3 `GITHUB_TOKEN`

Uvnitř jednotlivých workflow používat vestavěný `GITHUB_TOKEN` tam, kde stačí přístup k aktuálnímu repository.

Cross-repository operace musí být řešeny oddělenou autorizací s minimálním rozsahem.

## 17.4 Nezpřístupňovat credential Workspace repository nedůvěryhodnému PR kódu

PR z forku nebo od externího přispěvatele nesmí během validačního workflow získat credential, který umožňuje čtení privátního Workspace repository.

Externí PR má standardně:

```text
read-only validation
```

Privilegovaná synchronizace se spouští až nad důvěryhodnou změnou po merge do chráněné Product větve, nebo přes centrální správce.

## 17.5 Workflow soubory jsou bezpečnostně citlivé

Změny v:

```text
.github/workflows/**
```

a v souborech spravujících synchronizační konfiguraci musí mít zvýšenou úroveň review.

Doporučit například CODEOWNERS nebo odpovídající ruleset.

---

# 18. Preferovaná cílová architektura správce repozitářů

Pro postupné nasazení na více repozitářů má být finálním směrem centrální **Repository Manager / Product Sync Controller**.

```text
                       GitHub
                         │
                   webhook events
                         │
                         ▼
             Product Sync Controller
                         │
                  GitHub App auth
                 ┌───────┴────────┐
                 ▼                ▼
          Workspace A         Product B
             private           official
```

GitHub App se instaluje pouze na repository pairs, které má spravovat.

Controller:

- přijímá webhook události,
- ověřuje podpis webhooku,
- identifikuje repository pair,
- načte konfiguraci,
- získá krátkodobý installation token,
- provede synchronizační operaci,
- zaznamená stav.

Tím není nutné ukládat credential s přístupem k privátnímu A přímo do B.

To je preferovaný model zejména pokud:

- B je public repository,
- do B přispívají externí uživatelé,
- mechanismus se použije pro více projektů,
- správa se má centralizovat.

---

# 19. Přechodná jednodušší implementace

První verze může být implementována převážně pomocí GitHub Actions přímo v repository pair.

Je však nutné:

- chránit workflow soubory,
- používat GitHub App místo univerzálního osobního PAT,
- omezit permissions,
- nepouštět privileged sync v kontextu nedůvěryhodného PR,
- jednoznačně označovat synchronizační commity,
- zabránit smyčkám.

Tato varianta je vhodná pro pilotní ověření.

Při růstu počtu spravovaných repository pairs má být synchronizační logika přesunuta do centrální capability, nikoli kopírována v mnoha mírně odlišných verzích workflow.

---

# 20. GitHub webhooky v centrálním modelu

GitHub App má odebírat pouze potřebné události.

Minimálně zvážit:

```text
push
pull_request
installation
installation_repositories
```

Pro samotnou synchronizaci může být dostatečný `push` nad mapovanými větvemi.

PR eventy mohou sloužit:

- ke komentování stavu,
- vazbě na původní PR,
- provenance,
- diagnostice.

Webhook handler musí:

1. ověřit `X-Hub-Signature-256`,
2. odmítnout nevalidní podpis,
3. uložit GitHub delivery ID,
4. být idempotentní,
5. rychle potvrdit převzetí eventu,
6. vlastní synchronizační operaci vykonat odděleně, pokud je architektura asynchronní.

---

# 21. Branch protection a rulesets

Pro:

```text
develop
main
```

použít GitHub rulesets nebo branch protection podle možností účtu.

Preferované vlastnosti:

- zakázat force push,
- zakázat delete,
- vyžadovat Pull Request pro lidské změny,
- požadovat status checks,
- požadovat review tam, kde je to vhodné,
- chránit změny synchronizačních workflow,
- definovat úzkou bypass výjimku pouze pro synchronizační GitHub App, pokud je vyžadován `direct` režim.

Při správě většího množství repozitářů preferovat centralizované organization rulesets, pokud to GitHub plán umožňuje.

---

# 22. Concurrency

Na jednu repository pair + větev smí současně běžet pouze jedna synchronizace.

Doporučený logický concurrency key:

```text
product-sync:<workspace>:<product>:<branch>
```

Například:

```text
product-sync:flexideo/repo-a:flexideo/repo-b:develop
```

Pokud přijde několik commitů rychle za sebou, musí systém zpracovat konzistentní výsledný stav a nesmí nechat starší job přepsat novější stav.

---

# 23. Stavový model

Každá synchronizace má mít stav.

Minimální enum:

```text
RECEIVED
VALIDATING
NO-OP
PREPARING
PR-CREATED
WAITING-REVIEW
SYNCED
CONFLICT
BLOCKED
FAILED
```

Případně:

```text
SUPERSEDED
```

pokud novější synchronizace nahradila starší pending operaci.

---

# 24. Audit a provenance

Každý sync vytvořený managerem má mít lidsky čitelnou stopu.

Doporučená commit message:

```text
sync(product): workspace/develop → product/develop

Source-Repository: owner/workspace
Source-Branch: develop
Source-SHA: 1234567890abcdef
Sync-Direction: outbound
Sync-Id: ...
```

Inbound:

```text
sync(product): product/develop → workspace/product

Source-Repository: owner/product
Source-Branch: develop
Source-SHA: abcdef1234567890
Sync-Direction: inbound
Sync-Id: ...
```

PR body má obsahovat stejnou informaci.

---

# 25. `.github` v Product repository

Pokud je:

```text
Workspace/product/.github/
```

součástí produktu, standardně se synchronizuje stejně jako ostatní obsah.

Je však nutné rozlišit dvě kategorie:

1. **product-owned workflows** – CI, build, release apod.; patří do produktové projekce,
2. **repo-manager bootstrap / security configuration** – může být spravována centrálně.

Codex nemá bezdůvodně zavádět dvojí zdroj pravdy pro stejné workflow soubory.

Pokud se první verze rozhodne umístit sync workflow přímo do B, musí být jasně dokumentováno, zda je workflow součástí `product/`, nebo manager-owned bootstrap artefakt.

Preferovaný dlouhodobý model je držet vlastní synchronizační engine mimo produktový obsah.

---

# 26. Validace před synchronizací

Správce musí podporovat hook pro validaci.

Minimálně:

```text
product directory exists
target configured
branch mapping exists
target repository reachable
authentication valid
no forbidden path escape
diff computable
```

Dále volitelně projektové validační příkazy:

```yaml
validation:
  outbound:
    - command: dotnet test
  inbound:
    - command: dotnet test
```

Konkrétní příkaz není součástí obecného sync mechanismu.

Repository-specific validace musí být deklarativně konfigurovatelná nebo delegovaná existujícím CI.

---

# 27. Dry-run

Capability musí mít režim:

```text
dry-run
```

Dry-run:

- nic necommitne,
- nic nepushne,
- nezaloží PR,
- ukáže plánovanou větev,
- ukáže počet přidaných / změněných / odstraněných souborů,
- vypíše source SHA,
- vypíše target SHA,
- upozorní na konflikt nebo drift.

Dry-run je povinný pro bezpečné první zapnutí na novém repository pair.

---

# 28. Bootstrap nového repository pair

Správce repozitářů má poskytovat operaci ve smyslu:

```text
Configure Product Repository Sync
```

Codex při aktivaci provede:

1. detekci Workspace repository,
2. ověření `product/`,
3. načtení nebo vytvoření `.repo-manager/product-sync.yml`,
4. vyžádání / použití identifikace Product repository,
5. ověření existence Product repository,
6. ověření GitHub App installation,
7. detekci větví,
8. návrh branch mappingu,
9. dry-run A → B,
10. dry-run B → A,
11. kontrolu rulesetů,
12. vytvoření chybějící infrastruktury,
13. teprve poté enable synchronizace.

Neprovádět destruktivní první sync bez porovnání obou stran.

---

# 29. Počáteční stav existujícího B

Při napojení existujícího Product repository mohou existovat tři případy.

## 29.1 B je prázdné

A je autoritativní pro inicializaci:

```text
A/product → B
```

## 29.2 A/product a B jsou identické

Pouze se založí synchronizační baseline.

## 29.3 A/product a B se liší

Automaticky nic nepřepisovat.

Vytvořit report:

```text
ONLY-IN-WORKSPACE
ONLY-IN-PRODUCT
MODIFIED
```

a vyžadovat explicitní rozhodnutí o inicializačním baseline.

---

# 30. Branch baseline

Pro každé mapování uchovávat společný synchronizační bod.

Například:

```yaml
baseline:
  develop:
    workspaceSha: ...
    productSha: ...
  main:
    workspaceSha: ...
    productSha: ...
```

Nemusí být fyzicky uložen v konfiguračním YAML v repository.

Lepší může být interní stav manageru.

Důležité je, aby mechanismus znal poslední potvrzenou synchronizaci a mohl od ní detekovat paralelní změny.

---

# 31. Co nemá první verze řešit

První verzi zbytečně nerozšiřovat o:

- arbitrary N-way repository mesh,
- synchronizaci jednoho `product/` do více Product repository,
- automatické významové řešení merge konfliktů pomocí AI,
- sync každé feature větve,
- synchronizaci issues,
- synchronizaci Projects,
- synchronizaci Discussions,
- synchronizaci Secrets,
- synchronizaci Actions variables,
- release orchestration,
- package publishing,
- deployment.

Tyto oblasti mohou být samostatné capability.

První schopnost má být velmi přesná:

```text
Git repository product tree synchronization
```

---

# 32. Schopnosti Repository Manageru

Repository Manager má po implementaci rozumět následujícím operacím.

## 32.1 Configure

```text
configure product sync
```

Výsledek:

- nakonfigurovaný `product/`,
- target repository,
- branch mappings,
- authentication,
- rules,
- dry-run report.

## 32.2 Status

```text
product sync status
```

Vrací například:

```text
Workspace: owner/repo-a
Product: owner/repo-b

develop:
  state: IN-SYNC
  workspace: abc123
  product: def456
  last-sync: ...

main:
  state: PENDING-PR
  ...
```

## 32.3 Publish

```text
publish product develop
```

Manuální spuštění A → B.

## 32.4 Import

```text
import product develop
```

Manuální spuštění B → A.

## 32.5 Dry run

```text
dry-run product sync develop
```

## 32.6 Diagnose

```text
diagnose product sync
```

Detekuje:

- drift,
- chybějící permissions,
- chybějící GitHub App installation,
- invalid branch mapping,
- konflikty,
- pending PR,
- neuspořádané baseline,
- nedostupné target repository.

## 32.7 Disable / Enable

Umožnit synchronizaci dočasně vypnout bez odstranění konfigurace.

---

# 33. Codex – implementační pravidla

Při implementaci postupuj konzervativně.

## 33.1 Nejprve analyzuj

Nejdříve:

- projdi existující strukturu repository manageru,
- zjisti používaný jazyk a framework,
- zjisti existující abstrakce pro GitHub,
- najdi model repositories, branches, credentials a jobs,
- ověř, zda již existuje GitHub App integrace,
- nepřidávej druhou paralelní GitHub klientskou vrstvu bez potřeby.

## 33.2 Zachovej jednoduché rozhraní

Core model nesmí být svázán přímo s YAML workflow.

Oddělit:

```text
ProductSyncConfig
RepositoryProvider
SyncPlanner
SyncExecutor
SyncStateStore
GitHubAdapter
```

nebo ekvivalentní abstrakce odpovídající existující architektuře projektu.

Nezavádět tyto názvy mechanicky, pokud repository manager už používá jiný konzistentní model.

## 33.3 Plan před execute

Synchronizace má mít interní dvoufázový model:

```text
PLAN
   ↓
VALIDATE
   ↓
EXECUTE
```

`PLAN` musí být možné zobrazit jako dry-run.

## 33.4 Determinismus

Stejné:

```text
source tree + source SHA + target baseline
```

musí vytvořit stejný plán synchronizace.

AI nesmí být potřebná pro běžný sync.

---

# 34. Návrh interního sync planu

Příklad:

```json
{
  "syncId": "product-sync:...",
  "direction": "outbound",
  "workspaceRepository": "owner/repo-a",
  "productRepository": "owner/repo-b",
  "workspaceBranch": "develop",
  "productBranch": "develop",
  "sourceSha": "...",
  "targetSha": "...",
  "operations": [
    {
      "type": "modify",
      "source": "product/src/A.cs",
      "target": "src/A.cs"
    },
    {
      "type": "delete",
      "target": "docs/old.md"
    }
  ]
}
```

Toto je koncept, nikoli předepsaný storage formát.

---

# 35. Retry

GitHub API nebo Git operace mohou selhat přechodně.

Implementace musí rozlišovat:

```text
retryable failure
permanent failure
conflict
authorization failure
configuration failure
```

Retry nesmí vytvářet duplicity díky `syncId` a idempotenci.

---

# 36. GitHub Actions – zásady

Pokud jsou použity Actions:

- explicitně nastavovat `permissions`,
- výchozí permissions držet minimální,
- third-party actions připínat na full commit SHA,
- preferovat GitHub-maintained actions, pokud řeší stejný problém,
- používat concurrency group,
- filtrovat eventy na požadované větve,
- nepouštět cross-repo privileged operaci z nedůvěryhodného PR,
- secrets neposílat do shell commandu způsobem náchylným na injection,
- nepoužívat `pull_request_target` s checkoutem nedůvěryhodného PR kódu bez explicitního bezpečnostního důvodu.

---

# 37. Repository rules

Codex má při bootstrapu umět alespoň vyhodnotit doporučené nastavení.

Pro `develop`:

```text
PR preferred/required
status checks
no force push
no deletion
```

Pro `main`:

```text
PR required
status checks required
review required podle repository policy
no force push
no deletion
```

Synchronizační GitHub App smí dostat bypass pouze pokud je zvolený `outbound.mode: direct`.

Bypass nesmí být automaticky širší než nutné.

---

# 38. Testovací scénáře

Implementovat automatické testy minimálně pro následující případy.

## 38.1 A → B nový soubor

```text
A/product/new.txt
```

se objeví jako:

```text
B/new.txt
```

## 38.2 A → B změna souboru

Obsah se správně přenese.

## 38.3 A → B delete

Smazání v `product/` odstraní soubor v B.

## 38.4 Soubor mimo `product/`

Změna:

```text
A/.skills/foo.md
```

nesmí vytvořit žádnou změnu v B.

## 38.5 B → A nový soubor

```text
B/new.txt
```

se objeví v sync branch jako:

```text
A/product/new.txt
```

## 38.6 B → A nesmí zasáhnout mimo `product/`

Import nesmí změnit:

```text
A/.agents/
A/.skills/
A/internal-docs/
```

## 38.7 Loop prevention

Commit vytvořený A → B nesmí následně vytvořit nový věcně identický B → A PR.

## 38.8 Duplicate webhook

Stejná delivery dvakrát nesmí vytvořit dva PR.

## 38.9 Concurrent update

Dva rychlé push eventy nesmí vést k přepsání novějšího stavu starším jobem.

## 38.10 Conflict

Paralelní úprava stejného souboru na A i B musí skončit konfliktem, nikoli tichým přepsáním.

## 38.11 Unauthorized target

Pokud GitHub App nemá target repository, operace skončí čitelnou diagnostikou.

## 38.12 Branch mismatch

Neznámá větev se nesynchronizuje.

---

# 39. Acceptance criteria první produkční verze

Schopnost je připravena k použití, pokud:

- [ ] Workspace repository může deklarovat `product/`.
- [ ] Konfigurace obsahuje cílové GitHub repository.
- [ ] Funguje explicitní mapování `develop ↔ develop`.
- [ ] Funguje explicitní mapování `main ↔ main`.
- [ ] Merge/push do A/develop umí publikovat `product/` do B/develop.
- [ ] Merge/push do A/main umí publikovat `product/` do B/main.
- [ ] Změna v B/develop umí vytvořit PR měnící pouze `A/product/` proti A/develop.
- [ ] Změna v B/main umí vytvořit PR měnící pouze `A/product/` proti A/main.
- [ ] Přispěvatel do B nepotřebuje přístup do A.
- [ ] Soubor mimo `A/product/` se nikdy nepublikuje.
- [ ] Synchronizace je idempotentní.
- [ ] Je implementována loop prevention.
- [ ] Existuje dry-run.
- [ ] Existuje audit/provenance.
- [ ] Existuje detekce konfliktu/driftu.
- [ ] Cross-repo auth používá GitHub App nebo stejně úzce omezenou schválenou alternativu.
- [ ] Actions permissions jsou explicitně minimální.
- [ ] Kritické větve jsou chráněné rulesetem/branch protection.
- [ ] Testy pokrývají oba směry, delete, conflict, duplicate event a loop.
- [ ] Dokumentace popisuje bootstrap nového repository pair.

---

# 40. Fázování implementace

## Fáze 1 – Local sync engine

Vytvořit deterministický engine:

```text
A/product ↔ B/root
```

bez automatických webhooků.

Musí umět:

- diff,
- plan,
- dry-run,
- apply,
- delete,
- provenance,
- conflict detection.

## Fáze 2 – GitHub repository pair

Doplnit:

- target repository config,
- branch mapping,
- GitHub auth,
- create branch,
- commit,
- create PR.

## Fáze 3 – A → B automation

Aktivovat:

```text
A/develop → B/develop
A/main → B/main
```

## Fáze 4 – B → A automation

Aktivovat:

```text
B/develop → PR A/develop
B/main → PR A/main
```

## Fáze 5 – central Product Sync Controller

Přesunout citlivou cross-repository orchestrace do centrálního manageru / GitHub App webhook handleru.

## Fáze 6 – governance

Doplnit:

- organization rulesets podle plánu GitHub účtu,
- centrální observability,
- registry repository pairs,
- audit dashboard,
- retry/reconciliation job.

---

# 41. Registry repository pairs

Při správě více repozitářů bude manager potřebovat logický registry model:

```text
Workspace repo       Product repo       product path   branch mappings
-----------------------------------------------------------------------
owner/a               owner/b            product        develop/main
owner/c               owner/d            product        develop/main
```

Zdroj konfigurace má zůstat jednoznačný.

Preferovaný model:

- repository-specific nastavení deklarovat v A v `.repo-manager/product-sync.yml`,
- centrální manager drží runtime registry / cache,
- B nemusí zveřejňovat název privátního A,
- GitHub App installation + manager registry propojí event z B s odpovídajícím A.

---

# 42. Ochrana soukromí Workspace repository

Product repository nesmí obsahovat:

- clone URL privátního A, pokud není nutná,
- privátní GitHub token,
- deploy key s přístupem do A,
- GitHub App private key,
- seznam neveřejných souborů A,
- obsah interních adresářů,
- workflow logy obsahující interní data z A.

Pokud centrální manager potřebuje mapování B → A, má ho držet ve svém chráněném registry.

---

# 43. Poznámka k historii Git

Není požadováno zachovat identické commit SHA mezi:

```text
Workspace
```

a:

```text
Product
```

Protože stromy repository nejsou identické – A obsahuje další interní obsah.

Synchronizace má zachovávat **provenance**, nikoli předstírat, že se jedná o jeden Git repository.

Vazba mezi historiemi se eviduje přes:

```text
Source-SHA
Sync-Id
Target-SHA
```

---

# 44. Proč nepoužívat submodule jako hlavní mechanismus

Tato capability nemá být založena na Git submodule.

Požadovaný pracovní model je:

```text
Workspace obsahuje skutečný produktový strom
+
Workspace obsahuje další soukromý kontext
+
Product repository je samostatná oficiální projekce
+
změny mohou vznikat na obou stranách
```

Synchronizační služba proto lépe odpovídá požadovanému chování než pointer na jiný repository commit.

---

# 45. Proč nepoužívat blacklist

Zakázaný návrh:

```text
sync everything
except:
  .agents
  .skills
  internal-docs
```

Důvod:

nový interní adresář by mohl být omylem publikován.

Požadovaný návrh:

```text
only product/**
```

`product/` je bezpečnostní a architektonická hranice.

---

# 46. Oddělení odpovědností

Schopnost Product Repository Sync má řešit:

```text
repository content projection
branch mapping
Git synchronization
provenance
conflict/drift
security
```

Nemá sama rozhodovat:

- jak se produkt kompiluje,
- jak se deployuje,
- jak se releasuje,
- co znamená doménově správná změna,
- zda je změna funkčně vhodná.

Tyto validace poskytují CI, testy, build systém nebo jiné specializované capability.

---

# 47. AI a automatizace

Synchronizační jádro musí být deterministické.

AI lze použít pro:

- vysvětlení konfliktu,
- doporučení řešení,
- diagnostiku neúspěšného sync,
- návrh konfigurace,
- návrh branch mappingu.

AI nesmí být jediným mechanismem pro:

- určení, který soubor se smí publikovat,
- autorizaci,
- detekci hranice `product/`,
- rozhodnutí o přepsání konfliktu,
- validaci integrity synchronizace.

Architektura, konfigurace a validace musí zachovat kontrolu.

---

# 48. Doporučené výchozí rozhodnutí pro první nasazení

Pro první repository pair použít:

```yaml
version: 1

product:
  path: product

target:
  provider: github
  repository: OWNER/PRODUCT-REPOSITORY

branches:
  develop: develop
  main: main

outbound:
  enabled: true
  mode: pull-request

inbound:
  enabled: true
  mode: pull-request
  autoMerge: false

sync:
  deleteRemovedFiles: true
  requireCleanProjection: true
```

Až po ověření lze například A → B přepnout na:

```yaml
outbound:
  mode: direct
```

pokud ruleset dovolí bypass výhradně synchronizační GitHub App.

Inbound B → A doporučuji i dlouhodobě ponechat přes PR, protože jde o vstup změny z oficiálního / spolupracujícího repository do privátního vývojového workspace.

---

# 49. Codex – požadovaný výsledný výstup implementace

Po implementaci Codex odevzdá:

1. stručné shrnutí nalezené architektury repository manageru,
2. seznam přidaných / upravených komponent,
3. konfigurační schema,
4. implementaci `product/` boundary,
5. A → B sync,
6. B → A sync,
7. GitHub App auth,
8. branch mapping,
9. loop prevention,
10. provenance,
11. conflict/drift handling,
12. dry-run,
13. testy,
14. bootstrap návod,
15. security poznámky,
16. seznam vědomě neimplementovaných budoucích rozšíření.

Codex nemá pouze vyrobit dva ad-hoc YAML soubory.

Cílem je vytvořit **obecnou schopnost správce repozitářů**, kterou lze postupně aktivovat pro další repository pairs pomocí malé deklarativní konfigurace.

---

# 50. Fundamentální výsledný kontrakt

Celou schopnost lze shrnout takto:

```text
PRIVATE WORKSPACE REPOSITORY
│
├── private / development context
│   ├── .agents/
│   ├── .skills/
│   ├── .vscode/
│   └── ...
│
└── product/
      │
      │ A → B publish
      ▼
OFFICIAL PRODUCT REPOSITORY
      │
      │ contributions / PRs
      │
      │ B → A controlled import
      ▼
PRIVATE WORKSPACE / product/
```

Větve:

```text
A/develop  ↔  B/develop
A/main     ↔  B/main
```

Zásadní pravidlo:

> **`product/` je jediný produktový kontrakt mezi soukromým pracovním repozitářem a oficiálním produktovým repozitářem.**

Synchronizace může být obousměrná, ale musí být:

- explicitní,
- auditovatelná,
- idempotentní,
- branch-aware,
- conflict-aware,
- bezpečně autorizovaná,
- omezená na `product/`,
- řízená standardními GitHub review a protection mechanismy.

---

# 51. GitHub doporučení, o která se návrh opírá

Následující odkazy jsou primární dokumentace GitHub a představují technický základ tohoto zadání.

## GitHub App a cross-repository autentizace

- Making authenticated API requests with a GitHub App in a GitHub Actions workflow  
  https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow

- About authentication with a GitHub App  
  https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app

- Choosing permissions for a GitHub App  
  https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app

## GitHub Actions security

- Secure use reference  
  https://docs.github.com/en/actions/reference/security/secure-use

- Use GITHUB_TOKEN for authentication in workflows  
  https://docs.github.com/en/actions/reference/authentication-in-a-workflow

- Using secrets in GitHub Actions  
  https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions

## Branch protection a rulesets

- About protected branches  
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches

- About rulesets  
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets

- Available rules for rulesets  
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets

- Creating rulesets for repositories in your organization  
  https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization

## GitHub Actions workflow orchestrace

- Workflow syntax for GitHub Actions  
  https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

- Control the concurrency of workflows and jobs  
  https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency

## GitHub App webhooks

- Using webhooks with GitHub Apps  
  https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/using-webhooks-with-github-apps

- Validating webhook deliveries  
  https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries

- Best practices for using webhooks  
  https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks

---

# 52. Závěr pro implementaci

Implementaci začni co nejmenším funkčním jádrem:

```text
product/
+
target repository
+
develop/main mapping
+
dry-run
+
A → B
+
B → A přes PR
+
GitHub App
+
loop prevention
+
provenance
```

Teprve po ověření tohoto modelu přidávej centralizovaný webhook controller, organization-level governance a další automatizaci.

Prioritou je:

1. jasná hranice `product/`,
2. žádný únik privátního obsahu,
3. bezpečný příjem příspěvků z B zpět do A,
4. jednoduché a auditovatelné chování,
5. možnost stejnou capability bez kopírování logiky aktivovat na dalších repozitářích.
