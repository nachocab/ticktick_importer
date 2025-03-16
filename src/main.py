import csv

from ticktick_task import TickTickTask, TickTickTaskName


def write_csv(file_path: str, ticktick_tasks: list[TickTickTask]) -> None:
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(TickTickTaskName))
        writer.writeheader()
        for ticktick_task in ticktick_tasks:
            writer.writerow(ticktick_task.content)


if __name__ == "__main__":
    dynalist_opml_file_path = "ignored/dynalist-2025-3-15.opml"
    ticktick_tasks = TickTickTask.from_opml_file(dynalist_opml_file_path)

    write_csv("ignored/2025-03-15-dynalist-to-ticktick.csv", ticktick_tasks)

    # for task in tasks:
    #     print(f"Task: {task['text']}")
    #     print(f"Level: {task['level']}, Parent: {task['parent']}\n")
