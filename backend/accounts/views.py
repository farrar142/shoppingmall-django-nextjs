import os
from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
import requests

from accounts.models import User

# Create your views here.
