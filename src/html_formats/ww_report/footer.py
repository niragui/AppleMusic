import datetime


APPLE_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"


class WWReportFooter():
    def __init__(self,
                 genre: str) -> None:
        self.genre = genre

    def get_html(self):
        now = datetime.datetime.now()

        now_str = now.strftime("%B %d %H:%M")

        return f"""
            <div class="card-footer">
            <div class="bookmark">
                <img src="{APPLE_LOGO_URL}" alt="">
                <span>Apple Music {self.genre}</span>
            </div>
            <div class="date">{now_str}</div>
            </div>
        """