from src.ticktick_task import TickTickTask, TickTickTaskName


def test_extract_tasks():
    ticktick_tasks = TickTickTask.from_dynalist_opml_file(
        "tests/data/dynalist_sample.opml", list_name="-Hoy  (^D)"
    )
    expected = [
        TickTickTask(
            {
                TickTickTaskName.LIST_NAME: "-Hoy  (^D)",
                TickTickTaskName.TITLE: "recurrent task\nmon/tue, early due time",
                TickTickTaskName.DUE_DATE: "2025-03-15T08:00:00+0000",
                TickTickTaskName.REPEAT: "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU",
            }
        ),
        TickTickTask(
            {
                TickTickTaskName.LIST_NAME: "-Hoy  (^D)",
                TickTickTaskName.TITLE: "regular task with subtasks",
                TickTickTaskName.DUE_DATE: "2025-03-15T20:00:00+0000",
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
                TickTickTaskName.DUE_DATE: "2025-03-12T20:00:00+0000",
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

