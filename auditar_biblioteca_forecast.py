"""Coverage/deduplication of exact recent sale streams, before any new agent."""
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

OUT = Path('docs/evidencia/loop_publicos_20260925')


def fingerprint(events):
    # Native ranking uses event presence; prediction only tests summed q >= 4.
    # Clipping each q at four preserves that threshold and its q>=2 prior gate.
    return tuple(sorted((t, i, min(q, 4)) for (t, i), q in events.items()))


def main():
    output = OUT/'forecast_library_audit.json'
    streams_output = OUT/'recent_sale_streams.json'
    if output.exists() or streams_output.exists():
        raise FileExistsError(output)
    path = Path('submission/main_publico_arshs3_vq_top3.py')
    ns = {}
    exec(compile(path.read_bytes(), str(path), 'exec'), ns)
    names = ['BAKERY', 'BRUNCH_SPOT', 'FARMERS_MARKET', 'ICE_CREAM_SHOP', 'PET_CAFE', 'PIZZA_SHOP', 'SMOOTHIE_SHOP', 'YARN_STORE']
    library = {pair: ns['_v92_p_pair'](pair) for pair in itertools.product(names, repeat=2)}
    rows, streams = [], []
    dsm = json.loads((OUT/'dsm_current_analysis.json').read_text())['episodes']
    sources = [(r, r['me'], 'DSM', OUT/f'dsm_{r["id"]}.ledger.jsonl.gz') for r in dsm]
    first = json.loads((OUT/'top3_accepted_transactions_0234.json').read_text())
    sources += [(r, 1-r['me'], 'top3_opponent_0234', OUT/f'top3_{r["id"]}.ledger.jsonl.gz') for r in first]
    latest = json.loads((OUT/'top3_audit_0339.json').read_text())
    sources += [(r, 1-r['me'], 'top3_opponent_0339', Path(r['ledger'])) for r in latest]
    seen = {pair: {fingerprint(ev) for _, ev in candidates} for pair, candidates in library.items()}
    for row, player, source, ledger_path in sources:
        raw = Path(row['path']).read_bytes()
        replay = json.loads(raw)
        pair = tuple(replay['steps'][-1][0]['observation']['town']['unlocked_shops'][:2])
        ledger = [json.loads(line) for line in gzip.decompress(ledger_path.read_bytes()).decode().splitlines()]
        counts = Counter((r['step'], ns['_V92_P_ITEMS'].index(r['item'])) for r in ledger
                         if r['player'] == player and r['op'] == 'SELL' and r['item'] in ns['_V92_P_ITEMS'])
        events = {(t, i): q for (t, i), q in counts.items() if q >= 2 and
                  replay['steps'][t][0]['observation']['market']['prices'][ns['_V92_P_ITEMS'][i]] > 3}
        old = library[pair]
        keys = set(events)
        jaccard = max((len(keys & set(ev))/len(keys | set(ev)) for _, ev in old if keys | set(ev)), default=0)
        fp = fingerprint(events)
        duplicate = fp in seen[pair]
        seen[pair].add(fp)
        entry = dict(episode=row['id'], player=player, source=source, shops=pair, events=len(events),
                     existing_streams=len(old), semantic_duplicate=duplicate, closest_key_jaccard=jaccard,
                     replay_sha256=hashlib.sha256(raw).hexdigest(), ledger=str(ledger_path),
                     ledger_sha256=hashlib.sha256(ledger_path.read_bytes()).hexdigest())
        rows.append(entry)
        if not duplicate:
            streams.append(dict(**entry, sales=[[t, i, q] for (t, i), q in sorted(events.items())]))
    report = dict(base_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  library_streams=sum(map(len, library.values())), covered_shop_pairs=sum(bool(v) for v in library.values()),
                  total_shop_pairs=64, streams_per_pair=[min(map(len, library.values())), max(map(len, library.values()))],
                  existing_episode_ids_retained=False, temporal_coverage='Unknown: embedded entries have ep=-1, no source timestamps.',
                  source_selection='All four recency-selected DSM streams and all eight recency-selected top3 opponent streams; no W/L filter.',
                  recent_streams=len(rows), new_semantic_streams=len(streams), new_shop_pairs=0,
                  note='Coverage/dedup only. Not forecast accuracy or competitive validation. No agent was changed.', rows=rows)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
    streams_output.write_text(json.dumps(streams, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'rows'}, indent=2))
    for row in rows:
        print(row['episode'], row['source'], row['shops'], row['events'], row['semantic_duplicate'], round(row['closest_key_jaccard'], 3))


if __name__ == '__main__':
    main()
