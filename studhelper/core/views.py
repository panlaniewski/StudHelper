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

    if not request.user.is_authenticated:
        return render(request, 'not_logged_in.html')
  
    #Поиск------------------------------------------------------------------------------------------------------------------------------
    keyword = request.GET.get("keyword", "")
    if keyword:
        q = (Q(name__icontains=keyword) & Q(user=request.user)) if request.user.is_authenticated else Q(pk__isnull=True)
        subjects = Subject.objects.filter(q)
    else:
        q = Q(user=request.user) if request.user.is_authenticated else Q(pk__isnull=True)
        subjects = Subject.objects.filter(q)
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
        form = SubjectForm(request.POST, user=request.user)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect("home")
    else:
        form = SubjectForm(user=request.user)
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
