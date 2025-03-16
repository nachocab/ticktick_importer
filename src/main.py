import argparse
import csv

from ticktick_task import TickTickTask, TickTickTaskName


def write_csv(file_path: str, ticktick_tasks: list[TickTickTask]) -> None:
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        file.writelines(
            [
                "Date: 2025-03-16+0000\n"
                "Version: 7.1\n"
                "Status:\n"
                "0 Normal\n"
                "1 Completed\n"
                "2 Archived\n"
            ]
        )
        writer = csv.DictWriter(file, fieldnames=list(TickTickTaskName))
        writer.writeheader()
        for ticktick_task in ticktick_tasks:
            writer.writerow(ticktick_task.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Dynalist OPML to TickTick CSV.")
    parser.add_argument("-i", "--input", help="Path to the Dynalist OPML file")
    parser.add_argument("-o", "--output", help="Path to the TickTick CSV output file")
    args = parser.parse_args()

    ticktick_tasks = TickTickTask.from_dynalist_opml_file(args.input)
    write_csv(args.output, ticktick_tasks)
