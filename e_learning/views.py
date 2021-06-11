from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect


def index(request):
    # return HttpResponse("Hello Ron")
    return HttpResponseRedirect(reverse('Article:article_list'))
