# Documentation sync capability

Capability `documentation-sync` keeps repository-specific domain knowledge and the shared Docusaurus documentation aligned.

## Contract

The domain repository is reviewed first. Its `docs/agent-context/` documents describe verified implementation details and carry `general_documentation` paths such as `public/supp-...`. Only after that review may the sibling `documentation` repository be revised and published.

Changed public Markdown files retain `source`, `source_url`, and `exported_at` and add `revised_by` and `revised_at`. `revised_by` uses one of `minor`, `substantial`, or `structural` followed by a short reason. New sections use `source: repository` and a logical `repository` name.

The skill provides the judgment-heavy workflow; `toolkit/agent-infrastructure/validate_documentation_metadata.py` checks explicit files deterministically.

Install into an existing repository with:

```text
python toolkit/agent-infrastructure/repository_architecture.py install-capability <target> --name documentation-sync
```
