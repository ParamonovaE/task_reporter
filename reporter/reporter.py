import argparse
import csv
import importlib.util
from pathlib import Path
from tabulate import tabulate

class NewArgumentParser(argparse.ArgumentParser):
    def error(self, message: str):
        if "argument --files:" in message and "expected at least one argument" in message:
            self.exit(2, "Не указано ни одного файла. Используйте --files path1.csv\n")

        if "the following arguments are required: --files" in message:
            self.exit(2, "Не указано ни одного файла. Используйте --files path1.csv\n")

        if "argument --report:" in message and " expected one argument" in message:
            self.exit(2, "Не указан отчёт. Используйте --report <имя>.\n")    

        if "the following arguments are required: --report" in message:
            self.exit(2, "Не указан отчёт. Используйте --report <имя>.\n")

        if "argument --report:" in message and "invalid choice" in message:
            self.exit(2, "Неизвестный отчёт.\n")

        super().error(message)

def discover_reports():
    reports = {}  # словарь для найденных отчётов
    reports_dir = Path(__file__).parent / "reports"  # путь до подкаталога reports
    if not reports_dir.exists():
        return reports

    for file in reports_dir.glob("*.py"):
        mod_name = file.stem  
        spec = importlib.util.spec_from_file_location(mod_name, file)  # план как загрузить модуль с именем mod_name из файла file
        if not spec or not spec.loader:
            continue
        module = importlib.util.module_from_spec(spec)  # пустой объект модуля в памяти
        spec.loader.exec_module(module)  # выполняет код файла внутри этого объекта
        # игнорируем посторонние .py чтобы были только отчеты
        if hasattr(module, "name") and hasattr(module, "title") and hasattr(module, "generate"):
            reports[module.name] = module
    return reports

def parse_args(arguments=None, available_report_names=()):
    parser = NewArgumentParser(description="Анализ товаров")
    parser.add_argument("--files", nargs="+", type=Path, required=True, help="Один или несколько путей к файлам.")
    parser.add_argument("--report", required=True, type=str, choices=sorted(available_report_names), help="Имя отчёта")
    args = parser.parse_args(arguments)
    return args

def load_rows(files):  # все строки из всех CSV
    rows = []
    for path in files:
        if not path.exists() or not path.is_file():
            raise SystemExit(f"Файл не найден: {path}")
        
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({key: (value if isinstance(value, str) else value)
                             for key, value in row.items()})
    return rows
            

def main(arguments=None):
    all_reports = discover_reports()  # находим доступные отчёты заранее
    args = parse_args(arguments, all_reports.keys())
    data = load_rows(args.files)  # загружаем данные
    report_module = all_reports[args.report]  # выбираем отчёт 
    rows = report_module.generate(data)  # генерируем строки
    print(report_module.title)
    if rows:
        print(tabulate(rows, headers="keys", showindex=range(1, len(rows) + 1)))
    else:
        print("Данных нет")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())