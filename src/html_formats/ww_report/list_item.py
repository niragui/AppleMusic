from ...common.countries_handle import get_country_flag_iso, get_country_iso


class WWReportListItem():
    def __init__(self,
                 country: str,
                 position: int) -> None:
        self.country = country
        self.iso_code = get_country_iso(country)
        self.flag = get_country_flag_iso(self.iso_code)

        self.position = position

    def get_html(self):
        return f"""
                <div class="country-item">
                    <img src="{self.flag}" alt="{self.iso_code} Flag" class="flag">
                    <div class="country-info">{self.country}</div>
                    <div class="position">#{self.position}</div>
                </div>
                """