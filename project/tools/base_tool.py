from abc import ABC, abstractmethod
from tool_data import ToolData

class BaseTool(ABC):
    @abstractmethod
    def run(self, data: ToolData) -> ToolData:
        pass

    @abstractmethod
    def name(self) -> str:
        pass
