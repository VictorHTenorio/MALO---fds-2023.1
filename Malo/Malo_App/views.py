from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Ingredient, Dish, Category, Mesa, DishIngredient
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from .forms import IngredientForm, DishForm, DishIngredientForm,CategoryForm
from django.views.decorators.http import require_POST
# Create your views here.


@login_required(login_url='login')
def HomePage(request):
    return render (request, 'home.html')

def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.success(request, ("Usuário ou senha incorreto!"))
            return redirect('login') 

    return render (request, 'login.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1 != pass2:
            messages.success(request, ("Suas senhas sao divergentes"))
            return redirect('signup') 
        else:
            if User.objects.filter(username=uname).exists():
                messages.success(request, ('Já existe uma conta com esse nome de usuário. Por favor, escolha outro.'))
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.success(request, ('Já existe uma conta com esse email. Por favor, escolha outro.'))
                return redirect('signup')   
            else:
                my_user=User.objects.create_user(uname,email,pass1)
                my_user.save()
                return redirect('login') 
        
    return render (request, 'signup.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def All_ingredient(request):
    ingredient_list = Ingredient.objects.all()
    return render(request,'listadeingredientes.html',{
        'ingredient_list':ingredient_list,
    })

@login_required(login_url='login')
def Add_ingredient(request):
    submitted = False
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Ingrediente registrado com sucesso!"))
            return redirect('ingredient_list')
    else:
        form = IngredientForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_ingredient.html', {'form': form, 'submitted': submitted})

@login_required(login_url='login')
def Edit_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk = ingredient_id)
    form = IngredientForm(request.POST or None, instance=ingredient)
    if form.is_valid():
        form.save()
        messages.success(request, ("Ingrediente editado com sucesso!"))
        return redirect('ingredient_list')

    return render(request,'editingredient.html',{
        'ingredient': ingredient,
        'form': form,
    })

@login_required(login_url='login')
def Delete_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk = ingredient_id)
    ingredient.delete()
    return redirect('ingredient_list')

@login_required(login_url='login')
def Menu(request):
    dishes = Dish.objects.all()
    return render(request,'menu.html',{
        'dishes':dishes,
    })

@login_required(login_url='login')
def Category_menu(request):
    categories = Category.objects.all()
    dishes = Dish.objects.all()
    return render(request,'menu_category.html',{
        'categories':categories,
        'dishes':dishes,
    })

@login_required(login_url='login')
def Add_category(request):
    submitted = False
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Categoria registrada com sucesso!"))
            return redirect('menu_category')
    else:
        form = CategoryForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_category.html', {'form': form, 'submitted': submitted})

@login_required(login_url='login')
def Edit_category(request, category_id):
    category = Category.objects.get(pk = category_id)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, ("Categoria editada com sucesso!"))
        return redirect('menu_category')

    return render(request,'edit_category.html',{
        'category': category,
        'form': form,
    })

@login_required(login_url='login')
def Delete_category(request, category_id):
    category = Category.objects.get(pk = category_id)
    category.delete()
    return redirect('menu_category')

@login_required(login_url='login')
def Add_dish(request):
    submitted = False
    if request.method == "POST":
        form = DishForm(request.POST)
        DishIngredientFormset = modelformset_factory(DishIngredient, form=DishIngredientForm, extra=0)
        formset = DishIngredientFormset(request.POST, queryset=DishIngredient.objects.none())
        if all([form.is_valid(), formset.is_valid()]):
            parent = form.save(commit=False)
            parent.save()
            for form in formset:
                child = form.save(commit=False)
                child.dish = parent
                child.save()
            messages.success(request, ("Prato registrado com sucesso!"))
            return redirect('menu')
    else:
        form = DishForm
        DishIngredientFormset = modelformset_factory(DishIngredient, form=DishIngredientForm, extra=0)
        formset = DishIngredientFormset(queryset=DishIngredient.objects.none())
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_dish.html', {
        'form': form,
        'submitted': submitted,
        'formset': formset,
        })

@login_required(login_url='login')
def Edit_dish(request, dish_id):
    dish = Dish.objects.get(pk = dish_id)
    form = DishForm(request.POST or None, instance=dish)
    DishIngredientFormset = modelformset_factory(DishIngredient, form=DishIngredientForm, extra=0)
    qs = dish.dishingredient_set.all()
    formset = DishIngredientFormset(request.POST or None, queryset=qs)
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.dish = parent
            child.save()
        messages.success(request, ("Prato editado com sucesso!"))
        return redirect('menu')

    return render(request,'editdish.html',{
        'dish': dish,
        'form': form,
        'formset': formset,
    })

@login_required(login_url='login')
def Delete_dish(request, dish_id):
    dish = Dish.objects.get(pk = dish_id)
    dish.delete()
    return redirect('menu')

@login_required(login_url='login')
def all_Mesa(request):
    mesa_list = Mesa.objects.all()
    return render(request,'mesa.html',{
        'mesa_list':mesa_list,
    })

@login_required(login_url='login')
def add_mesa(request):
    if request.method == 'POST':
        numero = Mesa.proximo_numero()
        mesa = Mesa(numero=numero)
        mesa.save()
        return redirect('mesa')
    return render(request, 'mesa.html')

@login_required(login_url='login')
def add_mult_mesa(request):
    if request.method == 'POST':
        qtd_mesas = int(request.POST.get('qtd_mesas', 1))
        for i in range(qtd_mesas):
            numero = Mesa.proximo_numero()
            mesa = Mesa(numero=numero)
            mesa.save()
        return redirect('mesa')
    return render(request, 'mesa.html')
   
@login_required(login_url='login')
def delete_mesa(request, id=None):
    mesa = Mesa.objects.order_by('-numero').first()  # Verifica o primeiro objeto Mesa
    if mesa is not None:  # Verifica se teve retorno válido
        mesa = Mesa(pk=mesa.id)
        mesa.delete()
        return redirect('mesa')
    else:
        messages.success(request, ("Não existem mesas para serem removidas!"))
        return redirect('mesa')

@login_required(login_url='login')
def delete_mult_mesa(request):
    qtd_mesas = int(request.POST.get('qtd_mesas', 0))
    mesas = Mesa.objects.all()
    if mesas is not None and len(mesas)>= qtd_mesas:
        for i in range(qtd_mesas) :
            mesa = Mesa.objects.order_by('-numero').first()
            mesa.delete()
        return redirect('mesa')
    else:
        messages.success(request, ("Mesas insuficientes para serem removidas!"))
        return redirect('mesa')



