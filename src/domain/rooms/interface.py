from abc import ABC, abstractmethod

from src.domain.schemas import ResultsDTO, RoomsInfo


class IRoom(ABC):
    stats: RoomsInfo

    @abstractmethod
    async def move(self, player_id: str, move_text: str) -> ResultsDTO:
        pass

