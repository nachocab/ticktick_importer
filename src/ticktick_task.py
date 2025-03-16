from enum import StrEnum
from xml.etree.ElementTree import Element

from lxml import etree
from dynalist_task import DynalistTask, DynalistTaskName
from get_current_date import (
    get_current_date,
)
from typing import Optional


class TickTickTaskName(StrEnum):
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


DEFAULT_TICKTICK_TASK = {
    TickTickTaskName.FOLDER_NAME: "",
    TickTickTaskName.LIST_NAME: "Personal",
    TickTickTaskName.TITLE: "",
    TickTickTaskName.KIND: "",
    TickTickTaskName.TAGS: "",
    TickTickTaskName.CONTENT: "",
    TickTickTaskName.IS_CHECK_LIST: "N",
    TickTickTaskName.START_DATE: "",
    TickTickTaskName.DUE_DATE: "",
    TickTickTaskName.REMINDER: "",
    TickTickTaskName.REPEAT: "",
    TickTickTaskName.PRIORITY: "",
    TickTickTaskName.STATUS: "0",
    TickTickTaskName.CREATED_TIME: get_current_date(),
    TickTickTaskName.COMPLETED_TIME: "",
    TickTickTaskName.ORDER: "",
    TickTickTaskName.TIMEZONE: "Europe/Madrid",
    TickTickTaskName.IS_ALL_DAY: "false",
    TickTickTaskName.IS_FLOATING: "false",
    TickTickTaskName.COLUMN_NAME: "",
    TickTickTaskName.COLUMN_ORDER: "",
    TickTickTaskName.VIEW_MODE: "list",
    TickTickTaskName.TASK_ID: "",
    TickTickTaskName.PARENT_ID: "",
}


class TickTickTask:
    content: dict = {}

    def __init__(self, args):
        self.content = DEFAULT_TICKTICK_TASK.copy()

        for key, value in args.items():
            if value is not None:
                self.content[key] = value

    @staticmethod
    def from_dynalist_element(element: Element) -> Optional["TickTickTask"]:
        if dynalist_task := DynalistTask(element):
            return TickTickTask(
                {
                    TickTickTaskName.TITLE: dynalist_task.content.get(DynalistTaskName.TITLE),
                    TickTickTaskName.DUE_DATE: dynalist_task.content.get(DynalistTaskName.DUE_DATE),
                    TickTickTaskName.REPEAT: dynalist_task.content.get(DynalistTaskName.RECURRENCE),
                    TickTickTaskName.CONTENT: dynalist_task.content.get(
                        DynalistTaskName.DESCRIPTION
                    ),
                }
            )

    @staticmethod
    def from_dynalist_opml_file(opml_file_path: str) -> list["TickTickTask"]:
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(opml_file_path, parser)
        dynalist_tasks = tree.getroot().xpath(".//outline")[0].getchildren()

        return [
            ticktick_task
            for dynalist_task in dynalist_tasks
            if (ticktick_task := TickTickTask.from_dynalist_element(dynalist_task))
        ]
