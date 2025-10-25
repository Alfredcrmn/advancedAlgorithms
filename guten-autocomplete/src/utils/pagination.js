//src/utils/pagination.js

// Pagina por tamaño aproximado de caracteres y regresa offsets de inicio
export function paginateByChars(text, { targetChars = 1800, tolerance = 200 } = {}) {
  const clean = text.replace(/\r/g, '');
  const paras = clean.split(/\n{2,}/);
  const pages = [];
  let buf = '';

  for (const raw of paras) {
    const p = raw.trim();
    if (!p) continue;

    const candidate = buf ? buf + '\n\n' + p : p;
    if (candidate.length <= targetChars + tolerance) {
      buf = candidate;
      continue;
    }

    if (buf) { pages.push(buf); buf = ''; }

    if (p.length > targetChars * 1.5) {
      // partir por oraciones si el párrafo es larguísimo
      const sentences = p.split(/(?<=[.!?])\s+/);
      let temp = '';
      for (const s of sentences) {
        const cand = temp ? temp + ' ' + s : s;
        if (cand.length > targetChars + tolerance) {
          if (temp) pages.push(temp.trim());
          temp = s;
        } else {
          temp = cand;
        }
      }
      if (temp) pages.push(temp.trim());
    } else {
      buf = p;
    }
  }
  if (buf) pages.push(buf);

  // Mapear cada página a su offset real dentro de `text`
  const pageOffsets = [];
  let searchFrom = 0;
  for (const pg of pages) {
    const found = clean.indexOf(pg, searchFrom);
    const start = found === -1 ? searchFrom : found;
    pageOffsets.push(start);
    searchFrom = start + pg.length;
  }

  return { pages, pageOffsets };
}
