from django.http import HttpResponse
from django.shortcuts import render, redirect
from wasteSearch import models
from django import forms

def about(request):
    return render(request, 'about.html')

def help(request):
    return render(request, 'help.html')

# 展示指纹特征信息
def fingerFeature(request):
    return render(request, 'fingerFeature.html')