import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.rss_fetcher import extract_company_and_title


def test_extract_company_with_colon_format():
    """Test parsing 'Company: Job Title' dari title RSS."""
    entry = {"title": "Google: Senior Backend Engineer", "author": ""}
    company, title = extract_company_and_title(entry)
    assert company == "Google"
    assert title == "Senior Backend Engineer"


def test_extract_company_from_author_field():
    """Test kalau field author sudah terisi, pakai itu."""
    entry = {"title": "Some Job Title", "author": "Amazon"}
    company, title = extract_company_and_title(entry)
    assert company == "Amazon"
    assert title == "Some Job Title"


def test_extract_company_fallback_when_no_colon():
    """Test kalau title nggak ada format 'Company: Title'."""
    entry = {"title": "Just A Job Title Without Colon", "author": ""}
    company, title = extract_company_and_title(entry)
    assert company == "Tidak diketahui"
    assert title == "Just A Job Title Without Colon"