# Django Router

You have a data and you need to provide some CRUD functionality for it quickly. What do you do?

1. Create model
2. Add some views
3. ????
4. PROFIT!

Right? Right! Done! And nothing works! Why? `URLS.PY`!!! You always forget this ones? I have a solution!

Maintaining Django's `urls.py` can become really annoying when you have a lot of apps with dozens urls in each. Other frameworks deal with it in elegant ways, like Flask's `@app.route` decorator. This project brings same concept to Django by adding `@router` decorator functions.

# Installation

Package is hosted in `pypi.org` thus you can use any tool that works with it to install the package:

`pip install django-router`

`poetry add django-router`

Add `django_router` to your `INSTALLED_APPS`

```python
# superduperproject/settings.py
INSTALLED_APPS = [
    ...
    "django_router",
    ...
]
```

---

Modify project `urls.py` (the top one)

```python
# superduperproject/urls.py
from django_router import router

# the only time you need to modify any `urls.py`
urlpatterns = router.urlpatterns

# or with existing ones
urlpatterns = [
    ...
] + router.urlpatterns
```

# Usage

Just use decorator in your apps' `views.py`. Django Router uses **autodiscovery** feature, so make sure views you're interested in are either inside `views.py` or get imported into it.

```python
# employees/views.py
from django_router import router
from employees.models import Employee
from django.shortcuts import render
from django.views.generic.edit import CreateView

# Works with function based views
# Resulting url will be `/employees/employee_list/`
@router.path()
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees':employees})

# As well as with class based views
# Resulting url will be `/employees/employee_create/`
@router.path()
def EmployeeCreate(CreateView):
    model = Employee

```

And that's it! No more need to deal with lengthy `urls.py`!

# How it works

Router has two functions `path` and `re_path` which work exactly the same as `django.urls` functions you already know. Except that you don't even need to specify **url** or **name**.

View module path is used to determine the resulting URL prefix. So URL for views in `employees/views.py` app will start with `/employees/...` , `employees/manage/views.py` - `/employees/manage/...` URL etc.

Also first module will be used as a namespace for reverse

```python
reverse('employees:employee_list')
```

**NOTICE**: nested namespaces are not supported for now.

App has some functionality builtin for automatic `pattern` and `name` generation.

For FBVs if no name is provided function name will be used, camel case will be turned into snake case:

```python
# same as path('import_employees/', import_employees, name='import_employees')
@router.path()
def import_employees(request):
    ...

# same as path('import_employees/', ImportEmployees.as_view(), name='import_employees')
@router.path()
class ImportEmployees(View):
    ...
```

For generic Django views(`CreateView`,`UpdateView`,`ListView`,`DetailView`,`DeleteView`) there's some builtin autonaming behavior which tries to be logical.

```python
@route.path()
class NewEmployeeView(CreateView):
    model = Employee

# is same as
path('employee_create/', NewEmployeeView.as_view(), name='employee_create')

```

Of course you can specify path and name as usual:

```python
@router.path('im_emp/', name='employees_import')
def import_employees(request):
    ...
```

# Settings

Settings for the project are mostly to control autonaming behavior.
These are default settings for the project

```python
ROUTER_SETTINGS={
    "NAME_WORDS_SEPARATOR": "_",
    "TRY_USE_MODEL_NAMES": True,
    "MODEL_NAMES_MONOLITHIC": True,
    "DJANGO_ADMIN_LIKE_NAMES": False,
}
```

---

**`NAME_WORDS_SEPARATOR`**: a separator char that'll be used during camel to snake case conversion in view names:

```python
@router.path()
class EmployeeList(ListView):
    model = Employee
```

`NAME_WORDS_SEPARATOR = "_"`

`path('employee_list/', EmployeeList.as_view(), name=`**_`'employee_list'`_**`)`

`NAME_WORDS_SEPARATOR = "-"`

`path('employee_list/', EmployeeList.as_view(), name=`**_`'employee-list'`_**`)`

---

**`TRY_USE_MODEL_NAMES`**: try to use model name for view naming within CBV while forming URLs

```python
@router.path()
class Employees(ListView):
    model = Employee
```

`TRY_USE_MODEL_NAMES = True`

`path('employee_list/', Employees.as_view(), name='employee_list')`

`TRY_USE_MODEL_NAMES = False`

`path('employees/', Employees.as_view(), name='employees')`

---

`MODEL_NAMES_MONOLITHIC`: only works when `TRY_USE_MODEL_NAMES = True`, control whether separator is used for model names consisting of multiple words

```python
@router.path()
class EmployeeAddressList(ListView):
    model = EmployeeAddress
```

`MODEL_NAMES_MONOLITHIC = True`

`path('employeeaddress/', EmployeesAddressList.as_view(), name='employeeaddress_list')`

`MODEL_NAMES_MONOLITHIC = False`

`path('employee_address/', EmployeesAddressList.as_view(), name='employee_address_list')`

---

**`DJANGO_ADMIN_LIKE_NAMES`**: if true uses strings like in Django admin for view names and paths

-   `ListView: changelist`
-   `UpdateView: change`
-   `CreateView: add`

```python
@router.path()
class EmployeeCreate(CreateView):
    model = Employee
```

`path('employee/add/', EmployeeCreate.as_view(), name='employee_add')`

# Management commands

`python manage.py router_list` - to see list of all available routes created by the router.

`python manage.py router_urls` - to see list of all available routes as if they're in `urls.py`
