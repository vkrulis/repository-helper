---
name: maintain-domain-knowledge
description: Zařazuje ověřené poznatky do dokumentace repozitáře a připravuje doloženou lokální změnu. Použijte pro nový obsah, opravu či doplnění existující stránky; neurčuje projektové analytické stavy.
---

# Zařazení znalosti do dokumentace

Nejdříve přečtěte README/AGENTS a místní `.agents/documentation.json`, pokud existuje.
Určete dokumentační kořeny, autoritu, publikum a generované oblasti. Profil neuděluje
práva k zápisu; oprávnění poskytuje aktuální zadání nebo serverová autorizační vrstva.

1. U vstupu ověřte původ, jistotu, zamýšlené publikum a vztah ke skutečnému stavu.
   Návrh ani nepotvrzený analytický závěr neoznačujte za hotovou funkci.
2. Dohledejte související stránky pomocí `search-markdown-content` a přečtěte jejich
   obsah a rozcestníky. Vyberte nejmenší změnu, která udrží jedno hlavní místo tématu.
3. V generované oblasti opravujte zdroj a používejte nástroj producenta. Ruční
   vysvětlení ukládejte mimo generovaný strom s odkazem na příslušný snapshot.
4. Konflikt autorit či významnou změnu veřejných cest předložte jako konkrétní
   rozhodnutí, pokud ji už zadání neřeší. Zachovejte provenienci a místní metadata.
5. Proveďte autorizovanou úpravu; zkontrolujte dotčené odkazy a místní validační
   příkazy. Materiální změnu zaznamenejte podle pravidel repozitáře.

V Project Memory je `docs/` sdílená dokumentace aplikace. `context/`,
`application/` a `project/epics/` mají vlastní kontrakty: dokumentační úprava
nepotvrzuje baseline, nemění analytický stav ani neprovádí promotion Current Truth.
MCP mutace použijte jen pro operace, které nasazené rozhraní skutečně podporuje;
nevymýšlejte obecné zapisovací API. Publikaci řeší samostatný autorizovaný publisher.
