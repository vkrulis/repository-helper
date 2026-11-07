# Repository Foundation product

Jediný autoritativní publikovatelný produkt Repository-helperu. Poskytuje přenositelné
skills, profily, deterministické nástroje, reference a šablony pro založení, audit,
migraci, validaci a dlouhodobou údržbu agent-ready repozitářů.

Produkt je průřezová podpůrná vrstva společného Flexideo Implementátora. Není vrstvou
A–E a nemění jejich normativní mapu. Klientský projekt, vývojový repozitář,
authoring workspace a dokumentační repozitář jsou instalační profily a capability
tohoto produktu, nikoli další kopie produktu.

- Vstup: `skills/bootstrap-repository-foundation/SKILL.md`
- Skills: `skills/`
- Profily: `profiles/`
- Nástroje: `tools/`
- Přenositelné reference: `references/`
- Šablony instalované do cílových repozitářů: `templates/`
- Testy: `tests/`

Z klientského projektu se capability instalují nástrojem:

```powershell
python <repository-foundation>/tools/agent-infrastructure/repository_architecture.py install-capability <projekt> --name client-project
```

Project Memory zakládá Orchestrátor svým verzovaným template. Repository Foundation
do ní instaluje pouze výslovně podporovaný klientský obal a provozní capability;
nevytváří druhou analytickou paměť ani nemění MCP stav.
