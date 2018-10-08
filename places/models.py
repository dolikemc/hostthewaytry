import sys
from datetime import date
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse

from .image_filed_extend import ImageFieldExtend


class GeoName(models.Model):
    """ geonameid         : integer id of record in geonames database
        name              : name of geographical point (utf8) varchar(200)
        asciiname         : name of geographical point in plain ascii characters, varchar(200)
        alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience
                            attribute from alternatename table, varchar(10000)
        latitude          : latitude in decimal degrees (wgs84)
        longitude         : longitude in decimal degrees (wgs84)
        feature class     : see http://www.geonames.org/export/codes.html, char(1)
        feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
        country code      : ISO-3166 2-letter country code, 2 characters
        cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
        admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for
                            display names of this code; varchar(20)
        admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt;
                            varchar(80)
        admin3 code       : code for third level administrative division, varchar(20)
        admin4 code       : code for fourth level administrative division, varchar(20)
        population        : bigint (8 byte int)
        elevation         : in meters, integer
        dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''
                            x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
        timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
        modification date : date of last modification in yyyy-MM-dd format"""

    geo_name_id = models.PositiveIntegerField(primary_key=True, help_text='integer id of record in geonames database')
    name = models.CharField(max_length=200, help_text='name of geographical point (utf8)')
    ascii_name = models.CharField(max_length=200, help_text='name of geographical point in plain ascii characters')
    alternate_names = models.CharField(max_length=1000,
                                       help_text='comma separated, ascii names automatically transliterated, '
                                                 'convenience attribute from alternatename table')
    latitude = models.DecimalField(max_digits=13, decimal_places=10, help_text='latitude in decimal degrees')
    longitude = models.DecimalField(max_digits=13, decimal_places=10, help_text='longitude in decimal degrees')
    feature_class = models.CharField(max_length=1, help_text='see http://www.geonames.org/export/codes.html')
    feature_code = models.CharField(max_length=10, help_text='see http://www.geonames.org/export/codes.html')
    country_code = models.CharField(max_length=2, help_text='ISO-3166 2-letter country code')
    alternate_country_codes = models.CharField(max_length=200,
                                               help_text='alternate country codes, comma separated, ISO-3166 2-letter '
                                                         'country code')
    admin_1_code = models.CharField(max_length=20,
                                    help_text='fipscode (subject to change to iso code), see exceptions below, '
                                              'see file admin1Codes.txt for display names of this code')
    admin_2_code = models.CharField(max_length=80,
                                    help_text='code for the second administrative division, a county in the US, '
                                              'see file admin2Codes.txt')
    admin_3_code = models.CharField(max_length=20, help_text='code for third level administrative division')
    admin_4_code = models.CharField(max_length=20, help_text='code for fourth level administrative division')
    population = models.PositiveIntegerField(null=True, blank=True)
    elevation = models.PositiveIntegerField(null=True, blank=True)
    dem = models.PositiveIntegerField(null=True, blank=True, help_text='digital elevation model, srtm3 or gtopo30, '
                                                                       'average elevation of 3''x3'' (ca 90mx90m) or '
                                                                       '30''x30'' (ca 900mx900m) area in meters, '
                                                                       'integer. srtm processed by cgiar/ciat')
    timezone = models.CharField(max_length=40, help_text='the iana timezone id (see file timeZone.txt)')
    modification_date = models.CharField(max_length=10, help_text='date of last modification in yyyy-MM-dd format')

    def __str__(self):
        return f"{self.ascii_name} ({self.country_code}):{self.geo_name_id}"


class Place(models.Model):
    NO_MEAL = 'NO'
    ONLY_BREAKFAST = 'BR'
    BREAKFAST_LUNCH = 'BL'
    BREAKFAST_DINNER = 'BD'
    ALL_MEALS = 'AL'
    MEALS = ((NO_MEAL, 'no meal at all'), (ONLY_BREAKFAST, 'only breakfast'), (BREAKFAST_LUNCH, 'breakfast and lunch'),
             (BREAKFAST_DINNER, 'breakfast and dinner'), (ALL_MEALS, 'breakfast, lunch and dinner'))

    NO_CONTACT = 'NO'
    WITH_CONTACT = 'CO'
    SPENT_TIME = 'TI'
    PERSONAL_OFFER = 'PO'
    NO_ANSWER = 'NA'
    CONTACT_TYPES = (
        (NO_CONTACT, "Unfortunately I'm personally not available"), (WITH_CONTACT, "I'll be in contact with my guests"),
        (SPENT_TIME, "I'll spend time with my guests?"), (PERSONAL_OFFER, "I can personally offer my guests"),
        (NO_ANSWER, "I could not answer this question"))

    name = models.CharField(max_length=200, help_text='Name of your place')
    # if blank we try to use email data
    contact_first_name = models.CharField(max_length=100, help_text='Your first name', blank=True)
    contact_last_name = models.CharField(max_length=100, help_text='Your last name', default='owner')
    contact_type = models.CharField(max_length=2, help_text='What kind of contact you can offer your guest?',
                                    choices=CONTACT_TYPES, default=NO_ANSWER)
    # address could be filled with geo location data
    street = models.CharField(max_length=100, help_text='Street', blank=True)
    city = models.CharField(max_length=100, help_text='City', blank=True)

    country = models.CharField(max_length=2, help_text='Country Code', blank=True)
    address_add = models.CharField(max_length=200, help_text='Additional address information', blank=True)
    # contact data
    phone = models.CharField(max_length=30, help_text='Phone number', blank=True)
    mobile = models.CharField(max_length=20, help_text='Mobile number', blank=True)
    email = models.EmailField(help_text='Your contact email address', default='hosttheway@gmail.com')
    email_alt = models.EmailField(help_text='Alternative email address', blank=True)
    # information about you
    languages = models.CharField(max_length=100, help_text='Which languages do you speak?', default='EN')
    who_lives_here = models.CharField(max_length=200, help_text='Who lives in your house?', blank=True)
    # information about rooms
    rooms = models.PositiveSmallIntegerField(help_text='How many rooms do you rent?', default=1)
    beds = models.PositiveSmallIntegerField(help_text='How many beds do you have?', default=2)
    maximum_of_guests = models.PositiveSmallIntegerField(help_text='How many guests can stay in yourt house?',
                                                         default=1)
    """price_per_person = models.DecimalField(help_text='Price for the current category', decimal_places=2, default=10.00,
                                           max_digits=9)
    price_per_room = models.DecimalField(help_text='Price for the current category', decimal_places=2, default=0.00,
                                         max_digits=9)
    season_price_per_person = models.DecimalField(help_text='Price for the current category', decimal_places=2,
                                                  default=0.00, max_digits=9)
    season_price_per_room = models.DecimalField(help_text='Price for the current category', decimal_places=2,
                                                default=0.00, max_digits=9)"""

    bathrooms = models.PositiveSmallIntegerField(help_text='How many bathrooms do you have?', default=1)
    private_bathroom = models.BooleanField(help_text='Do guests have a private bathroom?', default=False)
    common_kitchen = models.BooleanField(
        help_text='Do guests have access to your kitchen and can use it for preparing food?', default=False)
    private_kitchen = models.BooleanField(help_text='Do guests have a private kitchen?', default=False)
    outdoor_place = models.BooleanField(help_text='Do you have a garden, aterrace or a balcony?', default=False)
    room_add = models.CharField(max_length=200, help_text='What other rooms can your guests use?', blank=True)
    smoking = models.BooleanField(help_text='Is smoking allowed in the house?', default=False)
    pets = models.BooleanField(help_text='Are peds wellcome?', default=True)
    family = models.BooleanField(help_text='Is your house suitable families/kids?', default=True)
    # about meal
    meals = models.CharField(max_length=2, help_text='How many meals per day your serve?', choices=MEALS,
                             default=NO_MEAL)
    vegetarian = models.BooleanField(help_text='Do you serve vegetarian meal option?', default=False)
    vegan = models.BooleanField(help_text='Do you serve vegan meal option?', default=False)
    meal_example = models.CharField(max_length=400, help_text='Please describe a typical meal in your home', blank=True)
    # other flags
    handicapped_enabled = models.BooleanField(help_text='Is your house suitable for handicapped guests?', default=False)
    laundry = models.BooleanField(
        help_text='Do you have laundry facilities at your house guests can use (washer/dryer)?', default=False)
    parking = models.BooleanField(help_text='Do you have parking at your house?', default=False)
    wifi = models.BooleanField(help_text='Do you have (free) WiFi at your house?', default=True)
    own_key = models.BooleanField(help_text='Do guests have their own key to the house?', default=False)
    separate_entrance = models.BooleanField(help_text='Is there a separate entrance to the house for guests?',
                                            default=False)
    description = models.CharField(max_length=500, default='', blank=True,
                                   help_text='What else would you like to tell your gusets?')
    # location data
    # todo: define a proper sub clss of models.ImageFiled with a resizing pres_save method
    picture = models.ImageField(help_text='Picture of your place',
                                upload_to='',
                                blank=True)
    longitude = models.FloatField(
        help_text='Where is your place (longitude)? Could be taken from the picture meta data', null=True, blank=True)
    latitude = models.FloatField(help_text='Where is your place (latitude)? Could be taken from the picture meta data',
                                 null=True, blank=True)
    max_stay = models.PositiveIntegerField(default=365, help_text='What is the maximum stay?')
    min_stay = models.PositiveIntegerField(default=1, help_text='What is the mimum stay?')
    currencies = models.CharField(max_length=50, default='€', help_text='What currencies do you accept?')
    check_out_time = models.PositiveIntegerField(default=12, help_text='Check out time')
    check_in_time = models.PositiveIntegerField(default=14, help_text='Check in time')
    pick_up_service = models.BooleanField(default=False,
                                          help_text='Can you pick up your guests from the airport, train station or '
                                                    'bus stop')

    # technical data
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(editable=False, default=False)
    deleted = models.BooleanField(editable=False, default=False)

    def __str__(self):
        return f"{self.name} ({self.country})"

    def save(self, **kwargs):
        # copied from https://djangosnippets.org/snippets/10597/

        # Opening the uploaded image
        try:
            im = Image.open(self.picture)

            # read lat and long
            img_ext = ImageFieldExtend(self.picture)
            if self.longitude is None or self.longitude == 0 or \
                    self.latitude is None or self.latitude == 0:
                (self.longitude, self.latitude) = img_ext.get_lat_lon(im)

            output = BytesIO()

            # todo: keep orientation
            im = im.resize((200, 200))
            # print(im.info)

            # after modifications, save it to the output
            im.save(output, format='JPEG', quality=100)
            output.seek(0)

            # change the image field value to be the newley modifed image value
            self.picture = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.picture.name.split('.')[0],
                                                'image/jpeg',
                                                sys.getsizeof(output), None)
        except FileNotFoundError:
            pass
        except ValueError:
            pass
        super(Place, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('places:detail', kwargs={'pk': self.pk})


class Price(models.Model):
    CATEGORY_C_PER_NIGHT = 'CN'
    CATEGORY_C_PER_ROOM = 'CR'
    CATEGORY_B_PER_NIGHT = 'BN'
    CATEGORY_B_PER_ROOM = 'BR'
    CATEGORY_A_PER_NIGHT = 'AN'
    CATEGORY_A_PER_ROOM = 'AR'
    CLEANING_FEE = 'CL'
    BREAKFAST = 'BR'
    BREAKFAST_LUNCH = 'BL'
    BREAKFAST_DINNER = 'BD'
    ALL_MEALS = 'AM'

    PRICE_CATEGORIES = (
        (CATEGORY_C_PER_NIGHT, 'Regular price per night'),
        (CATEGORY_C_PER_ROOM, 'Regular price per room'),
        (CATEGORY_B_PER_NIGHT, 'Special price per night'),
        (CATEGORY_B_PER_ROOM, 'Special price per room'),
        (CATEGORY_A_PER_NIGHT, 'Top price per night'),
        (CATEGORY_A_PER_ROOM, 'Top price per room'),
        (CLEANING_FEE, 'Cleaning fee'),
        (BREAKFAST, 'Price for breakfast'),
        (BREAKFAST_LUNCH, 'Price for breakfast and lunch'),
        (BREAKFAST_DINNER, 'Price for breakfast and dinner'),
        (ALL_MEALS, 'Price for three meals'))
    place_id = models.ForeignKey(to=Place, on_delete=models.DO_NOTHING)
    value = models.DecimalField(help_text='Price for the current category', decimal_places=2, default=0.00,
                                max_digits=9)
    currency = models.CharField(help_text='Currency ISO 3 Code', default='EUR', max_length=3)
    category = models.CharField(max_length=2, help_text='Waht kind of contact you can offer your guest?',
                                choices=PRICE_CATEGORIES, default=CATEGORY_C_PER_NIGHT)
    valid_from = models.DateField(help_text='Price is valid from this date', default=date(2018, 1, 1))
    valid_to = models.DateField(help_text='Price is valid to this date', default=date(2018, 12, 31))
    # technical data
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(editable=False, default=False)
    deleted = models.BooleanField(editable=False, default=False)
