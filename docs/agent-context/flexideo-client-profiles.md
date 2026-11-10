---
status: confirmed
general_documentation: []
revised_by: "substantial: rozšíření projektových profilů o OAuth a login URL"
revised_at: "2026-11-10T12:29:49+01:00"
---

# Projektové přihlašovací profily Flexideo

Repository Foundation distribuuje pravidlo výběru profilu a odkaz na jeho autoritu
prostřednictvím `product/skills/maintain-client-project-dimension/SKILL.md`,
`product/references/client-project-capability.md` a generovaného capability pravidla
v `product/tools/agent-infrastructure/repository_architecture.py`.

Profil je `credentials/<DEV|TEST|CODE|PROD>/<account>.env`. Skutečný profil nepatří
do Git; `.env.example` smí obsahovat jen anonymní příklad. Helper nečte jiné účty
ani nehádá roli z aliasu. Formát v2.2 a jeho parser vlastní výhradně
`Flexideo-authoring-tools/product/contracts/flexideo-client-credentials.md`.
Webový typ, XML Basic/Bearer transport a explicitní webová login URL jsou oddělené.
OAuth web může používat ruční `/login` i Basic technický transport; toto se deklaruje
explicitně, profil se nepřevádí automaticky.

Změna se promítá do budoucí řízené instalace capability; existující klientské
AGENTS, `.env`, Memory metadata ani registry se automaticky nemigrují.
Doménová revize provedena proti změnám produktu a kontraktu D. Samostatná obecná
Docusaurus stránka není vedena a touto změnou se nepublikuje.
