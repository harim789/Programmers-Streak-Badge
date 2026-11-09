import sys
from pathlib import Path

# streak/ 모듈을 평평하게 import (main.py가 스크립트로 실행될 때와 같은 방식)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
