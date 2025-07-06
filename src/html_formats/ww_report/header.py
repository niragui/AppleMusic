from ...items.apple_item import AppleItem


class WWReportHeader():
    def __init__(self,
                 apple_item: AppleItem) -> None:
        self.name = apple_item.name

        self.credits = ""
        if hasattr(apple_item, "credits"):
            self.credits = apple_item.credits

        self.image = apple_item.image

    def get_html(self):
        return f"""
            <div class="card-header">
            <img src="{self.image}" alt="Trophy Icon">
            <div class="header-text">
                <h2>{self.name}</h2>
                <div class="subtitle">{self.credits}</div>
            </div>
            </div>
        """