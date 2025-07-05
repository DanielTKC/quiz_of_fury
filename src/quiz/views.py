from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'quiz/index.html')

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})
