from dataclasses import dataclass, field

@dataclass
class TestResults:
    passed: set[str] = field(default_factory=set)
    failed: set[str] = field(default_factory=set)
