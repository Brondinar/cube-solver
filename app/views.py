from django.shortcuts import render
from json import loads, dumps
import kociemba


def cube_index(request):
    return render(request, 'app/index.html')


def cube_solve(request):
    try:
        cube_data = loads(request.POST["cube"])
        solve = kociemba.solve(cube_data['cube'])
    except ValueError:
        error_message = "Ошибка. Этот куб невозможен."
        return render(request, 'app/index.html', {'error_message': error_message})
    else:
        sides = dumps(cube_data['sides'])
        return render(request, 'app/solve.html', {'solve': solve, 'sides': sides})