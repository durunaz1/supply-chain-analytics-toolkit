from pathlib import Path
from src.pipeline import run
if __name__=='__main__':
 source=Path('data/raw/world_bank_awards.csv')
 if not source.exists():
  raise SystemExit('Official CSV missing. Download from https://financesone.worldbank.org/d/DS00028 and save as data/raw/world_bank_awards.csv')
 print(run(source,'outputs'))
