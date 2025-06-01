from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ToolData:
    domain: Optional[str] = None
    urls: List[str] = field(default_factory=list)          # Subdomains
    alive_urls: List[str] = field(default_factory=list)
    resolved_ips: List[str] = field(default_factory=list)  # IP sau khi resolve