"""Validate final own-sale quantities, source integrity and both parent noops."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import tarfile

from construir_atribucion_ventas import OUT as AGENTS, EVIDENCE as OUT


def validate_block(prefix, expected_games, expected_noops):
    record = json.loads((OUT / f'{prefix}.json').read_text())
    rows = record['results']; plan = record['plan']
    manifest = json.loads((AGENTS / 'manifest.json').read_text())
    keyed = {(r['arm'],r['seed'],r['seat']):r for r in rows}
    expected = {(arm,seed,seat) for arm in plan['agents'] for seed in plan['seeds'] for seat in (0,1)}
    assert len(rows) == len(keyed) == expected_games and set(keyed) == expected
    with tarfile.open(OUT / f'{prefix}.sources.tgz') as archive:
        for name,spec in plan['agents'].items():
            assert hashlib.sha256(Path(spec['path']).read_bytes()).hexdigest() == spec['sha256']
            assert hashlib.sha256(archive.extractfile(f'agents/{name}.py').read()).hexdigest() == spec['sha256']
        assert hashlib.sha256(archive.extractfile('opponent.py').read()).hexdigest() == plan['opponent']['sha256']
    noops = 0; activated = Counter(); corrected = Counter(); summaries = []
    for row in rows:
        name=row['arm']; assert row['max_turn_ms'] < 1000
        assert not any(v for d in row['reports'].values() for k,v in d.items() if 'error' in k and isinstance(v,(int,float)))
        if name in ('base','top3'): continue
        parent = manifest[name]['behavior_reference']; base=keyed[parent,row['seed'],row['seat']]
        if name.startswith('sales_noop'):
            assert row['action_hashes'] == base['action_hashes'] and row['rewards'] == base['rewards']
            assert row['changed_own_turns'] == row['changed_rival_turns'] == 0
            noops += 719; continue
        assert row['own_sales_checks'] > 0 and row['own_sales_mismatches'] == []
        assert row['reports']['_SA_REPORT']['checks'] == 719
        assert row['reports']['_SA_REPORT']['errors'] == 0
        corrected[name] += len(row['edits'])
        activated[name] += row['changed_own_turns'] > 0
        for event in row['edits']:
            assert 0 <= event['step'] < 719 and event['items']
            assert all(q >= 0 for q in event['new_own'].values())
            assert all(q >= 0 for q in event['new_left'].values())
        private=row['terminal_private'][0]
        summaries.append(dict(arm=name,seed=row['seed'],seat=row['seat'],changed_own_turns=row['changed_own_turns'],
                              snapshot_corrected_turns=len(row['edits']),parent_snapshot_mismatches=len(base['own_sales_mismatches']),
                              candidate_snapshot_mismatches=len(row['own_sales_mismatches']),same_shops=row['same_shops'],
                              same_accepted_work=row['accepted']==base['accepted'],same_harvest=row['harvested']==base['harvested'],
                              same_losses=row['nights']==base['nights'],escapes=row['escapes'],
                              terminal_products=sum(private['shed'].values())+sum(sum(b.values()) for b in private['inventories']),
                              base_margin=base['margin'],candidate_margin=row['margin']))
    assert noops == expected_noops
    validation=dict(passed=True,competitive_ready=False,games=expected_games,noop_exact_turns=noops,
                    max_turn_ms=max(r['max_turn_ms'] for r in rows),activated_cells=dict(activated),
                    corrected_snapshot_turns=dict(corrected),
                    candidate_hashes={n:r['sha256'] for n,r in manifest.items() if r['config']['enabled']},
                    base_hash=plan['agents']['base']['sha256'],control_hash=json.loads((OUT / 'close_panel_manifest.json').read_text())['controls']['top3']['sha256'],
                    own_sale_item_turn_checks=sum(r['own_sales_checks'] for r in rows if r['arm'].startswith('sales_sync')),
                    summary=summaries,note='Final own sale quantity exactly matches accepted sales. This does not resolve invisible sales at price floor or demonstrate WLT improvement.')
    return validation


def main():
    initial = validate_block('sale_attribution_smoke', 48, 11504)
    extra = validate_block('sale_attribution_coverage', 24, 5752)
    for field in ('candidate_hashes', 'base_hash'):
        assert initial[field] == extra[field]
    activated = Counter(initial['activated_cells']); activated.update(extra['activated_cells'])
    corrected = Counter(initial['corrected_snapshot_turns']); corrected.update(extra['corrected_snapshot_turns'])
    assert all(activated[name] > 0 and corrected[name] > 0 for name in ('sales_sync_vq','sales_sync_top3'))
    result = dict(initial, competitive_ready=True, games=72, noop_exact_turns=17256,
                  max_turn_ms=max(initial['max_turn_ms'], extra['max_turn_ms']),
                  activated_cells=dict(activated), corrected_snapshot_turns=dict(corrected),
                  own_sale_item_turn_checks=initial['own_sale_item_turn_checks'] + extra['own_sale_item_turn_checks'],
                  summary=initial['summary'] + extra['summary'],
                  development_blocks=['sale_attribution_smoke', 'sale_attribution_coverage'],
                  initial_coverage_failure_preserved='sale_attribution_validation.initial_failure.json')
    (OUT / 'sale_attribution_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='summary'}))


if __name__ == '__main__':main()
