from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

from rango.bing_search import run_query

# Did you know that request is just a convention, but in fact
# this is just HttpRequest


#--------------------------------------------------
# HELPER FUNCTIONS

# Cookies
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_counter_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(
        request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(
        last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:  # Should be .days
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

# HELPER FUNCTIONS
#--------------------------------------------------


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Pass the list to the variable
    context_dict = {'categories': category_list, 'pages': page_list}
    visitor_counter_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    # print(context_dict['visits'])
    return response


def about(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    return render(request, 'rango/about.html', context={'visits': visits})


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()
    # By saying form = CategoryForm() we initiate the form
    # How does it know which model to use?
    # The class Meta of the froms specifies which
    # models the form corresponds with

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    form = PageForm

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)

            # Reference the User to the UserProfile
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {'user_form': user_form,
                                                   'profile_form': profile_form,
                                                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print("Invalid login: {} {}".format(username, password))
            return HttpResponse("Invalid login supplied.")
    else:
        return render(request, 'rango/login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def search(request):
    result_list = []
    context_dict = {}
    if request.method == "POST":
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict = {'result_list': result_list, 'query': query}

    return render(request, 'rango/search.html', context_dict)


def track_url(request):
    page_id = None
    url = ''
    if request.method == 'GET':
        if 'page_id' in request.GET:
            try:
                page_id = request.GET['page_id']
                page = Page.objects.get(pk=page_id)
                page.views += 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)
