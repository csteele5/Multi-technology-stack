# Django Configuration Notes

## Setup
**VSCODE Setup**
To set up the Django linter, use the following steps:

*If the .vscode/settings.json file exists in the project folder, do this:*

open the .vscode/settings.json and add the following line:
```
"python.linting.pylintArgs": ["--load-plugins", "pylint_django"]

```

*If the file does not exist:*
Add .vscode/ to the .gitignore FIRST, then
```
mkdir .vscode
touch settings.json
```
Paste in the below code:
```
{
    "python.linting.pylintEnabled": true,
    "python.linting.enabled": true,
    "python.linting.pylintArgs": ["--load-plugins", "pylint_django"]
}
```

[Reference](https://code.visualstudio.com/docs/python/linting#_commandline-arguments-and-configuration-files)


**Initial Steps**
Create project directory
Create Dockerfile, requirements.txt, docker-compose.yml
Run the following: 
```
sudo docker-compose run web django-admin startproject sprintschedule .
sudo chown -R $USER:$USER .
```

Start system
```
docker-compose up
```

Create super user
```
sudo docker-compose run web python manage.py createsuperuser
```
Log in, verify it all works.  Now start building.
Create the app
```
sudo docker-compose run web python manage.py startapp schedule
docker-compose up -d --build
```

**Migrations!!**
```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```


## Tasks

**Extend User Model**
I need to add a flag to the user model to indicate they are participating in the sprint.
[Extending the Model](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)

*Trie using the OneToOne approach.  I bailed on this and created a new model for tech*

[Datefield format reference](https://strftime.org/)

[General examples including Datefield](https://www.fullstackpython.com/django-db-models-datefield-examples.html)

[Filtering dropdown in model](https://stackoverflow.com/questions/11508744/django-models-filter-by-foreignkey)

[Admin improvements](https://docs.djangoproject.com/en/3.0/intro/tutorial07/)


[Customize list_display](https://www.dothedev.com/blog/django-admin-show-custom-field-list_display/)
```
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "all_orders_of_this_customer", "phone_number")

    def all_orders_of_this_customer(self, obj):
        return format_html(
 '<a  href="{0}?customer={1}">Orders list of this customer</a>&nbsp;',
            reverse('admin:customerapp_foodorder_changelist' ), obj.id
        )

    all_orders_of_this_customer.short_description = 'Customer Orders'
    all_orders_of_this_customer.allow_tags = True
```
Use this instead: [Verbose Name](https://docs.djangoproject.com/en/3.1/topics/db/models/#verbose-field-names)

[Setting up User Authentication](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication)


[Date range filtering](https://stackoverflow.com/questions/42113894/django-admin-date-range-filter/42115549#42115549)

Filtering can span relationships - 
```
class PersonAdmin(admin.UserAdmin):
    list_filter = ('company__name',)
```
[Ref](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter)