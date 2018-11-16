import logging
from typing import Dict

import piexif
from PIL import Image

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ImageX:
    """ Supports only JPEG form see https://pillow.readthedocs.io

    """

    def __init__(self, name: str):
        self.name: str = name
        self.image: Image = None
        self.is_open: bool = False
        self.exif_data: Dict = {}

    def open(self, image: Image = None) -> bool:
        """opens the file and load the dictionary from the exif data of an PIL Image item.
        Also converts the GPS Tags"""
        # Copied from https://gist.github.com/erans/983821/cce3712b82b3de71c73fbce9640e25adef2b0392
        try:
            if image is None:
                self.image = Image.open(self.name)
            else:
                self.image = Image.open(image)
        except FileNotFoundError as exc:
            logger.warning(exc)
            return False
        logger.debug(f'{self.name} is open')
        self.is_open = True

        if 'exif' not in self.image.info:
            logger.warning(f"No exif data in image file {self.name}")
            return True

        self.exif_data = piexif.load(self.image.info["exif"])
        logger.debug(self.exif_data)
        return True

    @staticmethod
    def _convert_to_degress(value) -> float:
        """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    @property
    def latitude(self) -> float:
        if "GPS" in self.exif_data and len(self.exif_data["GPS"]) >= piexif.GPSIFD.GPSLatitude:
            return self._convert_to_degress(self.exif_data["GPS"][piexif.GPSIFD.GPSLatitude])
        return 0.0

    @property
    def longitude(self) -> float:
        if "GPS" in self.exif_data and len(self.exif_data["GPS"]) >= piexif.GPSIFD.GPSLongitude:
            return self._convert_to_degress(self.exif_data["GPS"][piexif.GPSIFD.GPSLongitude])
        return 0.0

    @property
    def orientation(self) -> int:
        if "0th" in self.exif_data:
            if piexif.ImageIFD.Orientation in self.exif_data["0th"]:
                return self.exif_data["0th"][piexif.ImageIFD.Orientation]
        return 0

    def save(self, fp=None, **kwargs) -> bool:
        exif_bytes = piexif.dump(self.exif_data)
        if fp is None:
            fp = self.name
        try:
            self.image.save(fp, format='JPEG', quality=100, exif=exif_bytes, **kwargs)
            return True
        except FileNotFoundError as exc:
            logger.warning(exc)
            return False

    def correct_orientation(self) -> Image:
        if self.orientation <= 1:
            return self.image
        if self.orientation == 2:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        elif self.orientation == 3:
            self.image = self.image.rotate(180)
        elif self.orientation == 4:
            self.image = self.image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        elif self.orientation == 5:
            self.image = self.image.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
        elif self.orientation == 6:
            self.image = self.image.rotate(-90, expand=True)
        elif self.orientation == 7:
            self.image = self.image.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
        elif self.orientation == 8:
            self.image = self.image.rotate(90, expand=True)
        self.exif_data["0th"][piexif.ImageIFD.Orientation] = 1
        return self.image

    def resize(self, width: int = 200, length: int = 200) -> Image:
        self.image = self.image.resize((width, length))
        return self.image

    def close(self):
        if self.is_open:
            self.image.close()
            self.is_open = False
