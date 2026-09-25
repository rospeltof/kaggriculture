"""Apply the same actual-feed/source/control checks to the independent cap study."""
from verificar_alimentacion_economica import main


if __name__=='__main__':
    main(tag='capped_bonus_smoke',manifest_file='capped_bonus_variants.json',
         output_file='capped_bonus_validation.json',expected_games=24,noop_name='cap_noop')
