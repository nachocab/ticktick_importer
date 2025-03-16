from enum import StrEnum
import re
from typing import Optional
from lxml import etree
from datetime import datetime, timezone


class DynalistTask(StrEnum):
    IMPORTANCE = "importance"
    DUE_DATE = "due_date"
    RECURRENCE = "recurrence"
    TITLE = "title"


class TickTickTask(StrEnum):
    FOLDER_NAME = "Folder Name"
    LIST_NAME = "List Name"
    TITLE = "Title"
    KIND = "Kind"
    TAGS = "Tags"
    CONTENT = "Content"
    IS_CHECK_LIST = "Is Check list"
    START_DATE = "Start Date"
    DUE_DATE = "Due Date"
    REMINDER = "Reminder"
    REPEAT = "Repeat"
    PRIORITY = "Priority"
    STATUS = "Status"
    CREATED_TIME = "Created Time"
    COMPLETED_TIME = "Completed Time"
    ORDER = "Order"
    TIMEZONE = "Timezone"
    IS_ALL_DAY = "Is All Day"
    IS_FLOATING = "Is Floating"
    COLUMN_NAME = "Column Name"
    COLUMN_ORDER = "Column Order"
    VIEW_MODE = "View Mode"
    TASK_ID = "taskId"
    PARENT_ID = "parentId"


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


def get_ticktick_task(args):
    default_task = {
        TickTickTask.FOLDER_NAME: "",
        TickTickTask.LIST_NAME: "📥Inbox task list",
        TickTickTask.TITLE: "",
        TickTickTask.KIND: "",
        TickTickTask.TAGS: "",
        TickTickTask.CONTENT: "",
        TickTickTask.IS_CHECK_LIST: "N",
        TickTickTask.START_DATE: "",
        TickTickTask.DUE_DATE: "",
        TickTickTask.REMINDER: "",
        TickTickTask.REPEAT: "",
        TickTickTask.PRIORITY: "",
        TickTickTask.STATUS: "0",
        TickTickTask.CREATED_TIME: get_current_date(),
        TickTickTask.COMPLETED_TIME: "",
        TickTickTask.ORDER: "",
        TickTickTask.TIMEZONE: "Europe/Madrid",
        TickTickTask.IS_ALL_DAY: "false",
        TickTickTask.IS_FLOATING: "false",
        TickTickTask.COLUMN_NAME: "",
        TickTickTask.COLUMN_ORDER: "",
        TickTickTask.VIEW_MODE: "list",
        TickTickTask.TASK_ID: "",
        TickTickTask.PARENT_ID: "",
    }

    for key, value in args.items():
        if value is not None:
            default_task[key] = value

    return default_task


def get_dynalist_task_details(text: str) -> dict:
    match = re.fullmatch(DYNALIST_ITEM_PATTERN, text)
    if not match:
        return {}

    importance, due_date, recurrence, title = match.groups()
    result = {}

    if importance:
        result[DynalistTask.IMPORTANCE] = int(importance)

    if due_date:
        result[DynalistTask.DUE_DATE] = (
            f"{due_date}T{get_hour_from_importance(importance)}:00:00+0000"
        )

    if recurrence:
        result[DynalistTask.RECURRENCE] = get_icalendar_rrule(recurrence)

    if title:
        result[DynalistTask.TITLE] = title.strip()

    return result


def get_hour_from_importance(importance: str) -> str:
    match importance:
        case None:
            return "23"

        case imp if int(imp) < 10:
            return "08"

        case imp:
            return importance


def get_current_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")


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


def extract_tasks_from_opml(file_path):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    tasks = []

    def get_nesting_info(element, level=0):
        text = element.get("text", "")
        note = element.get("_note", "")

        if bool(re.search(r"!\(", text)):
            dynalist_task = get_dynalist_task_details(text)
            # parent = element.xpath("..")[0]  # Direct parent

            task = get_ticktick_task(
                {
                    TickTickTask.TITLE: dynalist_task.get(DynalistTask.TITLE),
                    TickTickTask.DUE_DATE: dynalist_task.get(DynalistTask.DUE_DATE),
                    TickTickTask.REPEAT: dynalist_task.get(DynalistTask.RECURRENCE),
                    TickTickTask.CONTENT: note,
                }
            )
            tasks.append(task)

        for child in element:
            get_nesting_info(child, level + 1)

    get_nesting_info(root.xpath(".//outline")[0])

    return tasks


if __name__ == "__main__":
    3
    # file_path = "dynalist_export.opml"
    # tasks = extract_tasks_from_opml(file_path)
    # for task in tasks:
    #     print(f"Task: {task['text']}")
    #     print(f"Level: {task['level']}, Parent: {task['parent']}\n")
