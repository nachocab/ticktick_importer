from typing import Optional
from enum import StrEnum
import re

DYNALIST_ITEM_PATTERN = re.compile(
    r"\s*"
    r"(?:"
    r"(\d+)\s*"  # importance
    r")?"
    #
    r"(?:"
    r"!\("
    r"(\d{4}-\d{2}-\d{2})\s*"  # date
    #
    r"(?:"
    r"\|\s*"
    r"([^)]+)\s*"  # recurrence
    r")?"
    #
    r"\)\s*"
    r")?"
    #
    r"(.*)"  # Title
)

TAB = "    "


class DynalistTaskName(StrEnum):
    IMPORTANCE = "importance"
    DUE_DATE = "due_date"
    RECURRENCE = "recurrence"
    TITLE = "title"
    DESCRIPTION = "description"


class DynalistTask:
    content: dict

    def __init__(self, element):
        self.content = {}

        match = re.fullmatch(DYNALIST_ITEM_PATTERN, element.get("text"))

        if not match:
            raise ValueError(f"Invalid task: {element.get('text')}")

        importance, due_date, recurrence, title = match.groups()

        if note := element.get("_note"):
            self.content[DynalistTaskName.DESCRIPTION] = note

        if children := element.getchildren():
            self.content[DynalistTaskName.DESCRIPTION] = (
                f"{self.content.get(DynalistTaskName.DESCRIPTION, "")}"
                f"{self.to_nested_markdown_list(children)}"
            )

        if importance:
            self.content[DynalistTaskName.IMPORTANCE] = int(importance)

        if due_date:
            self.content[DynalistTaskName.DUE_DATE] = (
                f"{due_date}T{self.get_hour_from_importance(importance)}:00:00+0000"
            )

        if recurrence:
            self.content[DynalistTaskName.RECURRENCE] = self.get_icalendar_rrule(recurrence)

        self.content[DynalistTaskName.TITLE] = self.format_title(title)

    @staticmethod
    def format_title(title: str) -> str:
        return title.replace("👟", "").replace("![", "[").strip()

    @staticmethod
    def to_nested_markdown_list(elements) -> str:
        def to_markdown_list(elements, level=0):
            markdown = ""
            for element in elements:
                title = DynalistTask.format_title(element.get("text"))
                markdown += f"{TAB * level}{title}\n"

                if note := element.get("_note"):
                    notes = note.split("\n")
                    for note in notes:
                        markdown += f"{TAB * (level)}{DynalistTask.format_title(note)}\n"

                if children := element.getchildren():
                    markdown += to_markdown_list(children, level + 1)

            return markdown

        return to_markdown_list(elements)

    @staticmethod
    def get_hour_from_importance(importance: str) -> str:
        match importance:
            case None:
                return "23"

            case imp if int(imp) < 10:
                return "08"

            case imp:
                return importance

    @staticmethod
    def get_icalendar_rrule(dynalist_recurrence: str) -> Optional[str]:
        if not dynalist_recurrence:
            return None

        match = re.match(r"(\d+)([dwmy])(\d*)", dynalist_recurrence.strip().lower())
        if not match:
            return None

        interval, unit, days = match.groups()
        interval = int(interval)

        freq_map = {"d": "DAILY", "w": "WEEKLY", "m": "MONTHLY", "y": "YEARLY"}
        freq = freq_map.get(unit)
        if not freq:
            return None

        rrule = f"FREQ={freq};INTERVAL={interval}"

        if days:
            day_map = {"1": "MO", "2": "TU", "3": "WE", "4": "TH", "5": "FR", "6": "SA", "7": "SU"}
            byday = ",".join(day_map[d] for d in days if d in day_map)
            rrule += f";BYDAY={byday}"

        return rrule
