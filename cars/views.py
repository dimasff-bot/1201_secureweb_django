from django.shortcuts import render, redirect
from .models import TBCars
from django.db.models import Q

appType = "Monolith"


def index(request):
    return render(request, 'index.html', {'appType': 'Monolith'})

def createcar(request):
    return render(request, 'createcar.html')

def createcarsave(request):
    if request.method == "POST":
        TBCars.objects.create(
            carname=request.POST['carName'],
            carbrand=request.POST['carBrand'],
            carmodel=request.POST['carModel'],
            carprice=request.POST['carPrice']
        )
        return redirect('readcar')
    return redirect('createcar')

def readcar(request):
    rows = TBCars.objects.all()

    context = {
        "rows": rows
    }

    return render(request, "readcar.html", context)

def updatecar(request):
    return render(request, 'updatecar.html')

def updatecarsave(request):
    if request.method == "POST":
        oldName = request.POST['oldName']

        try:
            car = TBCars.objects.get(carname=oldName)
        except TBCars.DoesNotExist:
            return render(request, "error.html",
                          {"message": f"Data dengan nama {oldName} tidak ditemukan."})

        car.carname = request.POST['newName']
        car.carbrand = request.POST['carBrand']
        car.carmodel = request.POST['carModel']
        car.carprice = request.POST['carPrice']
        car.save()

        return redirect('readcar')
    return redirect('updatecar')

def deletecar(request):
    return render(request, 'deletecar.html')

def deletecarsave(request):
    if request.method == "POST":
        carName = request.POST['carName']
        TBCars.objects.filter(carname=carName).delete()
        return redirect('readcar')
    return redirect('deletecar')

def searchcar(request):
    return render(request, 'searchcar.html')

def searchcarsave(request):
    keyword = request.POST['keyword']
    rows = TBCars.objects.filter(
        Q(carname__icontains=keyword) |
        Q(carbrand__icontains=keyword)
    )
    return render(request, 'readcar.html', {'rows': rows, 'appType': appType})

def help(request):
    return render(request, 'help.html')