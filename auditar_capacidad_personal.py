"""Official PICKUP capacity probes plus offline audit of frozen loop23 events."""
from copy import deepcopy
import gzip
import hashlib
import importlib
import json
from pathlib import Path

OUT = Path('docs/evidencia/loop_publicos_20260925')


def main():
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    trace = [json.loads(line) for line in gzip.decompress((OUT / 'late_escapes_1080001.trace.jsonl.gz').read_bytes()).splitlines()]
    initial = next(row['observation'] for row in trace if row['step'] == 624)
    cases = []
    for held, stock, request in [(0, 20, 15), (8, 20, 5), (8, 20, 15), (15, 3, 5)]:
        farm = deepcopy(initial['farms'][0]); private = deepcopy(initial['private'])
        farm['farmer'] = [4, 4]
        private['inventories'][0] = {'MILK': held} if held else {}
        private['shed']['WHEAT'] = stock
        engine._apply_unit_action(farm, private, 0, ['PICKUP', 'WHEAT', request], 10, 26, 24, 100)
        taken = private['inventories'][0].get('WHEAT', 0)
        assert taken == min(stock, request)
        assert sum(private['inventories'][0].values()) == held+taken
        cases.append(dict(initial_personal_load=held, wheat_in_shed=stock, requested=request,
                          picked=taken, final_personal_load=held+taken))
    events = []
    tags = ['sheep_supply_smoke', 'sheep_supply_coverage_vq', 'sheep_supply_coverage_public_v7', 'sheep_supply_coverage_public_hs4']
    for tag in tags:
        for row in json.loads((OUT / (tag + '.json')).read_text()):
            edits = row.get('layer_events', {}).get('_SS_EVENTS', [])
            if not edits:
                continue
            units = [json.loads(line) for line in gzip.decompress((OUT / f"{tag}.{row['seed']}.{row['arm']}.{row['seat']}.units.jsonl.gz").read_bytes()).splitlines()]
            for edit in edits:
                matching = [unit for unit in units if unit['step'] == edit['step']+1 and unit['actor'] < edit['actor']
                            and unit['action'][:2] == ['PICKUP', 'WHEAT'] and tuple(unit['xy']) in ((4, 4), (5, 4), (4, 5), (5, 5))]
                requested = sum(int(unit['action'][2]) if len(unit['action']) > 2 else 1 for unit in matching)
                taken = sum(unit['inventory_delta'].get('WHEAT', 0) for unit in matching)
                events.append(dict(tag=tag, arm=row['arm'], seed=row['seed'], seat=row['seat'], step=edit['step'],
                                   native_predicted=edit['native_need'], native_requested=requested, native_taken=taken))
    assert len(events) == 4 and all(row['native_predicted'] == row['native_requested'] == row['native_taken'] == 5 for row in events)
    result = dict(passed=True, new_full_games=0, official_unit_probes=cases,
                  engine_sha256=hashlib.sha256(Path(engine.__file__).read_bytes()).hexdigest(), frozen_loop23_events=events,
                  limitation='The ten-unit personal capacity assumption in layer23 is wrong. It did not clip demand in its four observed development activations, so existing measured receipts remain valid. Frozen loop23 sources are unchanged; do not generalize that coverage to all future states. Layer32 uses full requested quantities.')
    (OUT / 'personal_capacity_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
