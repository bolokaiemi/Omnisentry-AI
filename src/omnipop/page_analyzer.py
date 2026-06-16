from bs4 import BeautifulSoup


def analyze_page(html: str):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    forms = len(
        soup.find_all("form")
    )

    inputs = len(
        soup.find_all("input")
    )

    return {
        "forms": forms,
        "inputs": inputs
    }