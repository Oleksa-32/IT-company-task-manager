from django.apps import apps
from django.contrib import admin

app = apps.get_app_config('task_manager')

for model in app.get_models():
    admin.site.register(model)
