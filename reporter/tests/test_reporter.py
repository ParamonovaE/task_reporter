from pathlib import Path
import pytest
import reporter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"  # папка с CSV
CSV1 = DATA_DIR / "products1.csv"
CSV2 = DATA_DIR / "products2.csv"

REPORTS = reporter.discover_reports()
AVAILABLE_REPORT_NAMES = list(REPORTS.keys())   # список доступных имён отчётов
# берем "average-rating", иначе возьмём первый попавшийся 
PREFERRED_REPORT = (
    "average-rating"
    if "average-rating" in REPORTS
    else (AVAILABLE_REPORT_NAMES[0] if AVAILABLE_REPORT_NAMES else None)
)

def test_discover_reports():
    reports = reporter.discover_reports()
    assert isinstance(reports, dict), "discover_reports() должен вернуть dict"
    assert reports, "Нет отчётов в папке 'reports'"
    for mod in reports.values():
        assert hasattr(mod, "name"), "нет name"
        assert hasattr(mod, "title"), "нет title"
        assert hasattr(mod, "generate"), "нет generate"
        assert callable(mod.generate), "generate должна быть функцией"


def test_parse_args_invalid_report():
    if not AVAILABLE_REPORT_NAMES:
        pytest.fail("Нет отчётов в 'reports'")
    with pytest.raises(SystemExit):
        reporter.parse_args(
            ["--files", str(CSV1), "--report", "_no_such_report_"],
            AVAILABLE_REPORT_NAMES,
        )


def test_parse_args_missing_files():
    if PREFERRED_REPORT is None:
        pytest.fail("Нет отчётов в 'reports'")
    with pytest.raises(SystemExit):
        reporter.parse_args(
            ["--report", PREFERRED_REPORT],
            AVAILABLE_REPORT_NAMES,
        )


def test_load_rows_missing_path():
    with pytest.raises(SystemExit) as e:
        reporter.load_rows([PROJECT_ROOT / "data" / "_no_such_.csv"])
    assert "Файл не найден" in str(e.value)
