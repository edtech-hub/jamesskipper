# James Skipper Painting: pitch prototype

Static preview site for James Skipper Painting (house painting, Chesapeake, VA), built by White Phoenix from the
pitch-prototypes starter. Plain HTML, CSS and one JS file; every page is `noindex`. Forms validate but send nothing.

- Content comes from the client's Facebook page and BBB profile. Anything unconfirmed is wrapped in a visible
  placeholder marker (`.ph`, `.ph-chip`, `.is-placeholder`) so the client can edit or remove it.
- Rebuild pages: `python3 tools/build_site.py .`
- Rebuild images: `cd tools && npm install && cd .. && node tools/images.js images.json` (stock originals are not committed)
- Logo: `python3 tools/logo.py .` redraws the Facebook logo as `assets/img/logo.svg`.
