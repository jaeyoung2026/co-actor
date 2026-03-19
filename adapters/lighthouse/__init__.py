"""lighthouse 소스 어댑터 — Co-actor Engine에 lighthouse 데이터를 연결하는 예제.

이 어댑터는 두 가지 모드로 동작한다:
1. sample 모드: 내장 샘플 데이터로 동작 (기본, 도입 테스트용)
2. live 모드: 실제 외부 기억 시스템에 연결

도입자는 이 어댑터를 참고하여 자기 서비스의 어댑터를 만들면 된다.
"""

from .identity_adapter import LighthouseIdentityAdapter
from .memory_adapter import LighthouseMemoryAdapter
from .knowledge_adapter import LighthouseKnowledgeAdapter
from .realtime_adapter import LighthouseRealtimeAdapter

__all__ = [
    "LighthouseIdentityAdapter",
    "LighthouseMemoryAdapter",
    "LighthouseKnowledgeAdapter",
    "LighthouseRealtimeAdapter",
]
