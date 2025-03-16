from ticktick_importer.main import TickTickTask, extract_tasks_from_opml, get_ticktick_task


def test_extract_tasks():
    ticktick_tasks = extract_tasks_from_opml("tests/data/dynalist_sample.opml")
    expected = [
        get_ticktick_task(
            {
                TickTickTask.TITLE: "recurrent task mon/tue, early due time",
                TickTickTask.DUE_DATE: "2025-03-15T08:00:00+0000",
                TickTickTask.REPEAT: "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU",
            }
        ),
        get_ticktick_task(
            {
                TickTickTask.TITLE: "regular task with subtasks",
                TickTickTask.DUE_DATE: "2025-03-15T23:00:00+0000",
            }
        ),
        get_ticktick_task(
            {
                TickTickTask.TITLE: "daily recurring task",
                TickTickTask.CONTENT: "multiline\ndescription",
                TickTickTask.DUE_DATE: "2025-03-12T23:00:00+0000",
                TickTickTask.REPEAT: "FREQ=DAILY;INTERVAL=1",
            }
        ),
    ]

    assert len(ticktick_tasks) == len(expected)

    for ticktick_task, index in zip(ticktick_tasks, range(len(ticktick_tasks))):
        assert ticktick_task is not None
        assert ticktick_task == expected[index]


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
