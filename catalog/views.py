from decimal import Decimal
import json
from django.views import generic
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Division, Device, MeterReading, TariffZone, DeliveryMethod
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

import datetime

from .forms import RenewBookForm, MeterReadingCreateForm, DeviceCreateForm, DivisionCreateForm, DeviceUpdateForm, MeterReadingUpdateForm, DivisionUpdateForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from .forms import CSVImportForm
from .models import Book
import csv

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_devices=Device.objects.count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    num_books_name_contains_dochka = len(Book.objects.filter(title__contains='dochka'))
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    # num_divisions=len(Division.objects.raw("SELECT * FROM catalog_Division where D_Date_End IS NOT NULL"))
    num_divisions = Division.objects.count()
    # print(Division.objects.raw("SELECT * FROM catalog_Division where D_Date_End IS NOT NULL").columns)
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # print('asd\ndgd\ndgd\ndgd')
    # print('''asdas %Y asd''')
    all_quantity_by_dates = Division.objects.raw(
                                                '''
        
        SELECT d.id, d.C_Name, device_sums_last.Month, sum_last - IFNULL(sum_prev,0) as N_Cons 
        FROM catalog_Division d
        
        INNER JOIN (
                        SELECT ed.id, ed.F_Division_id, CAST(substr(month.Date, 6, 2) AS INT) AS Month, SUM(m.N_Value) AS sum_last
                        FROM catalog_Device ed
                        INNER JOIN catalog_MeterReading m
                            ON m.F_Devices_id = ed.id
                        INNER JOIN catalog_Division d1
                            ON d1.id = m.F_Division_id
                        INNER JOIN 
                        (
                            SELECT '2024-01-01' as Date
                            UNION
                            SELECT '2024-02-01' as Date
                            UNION
                            SELECT '2024-03-01' as Date
                            UNION
                            SELECT '2024-04-01' as Date
                            UNION
                            SELECT '2024-05-01' as Date
                            UNION
                            SELECT '2024-06-01' as Date
                            UNION
                            SELECT '2024-07-01' as Date
                            UNION
                            SELECT '2024-08-01' as Date
                            UNION
                            SELECT '2024-09-01' as Date
                            UNION
                            SELECT '2024-10-01' as Date
                            UNION
                            SELECT '2024-11-01' as Date
                            UNION
                            SELECT '2024-12-01' as Date
                        ) month
                            ON CAST(substr(month.Date, 6, 2) AS INT) = CAST(substr(m.D_Date, 6, 2) AS INT)
                        
                        WHERE m.id = (
                                        SELECT id 
                                        FROM catalog_MeterReading m1 
                                        WHERE m1.F_Devices_id = m.F_Devices_id 
                                        AND CAST(substr(m1.D_Date, 6, 2) AS INT) = CAST(substr(month.Date, 6, 2) AS INT)
                                        ORDER BY D_Date DESC
                                        LIMIT 1
                                        )
                        GROUP BY ed.id, ed.F_Division_id, CAST(substr(month.Date, 6, 2) AS INT)
                    ) device_sums_last
            ON device_sums_last.F_Division_id = d.id
        LEFT JOIN (
                        SELECT ed.id, ed.F_Division_id, CAST(substr(month.Date, 6, 2) AS INT) AS Month, SUM(m.N_Value) AS sum_prev
                        FROM catalog_Device ed
                        INNER JOIN catalog_MeterReading m
                            ON m.F_Devices_id = ed.id
                        INNER JOIN catalog_Division d1
                            ON d1.id = m.F_Division_id
                        INNER JOIN 
                        (
                            SELECT '2024-01-01' as Date
                            UNION
                            SELECT '2024-02-01' as Date
                            UNION
                            SELECT '2024-03-01' as Date
                            UNION
                            SELECT '2024-04-01' as Date
                            UNION
                            SELECT '2024-05-01' as Date
                            UNION
                            SELECT '2024-06-01' as Date
                            UNION
                            SELECT '2024-07-01' as Date
                            UNION
                            SELECT '2024-08-01' as Date
                            UNION
                            SELECT '2024-09-01' as Date
                            UNION
                            SELECT '2024-10-01' as Date
                            UNION
                            SELECT '2024-11-01' as Date
                            UNION
                            SELECT '2024-12-01' as Date
                        ) month
                            ON CAST(substr(month.Date, 6, 2) AS INT) = CAST(substr(m.D_Date, 6, 2) AS INT)
                        
                        WHERE m.id = (
                                        SELECT id 
                                        FROM catalog_MeterReading m1 
                                        WHERE m1.F_Devices_id = m.F_Devices_id 
                                        AND CAST(substr(m1.D_Date, 6, 2) AS INT) < CAST(substr(month.Date, 6, 2) AS INT)
                                        ORDER BY D_Date DESC
                                        LIMIT 1
                                        )
                        GROUP BY ed.id, ed.F_Division_id, CAST(substr(month.Date, 6, 2) AS INT)
                    ) device_sums_prev
            ON device_sums_prev.F_Division_id = d.id
            ORDER BY device_sums_last.Month
                                                 ''')
    
    pre_charts_data = dict()
    pre_charts_data["month_list"] = []
    pre_charts_data["series"] = {}
    some_dict = dict()
    cons_by_date = dict()
    # print(all_quantity_by_dates)
    for p in all_quantity_by_dates:
        if(p.Month not in pre_charts_data["month_list"]):
            pre_charts_data["month_list"].append(p.Month)
        pre_charts_data["series"][p.C_Name] = []#pre_charts_data[p.C_Name].get()
        if p.C_Name not in cons_by_date.keys():
            cons_by_date[p.C_Name] = {}
        cons_by_date[p.C_Name][p.Month] = p.N_Cons
        if p.C_Name not in some_dict.keys():
            some_dict[p.C_Name] = []
        some_dict[p.C_Name].append(p.Month)
        # print(p.C_Name, p.Month, p.N_Cons)
    for p in pre_charts_data["series"]:
        for month in pre_charts_data["month_list"]:
            if(month in some_dict[p]):
                pre_charts_data["series"][p].append(cons_by_date[p][month])
            else:
                pre_charts_data["series"][p].append(0)

    # print(some_dict)
    # print(cons_by_date)
    # print(pre_charts_data["month_list"])
    # print(pre_charts_data["series"])

    charts_data = dict()
    charts_data["month_list"] = pre_charts_data["month_list"]
    charts_data["series"] = []
    for name, data in pre_charts_data["series"].items():
        charts_data["series"].append({"name": name, "data":data})

    # print(charts_data)

    def custom_serializer(obj):
        if isinstance(obj, (datetime, datetime.date)):
            serial = obj.isoformat()
            return serial
        if isinstance(obj, Decimal):
            return float(obj)
        
    charts_data = json.dumps(charts_data, default=custom_serializer)
    # print(charts_data)

    return render(
        request,
        'index.html',
        context={'charts_data':charts_data, 'num_devices':num_devices,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_divisions':num_divisions,'num_books_name_contains_dochka':num_books_name_contains_dochka, 'num_visits':num_visits},
        
    )



class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
class LoanedBooksForLibrarianListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'20/05/2024',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

#########################################################

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    # initial={'date_of_death':'20/05/2024',}

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

#########################################################

class DivisionListView(generic.ListView):
    model = Division
    paginate_by = 10

class DivisionDetailView(generic.DetailView):
    model = Division

class DeviceListView(generic.ListView):
    model = Device
    paginate_by = 10

class DeviceDetailView(generic.DetailView):
    model = Device

class MeterReadingListView(generic.ListView):
    model = MeterReading
    paginate_by = 10


def division_readings(request, pk):
    """
    Функция отображения показаний по цеху.
    """
    # # Генерация "количеств" некоторых главных объектов
    # num_books=Book.objects.all().count()
    # num_instances=BookInstance.objects.all().count()
    # # Доступные книги (статус = 'a')
    # num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    # num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # num_books_name_contains_dochka = len(Book.objects.filter(title__contains='dochka'))
    # # Отрисовка HTML-шаблона index.html с данными внутри
    # # переменной контекста context

    division = get_object_or_404(Division, pk=pk)

    # num_readings    = MeterReading.objects.filter(dvision__exact=pk).count()
    # readings        = MeterReading.objects.filter(dvision__exact=pk).all()

    # Render the HTML template index.html with the data in the context variable.

    return render(
        request,
        'catalog/division_readings.html',
        # context={'num_readings':num_readings,'readings':readings, ''}
        context={'division':division}
        
    )

def MeterReadingCreate(request):

    if request.method == 'POST':

        form = MeterReadingCreateForm(request.POST)

        if form.is_valid():

            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

    else:
        form = MeterReadingCreateForm(initial={'F_Creator': request.user})

    return render(request, 'catalog/MeterReading_form.html', {'form': form})



# class MeterReadingCreate(CreateView):
#     model = MeterReading
#     # fields = '__all__'
#     initial={'D_Date':datetime.datetime.now(), }
#     form_class = MeterReadingCreateForm 

class MeterReadingUpdate(UpdateView):
    model = MeterReading
    form_class = MeterReadingUpdateForm 
    # fields = '__all__'
    # form_class = MeterReadingUpdateForm
    # initial = {'D_Date':MeterReading.D_Date}
    # initial={'D_Date':datetime.datetime.now(),}
    # fields = ['first_name','last_name','date_of_birth','date_of_death']

class MeterReadingDelete(DeleteView):
    model = MeterReading
    success_url = reverse_lazy('Показания')



class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceCreateForm 
    # fields = '__all__'

class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceUpdateForm 
    # fields = '__all__'

class DeviceDelete(DeleteView):
    model = Device
    success_url = reverse_lazy('Приборы')



class DivisionCreate(CreateView):
    model = Division
    form_class = DivisionCreateForm 
    # fields = '__all__'

class DivisionUpdate(UpdateView):
    model = Division
    form_class = DivisionUpdateForm
    # fields = '__all__'

class DivisionDelete(DeleteView):
    model = Division
    success_url = reverse_lazy('Цеха')

def import_csv(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(csv_file)
            # print(request.FILES['csv_file'])
            
            for row in csv_reader:
                # print(row)
                MeterReading.objects.create(
                    F_Division          = get_object_or_404(Division, pk=row['F_Division']),
                    F_Devices           = get_object_or_404(Device,   pk=row['F_Devices']),
                    F_Tariff_Zones      = get_object_or_404(TariffZone, pk=row['F_Tariff_Zones']),
                    N_Value             = row['N_Value'],
                    D_Date              = row['D_Date'],
                    F_Delivery_Methods  = get_object_or_404(DeliveryMethod, pk=row['F_Delivery_Methods']),
                    F_Creator           = request.user,# row['F_Creator'],
                    C_Notes             = 'Импортировано из файла ' + str(request.FILES['csv_file']),
                    Img                 = None
                )

            return redirect('success_page')  # Redirect to a success page
    else:
        form = CSVImportForm()
    return render(request, 'catalog/import.html', {'form': form})

def success_page(request):
    return render(request, 'catalog/success.html')