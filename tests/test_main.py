from ticktick_importer.main import TickTickTask, extract_tasks_from_opml


def test_extract_tasks():
    tasks = extract_tasks_from_opml("tests/data/sample.opml")
    expected_tasks = [
        {
            TickTickTask.FOLDER_NAME: "",
            TickTickTask.LIST_NAME: "",
            TickTickTask.TITLE: "write a parser in python to import from dynalist to ticktick",
            TickTickTask.KIND: "",
            TickTickTask.TAGS: "",
            TickTickTask.CONTENT: "",
            TickTickTask.IS_CHECK_LIST: "",
            TickTickTask.START_DATE: "",
            TickTickTask.DUE_DATE: "2025-03-15T23:00:00+0000",
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
        },
        {
            TickTickTask.FOLDER_NAME: "",
            TickTickTask.LIST_NAME: "",
            TickTickTask.TITLE: "arregla reposapiés taburete",
            TickTickTask.KIND: "",
            TickTickTask.TAGS: "",
            TickTickTask.CONTENT: "asdf\nasdfd",
            TickTickTask.IS_CHECK_LIST: "",
            TickTickTask.START_DATE: "",
            TickTickTask.DUE_DATE: "2025-03-12T23:00:00+0000",
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
        },
    ]

    assert len(tasks) == len(expected_tasks)

    for object, index in zip(tasks, range(len(tasks))):
        assert object == expected_tasks[index]


# ( 1) "Folder Name" - "" 👍
# ( 2) "List Name" - "📥Inbox task list" 👍
# ( 3) "Title" - "high importance tarea for in " 👍
# ( 4) "Kind" - "TEXT" 👍
# ( 5) "Tags" - "my-tag" 👍
# ( 6) "Content" - "with description" 👍
# ( 7) "Is Check list" - "N" 👍
# ( 8) "Start Date" - "2025-03-16T17:00:00+0000" 👍
# ( 9) "Due Date" - "2025-03-16T17:00:00+0000"
# (10) "Reminder" - "PT0S"
# (11) "Repeat" - ""
# (12) "Priority" - "5"
# (13) "Status" - "0"
# (14) "Created Time" - "2025-03-15T15:16:38+0000"
# (15) "Completed Time" - ""
# (16) "Order" - "-1099511627776"
# (17) "Timezone" - "Europe/Madrid"
# (18) "Is All Day" - "false"
# (19) "Is Floating" - "false"
# (20) "Column Name" -
# (21) "Column Order" -
# (22) "View Mode" - "list"
# (23) "taskId" - "3"
# (24) "parentId" - ""
