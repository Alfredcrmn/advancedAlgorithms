//src/state/useSearch.js

import { useEffect, useState } from 'react'
import { zSearchAll } from '../lib/z_function'
import { makeSnippet } from '../lib/normalize'

function findPageIndex(pageOffsets, pos) {
  // búsqueda binaria del último offset <= pos
  let lo = 0, hi = pageOffsets.length - 1, ans = 0;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (pageOffsets[mid] <= pos) { ans = mid; lo = mid + 1; }
    else hi = mid - 1;
  }
  return ans;
}

export function useSearch(rawText, pageOffsets, query) {
  const [results, setResults] = useState([]);
  const [elapsedMs, setElapsedMs] = useState(0);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    let cancelled = false;
    if (!query || !rawText) { setResults([]); setElapsedMs(0); return; }

    setRunning(true);
    const t0 = performance.now();
    const positions = zSearchAll(rawText, query, { caseInsensitive: true });
    const t1 = performance.now();

    if (cancelled) return;

    const MAX = 500; // evita listas gigantes
    const res = positions.slice(0, MAX).map(pos => {
      const pageIndex = findPageIndex(pageOffsets, pos);
      const snip = makeSnippet(rawText, pos, query.length, 60);
      return { pos, pageIndex, ...snip };
    });

    setResults(res);
    setElapsedMs(Math.round(t1 - t0));
    setRunning(false);

    return () => { cancelled = true; };
  }, [rawText, pageOffsets, query]);

  return { results, elapsedMs, running };
}
