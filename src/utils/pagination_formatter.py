from dataclasses import dataclass
from math import ceil
from typing import Generic, TypeVar

TItem = TypeVar("TItem")

@dataclass
class PaginationParams(Generic[TItem]):
    data: list[TItem]
    page: int
    limit: int
    total_records: int
    show_all: bool | None = False

@dataclass
class PaginationResponse(Generic[TItem]):
    data: list[TItem]
    current_page: int
    records_per_page: int
    total_records: int
    total_pages: int
    has_next_page: bool

@dataclass
class AllDataResponse(Generic[TItem]):
    data: list[TItem]
    total_records: int

PaginationResult = PaginationResponse[TItem] | AllDataResponse[TItem]

def pagination_formatter(params: PaginationParams[TItem]) -> PaginationResult:
    if params.show_all:
        return AllDataResponse(
            data=params.data,
            total_records=params.total_records or len(params.data)
        )

    total_pages = ceil(params.total_records / params.limit)
    has_next_page = params.page < total_pages

    return PaginationResponse(
        data=params.data,
        current_page=params.page,
        records_per_page=params.limit,
        total_records=params.total_records,
        total_pages=total_pages,
        has_next_page=has_next_page
    )
