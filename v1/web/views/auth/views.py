from django.shortcuts import render, redirect

from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.models import User, Group

from .forms import LoginForm, StudentLoginForm



def login_page(request):
    #redirect_to = request.GET.get('next', '')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        #user = authenticate(email=username, password=password)
        
        if username is not None and password is not None:
            user = User.objects.filter(email=username)
            
            if user.exists():
                user_model = user.get()
                if user_model.check_password(password):
                    if user_model.is_active == True:
                        
                        role = ""
                        if user_model.is_superuser:
                            role = "admin"
                            
                            login(request, user_model)
                            return redirect('web:dashboard')
                            # return redirect('dashboard')

                        else:
                            roles = user_model.groups.filter().all()
                            for _role in roles:
                                role = _role.name
                                if role in ('student', 'aggent'):
                                    login(request, user_model)
                                    return redirect('web:dashboard')
                                else:
                                    error = "Invalid email or password"
                                    form.add_error(None, error)

                    else:
                        error = "Your account is deactivate"
                        form.add_error(None, error)

                else:
                    error = "Your password is wrong!"
                    form.add_error(None, error)
            else:
                error = "Your email is wrong!"
                form.add_error(None, error)
    
    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'auth/login.html', context )


def school_student_login(request):
    form = StudentLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        #user = authenticate(email=username, password=password)
        
        if username is not None and password is not None:
            user = User.objects.filter(username=username, groups__name='school_student')
            if user.exists():
                user_model = user.get()
                if user_model.check_password(password):
                    if user_model.is_active == True:
                        login(request, user_model)
                        return redirect('web:school_student_dashboard')
                    else:
                        error = "Your account is deactivate"
                        form.add_error(None, error)
                else:
                    error = "Your password is wrong!"
                    form.add_error(None, error)
            else:
                error = "Your username is wrong!"
                form.add_error(None, error)
    
    context = {
        'title': 'Student Login',
        'form': form
    }
    return render(request, 'auth/school_student_login.html', context )