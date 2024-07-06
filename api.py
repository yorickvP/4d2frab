from __future__ import annotations

import json
from datetime import datetime  # noqa: TCH003
from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from pathlib import Path

from pydantic import BaseModel


class DayAPI(BaseModel):
    id: int
    title: str
    date: datetime


class GenreAPI(BaseModel):
    id: int
    title: str
    description_short: str | None
    url: str
    postDate: datetime
    dateUpdated: datetime


DayPart = Literal["evening", "afternoon", "night"]


class LatLong(BaseModel):
    lat: float
    lng: float


class LocationAPI(BaseModel):
    id: int
    title: str
    description_short: str | None
    description: str | None
    marker: LatLong | None
    logo: str | None
    images: list
    url: str
    slug: str
    # "type": str
    mapboxImage: str | None
    customData: Any
    parent: int | None
    hasProgramOn: list[DayPart | None]
    postDate: datetime
    dateUpdated: datetime


class Ref(BaseModel):
    id: int

class DayRef(Ref):
    date: datetime


class Social(BaseModel):
    type: str
    url: str


class ProgramAPI(BaseModel):
    id: int
    act_id: int
    title: str
    day: DayRef
    day_part: DayPart
    sortDate: str
    start_time: str
    end_time: str
    location: Ref | None
    genres: list[Ref]
    theme: Ref | None
    is_highlight: bool
    originCountry: bool
    sort: None
    customData: Any
    ageWarnings: list[None]
    website: str | None
    description_short: str | None
    description: str
    images: list[dict]
    videolink: str | None
    tickets_price: float | None
    tickets_link: str | None
    tickets_soldout: bool
    url: str
    postDate: datetime
    dateUpdated: datetime
    socials: list[Social]
    related: list[str]
    slug: str
    shareText: str
    searchWords: None


class AllAPI(BaseModel):
    general: dict
    ads: list
    content: list
    coupons: list
    days: list[DayAPI]
    faq: list
    faqCategories: list
    food: list
    foodKitchen: list
    foodThemes: list
    genres: list[GenreAPI]
    locations: list[LocationAPI]
    onboarding: list
    partnerTypes: list
    partners: list
    poi: list
    poiCategories: list
    programs: list[ProgramAPI]
    themes: list
    updates: list

    @cached_property
    def days_ids(self) -> dict[int, DayAPI]:
        return {day.id: day for day in self.days}

    @cached_property
    def locations_ids(self) -> dict[int, LocationAPI]:
        return {location.id: location for location in self.locations}

    @cached_property
    def genres_ids(self) -> dict[int, GenreAPI]:
        return {genre.id: genre for genre in self.genres}

    @cached_property
    def programs_ids(self) -> dict[int, ProgramAPI]:
        return {program.id: program for program in self.programs}

    def day_ix_by_id(self, day_id: int) -> int:
        return next(i for i, day in enumerate(self.days) if day.id == day_id)

    def top_location(self, loc: LocationAPI) -> LocationAPI:
        while loc.parent is not None:
            loc = self.locations_ids[loc.parent]
        return loc


def load_api(p: Path) -> AllAPI:
    with p.open() as file:
        return AllAPI(**json.load(file))