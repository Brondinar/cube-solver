from django.shortcuts import render
from django.http import HttpResponse

from json import loads, dumps

import kociemba

# Create your views here.
def cube_index(request):
    return render(request, 'cube_solver/index.html')

def cube_solve(request):
    try:
        cube_data = loads(request.POST["cube"])
        print(cube_data['cube'])
        solve = kociemba.solve(cube_data['cube'])
    except ValueError:
        error_message = "Ошибка. Этот куб невозможен."
        return render(request, 'cube_solver/index.html', {'error_message': error_message})
    else:
        sides = dumps(cube_data['sides'])
        return render(request, 'cube_solver/solve.html', {'solve': solve, 'sides': sides})