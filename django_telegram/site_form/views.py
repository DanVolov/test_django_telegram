from django.shortcuts import render, redirect
from .forms import SiteForm
from .models import SiteModel


def index(request):

    if request.method == 'POST':
        form = SiteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = SiteForm()

    all_form = SiteModel.objects.all()

    data = {
        'form': form,
        'all_form': all_form,
    }

    return render(request, 'site_form/index.html', data)