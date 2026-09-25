"""Transform only additional-pattern support/size/horizon, preserve top1 signals."""
import ast
import hashlib
import json
from pathlib import Path

BASE = Path('submission/main_publico_arshs3_vq_top3.py')
OUT = Path('results/senales_extra_20260925')
EVIDENCE = Path('docs/evidencia/loop_publicos_20260925')


def layer(raw):
    tree = ast.parse(raw)
    node = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_v92_predict'][-1]
    body = ast.get_source_segment(raw, node)
    changes = [
        ('        votes = sum(1 for ev in best if _hp_quantity(ev, i, step, st["obs"]) >= _V92_P_K)\n        if votes < 1:\n            continue',
         '''        signals = [_hp_quantity(ev, i, step, st["obs"]) >= _V92_P_K for ev in best]
        if not any(signals):
            continue
        weak = not signals[0]
        _XF_REPORT['weak_signals'] += int(weak)
        allowed = True
        if _XF_POLICY == 'rank2': allowed = any(signals[:2])
        if _XF_POLICY == 'quorum': allowed = signals[0] or sum(signals) >= 2
        if not allowed:
            _XF_REPORT['blocked'] += 1
            continue
        horizon = 12 if weak and _XF_POLICY == 'short12' else _V92_P_H'''),
        ('step + _V92_P_H + 1', 'step + horizon + 1'),
        ('        qty = min(int(stock.get(item, 0)), ours)\n        if qty > 0:',
         '''        qty = min(int(stock.get(item, 0)), ours)
        original_qty = qty
        if weak and _XF_POLICY == 'half': qty = (qty+1)//2
        _XF_REPORT['cut_units'] += original_qty-qty
        if qty > 0:
            _XF_REPORT['fires'] += 1
            _XF_EVENTS.append(dict(step=step, item=item, signals=list(signals), weak=weak,
                                   horizon=horizon, stock=int(stock.get(item, 0)), planned=ours,
                                   original_quantity=original_qty, quantity=qty))''')]
    for old, new in changes:
        assert body.count(old) == 1, old
        body = body.replace(old, new)
    head = '''
_XF_PARENT = [v for v in list(globals().values()) if callable(v)][-1]
_XF_POLICY = 'original'
_XF_REPORT = dict(weak_signals=0, blocked=0, cut_units=0, fires=0)
_XF_EVENTS = []
'''
    tail = '''

def extra_forecast_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _XF_EVENTS.clear()
        for k in _XF_REPORT: _XF_REPORT[k] = 0
    start = len(_XF_EVENTS)
    action = _XF_PARENT(observation, configuration)
    for event in _XF_EVENTS[start:]: event['final_market'] = copy.deepcopy(action.get('market') or [])
    return action

extra_forecast_agent.telemetry = _XF_REPORT
'''
    return head+body+tail


def main():
    raw = BASE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '9668e30ad08f79d485bd230a3c660d4cc420b9382e87f9387b6908e3c94a5145'
    code = layer(raw.decode()); configs = {f'extra_{n}': n for n in ('rank2', 'quorum', 'half', 'short12')}
    configs['extra_noop'] = 'original'; OUT.mkdir(parents=True, exist_ok=True); manifest = {}
    for name, policy in configs.items():
        path = OUT/(name+'.py'); assert not path.exists()
        data = raw+b'\n'+code.encode()+f'\n_XF_POLICY={policy!r}\n'.encode()
        compile(data, str(path), 'exec'); path.write_bytes(data)
        manifest[name] = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), config=dict(policy=policy))
    vq = Path('submission/main_publico_arshs3_vq.py')
    assert hashlib.sha256(vq.read_bytes()).hexdigest() == '9b463dfb8076b4c63946e1ae4249cd1cfc3cc58b63115cf2bd5b00f96f188976'
    manifest['vq'] = dict(path=str(vq), sha256=hashlib.sha256(vq.read_bytes()).hexdigest(), config=dict(control=True))
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    candidates = {n: r for n, r in manifest.items() if n not in ('vq', 'extra_noop')}
    (EVIDENCE/'extra_forecast_variants.json').write_text(json.dumps(candidates, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__': main()
