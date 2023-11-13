from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.decorators import login_required



@login_required	
def logout_view(request):
    logout(request)
    return redirect("web:login_page")