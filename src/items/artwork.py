from typing import Optional

WIDTH_INDEX = "{w}"
HEIGHT_INDEX = "{h}"

class ArtWork():
    def __init__(self,
                 artwork: dict) -> None:
        self.url = artwork["url"]
        self.max_width: int = artwork["width"]
        self.max_height: int = artwork["height"]

        self.bgColor = artwork["bgColor"]
        self.textColor1 = artwork["textColor1"]
        self.textColor2 = artwork["textColor2"]
        self.textColor3 = artwork["textColor3"]
        self.textColor4 = artwork["textColor4"]

    def get_sizes(self,
                  width: Optional[int] = None,
                  height: Optional[int] = None):
        """
        Return the sizes to use for the image to create.

        Parameters:
            - width: Width to use. If None, the max possible will be used
            - height: Height to use. If None, the max possible will be used
        """
        if width is None:
            width = self.max_width
        elif width > self.max_width:
            width = self.max_width

        if height is None:
            height = self.max_height
        elif height > self.max_height:
            height = self.max_height

        real_ratio = self.max_width / self.max_height
        new_width = int(height * real_ratio)
        if new_width < width:
            return new_width, height
        else:
            new_height = int(width / real_ratio)
            return new_height, width

    def get_image(self,
                  width: Optional[int] = None,
                  height: Optional[int] = None):
        """
        Returns the url of the image for the artwork

        Parameters:
            - width: Width to use. If None, the max possible will be used
            - height: Height to use. If None, the max possible will be used
        """
        width, height = self.get_sizes(width, height)

        image_url = self.url.replace(WIDTH_INDEX, str(width))
        image_url = image_url.replace(HEIGHT_INDEX, str(height))

        return image_url
