"""프로파일 로더 — YAML 프로파일에서 정체성, 약속, 소스, 시뮬레이터 설정을 로드."""

from __future__ import annotations

import yaml
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class PromiseConfig:
    predicate: str
    rationale: str = ""


@dataclass
class IdentityConfig:
    name: str
    role: str
    permanent_promises: list[PromiseConfig] = field(default_factory=list)


@dataclass
class SourceConfig:
    name: str
    role: str  # identity | memory | knowledge | realtime
    type: str = "mock"  # mock | http | function
    config: dict = field(default_factory=dict)


@dataclass
class SimulatorConfig:
    model: str = "gpt-4.1"
    temperature: float = 0.7
    system_prompt: str = ""


@dataclass
class Profile:
    identity: IdentityConfig
    sources: list[SourceConfig] = field(default_factory=list)
    agent_simulator: SimulatorConfig = field(default_factory=SimulatorConfig)


def load_profile(path: str | Path) -> Profile:
    """YAML 프로파일 파일을 로드한다."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"프로파일을 찾을 수 없다: {path}")

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    identity_data = data.get("identity", {})
    identity = IdentityConfig(
        name=identity_data.get("name", "Agent"),
        role=identity_data.get("role", ""),
        permanent_promises=[
            PromiseConfig(
                predicate=p.get("predicate", ""),
                rationale=p.get("rationale", ""),
            )
            for p in identity_data.get("permanent_promises", [])
        ],
    )

    sources = [
        SourceConfig(
            name=s.get("name", ""),
            role=s.get("role", "knowledge"),
            type=s.get("type", "mock"),
            config=s.get("config", {}),
        )
        for s in data.get("sources", [])
    ]

    sim_data = data.get("agent_simulator", {})
    simulator = SimulatorConfig(
        model=sim_data.get("model", "gpt-4.1"),
        temperature=sim_data.get("temperature", 0.7),
        system_prompt=sim_data.get("system_prompt", ""),
    )

    return Profile(identity=identity, sources=sources, agent_simulator=simulator)
