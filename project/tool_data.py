from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ToolData:
    domain: Optional[str] = None
    urls: List[str] = field(default_factory=list)          # Subdomains
    alive_urls: List[str] = field(default_factory=list)
    resolved_ips: List[str] = field(default_factory=list)  # IP sau khi resolve
    form_links: List[str] = field(default_factory=list)
    api_links: List[str] = field(default_factory=list)
    static_links: List[str] = field(default_factory=list)
    httpx_results: list[str] = field(default_factory=list)
    ffuf_paths: list[str] = field(default_factory=list)
    open_ports: list[int] = field(default_factory=list)
    sqli_results: list[str] = field(default_factory=list)
    xss_targets: list[str] = field(default_factory=list)
    xss_results: list[str] = field(default_factory=list)
    a05_misconfig: list[str] = field(default_factory=list)



