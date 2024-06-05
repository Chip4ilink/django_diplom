# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Author, Genre, Book, BookInstance, Language, Division, Device, DeviceType, DeliveryMethod, TariffZone, MeterMeasure, MeterReading

# admin.site.register(Book)
admin.site.register(Language)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
class BooksInline(admin.TabularInline):
    model = Book
    extra = 0
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)




class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
# Register the Admin classes for Book using the decorator

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

#########################################################

admin.site.register(Division)
admin.site.register(Device)
admin.site.register(DeviceType)
admin.site.register(DeliveryMethod)
admin.site.register(TariffZone)
admin.site.register(MeterMeasure)

@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_filter = ('F_Division', 'D_Date', 'F_Devices')

    # @admin.display(description="Изображение")
    # def post_img(self, MeterReading: MeterReading):
    #     return mark_safe(f"<img src='{MeterReading.Img.url}' width=50>")

# admin.site.register(MeterReading)