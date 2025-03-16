from lxml import etree

from ticktick_importer.ticktick_task import TickTickTask


def process_dynalist_tasks(opml_file_path: str) -> list:
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(opml_file_path, parser)
    dynalist_tasks = tree.getroot().xpath(".//outline")[0].getchildren()

    return [
        ticktick_task
        for dynalist_task in dynalist_tasks
        if (ticktick_task := TickTickTask.from_dynalist_task(dynalist_task))
    ]


if __name__ == "__main__":
    3
    # file_path = "dynalist_export.opml"
    # tasks = extract_tasks_from_opml(file_path)
    # for task in tasks:
    #     print(f"Task: {task['text']}")
    #     print(f"Level: {task['level']}, Parent: {task['parent']}\n")
