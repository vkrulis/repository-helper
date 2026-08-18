# Zásadní změna názvů repozitářů

Cílem této úpravy je z výchozího historického stavu pojmenování zavést pojmy, které mezi sebou správně korspondují. 

## Původní hierarchie na lokálním uložišti

Popisujeme zde obsah složky `c:\flexideo\develop-sources\` a její kmenovou strukturu (00).
Zde jsou záměrně řádky číslovány, protože právě číslo je stabilním identifikátorem složky ve schématu přejmenování.

  00  │
  01  ├───1-Replikator
  02  │   ├───fxdReplicator_NET
  03  │   ├───work-folder-zero
  04  │   └───fxd-xds-authoring
  05  ├───2-Intranet
  06  │   ├───fxdIntranet_NET
  07  │   ├───fxd-intranet-authoring
  08  │   ├───fxd-intranet-web
  09  │   └───fxd-intranet-web-2.0
  10  ├───3-comex
  11  │   ├───comex-authoring
  12  │   ├───comex-draftsman
  13  │   └───comex-web
  14  ├───4-Server
  15  ├───5-shared
  16  │   ├───!repository-helper
  17  │   ├───documentation
  18  │   ├───fdt-templates
  19  │   ├───Flexideo-orchestrator
  20  │   ├───fxd-updater
  21  │   └───public-web
  22  └───6-projects
  23      ├───IDS
  24      └───Reno-RDO
  25

## Nová hierarchie na lokálním uložišti

Cílem nového uspořádání je zbavit se ne úplně smysluplného vnořování do pomocných složek 1 - 6, tyto nadřazené složky v novém schématu jsou pryč, tento obal již v novém není (na jejich číslech řádků je prázdno). 
Také se zbavujeme jednoho z repozitářů - to explicitně potvrzuji, zbavujeme se repozitáře z řádku 06. Server (14) necháváme, kde je, jen přejmenováváme. Ostatní repozitáře přesouváme o úroveň výš do rootu složky.

  00  │
  01  │
  02  ├───Flexideo-replicator
  03  ├───Flexideo-replicator-work-folder
  04  ├───Flexideo-XDS-authoring
  05  │
  06  │
  07  ├───Flexideo-intranet-authoring
  08  ├───Flexideo-intranet
  09  ├───Flexideo-intranet-2.0
  10  │
  11  ├───Flexideo-comex-authoring
  12  ├───Flexideo-comex-draftsman
  13  ├───Flexideo-comex
  14  ├───Flexideo-server
  15  │
  16  ├───Repository-helper
  17  ├───Flexideo-Documentation
  18  ├───Flexideo-render-templates
  19  ├───Flexideo-orchestrator
  20  ├───Flexideo-updater
  21  ├───Flexideo-public-web
  22  │
  23  ├───Project-IDS
  24  └───Project-Reno-RDO
  25

## Zadání

Provést přesuny a přejmenování a přejmenování a upravit vzájemné odkazy mezi jednotlivými repozitáři. 
Jakmile to bude hotovo, zavedou se napojení na GitHub přejmenované repozitáře nebo se jen potvrdí napojení tak, aby lokální názvy korepondovali se vzdálenými na mém účtu.

Další fáze bude dle zadání napojení oficiálních repozitářů jen s cílovým produktem bez pomocných a agentních souborů, které tak zůstanou jen mé privátní.
