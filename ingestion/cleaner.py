from bs4 import BeautifulSoup
from pathlib import Path

RAW_PATH = Path("data/raw_docs")
CLEAN_PATH = Path("data/clean_docs")
CLEAN_PATH.mkdir(exist_ok=True)

def clean_html(file_path: Path) -> str:
    soup = BeautifulSoup(file_path.read_text(encoding="utf-8"), "html.parser")

    # Remove nav, footer, scripts
    for tag in soup(["nav", "footer", "script", "style"]):
        tag.decompose()

    main = soup.find("main")
    text = main.get_text(separator="\n") if main else soup.get_text()

    # Clean spacing
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def run():
    for html_file in RAW_PATH.glob("*.html"):
        cleaned = clean_html(html_file)
        out = CLEAN_PATH / f"{html_file.stem}.txt"
        out.write_text(cleaned, encoding="utf-8")
        print(f"Cleaned {html_file.name}")

if __name__ == "__main__":
    run()
