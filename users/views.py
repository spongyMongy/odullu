from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm

def signup(request):
    context = {}
    if request.method == 'POST':
        print('898989898989')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('0000000000')

            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = request.user
            print('made it', username, password, user)
            if user is not None:
                # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                print('got here')
                user.save()
                return redirect('login')

                ###ADD USER TO DATABASE....
            else:
                print('user is none')
        else:
            form = UserCreationForm()
            context['form'] = form
            return render(request, 'users/signup.html', context)
        # context['form'] = form
    if request.method == 'GET':
        form = UserCreationForm()
        context['form'] = form
        return render(request, 'users/signup.html', context)