"""Reuse the accepted-feed instrumentation with an independent frozen plan."""
from construir_bonus_limitado import OUT
from sonda_alimentacion_economica import main


if __name__=='__main__':
    main(manifest_path=OUT/'manifest.json',tag='capped_bonus_smoke',
         seeds=(1039000,1004000,1272457736),noop_name='cap_noop',extra_reports=('_BC_REPORT',))
