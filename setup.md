# Setup (Dependencies)

## 목적
이 문서는 의존성 설치 절차만 정리한다. 프로젝트 구조/설정은 별도 태스크에서 확정한다.

## 절차 (cmd)
1. `python -m venv .venv`
2. `.\.venv\Scripts\activate`
3. `python -m pip install -r requirements.txt`
4. `python -m playwright install`

## 참고
- Windows에서 `mysqlclient` 설치가 실패하면 C++ Build Tools가 필요할 수 있다.
