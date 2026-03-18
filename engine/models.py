from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class AgencyGradient(str, Enum):
    doing = "doing"
    suggesting = "suggesting"
    asking = "asking"


class FailureLayer(str, Enum):
    promise = "promise"
    attention = "attention"
    relationship = "relationship"


class PromiseStatus(str, Enum):
    active = "active"
    kept = "kept"
    broken = "broken"
    revised = "revised"


class Promise(BaseModel):
    id: str
    predicate: str
    source_turn: int
    is_permanent: bool
    status: PromiseStatus = PromiseStatus.active
    evidence: str | None = None


class AttentionSlot(BaseModel):
    label: str
    content: str
    relevance: float = Field(ge=0.0, le=1.0)


class AttentionFrame(BaseModel):
    slots: list[AttentionSlot]
    entropy: float = Field(ge=0.0, le=1.0)


class RelationshipEntry(BaseModel):
    turn: int
    initiative_balance: float = Field(ge=-1.0, le=1.0)
    agency_gradient: AgencyGradient
    boundary_event: str | None = None
    recovery_event: str | None = None


class Violation(BaseModel):
    promise_id: str
    description: str
    severity: Literal["minor", "major"]


class TurnContext(BaseModel):
    conversation_id: str
    turn_number: int
    user_message: str
    conversation_summary: str
    agent_state: dict | None = None


class TurnResult(BaseModel):
    conversation_id: str
    turn_number: int
    agent_output: str
    tools_used: list[str] = Field(default_factory=list)
    agent_state_after: dict | None = None


class PlanResult(BaseModel):
    promise_snapshot: list[Promise]
    attention_frame: AttentionFrame
    relationship_constraints: list[str]
    agency_gradient_hint: AgencyGradient


class AuditResult(BaseModel):
    promise_kept: bool
    attention_appropriate: bool
    relationship_strengthened: bool
    violations: list[Violation]
    relationship_impact: Literal["positive", "neutral", "negative"]
    promise_revisions: list[Promise]
    failure_layer: FailureLayer | None = None


class ConversationState(BaseModel):
    conversation_id: str
    turn_count: int = 0
    promises: list[Promise] = Field(default_factory=list)
    attention_history: list[AttentionFrame] = Field(default_factory=list)
    relationship_ledger: list[RelationshipEntry] = Field(default_factory=list)
    last_audit: AuditResult | None = None
