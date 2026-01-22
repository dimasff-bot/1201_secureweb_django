import json
import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import TBCars

# ----------------------
# Session
# ----------------------

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")

        # dummy auth
        if username:
            request.session['is_authenticated'] = True
            request.session["username"] = username
            request.session['login_uuid'] = str(uuid.uuid4())
            request.session.set_expiry(30)

            token = str(uuid.uuid4())
            request.session['secure_token'] = token

            return redirect(f"/profilesecure/?token={token}")

    return render(request, 'signin.html', {"appType": "Web Service (Django)"})

def profilesecure(request):
    token = request.GET.get('token')
    session_token = request.session.get('secure_token')

    if token != session_token:
        return redirect('/signin/')

    # one-time token
    del request.session['secure_token']

    return render(request, 'profilesecure.html', {"appType": "Web Service (Django)"})

# ----------------------
# HTML Views (client)
# ----------------------
# NOTE: Pastikan API_URL sesuai dengan server Django yang menjalankan API.
API_URL = "http://127.0.0.1:8000/api/cars/"

def index(request):
    # session check
    if not request.session.get('is_authenticated'):
        return redirect('signin')

    return render(request, 'index.html', {"appType": "Web Service (Django)"})

def createcar(request):
    # session check
    if not request.session.get('is_authenticated'):
        return redirect('signin')

    return render(request, 'createcar.html', {"appType": "Web Service (Django)"})

def readcar(request):
    # session check
    if not request.session.get('is_authenticated'):
        return redirect('signin')

    # client-side will call the API internally (server-side request)
    rows = TBCars.objects.all()
    return render(
        request,
        'readcar.html',
        {
            "rows": rows,
            "appType": "Web Service (Django)"
        }
    )

def updatecar(request):
    # session check
    if not request.session.get('is_authenticated'):
        return redirect('signin')

    return render(request, 'updatecar.html', {"appType": "Web Service (Django)"})

def deletecar(request):
    # session check
    if not request.session.get('is_authenticated'):
        return redirect('signin')

    return render(request, 'deletecar.html', {"appType": "Web Service (Django)"})

def searchcar(request):
    # session check
    if not request.session.get('is_authenticated'):
        return redirect('signin')

    return render(request, 'searchcar.html', {"appType": "Web Service (Django)"})

def help(request):
    return HttpResponse("Help page - coming soon", content_type="text/plain")

# Handlers that receive HTML form -> call API
def createcarsave(request):
    if request.method == "POST":
        import requests
        data = {
            "carname": request.POST.get("carName"),
            "carbrand": request.POST.get("carBrand"),
            "carmodel": request.POST.get("carModel"),
            "carprice": request.POST.get("carPrice"),
        }
        requests.post(API_URL, json=data)
    return redirect('readcar')

def updatecarsave(request):
    if request.method == "POST":
        import requests
        payload = {
            "oldName": request.POST.get("oldName"),
            "newName": request.POST.get("newName"),
            "carbrand": request.POST.get("carBrand"),
            "carmodel": request.POST.get("carModel"),
            "carprice": request.POST.get("carPrice"),
        }
        # send as JSON body with PUT
        requests.put(API_URL, json=payload)
    return redirect('readcar')

def deletecarsave(request):
    if request.method == "POST":
        import requests
        payload = {"carname": request.POST.get("carName")}
        requests.delete(API_URL, json=payload)
    return redirect('readcar')

def searchcarsave(request):
    if request.method == "POST":
        import requests
        keyword = request.POST.get("keyword")
        resp = requests.get(API_URL, params={"q": keyword})
        rows = resp.json() if resp.status_code == 200 else []
        return render(request, 'readcar.html', {"rows": rows, "appType": "Web Service (Django)"})
    return redirect('searchcar')


# ----------------------
# REST API Views (server)
# ----------------------

@csrf_exempt
def api_cars(request):
    """
    Supports:
    - GET /api/cars/         -> list all or search q=
    - POST /api/cars/        -> create (expects JSON body)
    - PUT /api/cars/         -> update (expects JSON body with oldName + new fields)
    - DELETE /api/cars/      -> delete (expects JSON body with carname)
    """
    # GET (list or search)
    if request.method == "GET":
        q = request.GET.get('q', None)
        if q:
            qs = TBCars.objects.filter(models.Q(carname__icontains=q) | models.Q(carbrand__icontains=q))
        else:
            qs = TBCars.objects.all()
        data = [
            {
                "id": r.id,
                "carname": r.carname,
                "carbrand": r.carbrand,
                "carmodel": r.carmodel,
                "carprice": r.carprice,
            } for r in qs
        ]
        return JsonResponse(data, safe=False)

    # parse JSON body safely for other methods
    try:
        body = json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    # POST (create)
    if request.method == "POST":
        carname = body.get("carname") or body.get("carName")
        carbrand = body.get("carbrand") or body.get("carBrand")
        carmodel = body.get("carmodel") or body.get("carModel")
        carprice = body.get("carprice") or body.get("carPrice")
        TBCars.objects.create(
            carname=carname or "",
            carbrand=carbrand or "",
            carmodel=carmodel or "",
            carprice=carprice or "",
        )
        # return full list (like Flask did)
        qs = TBCars.objects.all()
        data = [
            {"id": r.id, "carname": r.carname, "carbrand": r.carbrand, "carmodel": r.carmodel, "carprice": r.carprice}
            for r in qs
        ]
        return JsonResponse(data, safe=False)

    # PUT (update)
    if request.method == "PUT":
        old_name = body.get("oldName") or body.get("oldname") or body.get("carname")
        if not old_name:
            return HttpResponseBadRequest("oldName required for update")

        # find matching rows
        qs = TBCars.objects.filter(carname=old_name)
        if not qs.exists():
            return JsonResponse([], safe=False)

        # fields to update (only if present and non-empty)
        new_name = body.get("newName")
        carbrand = body.get("carbrand") or body.get("carBrand")
        carmodel = body.get("carmodel") or body.get("carModel")
        carprice = body.get("carprice") or body.get("carPrice")

        update_data = {}
        if new_name:
            update_data["carname"] = new_name
        if carbrand:
            update_data["carbrand"] = carbrand
        if carmodel:
            update_data["carmodel"] = carmodel
        if carprice:
            update_data["carprice"] = carprice

        if update_data:
            qs.update(**update_data)

        qs_all = TBCars.objects.all()
        data = [
            {"id": r.id, "carname": r.carname, "carbrand": r.carbrand, "carmodel": r.carmodel, "carprice": r.carprice}
            for r in qs_all
        ]
        return JsonResponse(data, safe=False)

    # DELETE
    if request.method == "DELETE":
        carname = body.get("carname") or body.get("carName")
        if not carname:
            return HttpResponseBadRequest("carname required for delete")

        TBCars.objects.filter(carname=carname).delete()

        qs_all = TBCars.objects.all()
        data = [
            {"id": r.id, "carname": r.carname, "carbrand": r.carbrand, "carmodel": r.carmodel, "carprice": r.carprice}
            for r in qs_all
        ]
        return JsonResponse(data, safe=False)

    return HttpResponse(status=405)
