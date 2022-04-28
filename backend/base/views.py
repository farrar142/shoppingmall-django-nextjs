
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from django import forms

from commons.models import UploadFileModel


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ('file',)

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False


@csrf_exempt
def index(request):
    if request.method == 'POST':
        print(request.FILES)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})
