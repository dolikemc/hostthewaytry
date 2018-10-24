import logging
import sys
from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO
from typing import List

from PIL import Image
from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models import Avg, Sum, Min, Max
from django.urls import reverse

from .image_filed_extend import ImageFieldExtend

# Get an instance of a logger
logger = logging.getLogger(__name__)

# date depended constant used for defaults
current_year = date.today().year


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
    alternate_names = models.CharField(
        max_length=1000, help_text='comma separated, ascii names automatically transliterated, '
                                   'convenience attribute from alternate name table')
    latitude = models.DecimalField(max_digits=13, decimal_places=10, help_text='latitude in decimal degrees')
    longitude = models.DecimalField(max_digits=13, decimal_places=10, help_text='longitude in decimal degrees')
    feature_class = models.CharField(max_length=1, help_text='see http://www.geonames.org/export/codes.html')
    feature_code = models.CharField(max_length=10, help_text='see http://www.geonames.org/export/codes.html')
    country_code = models.CharField(max_length=2, help_text='ISO-3166 2-letter country code')
    alternate_country_codes = models.CharField(
        max_length=200, help_text='alternate country codes, comma separated, ISO-3166 2-letter country code')
    admin_1_code = models.CharField(
        max_length=20, help_text='fipscode (subject to change to iso code), see exceptions below, '
                                 'see file admin1Codes.txt for display names of this code')
    admin_2_code = models.CharField(max_length=80,
                                    help_text='code for the second administrative division, a county in the US, '
                                              'see file admin2Codes.txt')
    admin_3_code = models.CharField(max_length=20, help_text='code for third level administrative division')
    admin_4_code = models.CharField(max_length=20, help_text='code for fourth level administrative division')
    population = models.PositiveIntegerField(null=True, blank=True)
    elevation = models.PositiveIntegerField(null=True, blank=True)
    dem = models.PositiveIntegerField(null=True, blank=True,
                                      help_text='digital elevation model, srtm3 or gtopo30, '
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

    NO_ANSWER = 'NA'
    ALWAYS_ON_TOP = 'AW'
    PRIORITY_TYPES = ((NO_ANSWER, "No special category"), (ALWAYS_ON_TOP, "Always on top"))

    TINY = "TI"
    SMALL = "SM"
    MEDIUM = "ME"
    LARGE = "LA"
    HOTEL = "HO"
    NOT_AVAILABLE = "NA"
    HOST_CATEGORY = ((TINY, "One room to rent with 2 beds"), (SMALL, "Two rooms with 2-3 beds"),
                     (MEDIUM, "Three rooms with 2-6 beds"), (LARGE, "Four rooms with 2-6 beds"),
                     (HOTEL, "More than four rooms to rent "), (NOT_AVAILABLE, "n/a"))

    name = models.CharField(max_length=200, help_text='Name of your place', null=False)
    description = models.CharField(max_length=500, default='', blank=True,
                                   help_text='What else would you like to tell your guests?')

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
    website = models.URLField(help_text='Website of the place', blank=True)

    # information about you
    languages = models.CharField(max_length=100, help_text='Which languages do you speak?', default='EN')
    who_lives_here = models.CharField(max_length=200, help_text='Who lives in your house?', blank=True)

    # information about the place
    common_kitchen = models.BooleanField(
        help_text='Do guests have access to your kitchen and can use it for preparing food?', default=False)
    outdoor_place = models.BooleanField(help_text='Do you have a garden, aterrace or a balcony?', default=False)
    parking = models.BooleanField(help_text='Do you have parking at your house?', default=False)
    wifi = models.BooleanField(help_text='Do you have (free) WiFi at your house?', default=True)
    own_key = models.BooleanField(help_text='Do guests have their own key to the house?', default=False)
    separate_entrance = models.BooleanField(help_text='Is there a separate entrance to the house for guests?',
                                            default=False)
    max_stay = models.PositiveIntegerField(default=365, help_text='What is the maximum stay?')
    min_stay = models.PositiveIntegerField(default=1, help_text='What is the minimum stay?')
    category = models.CharField(max_length=2, help_text='Category of your place', choices=HOST_CATEGORY,
                                default=NOT_AVAILABLE)

    # about meal
    meals = models.CharField(max_length=2, help_text='How many meals per day your serve?', choices=MEALS,
                             default=NO_MEAL)
    vegetarian = models.BooleanField(help_text='Do you serve vegetarian meal option?', default=False)
    vegan = models.BooleanField(help_text='Do you serve vegan meal option?', default=False)
    meal_example = models.CharField(max_length=400, help_text='Please describe a typical meal in your home', blank=True)
    # other flags
    laundry = models.BooleanField(
        help_text='Do you have laundry facilities at your house guests can use (washer/dryer)?', default=False)

    # location data
    # todo: define a proper sub class of models.ImageFiled with a resizing pres_save method
    picture = models.ImageField(help_text='Picture of your place', upload_to='', blank=True)
    longitude = models.FloatField(help_text='Where is your place (longitude)?', null=True, blank=True)
    latitude = models.FloatField(help_text='Where is your place (latitude)?', null=True, blank=True)

    # services
    currency = models.CharField(help_text='Currency ISO 3 Code', default='EUR', max_length=3)
    currencies = models.CharField(max_length=50, default='€', help_text='What currencies do you accept?')
    check_out_time = models.PositiveIntegerField(default=12, help_text='Check out time')
    check_in_time = models.PositiveIntegerField(default=14, help_text='Check in time')
    pick_up_service = models.BooleanField(
        default=False, help_text='Can you pick up your guests from the airport, train station or bus stop')

    # payed priority
    priority_value = models.PositiveSmallIntegerField(default=0, blank=True, null=True, editable=False)
    priority_valid_until = models.DateTimeField(blank=True, null=True)
    priority_category = models.CharField(max_length=2, choices=PRIORITY_TYPES, default=NO_ANSWER, blank=True, null=True)

    # technical data
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(editable=False, default=False)
    deleted = models.BooleanField(editable=False, default=False)

    @property
    def average_price(self) -> Decimal:
        return self.room_set.aggregate(Avg('price_per_person'))['price_per_person__avg']

    @property
    def beds(self) -> int:
        return self.room_set.aggregate(Sum('beds'))['beds__sum']

    @property
    def pets(self) -> bool:
        return self.room_set.filter(pets=True).count() > 0

    @property
    def smoking(self) -> bool:
        return self.room_set.filter(smoking=True).count() > 0

    @property
    def private_bathroom(self) -> bool:
        return self.bathrooms > 0

    @property
    def price_low(self) -> Decimal:
        return self.valid_rooms().aggregate(Min('price_per_person'))['price_per_person__min']

    @property
    def price_high(self) -> Decimal:
        return self.valid_rooms().aggregate(Max('price_per_person'))['price_per_person__max']

    def valid_rooms(self) -> List:
        return self.room_set.filter(valid_from__lte=date.today() + timedelta(days=7)).filter(price_per_person__gt=0.0)

    @property
    def bathrooms(self) -> int:
        return self.room_set.filter(bathroom=True).count()

    def add_std_rooms_and_prices(self, std_price: Decimal) -> bool:
        if self.category == self.TINY:
            Room.objects.create(place_id=self.id, room_number='your room', beds=2,
                                price_per_person=std_price)
            return True
        if self.category == self.SMALL:
            Room.objects.create(place_id=self.id, room_number='01', beds=2,
                                price_per_person=std_price)
            Room.objects.create(place_id=self.id, room_number='02', beds=3,
                                price_per_person=std_price)
            return True
        if self.category == self.MEDIUM:
            Room.objects.create(place_id=self.id, room_number='01', beds=2,
                                price_per_person=std_price)
            Room.objects.create(place_id=self.id, room_number='02', beds=3,
                                price_per_person=std_price)
            Room.objects.create(place_id=self.id, room_number='03', beds=6,
                                price_per_person=std_price)
            return True
        if self.category == self.LARGE:
            Room.objects.create(place_id=self.id, room_number='01', beds=2,
                                price_per_person=std_price)
            Room.objects.create(place_id=self.id, room_number='02', beds=3,
                                price_per_person=std_price)
            Room.objects.create(place_id=self.id, room_number='03', beds=3,
                                price_per_person=std_price)
            Room.objects.create(place_id=self.id, room_number='04', beds=6,
                                price_per_person=std_price)
            return True

        return False

    def create_user_group(self, user: User) -> Group:
        index, group_name = 0, self.name
        while Group.objects.filter(name=group_name).count() > 0:
            group_name = self.name + str(index)
            index += 1
        group = Group.objects.create(name=group_name)
        self.group = group
        user.groups.add(group)
        return group

    def __str__(self) -> str:
        return f"{self.name} ({self.country})"

    def save(self, **kwargs):
        self.country = str.upper(self.country)
        self.currency = str.upper(self.currency)
        self.currencies = str.upper(self.currencies)

        # Opening the uploaded image
        try:
            # copied from https://djangosnippets.org/snippets/10597/
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
        return super(Place, self).save(**kwargs)

    def get_absolute_url(self) -> str:
        return reverse('places:detail', kwargs={'pk': self.pk})


class Price(models.Model):
    CLEANING_FEE = 'CL'
    BREAKFAST = 'BR'
    BREAKFAST_LUNCH = 'BL'
    BREAKFAST_DINNER = 'BD'
    ALL_MEALS = 'AM'

    PRICE_CATEGORIES = (
        (CLEANING_FEE, 'Cleaning fee'),
        (BREAKFAST, 'Price for breakfast'),
        (BREAKFAST_LUNCH, 'Price for breakfast and lunch'),
        (BREAKFAST_DINNER, 'Price for breakfast and dinner'),
        (ALL_MEALS, 'Price for three meals'))

    place = models.ForeignKey(to=Place, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, blank=True,
                                   help_text='Description of this price')
    value = models.DecimalField(help_text='Price for the current category', decimal_places=2, default=0.00,
                                max_digits=9)
    category = models.CharField(max_length=2, help_text='For what is the price for?',
                                choices=PRICE_CATEGORIES, default=CLEANING_FEE)

    # technical data
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(editable=False, default=False)
    deleted = models.BooleanField(editable=False, default=False)

    def __str__(self) -> str:
        return f"{self.place} - {self.category} - {self.value}{self.place.currency}"


class Room(models.Model):
    place = models.ForeignKey(to=Place, on_delete=models.CASCADE)

    # room equipment
    room_number = models.CharField(help_text='Room number/identifier', default='01', max_length=50)
    beds = models.PositiveIntegerField(help_text='Number of beds in this room', default=2)
    bathroom = models.BooleanField(help_text='Do this room have a private bathroom?', default=True)
    kitchen = models.BooleanField(help_text='Do this room  have a private kitchen?', default=False)
    outdoor_place = models.BooleanField(help_text='Do this room have a garden, a terrace or a balcony?', default=False)
    room_add = models.CharField(max_length=200, help_text='Additional information about this room', blank=True)
    smoking = models.BooleanField(help_text='Smoking allowed in the room?', default=False)
    pets = models.BooleanField(help_text='Are peds wellcome?', default=True)
    family = models.BooleanField(help_text='Is this room suitable families/kids?', default=True)
    handicapped_enabled = models.BooleanField(help_text='Is this room suitable for handicapped guests?', default=False)

    # prices and validity
    price_per_person = models.DecimalField(help_text='Price for the current category', decimal_places=2, default=0.00,
                                           max_digits=9, max_length=12)
    price_per_room = models.DecimalField(help_text='Price for the current category', decimal_places=2, default=0.00,
                                         max_digits=9, max_length=12)
    valid_from = models.DateField(help_text='Price is valid from this date', default=date(current_year, 1, 1))
    valid_to = models.DateField(help_text='Price is valid to this date', default=date(current_year, 12, 31))

    # technical data
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(editable=False, default=False)
    deleted = models.BooleanField(editable=False, default=False)

    def __str__(self) -> str:
        return f"{self.place} - {self.room_number} - ({self.beds})"
