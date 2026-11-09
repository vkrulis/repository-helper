# Authoring feedback toolkit

Deterministický stdlib adaptér pro kontrakt FCL `authoring-feedback-event-v1`.
Validuje event, zapisuje jej jako strukturovaný blok do `.logs/YYYY/MM/YYYY-MM-DD.md`
a vytváří read-only agregát. Staré logy bez feedback bloku zůstávají platné.

```powershell
python tools/authoring-feedback/authoring_feedback.py validate-event --event <event.json>
python tools/authoring-feedback/authoring_feedback.py record <projekt> --event <event.json>
python tools/authoring-feedback/authoring_feedback.py validate <projekt>
python tools/authoring-feedback/authoring_feedback.py scan <projekt>
```

Nástroj neodesílá data do FCL ani na síť. Globální ingest, retence a tenantová
autorizace jsou samostatná budoucí hranice. `scan` deduplikuje použití jednotkou
`run × verze × role`; fyzická volání, retries, výsledky, chyby a recovery drží
odděleně a roli uvádí v klíči agregátu.
