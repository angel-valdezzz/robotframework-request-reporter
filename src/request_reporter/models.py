"""Serializable report records, independent of Robot execution objects."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Validation:
    label: str
    keyword: str
    status: str
    actual: Any = None
    expected: Any = None
    arguments: list[Any] = field(default_factory=list)
    error: str = ""


@dataclass
class Exchange:
    id: str
    name: str
    method: str
    url: str
    status_code: int
    duration_ms: float
    request_headers: dict[str, str]
    response_headers: dict[str, str]
    request_body: Any
    response_body: Any
    validations: list[Validation] = field(default_factory=list)


@dataclass
class ExecutionError:
    keyword: str
    message: str


@dataclass
class RequestError:
    name: str
    method: str
    url: str
    message: str


@dataclass
class Case:
    name: str
    source: str
    test_id: str
    started: str
    suite: str = ""
    status: str = "RUNNING"
    duration_ms: float = 0
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    exchanges: list[Exchange] = field(default_factory=list)
    execution_errors: list[ExecutionError] = field(default_factory=list)
    request_errors: list[RequestError] = field(default_factory=list)
    ended: str | None = None
