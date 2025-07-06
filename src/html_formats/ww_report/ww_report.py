from typing import List, Dict, Any

from .constants import CSS_CONSTANTS

from .list_item import WWReportListItem
from .header import WWReportHeader
from .footer import WWReportFooter

from ...items.apple_item import AppleItem

class WWReport():
    def __init__(self,
                 item: AppleItem,
                 genre: str) -> None:
        self.item = item
        self.genre = genre

        self.header = WWReportHeader(item)
        self.footer = WWReportFooter(genre)

    def get_html(self,
                 countries: List[Dict[str, Any]]):
        html = """
                <!DOCTYPE html>
                <html lang="en">
                """

        html += CSS_CONSTANTS

        html += """
                <body>
                <div class="ranking-card">
                """

        html += self.header.get_html()

        for country_data in countries:
            country = country_data["country"]
            position = country_data["position"]

            list_item = WWReportListItem(country, position)

            html += list_item.get_html()

        html += self.footer.get_html()

        html += """
                    </div>
                </body>
                </html>
                """

        return html
