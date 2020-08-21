from django.shortcuts import render
from django.db.models import Q
from .models import Reader, Document, Copy, Reserves, Branch, Borrows , Fine
from datetime import datetime
from django.db.models import Count
import pytz


def index(request):
    return render(request, 'CityLibrary/html/index.html',)


def reader(request):
    if request.method == 'POST':
        user_id = request.POST['reader_id']
        if user_id:
            try:
                reader_objects = Reader.objects.get(readerid=user_id)
            except Reader.DoesNotExist:
                return render(request, 'CityLibrary/html/reader.html')
            if reader_objects:
                context = {'reader': reader_objects, 'reader_id': user_id}
                return render(request, 'CityLibrary/html/reader.html', context)
            else:
                return render(request, 'CityLibrary/html/reader.html')
        else:
            return render(request, 'CityLibrary/html/reader.html')
    else:
        return render(request, 'CityLibrary/html/reader.html')


def get_reader(request, reader_id):
    try:
        reader_objects = Reader.objects.get(readerid=reader_id)
        if reader_objects:
            context = {'reader': reader_objects, 'reader_id': reader_id}
            return render(request, 'CityLibrary/html/reader_operations.html', context)
        else:
            return render(request, 'CityLibrary/html/reader_operations.html', {'reader_id': reader_id})
    except Reader.DoesNotExist:
        return render(request, 'CityLibrary/html/reader_operations.html', {'reader_id': reader_id})


def search_document(request, reader_id):
    if request.method == 'POST':
        s = request.POST['search']
        if s:
            try:
                documents = Document.objects.filter(Q(title__icontains=s) | Q(docid__icontains=s)
                                                    | Q(publisherid__pubname__icontains=s)).filter()
                print(documents.query)
            except Document.DoesNotExist:
                return render(request, 'CityLibrary/html/search_document.html', {'reader_id': reader_id})
            if documents:
                context = {'documents': documents, 'reader_id': reader_id}
                return render(request, 'CityLibrary/html/search_document.html', context)
            else:
                return render(request, 'CityLibrary/html/search_document.html', {'reader_id': reader_id})
        else:
            return render(request, 'CityLibrary/html/search_document.html', {'reader_id': reader_id})
    else:
        return render(request, 'CityLibrary/html/search_document.html', {'reader_id': reader_id})


def reserve_document(request, doc_id, reader_id):
    try:
        document_copy = Copy.objects.filter(docid=doc_id).filter(status=True)
        context = {'reader_id': reader_id, 'document_copy': document_copy}
    except Copy.DoesNotExist:
        return render(request, 'CityLibrary/html/reserve_document.html', {'reader_id': reader_id})
    return render(request, 'CityLibrary/html/reserve_document.html', context)


def borrow_document(request, doc_id, reader_id):
    try:
        document_copy = Copy.objects.filter(docid=doc_id).filter(status=True)
        context = {'reader_id': reader_id, 'document_copy': document_copy}
    except Copy.DoesNotExist:
        return render(request, 'CityLibrary/html/borrow_document.html', {'reader_id': reader_id})
    return render(request, 'CityLibrary/html/borrow_document.html', context)


def reserve_document_copy(request, copy_id, reader_id):
    try:
        doc_copy = Copy.objects.filter(copyid=copy_id).filter(status=True)
        if doc_copy:
            a = Reserves(None, reader_id, copy_id)
            a.status = True
            a.save()
            Copy.objects.filter(copyid=copy_id).update(status=False)
            context = {'reserved_copy': a, 'reader_id': reader_id, 'copy_id': copy_id}
            return render(request, 'CityLibrary/html/reserve_document_copy.html', context)
    except Reserves.DoesNotExist:
        return render(request, 'CityLibrary/html/reserve_document_copy.html', {'reader_id': reader_id})
    return render(request, 'CityLibrary/html/reserve_document_copy.html', {'reader_id': reader_id})


def view_reserved_documents(request, reader_id):
    try:
        reserved_docs = Reserves.objects.filter(readerid=reader_id).filter(status=True)
        if reserved_docs:
            context = {'reader_id': reader_id, 'rsv_docs': reserved_docs}
            return render(request, 'CityLibrary/html/view_reserved_documents.html', context)
        return render(request, 'CityLibrary/html/view_reserved_documents.html', {'reader_id': reader_id})
    except Reserves.DoesNotExist:
        return render(request, 'CityLibrary/html/view_reserved_documents.html', {'reader_id': reader_id})


def documents_by_publisher(request, reader_id):
    if request.method == 'POST':
        s = request.POST['search']
        if s:
            try:
                documents = Document.objects.filter(publisherid__pubname__icontains=s)
                if documents:
                    context = {'documents': documents, 'reader_id': reader_id}
                    return render(request, 'CityLibrary/html/search_publisher_documents.html', context)
                else:
                    return render(request, 'CityLibrary/html/search_publisher_documents.html', {'reader_id': reader_id})
            except Document.DoesNotExist:
                return render(request, 'CityLibrary/html/search_publisher_documents.html', {'reader_id': reader_id})
        else:
            return render(request, 'CityLibrary/html/search_publisher_documents.html', {'reader_id': reader_id})
    else:
        return render(request, 'CityLibrary/html/search_publisher_documents.html', {'reader_id': reader_id})


def search_document_reserve(request, reader_id):
    branch = Branch.objects.all()
    document = Document.objects.all()
    context = {'branch': branch, 'document': document, 'reader_id': reader_id}
    if request.method == 'POST':
        b = request.POST['branch_select']
        d = request.POST['document_select']
        if b and d:
            try:
                copy = Copy.objects.filter(docid=d).filter(libid=b).filter(status=True)
            except Copy.DoesNotExist:
                return render(request, 'CityLibrary/html/search_reserve_document.html', context)
            context['document_copy'] = copy
            return render(request, 'CityLibrary/html/search_reserve_document.html', context)
        else:
            return render(request, 'CityLibrary/html/search_reserve_document.html', context)
    return render(request, 'CityLibrary/html/search_reserve_document.html', context)


def search_document_borrow(request, reader_id):
    branch = Branch.objects.all()
    document = Document.objects.all()
    context = {'branch': branch, 'document': document, 'reader_id': reader_id}
    if request.method == 'POST':
        b = request.POST['branch_select']
        d = request.POST['document_select']
        if b and d:
            try:
                document_copy = Copy.objects.filter(docid=d).filter(libid=b).filter(status=True)
            except Copy.DoesNotExist:
                return render(request, 'CityLibrary/html/search_borrow_document.html', context)
            context['document_copy'] = document_copy
            return render(request, 'CityLibrary/html/search_borrow_document.html', context)
        else:
            return render(request, 'CityLibrary/html/search_borrow_document.html', context)
    return render(request, 'CityLibrary/html/search_borrow_document.html', context)


def borrow_document_copy(request, copy_id, reader_id):
    try:
        doc_copy = Copy.objects.filter(copyid=copy_id).filter(status=True)
        if doc_copy:
            a = Borrows(None, reader_id, copy_id)
            a.save()
            Copy.objects.filter(copyid=copy_id).update(status=False)
            context = {'borrowed_copy': a, 'reader_id': reader_id, 'copy_id': copy_id}
            return render(request, 'CityLibrary/html/borrow_document_copy.html', context)
    except Reserves.DoesNotExist:
        return render(request, 'CityLibrary/html/borrow_document_copy.html', {'reader_id': reader_id})
    return render(request, 'CityLibrary/html/borrow_document_copy.html', {'reader_id': reader_id})


def borrow_reserved_copy(request, copy_id, reader_id, res_number):
    try:
        x = Reserves.objects.get(resnumber=res_number)
        x.status = False
        x.save()
        a = Borrows(None, reader_id, copy_id)
        a.save()
        Copy.objects.filter(copyid=copy_id).update(status=False)
        context = {'borrowed_copy': a, 'reader_id': reader_id, 'copy_id': copy_id}
        return render(request, 'CityLibrary/html/borrow_document_copy.html', context)
    except Reserves.DoesNotExist:
        return render(request, 'CityLibrary/html/borrow_document_copy.html', {'reader_id': reader_id})


def view_borrowed_documents(request, reader_id):
    try:
        borrowed_docs = Borrows.objects.filter(readerid=reader_id).filter(rdtime__isnull=True)
        if borrowed_docs:
            context = {'reader_id': reader_id, 'brw_docs': borrowed_docs}
            return render(request, 'CityLibrary/html/return_documents.html', context)
        return render(request, 'CityLibrary/html/return_documents.html', {'reader_id': reader_id})
    except Reserves.DoesNotExist:
        return render(request, 'CityLibrary/html/return_documents.html', {'reader_id': reader_id})


def return_borrowed_documents(request, reader_id, borrowid, copy_id):
    try:
        a = Borrows.objects.filter(bornumber=borrowid).update(rdtime=datetime.now())
        b = Copy.objects.filter(copyid=copy_id).update(status=True)
        if a and b:
            current_date = datetime.now(tz=pytz.utc)
            borrow_date = Borrows.objects.get(bornumber=borrowid)
            delta = current_date - borrow_date.bdtime
            delta = delta.days
            if delta > 20:
                delta = delta - 20
                delta = delta * 0.2
            else:
                delta = 0
            f = Fine(None, delta, borrowid)
            f.save()
            print(f.fine)
            document = Borrows.objects.get(bornumber=borrowid)
            context = {'doc': document, 'reader_id': reader_id, 'borr_id': borrowid, 'copy_id': copy_id}
            return render(request, 'CityLibrary/html/return_document_copy.html', context)
        else:
            return render(request, 'CityLibrary/html/return_document_copy.html', {'reader_id': reader_id})
    except Borrows.DoesNotExist or Copy.DoesNotExist:
        return render(request, 'CityLibrary/html/return_document_copy.html', {'reader_id': reader_id})


def frequent_borrowers(request):
    branches = Branch.objects.all()
    context = {'branches': branches}
    if request.method == ['POST']:
        libid = request.POST['branch_select']
        top_borrowers = Borrows.objects.filter(Borrows.copyid in Copy.objects.filter(libid=libid))\
            .annotate(reader_count=Count('readerid'), book_count=Count('copyid')).order_by('-reader_count')[:10]
        context['top_borrowers'] = top_borrowers
    return render(request, 'CityLibrary/html/frequent_borrowers.html', context)


def check_fine(request, reader_id, borrowid):

    current_date = datetime.now(tz=pytz.utc)
    borrow_date = Borrows.objects.get(bornumber=borrowid)
    delta = current_date - borrow_date.bdtime
    delta = delta.days
    no_of_days = delta
    if delta > 20:
        delta = delta - 20
        delta = delta * 0.2
    else:
        delta = 0
    context = {'reader_id': reader_id, 'delta': delta, 'borrow_date': borrow_date, 'no_of_days': no_of_days}
    return render(request, 'CityLibrary/html/check_fine.html', context)


def view_borrowed_doc(request, reader_id):
    borrow = Borrows.objects.filter(readerid=reader_id).filter(rdtime__isnull=True)
    context = {'borrow': borrow, 'reader_id': reader_id}
    if request.method == 'POST':
        b = request.POST['borrow_id']
        if b:
            try:
                current_date = datetime.now(tz=pytz.utc)
                borrow_date = Borrows.objects.get(bornumber=b)
                delta = current_date - borrow_date.bdtime
                delta = delta.days
                no_of_days = delta
                if delta > 20:
                    delta = delta - 20
                    delta = delta * 0.2
                else:
                    delta = 0
                context = {'reader_id': reader_id, 'delta': delta, 'borrow_date': borrow_date, 'no_of_days': no_of_days}
                return render(request, 'CityLibrary/html/check_fine.html', context)
            except Borrows.DoesNotExist:
                return render(request, 'CityLibrary/html/view_documents_borrowed.html', context)
        else:
            return render(request, 'CityLibrary/html/view_documents_borrowed.html', context)
    return render(request, 'CityLibrary/html/view_documents_borrowed.html', context)


def cancel_reservation(request, reader_id, res_number):
    r = Reserves.objects.get(resnumber=res_number)
    m = r.copyid
    c = Copy.objects.get(copyid=m.copyid)
    print(c.status)
    r.status = False
    c.status = True
    r.save()
    c.save()
    print(c.status)
    return render(request, 'CityLibrary/html/reservation_canceled.html', {'reader_id': reader_id, 'r': r})
