from enum import StrEnum
import re
from typing import Optional
from lxml import etree


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


class DynalistTask(StrEnum):
    IMPORTANCE = "importance"
    DUE_DATE = "due_date"
    RECURRENCE = "recurrence"
    TITLE = "title"
    DESCRIPTION = "description"


def get_dynalist_task(text: str) -> dict:
    match = re.fullmatch(DYNALIST_ITEM_PATTERN, text)
    if not match:
        return {}

    importance, due_date, recurrence, title = match.groups()
    result = {}

    if importance:
        result[DynalistTask.IMPORTANCE] = int(importance)
    if due_date:
        result[DynalistTask.DUE_DATE] = f"{due_date}T23:00:00+0000"
    if recurrence:
        result[DynalistTask.RECURRENCE] = recurrence
    if title:
        result[DynalistTask.TITLE] = title.strip()

    return result


def extract_tasks_from_opml(file_path):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    tasks = []

    def get_nesting_info(element, level=0):
        text = element.get("text", "")
        note = element.get("_note", "")

        if bool(re.match(r"\s*!\(", text)):
            dynalist_task = get_dynalist_task(text)
            # parent = element.xpath("..")[0]  # Direct parent

            task = {
                TickTickTask.FOLDER_NAME: "",
                TickTickTask.LIST_NAME: "",
                TickTickTask.TITLE: dynalist_task.get(DynalistTask.TITLE, ""),
                TickTickTask.KIND: "",
                TickTickTask.TAGS: "",
                TickTickTask.CONTENT: note,
                TickTickTask.IS_CHECK_LIST: "",
                TickTickTask.START_DATE: "",
                TickTickTask.DUE_DATE: dynalist_task.get(DynalistTask.DUE_DATE, ""),
                TickTickTask.REMINDER: "",
                TickTickTask.REPEAT: "",
                TickTickTask.PRIORITY: "",
                TickTickTask.STATUS: "",
                TickTickTask.CREATED_TIME: "",
                TickTickTask.COMPLETED_TIME: "",
                TickTickTask.ORDER: "",
                TickTickTask.TIMEZONE: "",
                TickTickTask.IS_ALL_DAY: "",
                TickTickTask.IS_FLOATING: "",
                TickTickTask.COLUMN_NAME: "",
                TickTickTask.COLUMN_ORDER: "",
                TickTickTask.VIEW_MODE: "",
                TickTickTask.TASK_ID: "",
                TickTickTask.PARENT_ID: "",
            }
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
