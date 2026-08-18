# Capability: doménové inventáře

Repository-helper poskytuje skill `maintain-domain-inventories` pro živé mapy
aktuálního stavu zdrojového kódu. Capability je záměrně obecná: helper
nedistribuuje konkrétní regexy ani projektový generátor, protože ty patří do
domény cílového repozitáře.

Instalace do existujícího repozitáře:

```text
python <repository-helper>/toolkit/agent-infrastructure/repository_architecture.py install-capability <target-repository> --name domain-inventories
```

Aktualizace existující kopie po kontrole lokálních úprav:

```text
python <repository-helper>/toolkit/agent-infrastructure/repository_architecture.py install-capability <target-repository> --name domain-inventories --force
```

Příkaz kopíruje kanonický skill a podpůrné README pro `domain/` a
`toolkit/domain/`; projektové `*.generated.md` ani vlastní generátory
nepřepisuje. Pokud cílový repozitář už má Claude konektor v
`.claude/skills/`, automaticky synchronizuje označenou odvozenou kopii.
Neoznačenou ruční kopii nepřepisuje a skončí s akcí k ruční kontrole.
