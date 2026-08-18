---
title: "Dokumentace kódu a živé doménové inventáře"
created_at: "2026-07-31T08:02:28+02:00"
updated_at: "2026-07-31T08:02:28+02:00"
source: "Pracovní poznámka z komunikace"
source_repository: "C:\\flexideo\\develop-sources\\2-Intranet\\fxd-intranet-web-2.0"
owner_repository: "C:\\flexideo\\develop-sources\\5-shared\\!repository-helper"
purpose: "Zachytit návrh, jak trvale dokumentovat mapovací operace a aktuální stav kódu."
status: "realizováno částečně"
used_for:
  - "Návrh a zavedení capability domain-inventories v repository-helper."
  - "Zavedení skillu maintain-domain-inventories pro přenos do vybraných repozitářů."
  - "Oddělení generovaných doménových inventářů od logů, ADR a vývojových pravidel."
authoritative: false
notes: "Konkrétní generátory inventářů zůstávají projektové; tento soubor je vstupní pracovní podklad."
---

# Dokumentace kódu

Uvedené příklady jsou ze zkušebního repozitáře tvorby webové aplikace, který je dostupný zde:
- `C:\flexideo\develop-sources\2-Intranet\fxd-intranet-web-2.0`

## Příklad komunikace

Shrnutí Fáze 1
scripts-g/xslt-wrapper.js (nový) — redefinuje setStyleVar (nahraje se až za both.js, takže žádná z ~301 volajících míst ani both.js samo se nemusí měnit): u migrovaného xsl:param hodnotu jen zapíše do mapy (getXsltParams), sdílenou šablonu nemutuje; u zatím nemigrovaného xsl:variable chová se přesně jako dřív. Umožňuje migraci soubor po souboru.
desktop.xsl (25) a panels.xsl (39) — globální xsl:variable → xsl:param, přesná bytová záměna jen názvu tagu (parser hlídal hloubku, aby se netkly lokální proměnné ani xsl:param uvnitř šablon). Kódování a CRLF zachovány.
Cestou se ukázalo, že v msxml-shim.js chybí .load(url) — obase.XSLTs.prepOneTmp (jádro přípravy šablon v base.js) by bez něj padalo. Doplněno.
Chyba, kterou jsem sám udělal a opravil: Python čtení v textovém módu při konverzi .xsl souborů tiše převedlo CRLF na LF. Zachytil jsem to při kontrole, opravil zpětným převodem (bezpečné, protože originály měly nulu "bare" LF) a ověřil.
Ověřeno strukturálně (žádný server k dispozici): na desktop.xsl setStyleVar nastaví parametr beze změny select atributu; na nemigrovaném doccontrol.xsl mutuje select přesně jako dřív. base.htm se dál načítá bez pádu (regresní test prošel).

Zůstává (zapsáno v ADR-0003): ~89 dalších .xsl souborů a ~262 dalších setStyleVar volání čeká na postupnou migraci; Fáze 2 (volba skutečného XSLT enginu) je pořád samostatné budoucí rozhodnutí.

## Myšlenka

Otázka trochu mimo, ale důležitá.

Jak nejlépe dokumentovat refaktoring, který tu řešíme?
Cílem by mělo být nejen, že další vývojáři budou rozumět tomu, co se tu dělo, ale děláme tu spoustu mapovacích operací, ze kterých by mohla postupně vznikat dokumentace. Jak to nejlépe pojmout?
Show less

## Závěr

Dobrá otázka a myslím, že už teď máme skoro celou skládačku, jen jí chybí jeden díl.

Co už máme a funguje dobře:

.logs/ — chronologický deník ("co se stalo, v jakém pořadí") — nesahat, funguje.
docs/agent-context/decisions/ (ADR) — "proč jsme zvolili A, ne B" — funguje, ale dnes se do ADR zápisů cpe i syrová průzkumová data (počty výskytů, seznamy souborů), což je zatěžuje.
docs/agent-context/development-rules.md — "recept": jak mechanicky převést vzor X na Y (substr→substring, ActiveXObject→newXmlDoc()...). Funguje, roste správně.
Co chybí: docs/agent-context/domain/ je v README avízovaná, ale prázdná. Přesně tam patří ty mapovací operace, které dnes dělám ad-hoc přes grep a pak výsledek jen napíšu do chatu/ADR a zmizí. Bez trvalého místa je zítra někdo (ty, já, jiný vývojář) bude muset spočítat znovu.

Návrh:

docs/agent-context/domain/migration-inventory.md (nebo rozdělené po tématu jako msxml-api-inventory.md, xslt-templates-inventory.md) — živý přehled/checklist: který soubor má ActiveXObject vyřešený, který document.all gate odstraněný, které .xsl má xsl:param, kde zůstává transformNode. Dnešní čísla (377 ActiveXObject, 2669 selectSingleNode, 25+39 převedených proměnných...) by tam měla trvalá podoba, ne jen v historii chatu.
Část toho jde generovat, ne psát ručně — přesně jako page-runtime-map.generated.md v 1.0 (ten už tenhle vzor validuje). Skript by prošel scripts-g/*.js + stylesheets-g/*.xsl, spočítal totéž, co dnes dělám ručně přes grep, a vyplivnul aktuální tabulku. Menší riziko zastarání než ruční údržba.
ADR necháme lean — odkaz do inventáře místo vkládání syrových čísel přímo do textu rozhodnutí.
Chceš, abych tohle rovnou založil (strukturu + první generovaný inventář z toho, co dnes víme), nebo si to nejdřív probereme podrobněji?

## První realizace

Ve zkušebním repozitáři vzniklo následující:

Nová vrstva docs/agent-context/domain/ — čtvrtý typ dokumentace vedle .logs/ (co se stalo), decisions/ (proč), development-rules.md (jak převést vzor X→Y): odpovídá na „co v kódu aktuálně je a v jakém je to stavu".

domain/README.md — pravidla: generovaný vs. psaný dokument, generátor se spouští nad aktuálním stavem (ne z paměti konverzace), do ADR se nekopírují syrová čísla jen odkaz, baseline srovnání s 1.0 kde má smysl, aktualizace je součástí práce na souboru, ne samostatný úkol.
toolkit/domain/build_migration_inventory.py (nový, po vzoru existujícího build_page_runtime_map.py z 1.0) — skenuje public/scripts-g/*.js + public/stylesheets-g/*.xsl na 4 sledované vzory (ActiveXObject→newXmlDoc, IE document.all gate, transformNode, globální xsl:variable→xsl:param) a srovnává s baseline v fxd-intranet-web (1.0), aby rozlišil, co vzniklo dnešní migrací od toho, co tam bylo odjakživa — to byl netriviální bod: několik .xsl šablon mělo xsl:param už v 1.0, nesouvisí s dnešní Fází 1.
domain/migration-inventory.generated.md — vygenerovaný výstup (78 JS + 85 XSL souborů, aktuální čísla).
domain/migration-inventory.md — návod k použití, včetně dvou zdokumentovaných falešných poplachů (msxml-shim.js sám sebe hlásí jako „nemigrováno" kvůli komentářům v hlavičce).
Odkazy doplněny do docs/agent-context/README.md (a opravena zastaralá poznámka „ADR-0003 stav proposed" → teď bez ní, protože je accepted), development-rules.md a ADR-0003 (Navazující práce). Zapsáno do work logu, všechny tři validace (repository_architecture.py, validate_skill_collection.py, work-log.py) prošly bez chyby.

## Požadavek

Prověř z hlediska již existujících dovedností, které se přenášejí do repozitářů a podle popsané situace reviduj nebo vytvoř nové nástroje, které se budou z `C:\flexideo\develop-sources\5-shared!repository-helper` přenášet i případně do dalších.

Pokud uznáš za vhodné rovnou vylepšit i zkušební webový repozitář, dej vědět.
