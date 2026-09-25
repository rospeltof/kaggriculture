"""Thirty registered development games; full market and field ledgers."""
from sonda_alimentacion_economica import main


if __name__ == '__main__':
    main(manifest_path='results/reventa_town_20260925/manifest.json',
         tag='town_trade_smoke', seeds=(1048000, 1048001, 588616997),
         noop_name='town_noop', extra_reports=('_TR_REPORT',), extra_events=('_TR_EVENTS',))
