from django.contrib import admin
from .models import Ingredient,Mesa,Dish,Category, DishIngredient

# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Mesa)
admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(DishIngredient)