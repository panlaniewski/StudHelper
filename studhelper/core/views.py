from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from django.db.models import Q
# ------------------------------------------------------------------------------------------------------------------------------
from subjects.models import Subject
from subjects.forms import SubjectForm
from .forms import SearchForm
# ------------------------------------------------------------------------------------------------------------------------------
def index(request):
    subjects = Subject.objects.all()
    #Поиск------------------------------------------------------------------------------------------------------------------------------
    keyword = request.GET.get("keyword", "")
    if keyword:
        q = Q(name__icontains=keyword)
        subjects = Subject.objects.filter(q)
    else:
        subjects = Subject.objects.all()
    #Пагинация------------------------------------------------------------------------------------------------------------------------------
    paginator = Paginator(subjects, 6)
    if "page" in request.GET:
        page_num = request.GET["page"]
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    # ------------------------------------------------------------------------------------------------------------------------------    
    search_form = SearchForm(initial={"keyword": keyword})
    #Создание нового предмета------------------------------------------------------------------------------------------------------------------------------    
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            # subject.user = request.user
            subject.save()
            return redirect("home")
    else:
        form = SubjectForm()
    # ------------------------------------------------------------------------------------------------------------------------------    
    context = { 
        "subjects": page.object_list, 
        "form": form, 
        "page": page, 
        "search_form": search_form,
        "keyword": keyword,
    }
    return render(request, 'index.html', context)
# -----------------------------------------------------------------------------------------------------------------------------------
def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена(")
