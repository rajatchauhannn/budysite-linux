from django.shortcuts import render
from .lib.budy import phase1
from .models import exercises_Db
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    exer = exercises_Db.objects.all()
    return render(request, 'budy/dashboard.html', {'exer' : exer})

@login_required
def home(request):

    if request.method == 'POST':
        area = request.POST.get('area')
        timming = request.POST.get('timming')

        list_of_workouts = phase1(area, int(timming))
        string_of_workouts = ', '.join(str(ex) for ex in list_of_workouts)

        return render(request, 'budy/regime.html', {'area': area, 'workouts': string_of_workouts })

    return render(request, 'budy/dashboard.html')



