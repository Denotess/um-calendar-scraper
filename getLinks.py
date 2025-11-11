from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def getDropdownNames(url="https://urnik.fov.um.si/"):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    iframe = soup.find('iframe', {'id': 'iframeContent'})
    iframeUrl = urljoin(url, iframe['src'])

    iframeResponse = requests.get(iframeUrl)
    iframeSoup = BeautifulSoup(iframeResponse.content, 'html.parser')

    dropdowns = iframeSoup.find_all('select')

    names = None

    for dropdown in dropdowns:
        options = dropdown.find_all('option')
        names = []
        for option in options:
            text = option.text.strip()
            if text and text[0].isnumeric():
                names.append(text)
    return names
