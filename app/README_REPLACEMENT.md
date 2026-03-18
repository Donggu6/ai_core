# Replacement-ready app folder

이 폴더는 기존 `app` 폴더를 **통째로 교체할 수 있게** 다시 정리한 버전입니다.

## 포함된 정리
- `domain/entities` 추가
- `platform` 추가
- `services/llm/*` 패키지화
- `services/scoring/core.py` 분리
- `features/common/builder.py` 분리
- 기존 import 호환용 shim 유지

## 교체 방법
1. 기존 폴더 백업
2. 이 ZIP을 풀면 나오는 `app` 폴더를 기존 위치에 덮어쓰기
3. 서버 실행
4. 문제가 있으면 `app_backup`으로 롤백

## 기대 결과
- 기존 import 대부분 유지
- 새 구조도 같이 확보
- 점진 리팩토링 준비 완료
