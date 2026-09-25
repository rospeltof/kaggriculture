"""Forty-two fixed development games with top3/noop/VQ and four policies."""
from sonda_alimentacion_economica import main


if __name__ == '__main__':
    main(manifest_path='results/senales_extra_20260925/manifest.json',
         tag='extra_forecast_smoke', seeds=(1051000, 1326447728, 1418183474),
         noop_name='extra_noop', extra_reports=('_XF_REPORT',), extra_events=('_XF_EVENTS',))
