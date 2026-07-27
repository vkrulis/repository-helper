# Work log toolkit

Deterministický nástroj pro vytváření, prohledávání a ověřování kanonické pracovní historie v `.logs/YYYY/MM/YYYY-MM-DD.md`.

```bash
python toolkit/work-log/work-log.py add . --title "Název" --type change --status done --summary "Výsledek"
python toolkit/work-log/work-log.py recent . --days 14
python toolkit/work-log/work-log.py search . --query "téma"
python toolkit/work-log/work-log.py validate .
```

Nástroj používá pouze standardní knihovnu Pythonu. Podrobná pravidla zápisu určuje `.agents/skills/maintain-work-log/SKILL.md`.
