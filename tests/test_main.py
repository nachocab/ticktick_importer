from src.ticktick_task import TickTickTask, TickTickTaskName


def test_extract_tasks():
    ticktick_tasks = TickTickTask.from_dynalist_opml_file(
        "tests/data/dynalist_sample.opml", list_name="-Hoy  (^D)"
    )
    expected = [
        TickTickTask(
            {
                TickTickTaskName.LIST_NAME: "-Hoy  (^D)",
                TickTickTaskName.TITLE: "recurrent task mon/tue, early due time",
                TickTickTaskName.DUE_DATE: "2025-03-15T08:00:00+0000",
                TickTickTaskName.REPEAT: "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU",
            }
        ),
        TickTickTask(
            {
                TickTickTaskName.LIST_NAME: "-Hoy  (^D)",
                TickTickTaskName.TITLE: "regular task with subtasks",
                TickTickTaskName.DUE_DATE: "2025-03-15T23:00:00+0000",
                TickTickTaskName.CONTENT: ""
                "subtask 1\n"
                "subtask 2\n"
                "    subtask 2a [Pasted image](https://dynalist.io/u/NGyjalPi7yK-jAouOSB5RC-E)\n"
                "    multi\n"
                "    note\n"
                "    subtask 2b\n",
            }
        ),
        TickTickTask(
            {
                TickTickTaskName.LIST_NAME: "-Hoy  (^D)",
                TickTickTaskName.TITLE: "daily recurring task",
                TickTickTaskName.CONTENT: "multiline\ndescription",
                TickTickTaskName.DUE_DATE: "2025-03-12T23:00:00+0000",
                TickTickTaskName.REPEAT: "FREQ=DAILY;INTERVAL=1",
            }
        ),
        TickTickTask(
            {
                TickTickTaskName.LIST_NAME: "-Hoy  (^D)",
                TickTickTaskName.TITLE: "task with image [Pasted image](https://dynalist.io/u/NGyjalPi7yK-jAouOSB5RC-E)",
            }
        ),
    ]

    assert len(ticktick_tasks) == len(expected)

    for index, ticktick_task in enumerate(ticktick_tasks):
        assert ticktick_task is not None
        assert ticktick_task.content == expected[index].content


# ( 1) "Folder Name" - "" 👍
# ( 2) "List Name" - "📥Inbox task list" 👍
# ( 3) "Title" - "high importance tarea for in " 👍
# ( 4) "Kind" - "TEXT" 👍
# ( 5) "Tags" - "my-tag" 👍
# ( 6) "Content" - "with description" 👍
# ( 7) "Is Check list" - "N" 👍
# ( 8) "Start Date" - "2025-03-16T17:00:00+0000" 👍
# ( 9) "Due Date" - "2025-03-16T17:00:00+0000" 👍
# (10) "Reminder" - "PT0S" 👍
# (11) "Repeat" - "" 👍
# (12) "Priority" - "5" 👍
# (13) "Status" - "0" 👍
# (14) "Created Time" - "2025-03-15T15:16:38+0000" 👍
# (15) "Completed Time" - "" 👍
# (16) "Order" - "-1099511627776" ???
# (17) "Timezone" - "Europe/Madrid" 👍
# (18) "Is All Day" - "false" 👍
# (19) "Is Floating" - "false" 👍
# (20) "Column Name" - 👍
# (21) "Column Order" - 👍
# (22) "View Mode" - "list" 👍
# (23) "taskId" - "3" ???
# (24) "parentId" - ""
