from datetime import datetime, timezone
import re


def generate_time() -> datetime:
    return datetime.now(timezone.utc)


PAGE_RANGE_REGEX = re.compile(r'^\s*(\d+(-\d+)?)(\s*,\s*(\d+(-\d+)?))*\s*$')

def is_valid_page_range(page_range: str) -> bool:
    return bool(PAGE_RANGE_REGEX.match(page_range))


def count_pages_in_range(page_range: str, total_pages: int | None = None) -> int:
    is_valid = is_valid_page_range(page_range)
    if not is_valid:
        return 0
    
    page_numbers = set()  

    for part in page_range.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            if start > end or start < 1 or end < 1:
                return 0
            if total_pages and end > total_pages:
                return 0
            page_numbers.update(range(start, end + 1))
        else:
            page = int(part)
            if page < 1:
                return 0
            if total_pages and page > total_pages:
                return 0
            page_numbers.add(page)

    return len(page_numbers)


if __name__ == "__main__":
    page_range = "1-9, 10"
    print(count_pages_in_range(page_range, 10))
