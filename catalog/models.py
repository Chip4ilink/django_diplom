# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

import uuid 

class Genre(models.Model):

    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):

        return self.name

class Language(models.Model):
    
    name = models.CharField(max_length=200,unique=True,help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):

        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):

        return self.name
    

class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


    def __str__(self):

        return self.title


    def get_absolute_url(self):

        return reverse('book-detail', args=[str(self.id)])
    


class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    def display_book(self):
        return self.book.title
    display_book.short_description = 'Book'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):

        return '%s (%s)' % (self.id,self.book.title)

class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):

        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):

        return '%s, %s' % (self.last_name, self.first_name)



class Division(models.Model):

    C_Name          = models.CharField('Наименование',max_length=100)
    D_Date_Begin    = models.DateField('Дата открытия',null=True, blank=True)
    D_Date_End      = models.DateField('Дата закрытия',null=True, blank=True)
    C_Notes         = models.TextField('Примечание', null=True) 

    def get_absolute_url(self):

        return reverse('division-detail', args=[str(self.id)])


    def __str__(self):

        return '%s' % (self.C_Name)

class DeviceType(models.Model):

    C_Name         = models.CharField('Наименование', max_length=200, help_text="Введите тип прибора")
    C_Manufacturer = models.CharField('Производитель', max_length=200, help_text="Введите производителя", null=True, blank=True)

    def __str__(self):

        return self.C_Name
    
class Device(models.Model):
    F_Division      = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Цех')
    F_Device_Types  = models.ForeignKey(DeviceType, on_delete=models.SET_NULL, null=True, verbose_name='Тип прибора')
    C_Serial_Number = models.CharField('Серийный номер', max_length=200)
    D_Replace_Date  = models.DateField('Дата снятия', null=True, blank=True)

    # LOAN_STATUS = (
    #     ('m', 'Maintenance'),
    #     ('o', 'On loan'),
    #     ('a', 'Available'),
    #     ('r', 'Reserved'),
    # )

    # status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    # def display_book(self):
    #     return self.book.title
    # display_book.short_description = 'Book'

    # @property
    # def is_overdue(self):
    #     if self.due_back and date.today() > self.due_back:
    #         return True
    #     return False

    class Meta:
        ordering = ["C_Serial_Number", "D_Replace_Date"]
        # permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):

        return '№%s (%s)' % (self.C_Serial_Number,self.F_Device_Types.C_Name)
    
class DeliveryMethod(models.Model):

    C_Name = models.CharField('Наименование', max_length=200, help_text="Введите источник показания")

    def __str__(self):

        return self.C_Name
    
class TariffZone(models.Model):
    
    C_Name = models.CharField('Наименование', max_length=200, help_text="Введите тарифную зону")

    def __str__(self):

        return self.C_Name
    
class MeterMeasure(models.Model):
    
    F_Devices       = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Прибор')
    F_Tariff_Zones  = models.ForeignKey(TariffZone, on_delete=models.CASCADE, verbose_name='Тарифная зона')
    N_Digits        = models.FloatField(verbose_name='Разрядность')
    # USer = models.ForeignKey(User, default=User.)

    def __str__(self):

        return self.C_Name
    
class MeterReading(models.Model):

    F_Division          = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Цех')
    F_Devices           = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Прибор')
    F_Tariff_Zones      = models.ForeignKey(TariffZone, on_delete=models.CASCADE, verbose_name='Тарифная зона')
    N_Value             = models.FloatField(verbose_name='Значение')
    D_Date              = models.DateField('Дата показания')
    F_Delivery_Methods  = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE, verbose_name='Источник показания')
    F_Creator           = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор записи')
    C_Notes             = models.CharField('Примечание', max_length=200, null=True, blank=True) 
    Img                 = models.ImageField(upload_to ='img/', null=True, blank=True, verbose_name='Фото')

    class Meta:
        ordering = ["F_Division", "D_Date"]

    def __str__(self):

        return '№%s (%s) - %s' % (self.F_Devices.C_Serial_Number,self.F_Devices.F_Device_Types.C_Name, self.D_Date)