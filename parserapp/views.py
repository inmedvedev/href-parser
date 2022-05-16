from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import UrlForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from bs4 import BeautifulSoup
import requests
import re
from celery.result import AsyncResult
from .models import DomainInfo
from .tasks import load_domain_data


@method_decorator(csrf_exempt, name='dispatch')
class BaseView(View):
    def get(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            url = request.GET.get('url', '')
            task_id = request.GET.get('task', '')
            task_result = AsyncResult(task_id)
            task_status = {'task_status': task_result.status}
            domain_data = list(DomainInfo.objects.filter(base_url=url).values())
            return JsonResponse({'data': domain_data, 'task_status': task_status})
        form = UrlForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        form = UrlForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax and form.is_valid():
            url = form.cleaned_data['url']
            hrefs = find_all_hrefs(url)
            task = load_domain_data.delay(hrefs, url)
            return JsonResponse({'url': url, 'task_id': task.id})


def find_all_hrefs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hrefs = [
        href['href'] for href in soup.find_all(
            'a',
            attrs={'href': re.compile("^https://")}
        )
    ]
    return hrefs

