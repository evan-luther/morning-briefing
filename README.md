# Philadelphia Morning Briefing

A public, link-card-friendly morning briefing with:

- Philadelphia weather from Open-Meteo
- three current NPR headlines
- sunrise and sunset times
- a live CSS sky computed for Philadelphia at the moment the page opens
- a 1200x630 Open Graph image regenerated before daily delivery

The sky renderer is adapted from [Horizon](https://github.com/dnlzro/horizon) by Daniel Lázaro under the MIT License. See `HORIZON-LICENSE`.

## Build

```bash
npm install
npm run build
scripts/render_preview.sh
```

The published page uses Apple's SF Pro when opened on Apple devices, with system sans-serif fallbacks elsewhere.
