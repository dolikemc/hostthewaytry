import piexif
from PIL import Image
from django.db import models


# Create your models here.

class ImageFieldExtend(models.ImageField):

    # Copied from https://gist.github.com/erans/983821/cce3712b82b3de71c73fbce9640e25adef2b0392

    def get_exif_data(self, im: Image = None):
        """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
        # Opening the uploaded image
        if im is None:
            im = Image.open(self.name)
        if 'exif' not in im.info:
            return {}

        exif_data = piexif.load(im.info["exif"])

        return exif_data

    @staticmethod
    def _convert_to_degress(value):
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

    def get_lat_lon(self, im: Image = None):
        """Returns the latitude and longitude, if available, from the provided exif_data
        (obtained through get_exif_data above)"""
        lat = None
        lon = None
        exif_data = self.get_exif_data(im)
        if "GPS" in exif_data:
            if piexif.GPSIFD.GPSLatitude in exif_data["GPS"]:
                lat = self._convert_to_degress(exif_data["GPS"][piexif.GPSIFD.GPSLatitude])

            if piexif.GPSIFD.GPSLongitude in exif_data["GPS"]:
                lon = self._convert_to_degress(exif_data["GPS"][piexif.GPSIFD.GPSLongitude])
        return lat, lon
