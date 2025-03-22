# Dynalist to TickTick importer

After almost 2000 days using Dynalist (~5.5 years), I've moved my task management to [TickTick](https://ticktick.com/r?c=q6hwo20b).

Since there wasn't a pre-built importer, I wrote my own (customized to how I used Dynalist). If you're in a similar situation, you can use this code to tailor it to your needs.

## Usage

```
poetry run python src/main.py --input /path/to/your-dynalist-file.opml --output /path/to/your-ticktick-to-import-file.csv --list-name NameOfListToImportTo
```
