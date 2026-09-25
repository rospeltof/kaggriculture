"""Run the 30 registered development games for buy-slot/size interventions."""
from sonda_alimentacion_economica import main


if __name__ == '__main__':
    main(manifest_path='results/trigo_reventa_20260925/manifest.json',
         tag='wheat_trade_smoke', seeds=(588616997, 1045000, 1028000),
         noop_name='wheat_noop', extra_reports=('_WT_REPORT',), extra_events=('_WT_EVENTS',))
