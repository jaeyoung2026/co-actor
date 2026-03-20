"""프로파일 로더 — YAML 프로파일에서 정체성, 약속, 소스, 시나리오, 시뮬레이터 설정을 로드."""

from __future__ import annotations

import yaml
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class PromiseConfig:
    predicate: str
    rationale: str = ""
    antipattern: str = ""


@dataclass
class IdentityConfig:
    name: str
    role: str
    permanent_promises: list[PromiseConfig] = field(default_factory=list)


@dataclass
class SourceConfig:
    name: str
    role: str  # identity | memory | knowledge | realtime
    type: str = "mock"  # mock | builtin | adapter
    config: dict = field(default_factory=dict)


@dataclass
class ScenarioConfig:
    name: str
    signal: str = ""
    agency_default: str = "suggesting"  # doing | suggesting | asking
    situational_promises: list[str] = field(default_factory=list)


@dataclass
class ScenariosConfig:
    classification: list[ScenarioConfig] = field(default_factory=list)
    audit_domain_checklist: list[str] = field(default_factory=list)


@dataclass
class SimulatorConfig:
    model: str = "gemini-3-flash-preview"
    temperature: float = 0.7
    system_prompt: str = ""


@dataclass
class Profile:
    identity: IdentityConfig
    sources: list[SourceConfig] = field(default_factory=list)
    agent_simulator: SimulatorConfig = field(default_factory=SimulatorConfig)
    system_prompt: str = ""
    first_visit: str = ""
    revisit: str = ""
    scenarios: ScenariosConfig = field(default_factory=ScenariosConfig)


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
                antipattern=p.get("antipattern", ""),
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
        model=sim_data.get("model", "gemini-3-flash-preview"),
        temperature=sim_data.get("temperature", 0.7),
        system_prompt=sim_data.get("system_prompt", ""),
    )

    # 시나리오
    scenarios_data = data.get("scenarios", {})
    scenarios = ScenariosConfig(
        classification=[
            ScenarioConfig(
                name=sc.get("name", ""),
                signal=sc.get("signal", ""),
                agency_default=sc.get("agency_default", "suggesting"),
                situational_promises=sc.get("situational_promises", []),
            )
            for sc in scenarios_data.get("classification", [])
        ],
        audit_domain_checklist=scenarios_data.get("audit_domain_checklist", []),
    )

    return Profile(
        identity=identity,
        sources=sources,
        agent_simulator=simulator,
        system_prompt=data.get("system_prompt", ""),
        first_visit=data.get("first_visit", ""),
        revisit=data.get("revisit", ""),
        scenarios=scenarios,
    )
