# Django Router

You have a data and you need to provide some CRUD functionality for it quickly. What do you do?

1. Create model
2. Add some views
3. ????
4. PROFIT!

Right? Right! Done! And nothing works! Why? `URLS.PY`!!! You always forget this ones? I have a solution!

Maintaining Django's `urls.py` can become really annoying when you have a lot of apps with dozens urls in each. Other frameworks deal with it in elegant ways, like Flask's `@app.route` decorator. This project brings same concept to Django by adding `@router` decorator functions.

# Compatibility

This project is automatically tested with Python 3.8, 3.9, 3.10, 3.11, 3.12 and Django 3.2, 4.0, 4.1, 4.2, 5.0, 5.1. Latest version for each release. Compatibility with earlier versions of Python or Django(starting from 2.0) is possible, but not guaranteed.

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

# Concept

To easily understand all the auto naming concept of the app take a look at testing project within the repo.

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
path('employee/create/', NewEmployeeView.as_view(), name='employee_create')

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
ROUTER_SETTINGS = {
    "SIMPLE_AUTO_NAMING": False,
    "WORDS_SEPARATOR": "_",
    "MODEL_NAMES_MONOLITHIC": True,
    "DJANGO_ADMIN_LIKE_NAMES": False,
    "MODULE_PATH_MAP": False
}
```

---

**`SIMPLE_AUTO_NAMING`**: if set to true all other settings are ignored, name and url are composed from view name, `CamelCase` turned to `snake_case`:

```
"test_app.views.SimpleCbv" -> ["/test_app/simple_cbv/", "test_app:simple_cbv"],
"test_app.views.simple_fbv" -> ["/test_app/simple_fbv/", "test_app:simple_fbv"],
```

---

**`WORDS_SEPARATOR`**: a separator char that'll be used during camel to snake case conversion in view names:

```python
@router.path()
class EmployeeList(ListView):
    model = Employee
```

`WORDS_SEPARATOR = "_"`

`path('employee_list/', EmployeeList.as_view(), name=`**_`'employee_list'`_**`)`

`WORDS_SEPARATOR = "-"`

`path('employee_list/', EmployeeList.as_view(), name=`**_`'employee-list'`_**`)`

---

`MODEL_NAMES_MONOLITHIC`: only works when `MODEL_BASED_PATTERNS = True`, control whether separator is used for model names consisting of multiple words

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

---

**`MODULE_PATH_MAP`**: By default router uses view module path to generate resulting url:
`students.views.StudentUpdate` is split into three parts:
- `students`: top level app name, will be used as a prefix for all views inside `student.views`
- `views`: name of the module containing views, skipped during path name generation
- `StudentList`: view name, turned into a last part of the url depending on previous settings
So resulting url for the view may look like this
`/students/<int:pk>/update/`

However you may have a view that has following module path:
`companies.departments.views.DepartmentUpdate`, by default resulting url will look like this:
`/companies/departments/<int:pk>/update/`
If you want to avoid this and skip everything between app name and last module name set this settings to `False`.


# Management commands

`python manage.py router_list` - to see list of all available routes created by the router.

`python manage.py router_urls` - to see list of all available routes as if they're in `urls.py`
