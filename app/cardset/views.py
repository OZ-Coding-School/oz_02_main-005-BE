from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from .models import CardSet

executor = ThreadPoolExecutor(max_workers=5)
# Create your views here.
