# sroai.github.io

Website of the SRO AI organization — AI for streaming readout — served at
<https://sroai.github.io/>.

```
index.md                  # organization landing page
ai-epic-background/       # EIC AI Background project pages (/ai-epic-background/)
public/                   # static assets (diagrams)
.vitepress/               # VitePress config, theme and Vue components
scripts/                  # summarize_rucio_dids.py, used by the update-data-md skill
.claude/skills/           # update-data-md skill (refreshes ai-epic-background/data.md)
.github/workflows/        # builds and deploys the site on push to main
```

Local preview:

```bash
npm install
npm run dev
```

`npm run build` fails on dead internal links, so run it before pushing.

## History

The EIC AI Background pages were developed in
[eic/ai-epic-background](https://github.com/eic/ai-epic-background) (archived), whose git
history this repository continues. The simulation pipeline lives in
[JeffersonLab/msf-simulation-pipeline](https://github.com/JeffersonLab/msf-simulation-pipeline),
the CSV converter in [sroai/eic2ai](https://github.com/sroai/eic2ai).

## License

MIT.
