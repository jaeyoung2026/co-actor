"""내장 범용 어댑터 — 외부 서비스 없이 바로 사용할 수 있는 어댑터."""

from .identity_adapter import BuiltinIdentityAdapter
from .memory_adapter import BuiltinMemoryAdapter
from .realtime_adapter import BuiltinRealtimeAdapter

__all__ = [
    "BuiltinIdentityAdapter",
    "BuiltinMemoryAdapter",
    "BuiltinRealtimeAdapter",
]
