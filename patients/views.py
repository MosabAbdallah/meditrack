from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Patient, Vital
from users.models import User
from django.db.models import Count, Q
from django.http import JsonResponse

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])

    search_query = request.GET.get('search', '')
    if search_query:
        patients = Patient.objects.filter(
            Q(created_by=user) & Q(name__icontains=search_query)
        ).annotate(vital_count=Count('vitals'))
    else:
        patients = Patient.objects.filter(created_by=user).annotate(vital_count=Count('vitals'))

    return render(request, 'patients/dashboard.html', {
        'patients': patients,
        'search_query': search_query,
    })

def add_patient(request):
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        errors = Patient.objects.validate_patient(request.POST)
        if errors:
            for msg in errors.values():
                messages.error(request, msg)
            return redirect('add_patient')

        Patient.objects.create(
            name=request.POST['name'],
            age=request.POST['age'],
            gender=request.POST['gender'],
            medical_notes=request.POST.get('medical_notes', ''),
            created_by=User.objects.get(id=request.session['user_id'])
        )
        return redirect('dashboard')

    return render(request, 'patients/add_patient.html')

def edit_patient(request, patient_id):
    if 'user_id' not in request.session:
        return redirect('login')

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        errors = Patient.objects.validate_patient(request.POST)
        if errors:
            for msg in errors.values():
                messages.error(request, msg)
            return redirect('edit_patient', patient_id=patient_id)

        patient.name = request.POST['name']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.medical_notes = request.POST.get('medical_notes', '')
        patient.save()
        return redirect('dashboard')

    return render(request, 'patients/edit_patient.html', {'patient': patient})

def delete_patient(request, patient_id):
    if 'user_id' not in request.session:
        return redirect('login')

    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, "Patient deleted successfully.")
        return redirect('dashboard')

    return render(request, 'patients/delete_confirm.html', {'patient': patient})

def patient_detail(request, patient_id):
    if 'user_id' not in request.session:
        return redirect('login')

    patient = get_object_or_404(Patient, id=patient_id)
    vitals = Vital.objects.filter(patient=patient).order_by('-recorded_at')

    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'vitals': vitals
    })

def add_vital(request, patient_id):
    if 'user_id' not in request.session:
        return redirect('login')

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        errors = Vital.objects.validate_vitals(request.POST)
        if errors:
            for msg in errors.values():
                messages.error(request, msg)
            return redirect('patient_detail', patient_id=patient_id)

        Vital.objects.create(
            patient=patient,
            blood_pressure=request.POST['blood_pressure'],
            heart_rate=request.POST['heart_rate'],
            temperature=request.POST['temperature'],
            oxygen_saturation=request.POST['oxygen_saturation']
        )
        messages.success(request, "Vital signs added successfully.")
        return redirect('patient_detail', patient_id=patient_id)

    return redirect('patient_detail', patient_id=patient_id)

def vitals_api(request, patient_id):
    if 'user_id' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    from .models import Vital, Patient

    
    try:
        patient = Patient.objects.get(id=patient_id, created_by_id=request.session['user_id'])
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found or unauthorized'}, status=404)

    vitals = Vital.objects.filter(patient=patient).values(
        'blood_pressure', 'heart_rate', 'temperature', 'oxygen_saturation', 'recorded_at'
    ).order_by('-recorded_at')

    return JsonResponse(list(vitals), safe=False)