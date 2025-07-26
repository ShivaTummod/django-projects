from django.shortcuts import render, redirect
from .forms import InputForm

def input_data(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'inputapp/success.html')
    else:
        form = InputForm()
    return render(request, 'inputapp/input_form.html', {'form': form})
