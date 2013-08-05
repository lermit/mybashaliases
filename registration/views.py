from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from forms import ProfileForm

@login_required
def my_profile(request):

    if request.method == "POST":
        form = ProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account is now up to date !")
    else:
        form = ProfileForm(instance=request.user)

    context = {}
    context.update({"form": form})
    return render(request, 'registration/my_profile.html', context)

