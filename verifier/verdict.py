from dataclasses import dataclass, asdict
from typing import Optional
import json


@dataclass
class Verdict:
    asset: str
    issuer: Optional[str]
    trust_status: str
    hard_binding: str
    soft_binding: str
    verdict: str
    explanation: str

    def to_dict(self):
        return asdict(self)

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
