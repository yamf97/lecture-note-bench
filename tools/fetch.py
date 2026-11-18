#!/usr/bin/env python3
"""껍데기 — 본체는 src/lnb/fetch.py. 설치했으면 `lnb …` 로 부른다 (README 「설치」).

설치 없이 저장소에서 `python3 tools/fetch.py …` 로 불러도 예전과 똑같이 돈다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "src"))
from lnb.fetch import *  # noqa: E402,F401,F403 — 예전처럼 이 파일에서 import 하던 코드를 위해
from lnb.fetch import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
