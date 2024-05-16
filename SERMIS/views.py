from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Beneficiary
from django.urls import reverse
from .models import SEMCMentoringCoaching, SEMCCommunityParticipation, SEMCSBCC, SPGFA, SPNutricashDetails, SPSAGEdetails, LPDOnFarm, LPDOffFarm, LPDNonFarm, FinlitBeneficiary, FinLitDetails, NutricashBeneficiary, SAGEBeneficiary
from .forms import GroupForm, BeneficiaryForm, NutricashBeneficiaryForm,  SEMCMentoringCoachingForm, SEMCCommunityParticipationForm, SEMCSBCCForm, SPGFAForm, SPNutricashForm, FinlitBeneficiaryForm, FinlitDetailsForm, SAGEBeneficiaryForm, SPSAGEForm, LPDOnFarmForm, LPDOffFarmForm, LPDNonFarmForm
from django.apps import apps
from django.http import JsonResponse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files.base import ContentFile
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime



# Group Views--------------------------------------------------------------------------
@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    beneficiaries = group.beneficiary_set.order_by('-created_at')  # Order by creation date in descending order
    # beneficiaries = group.get_beneficiaries()

    group_create_url = reverse('group_create')
   
    return render(request, 'group_detail.html', {'group': group, 'group_create': group_create, 'beneficiaries': beneficiaries})


@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.total_members_count = 0
            group.male_members_count = 0
            group.female_members_count = 0
            group.num_refugees_count = 0
            group.male_refugees_count = 0
            group.female_refugees_count = 0
            group.num_youth_count = 0
            group.male_youth_count = 0
            group.female_youth_count = 0
            group.num_disabilities_count = 0
            group.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'group_form.html', {'form': form})
# @login_required
# def group_create(request):
#     if request.method == 'POST':
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             group = form.save()
#             return redirect('group_list')
#     else:
#         form = GroupForm()
#     return render(request, 'group_form.html', {'form': form})


@login_required
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_detail', pk=pk)
    else:
        form = GroupForm(instance=group)
    return render(request, 'group_form.html', {'form': form})


@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'group_confirm_delete.html', {'group': group})

# Beneficiary Views-----------------------------------------------------------------
@login_required
def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'beneficiary_list.html', {'beneficiaries': beneficiaries})


@login_required
def beneficiary_detail(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    group = beneficiary.group 
    # nutricash_beneficiaries = NutricashBeneficiary.objects.filter(group_representative=beneficiary)
    nutricash_beneficiaries = NutricashBeneficiary.objects.filter(group_representative=beneficiary)

    sage_beneficiaries = SAGEBeneficiary.objects.filter(group_representative=beneficiary)
    finlit_beneficiaries = FinlitBeneficiary.objects.filter(group_representative=beneficiary)
    
    print("Beneficiary Object:", beneficiary)
    semcmentoringcoaching_details = SEMCMentoringCoaching.objects.filter(beneficiary=beneficiary)
    semccommunityparticipation_details = SEMCCommunityParticipation.objects.filter(beneficiary=beneficiary)
    semcsbcc_details = SEMCSBCC.objects.filter(beneficiary=beneficiary)
    spgfa_details = SPGFA.objects.filter(beneficiary=beneficiary)
    # spnutricash_details = SPNutricash.objects.filter(nutricash_beneficiary=nutricash_beneficiary)
    spsage_details = SPSAGEdetails.objects.filter(name_of_participant=beneficiary)
    lpdonfarm_details = LPDOnFarm.objects.filter(name_of_participant=beneficiary)
    lpdofffarm_details = LPDOffFarm.objects.filter(name_of_participant=beneficiary)
    lpdnonfarm_details = LPDNonFarm.objects.filter(name_of_participant=beneficiary)
    finlit_details = FinLitDetails.objects.filter(group_representative=beneficiary)
    # nutricashbeneficiary_details = NutricashBeneficiary.objects.filter(group_representative=beneficiary)
    
   
    
    return render(
        request, 'beneficiary_detail.html', {'beneficiary': beneficiary,
                                            'semcmentoringcoaching_details': semcmentoringcoaching_details,
                                            'semccommunityparticipation_details': semccommunityparticipation_details,
                                            'semcsbcc_details': semcsbcc_details,
                                            'spgfa_details': spgfa_details,
                                            # 'spnutricash_details': spnutricash_details,
                                            'spsage_details': spsage_details,
                                            'lpdonfarm_details': lpdonfarm_details,
                                            'lpdofffarm_details': lpdofffarm_details,
                                            'lpdnonfarm_details': lpdnonfarm_details,
                                            'finlit_details': finlit_details,
                                            # 'nutricashbeneficiary_details': nutricashbeneficiary_details,
                                            'nutricash_beneficiaries': nutricash_beneficiaries,
                                            'sage_beneficiaries': sage_beneficiaries,
                                            'finlit_beneficiaries': finlit_beneficiaries                                           

                                              }
        )
@login_required
def beneficiary_create(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)

        if form.is_valid():
            beneficiary = form.save(commit=False)
            beneficiary.group = group
            beneficiary.save()

            return redirect('group_detail', pk=pk)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = BeneficiaryForm()

    return render(request, 'beneficiary_form.html', {'form': form})

# def beneficiary_create(request, pk):
#     group = get_object_or_404(Group, pk=pk)

#     if request.method == 'POST':
#         form = BeneficiaryForm(request.POST, request.FILES)

#         # Proceed with form processing if image data is not present
#         if form.is_valid():
#             # Access the captured image data
#             webimg_data = request.POST.get('webimg')
            
#             # Convert base64 image data to a file and associate it with the form
#             if webimg_data:
#                 format, imgstr = webimg_data.split(';base64,') 
#                 ext = format.split('/')[-1]

#                 # Create a ContentFile from the base64 data
#                 image_data = ContentFile(base64.b64decode(imgstr), name=f'webimg.{ext}')

#                 # Associate the image data with the form
#                 #form.cleaned_data['participant_photo'] = image_data
#                 form.instance.participant_photo = image_data

#             beneficiary = form.save(commit=False)
#             beneficiary.group = group
#             beneficiary.save()

#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'errors': form.errors})
#     else:
#         form = BeneficiaryForm()

#     return render(request, 'beneficiary_form.html', {'form': form})

@login_required
def beneficiary_update(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=beneficiary)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=pk)
    else:
        form = BeneficiaryForm(instance=beneficiary)
    return render(request, 'beneficiary_form.html', {'form': form})

@login_required
def beneficiary_delete(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    if request.method == 'POST':
        group_pk = beneficiary.group.pk
        beneficiary.delete()  
        return redirect('group_detail', pk=group_pk)
    return render(request, 'delete_confirmation.html', {'beneficiary': beneficiary})


@login_required
def get_record_counts(request, beneficiary_id):
    # Fetch the counts for each model instance
    semc_mentoring_count = SEMCMentoringCoaching.objects.filter(pk=beneficiary_id).count()
    semc_community_count = SEMCCommunityParticipation.objects.filter(pk=beneficiary_id).count()
    semc_sbcc_count = SEMCSBCC.objects.filter(pk=beneficiary_id).count()

    # Calculate the total count by summing the individual counts
    total_count = semc_mentoring_count + semc_community_count + semc_sbcc_count

    # Create a JSON response with the total count
    data = {
        'total_count': total_count,
    }
    
    return JsonResponse(data)










# SEMCCommunityParticipation--------------------------------------------------------------

@login_required
def semccommunityparticipation_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = SEMCCommunityParticipationForm(request.POST)
        if form.is_valid():
            semccommunityparticipation = form.save(commit=False)
            semccommunityparticipation.district = beneficiary  # Set district           
            semccommunityparticipation.group = beneficiary  
            semccommunityparticipation.region = beneficiary  # Set region
            semccommunityparticipation.settlement = beneficiary # Set settlement
            semccommunityparticipation.actual_group = beneficiary.nationality  # Set actual_nationality
            semccommunityparticipation.actual_region = beneficiary.region  # Set actual_region
            semccommunityparticipation.actual_district = beneficiary.district  # Set actual_district
            semccommunityparticipation.actual_settlement = beneficiary.settlement 
            semccommunityparticipation.beneficiary = beneficiary
            semccommunityparticipation.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = SEMCCommunityParticipationForm()

    return render(request, 'semccommunityparticipation_form.html', {'form': form})

@login_required
def semccommunityparticipation_update(request, pk):
    semccommunityparticipation = get_object_or_404(SEMCCommunityParticipation, pk=pk)
    
    if request.method == 'POST':
        form = SEMCCommunityParticipationForm(request.POST, instance=semccommunityparticipation)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=semccommunityparticipation.beneficiary.pk)
    else:
        form = SEMCCommunityParticipationForm(instance=semccommunityparticipation)

    return render(request, 'semccommunityparticipation_form.html', {'form': form})

@login_required
def semccommunityparticipation_delete(request, pk):
    semccommunityparticipation = get_object_or_404(SEMCCommunityParticipation, pk=pk)
    beneficiary_pk = semccommunityparticipation.beneficiary.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        semccommunityparticipation.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'semccommunityparticipation_delete.html', {'beneficiary_pk': beneficiary_pk})

# SEMCSBCC Views------------------------------------------------------------------------------
@login_required
def semcsbcc_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = SEMCSBCCForm(request.POST)
        if form.is_valid():
            semcsbcc = form.save(commit=False)
            semcsbcc.beneficiary = beneficiary
            semcsbcc.district = beneficiary  # Set district           
            semcsbcc.group = beneficiary  
            semcsbcc.region = beneficiary  # Set region
            semcsbcc.settlement = beneficiary # Set settlement
            semcsbcc.actual_group = beneficiary.nationality  # Set actual_nationality
            semcsbcc.actual_region = beneficiary.region  # Set actual_region
            semcsbcc.actual_district = beneficiary.district  # Set actual_district
            semcsbcc.actual_settlement = beneficiary.settlement 
            semcsbcc.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = SEMCSBCCForm()

    return render(request, 'semcsbcc_form.html', {'form': form})

@login_required
def semcsbcc_update(request, pk):
    semcsbcc = get_object_or_404(SEMCSBCC, pk=pk)
    
    if request.method == 'POST':
        form = SEMCSBCCForm(request.POST, instance=semcsbcc)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=semcsbcc.beneficiary.pk)
    else:
        form = SEMCSBCCForm(instance=semcsbcc)

    return render(request, 'semcsbcc_form.html', {'form': form})

@login_required
def semcsbcc_delete(request, pk):
    semcsbcc = get_object_or_404(SEMCSBCC, pk=pk)
    beneficiary_pk = semcsbcc.beneficiary.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        semcsbcc.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'semcsbcc_delete.html', {'beneficiary_pk': beneficiary_pk})




# SEMCMentoringCoaching Views-----------------------------------------------------------------
@login_required
def semc_mentoring_coaching_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = SEMCMentoringCoachingForm(request.POST)
        if form.is_valid():
            semc_mentoring_coaching = form.save(commit=False)
            semc_mentoring_coaching.beneficiary = beneficiary
            semc_mentoring_coaching.district = beneficiary  # Set district           
            semc_mentoring_coaching.group = beneficiary  
            semc_mentoring_coaching.region = beneficiary  # Set region
            semc_mentoring_coaching.settlement = beneficiary # Set settlement
            semc_mentoring_coaching.actual_group = beneficiary.nationality  # Set actual_nationality
            semc_mentoring_coaching.actual_region = beneficiary.region  # Set actual_region
            semc_mentoring_coaching.actual_district = beneficiary.district  # Set actual_district
            semc_mentoring_coaching.actual_settlement = beneficiary.settlement  # Set actual_settlement
     
            semc_mentoring_coaching.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = SEMCMentoringCoachingForm()

    return render(request, 'semc_mentoring_coaching_form.html', {'form': form})

@login_required
def semc_mentoring_coaching_update(request, pk):
    semc_mentoring_coaching = get_object_or_404(SEMCMentoringCoaching, pk=pk)
    
    if request.method == 'POST':
        form = SEMCMentoringCoachingForm(request.POST, instance=semc_mentoring_coaching)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=semc_mentoring_coaching.beneficiary.pk)
    else:
        form = SEMCMentoringCoachingForm(instance=semc_mentoring_coaching)

    return render(request, 'semc_mentoring_coaching_form.html', {'form': form})

@login_required
def semc_mentoring_coaching_delete(request, pk):
    semc_mentoring_coaching = get_object_or_404(SEMCMentoringCoaching, pk=pk)
    beneficiary_pk = semc_mentoring_coaching.beneficiary.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        semc_mentoring_coaching.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'semc_mentoring_coaching_delete.html', {'beneficiary_pk': beneficiary_pk})

#SPGFA views-----------------------------------------------------------------------------------------------

@login_required
def spgfa_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = SPGFAForm(request.POST)
        if form.is_valid():
            spgfa = form.save(commit=False)
            spgfa.beneficiary = beneficiary
            spgfa.group = beneficiary 
            spgfa.district = beneficiary  # Set district           
            spgfa.nationality = beneficiary  
            spgfa.region = beneficiary  # Set region
            spgfa.settlement = beneficiary # Set settlement
            spgfa.actual_nationality = beneficiary.nationality  # Set actual_nationality
            spgfa.actual_group = beneficiary.group
            spgfa.actual_region = beneficiary.region  # Set actual_region
            spgfa.actual_district = beneficiary.district  # Set actual_district
            spgfa.actual_settlement = beneficiary.settlement 





            spgfa.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = SPGFAForm()

    return render(request, 'spgfa_form.html', {'form': form})

@login_required
def spgfa_update(request, pk):
    spgfa = get_object_or_404(SPGFA, pk=pk)
    
    if request.method == 'POST':
        form = SPGFAForm(request.POST, instance=spgfa)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=spgfa.beneficiary.pk)
    else:
        form = SPGFAForm(instance=spgfa)

    return render(request, 'spgfa_form.html', {'form': form})

@login_required
def spgfa_delete(request, pk):
    spgfa = get_object_or_404(SPGFA, pk=pk)
    beneficiary_pk = spgfa.beneficiary.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        spgfa.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'spgfa_delete.html', {'beneficiary_pk': beneficiary_pk})


#Nutricash Beneficiary views-----------------------------------------------------------------------------------------------


# def add_nutricash_beneficiary(request, pk):
#     beneficiary = get_object_or_404(Beneficiary, pk=pk)
    
#     if request.method == 'POST':
#         form = NutricashBeneficiaryForm(request.POST)
#         if form.is_valid():
#             nutricash_beneficiary = form.save(commit=False)
#             nutricash_beneficiary.group_representative_id = beneficiary.pk
#             nutricash_beneficiary.save()
#             return redirect('beneficiary_detail', pk=beneficiary.pk)
#     else:
#         form = NutricashBeneficiaryForm()
    
#     return render(request, 'add_nutricash_beneficiary.html', {'form': form})
def add_nutricash_beneficiary(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    
    if request.method == 'POST':
        form = NutricashBeneficiaryForm(request.POST)
        if form.is_valid():
            nutricash_beneficiary = form.save(commit=False)
            nutricash_beneficiary.group_representative = beneficiary
            nutricash_beneficiary.region = beneficiary
            nutricash_beneficiary.district = beneficiary
            nutricash_beneficiary.settlement = beneficiary
            nutricash_beneficiary.nationality = beneficiary
            nutricash_beneficiary.actual_region = beneficiary.region
            nutricash_beneficiary.actual_district = beneficiary.district 
            nutricash_beneficiary.actual_settlement= beneficiary.district 
            nutricash_beneficiary.actual_nationality = beneficiary.nationality
            
            nutricash_beneficiary.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        initial_data = {
            'region': beneficiary.region,
            'district': beneficiary.district,
            'settlement': beneficiary.settlement,
            'nationality': beneficiary.nationality,
            'group_representative': beneficiary
        }
        form = NutricashBeneficiaryForm(initial=initial_data)
    
    return render(request, 'add_nutricash_beneficiary.html', {'form': form})

def nutricashbeneficiary_detail(request, pk):
    nutricashbeneficiary = get_object_or_404(NutricashBeneficiary, pk=pk)
    spnutricash_details = nutricashbeneficiary.nutricash_beneficiaryname.all()
    return render(request, 'nutricashbeneficiary_detail.html', {'nutricashbeneficiary': nutricashbeneficiary, 'spnutricash_details': spnutricash_details})

def nutricashbeneficiary_delete(request, pk):
    nutricashbeneficiary = get_object_or_404(NutricashBeneficiary, pk=pk)

    if request.method == 'POST':
        # Get the related beneficiary's pk
        beneficiary_pk = nutricashbeneficiary.group_representative.pk

        # Delete the nutricashbeneficiary
        nutricashbeneficiary.delete()

        # Redirect to beneficiary_detail with the beneficiary's pk
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        # return render(request, 'beneficiary_detail.html', {'nutricashbeneficiary': nutricashbeneficiary})
        return render(request, 'delete_confirmation.html', {'nutricashbeneficiary': nutricashbeneficiary})


@login_required
def nutricashbeneficiary_update(request, pk):
    nutricashbeneficiary = get_object_or_404(NutricashBeneficiary, pk=pk)
    beneficiary = nutricashbeneficiary.group_representative 
    
    if request.method == 'POST':
        form = NutricashBeneficiaryForm(request.POST, instance=nutricashbeneficiary)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = NutricashBeneficiaryForm(instance=nutricashbeneficiary)
    return render(request, 'add_nutricash_beneficiary.html', {'form': form})


#NUTRICASH DETAILS------------------------------------------------------------------

@login_required
def spnutricash_create(request, pk):
    nutricash_beneficiary = get_object_or_404(NutricashBeneficiary, pk=pk)
    beneficiary = nutricash_beneficiary.group_representative 

# Check if the exit_date has been exceeded
    if nutricash_beneficiary.exit_date is not None and timezone.now() > datetime.combine(nutricash_beneficiary.exit_date, datetime.min.time()).replace(tzinfo=timezone.get_current_timezone()):
        nutricash_beneficiary.beneficiary_status = 'Exited'
        nutricash_beneficiary.save()  # Save the updated status
        return HttpResponse("The exit date has been exceeded. The beneficiary is no longer eligible for assistance.")
        
    if request.method == 'POST':
        form = SPNutricashForm(request.POST)
        if form.is_valid():
            spnutricash = form.save(commit=False)
            spnutricash.nutricash_beneficiary_name = nutricash_beneficiary
            spnutricash.group_representative = nutricash_beneficiary.group_representative  # Set group_representative
            spnutricash.ID_number = nutricash_beneficiary # Set ID_number
            spnutricash.ID_type = nutricash_beneficiary # Set ID_type
            spnutricash.district = nutricash_beneficiary # Set district
            spnutricash.nationality = nutricash_beneficiary  # Set nationality
            spnutricash.region = nutricash_beneficiary  # Set region
            spnutricash.settlement = nutricash_beneficiary  # Set settlement
            spnutricash.actual_nationality = beneficiary.nationality  # Set actual_nationality
            spnutricash.actual_region = beneficiary.region  # Set actual_region
            spnutricash.actual_district = beneficiary.district  # Set actual_district
            spnutricash.actual_settlement = beneficiary.settlement  # Set actual_settlement
            spnutricash.actual_ID_type = nutricash_beneficiary.ID_type  # Set actual_ID_type
            spnutricash.actual_ID_number = nutricash_beneficiary.ID_number  # Set actual_ID_number

            spnutricash.save()
            return redirect('nutricashbeneficiary_detail', pk=nutricash_beneficiary.pk)
    else:
        form = SPNutricashForm()

    return render(request, 'spnutricash_form.html', {'form': form})



@login_required
def spnutricash_details(request, pk):
    nutricashbeneficiary = get_object_or_404(NutricashBeneficiary, pk=pk)
    spnutricash_details = nutricashbeneficiary.spnutricashdetails_set.all()
    return render(request, 'nutricashbeneficiary_detail.html', {'nutricashbeneficiary': nutricashbeneficiary, 'spnutricash_details': spnutricash_details})


@login_required
def spnutricash_update(request, pk):
    spnutricash = get_object_or_404(SPNutricashDetails, pk=pk)

    if request.method == 'POST':
        form = SPNutricashForm(request.POST, instance=spnutricash)
        if form.is_valid():
            form.save()
            # Check if the related beneficiary exists before redirecting
            if spnutricash.nutricash_beneficiary_name:
                return redirect('nutricashbeneficiary_detail', pk=spnutricash.nutricash_beneficiary_name.pk)
            else:

                messages.error(request, 'No related beneficiary found in database')
    else:
        form = SPNutricashForm(instance=spnutricash)

    return render(request, 'spnutricash_form.html', {'form': form})

@login_required
def spnutricash_delete(request, pk):
    spnutricash = get_object_or_404(SPNutricashDetails, pk=pk)
    nutricash_beneficiary_pk = spnutricash.nutricash_beneficiary_name.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        spnutricash.delete()
        return redirect('nutricashbeneficiary_detail', pk=nutricash_beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'spnutricash_delete.html', {'nutricash_beneficiary_pk': nutricash_beneficiary_pk})


#SAGEbeneficiary viewa-------------------------------------------------------------------------------------
@login_required
def add_sage_beneficiary(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    
    if request.method == 'POST':
        form = SAGEBeneficiaryForm(request.POST)
        if form.is_valid():
            sage_beneficiary = form.save(commit=False)
            sage_beneficiary.group_representative = beneficiary
            sage_beneficiary.region = beneficiary
            sage_beneficiary.district = beneficiary
            sage_beneficiary.settlement = beneficiary
            sage_beneficiary.nationality = beneficiary
            sage_beneficiary.household_id = beneficiary
            sage_beneficiary.actual_region = beneficiary.region
            sage_beneficiary.actual_district = beneficiary.district 
            sage_beneficiary.actual_settlement= beneficiary.district 
            sage_beneficiary.actual_nationality = beneficiary.nationality

            
            sage_beneficiary .save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        initial_data = {
            'region': beneficiary.region,
            'district': beneficiary.district,
            'settlement': beneficiary.settlement,
            'nationality': beneficiary.nationality,
            'group_representative': beneficiary
        }
        form = SAGEBeneficiaryForm(initial=initial_data)
    
    return render(request, 'add_sage_beneficiary.html', {'form': form})

@login_required
def sagebeneficiary_detail(request, pk):
    sagebeneficiary = get_object_or_404(SAGEBeneficiary, pk=pk)
    sagebeneficiary_details = sagebeneficiary.sage_beneficiary.all()
    return render(request, 'sage_beneficiary_detail.html', {'sagebeneficiary': sagebeneficiary, 'sagebeneficiary_details': sagebeneficiary_details})


@login_required
def sagebeneficiary_delete(request, pk):
    sagebeneficiary = get_object_or_404(SAGEBeneficiary, pk=pk)

    if request.method == 'POST':
        # Get the related beneficiary's pk
        beneficiary_pk = sagebeneficiary.group_representative.pk

        # Delete the nutricashbeneficiary
        sagebeneficiary.delete()

        # Redirect to beneficiary_detail with the beneficiary's pk
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        # return render(request, 'beneficiary_detail.html', {'nutricashbeneficiary': nutricashbeneficiary})
        return render(request, 'delete_confirmation.html', {'sagebeneficiary': sagebeneficiary})


@login_required
def sagebeneficiary_update(request, pk):
    sagebeneficiary = get_object_or_404(SAGEBeneficiary, pk=pk)
    beneficiary = sagebeneficiary.group_representative 
    
    if request.method == 'POST':
        form = SAGEBeneficiaryForm(request.POST, instance=sagebeneficiary)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = SAGEBeneficiaryForm(instance=sagebeneficiary)
    return render(request, 'add_sage_beneficiary.html', {'form': form})









#SPSAGE Deatils views-----------------------------------------------------------------------------------------------

@login_required
def spsage_create(request, pk):
    sagebeneficiary = get_object_or_404(SAGEBeneficiary, pk=pk)
    beneficiary = sagebeneficiary.group_representative

    if request.method == 'POST':
        form = SPSAGEForm(request.POST)
        if form.is_valid():
            spsage = form.save(commit=False)

            spsage.sage_beneficiary_name = sagebeneficiary
            spsage.name_of_participant = sagebeneficiary.group_representative  # Set group_representative
            spsage.ID_type = sagebeneficiary 
            spsage.ID_number = sagebeneficiary  # Set ID_number
            spsage.candidate_individual_id = sagebeneficiary  # Set ID_type
            spsage.district = beneficiary  # Set district           
            spsage.nationality = beneficiary  
            spsage.region = beneficiary  # Set region
            spsage.settlement = beneficiary # Set settlement
            spsage.actual_nationality = beneficiary.nationality  # Set actual_nationality
            spsage.actual_region = beneficiary.region  # Set actual_region
            spsage.actual_district = beneficiary.district  # Set actual_district
            spsage.actual_settlement = beneficiary.settlement  # Set actual_settlement
            spsage.actual_ID_type = sagebeneficiary.ID_type  # Set actual_ID_type
            spsage.actual_candidate_individual_id = sagebeneficiary.candidate_individual_id
            spsage.sage_beneficiary_dob = sagebeneficiary
            spsage.sagebeneficiary = sagebeneficiary
            spsage.save()
            return redirect('sagebeneficiary_detail', pk=sagebeneficiary.pk)
    else:
        form = SPSAGEForm()

    return render(request, 'spsage_form.html', {'form': form})

@login_required
def spsage_update(request, pk):
    spsage = get_object_or_404(SPSAGEdetails, pk=pk)
    
    if request.method == 'POST':
        form = SPSAGEForm(request.POST, instance=spsage)
        if form.is_valid():
            form.save()
            return redirect('sagebeneficiary_detail', pk=spsage.sage_beneficiary_name.pk)
    else:
        form = SPSAGEForm(instance=spsage)

    return render(request, 'spsage_form.html', {'form': form})

@login_required
def spsage_delete(request, pk):
    spsage = get_object_or_404(SPSAGEdetails, pk=pk)

    if request.method == 'POST':
       
        spsage.delete()
        return redirect('sagebeneficiary_detail', pk=spsage.sage_beneficiary_name.pk)

    else:
        # Display the confirmation page
        return render(request, 'spsage_delete.html', {'spsage': spsage})
    





#Finlit beneficiary views-------------------------------------------------------------------------------------
@login_required
def add_finlit_beneficiary(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    
    if request.method == 'POST':
        form = FinlitBeneficiaryForm(request.POST)
        if form.is_valid():
            finlit_beneficiary = form.save(commit=False)
            finlit_beneficiary.group_representative = beneficiary
            finlit_beneficiary.region = beneficiary
            finlit_beneficiary.district = beneficiary
            finlit_beneficiary.settlement = beneficiary
            finlit_beneficiary.nationality = beneficiary
            finlit_beneficiary.household_id = beneficiary
            finlit_beneficiary.actual_region = beneficiary.region
            finlit_beneficiary.actual_district = beneficiary.district 
            finlit_beneficiary.actual_settlement= beneficiary.district 
            finlit_beneficiary.actual_nationality = beneficiary.nationality

            
            finlit_beneficiary.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        initial_data = {
            'region': beneficiary.region,
            'district': beneficiary.district,
            'settlement': beneficiary.settlement,
            'nationality': beneficiary.nationality,
            'group_representative': beneficiary
        }
        form = FinlitBeneficiaryForm(initial=initial_data)
    
    return render(request, 'add_finlit_beneficiary.html', {'form': form})

@login_required
def finlitbeneficiary_detail(request, pk):
    finlitbeneficiary = get_object_or_404(FinlitBeneficiary, pk=pk)
    finlitbeneficiary_details = finlitbeneficiary.finlit_candidate.all()
    return render(request, 'finlit_beneficiary_detail.html', {'finlitbeneficiary': finlitbeneficiary, 'finlitbeneficiary_details': finlitbeneficiary_details})


@login_required
def finlitbeneficiary_delete(request, pk):
    finlitbeneficiary = get_object_or_404(FinlitBeneficiary, pk=pk)

    if request.method == 'POST':
        # Get the related beneficiary's pk
        beneficiary_pk = finlitbeneficiary.group_representative.pk

        # Delete the nutricashbeneficiary
        finlitbeneficiary.delete()

        # Redirect to beneficiary_detail with the beneficiary's pk
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        # return render(request, 'beneficiary_detail.html', {'nutricashbeneficiary': nutricashbeneficiary})
        return render(request, 'delete_confirmation.html', {'finlitbeneficiary': finlitbeneficiary})


@login_required
def finlitbeneficiary_update(request, pk):
    finlitbeneficiary = get_object_or_404(FinlitBeneficiary, pk=pk)
    beneficiary = finlitbeneficiary.group_representative 
    
    if request.method == 'POST':
        form = FinlitBeneficiaryForm(request.POST, instance=finlitbeneficiary)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = FinlitBeneficiaryForm(instance=finlitbeneficiary)
    return render(request, 'add_finlit_beneficiary.html', {'form': form})




#FinLit Details views-----------------------------------------------------------------------------------------------

@login_required
def finlit_details_create(request, pk):
    finlitbeneficiary = get_object_or_404(FinlitBeneficiary, pk=pk)
    beneficiary = finlitbeneficiary.group_representative

    if request.method == 'POST':
        form = FinlitDetailsForm(request.POST)
        if form.is_valid():
            finlit = form.save(commit=False)

            finlit.finlit_candidate_name = finlitbeneficiary
            finlit.group_representative = finlitbeneficiary.group_representative  # Set group_representative


            finlit.district = finlitbeneficiary  # Set district           
            finlit.nationality = finlitbeneficiary  
            finlit.region = finlitbeneficiary  # Set region
            finlit.settlement = finlitbeneficiary # Set settlement
            finlit.actual_nationality = beneficiary.nationality  # Set actual_nationality
            finlit.actual_region = beneficiary.region  # Set actual_region
            finlit.actual_district = beneficiary.district  # Set actual_district
            finlit.actual_settlement = beneficiary.settlement  # Set actual_settlement
            finlit.finlitbeneficiary = finlitbeneficiary
            finlit.save()
            return redirect('finlitbeneficiary_detail', pk=finlitbeneficiary.pk)
    else:
        form = FinlitDetailsForm()

    return render(request, 'finlit_details_form.html', {'form': form})

@login_required
def finlit_details_update(request, pk):
    finlit = get_object_or_404(FinLitDetails, pk=pk)
    
    if request.method == 'POST':
        form = FinlitDetailsForm(request.POST, instance=finlit)
        if form.is_valid():
            form.save()
            return redirect('finlitbeneficiary_detail', pk=finlit.finlit_candidate_name.pk)
    else:
        form = FinlitDetailsForm(instance=finlit)

    return render(request, 'finlit_details_form.html', {'form': form})

@login_required
def finlit_details_delete(request, pk):
    finlit = get_object_or_404(FinLitDetails, pk=pk)

    if request.method == 'POST':
       
        finlit.delete()
        return redirect('finlit_beneficiary_detail', pk=finlit.finlit_candidate_name.p)

    else:
        # Display the confirmation page
        return render(request, 'finlit_details_delete.html', {'finlit': finlit})




















#LPDOnFarm views-----------------------------------------------------------------------------------------------
@login_required
def lpdonfarm_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = LPDOnFarmForm(request.POST)
        if form.is_valid():
            lpdonfarm = form.save(commit=False)
            lpdonfarm.beneficiary = beneficiary
            lpdonfarm.district = beneficiary  # Set district           
            lpdonfarm.group = beneficiary  
            lpdonfarm.region = beneficiary  # Set region
            lpdonfarm.settlement = beneficiary # Set settlement
            lpdonfarm.actual_group = beneficiary.group  # Set actual_nationality
            lpdonfarm.actual_region = beneficiary.region  # Set actual_region
            lpdonfarm.actual_district = beneficiary.district  # Set actual_district
            lpdonfarm.actual_settlement = beneficiary.settlement 
            lpdonfarm.name_of_participant = beneficiary
            lpdonfarm.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = LPDOnFarmForm()

    return render(request, 'lpdonfarm_form.html', {'form': form})

@login_required
def lpdonfarm_update(request, pk):
    lpdonfarm = get_object_or_404(LPDOnFarm, pk=pk)
    
    if request.method == 'POST':
        form = LPDOnFarmForm(request.POST, instance=lpdonfarm)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=lpdonfarm.name_of_participant.pk)
    else:
        form = LPDOnFarmForm(instance=lpdonfarm)

    return render(request, 'lpdonfarm_form.html', {'form': form})

@login_required
def lpdonfarm_delete(request, pk):
    lpdonfarm = get_object_or_404(LPDOnFarm, pk=pk)
    beneficiary_pk = lpdonfarm.name_of_participant.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        lpdonfarm.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'lpdonfarm_delete.html', {'beneficiary_pk': beneficiary_pk})
    
#LPDOffFarm views-----------------------------------------------------------------------------------------------
@login_required
def lpdofffarm_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = LPDOffFarmForm(request.POST)
        if form.is_valid():
            lpdofffarm = form.save(commit=False)
            lpdofffarm.beneficiary = beneficiary
            lpdofffarm.district = beneficiary  # Set district           
            lpdofffarm.group = beneficiary  
            lpdofffarm.region = beneficiary  # Set region
            lpdofffarm.settlement = beneficiary # Set settlement
            lpdofffarm.actual_group = beneficiary.group  # Set actual_nationality
            lpdofffarm.actual_region = beneficiary.region  # Set actual_region
            lpdofffarm.actual_district = beneficiary.district  # Set actual_district
            lpdofffarm.actual_settlement = beneficiary.settlement 
            lpdofffarm.name_of_participant = beneficiary
            lpdofffarm.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = LPDOffFarmForm()

    return render(request, 'lpdofffarm_form.html', {'form': form})

@login_required
def lpdofffarm_update(request, pk):
    lpdofffarm = get_object_or_404(LPDOffFarm, pk=pk)
    
    if request.method == 'POST':
        form = LPDOffFarmForm(request.POST, instance=lpdofffarm)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=lpdofffarm.name_of_participant.pk)
    else:
        form = LPDOffFarmForm(instance=lpdofffarm)

    return render(request, 'lpdofffarm_form.html', {'form': form})

@login_required
def lpdofffarm_delete(request, pk):
    lpdofffarm = get_object_or_404(LPDOffFarm, pk=pk)
    beneficiary_pk = lpdofffarm.name_of_participant.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        lpdofffarm.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'lpdofffarm_delete.html', {'beneficiary_pk': beneficiary_pk})


#LPDNonFarm views-----------------------------------------------------------------------------------------------
@login_required
def lpdnonfarm_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = LPDNonFarmForm(request.POST)
        if form.is_valid():
            lpdnonfarm = form.save(commit=False)
            lpdnonfarm.beneficiary = beneficiary
            lpdnonfarm.district = beneficiary  # Set district           
            lpdnonfarm.group = beneficiary  
            lpdnonfarm.region = beneficiary  # Set region
            lpdnonfarm.settlement = beneficiary # Set settlement
            lpdnonfarm.actual_group = beneficiary.group  # Set actual_nationality
            lpdnonfarm.actual_region = beneficiary.region  # Set actual_region
            lpdnonfarm.actual_district = beneficiary.district  # Set actual_district
            lpdnonfarm.actual_settlement = beneficiary.settlement 
            lpdnonfarm.name_of_participant = beneficiary
            lpdnonfarm.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = LPDNonFarmForm()

    return render(request, 'lpdnonfarm_form.html', {'form': form})

@login_required
def lpdnonfarm_update(request, pk):
    lpdnonfarm = get_object_or_404(LPDNonFarm, pk=pk)
    
    if request.method == 'POST':
        form = LPDNonFarmForm(request.POST, instance=lpdnonfarm)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=lpdnonfarm.name_of_participant.pk)
    else:
        form = LPDNonFarmForm(instance=lpdnonfarm)

    return render(request, 'lpdnonfarm_form.html', {'form': form})

@login_required
def lpdnonfarm_delete(request, pk):
    lpdnonfarm = get_object_or_404(LPDNonFarm, pk=pk)
    beneficiary_pk = lpdnonfarm.name_of_participant.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        lpdnonfarm.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'lpdnonfarm_delete.html', {'beneficiary_pk': beneficiary_pk})


# #DFI views-----------------------------------------------------------------------------------------------
# @login_required
# def dfi_create(request, pk):
#     beneficiary = get_object_or_404(Beneficiary, pk=pk)

#     if request.method == 'POST':
#         form = DFIForm(request.POST)
#         if form.is_valid():
#             dfi = form.save(commit=False)
#             dfi.beneficiary = beneficiary
#             dfi.save()
#             return redirect('beneficiary_detail', pk=beneficiary.pk)
#     else:
#         form = DFIForm()

#     return render(request, 'dfi_form.html', {'form': form})

# @login_required
# def dfi_update(request, pk):
#     dfi = get_object_or_404(DFI, pk=pk)
    
#     if request.method == 'POST':
#         form = DFIForm(request.POST, instance=dfi)
#         if form.is_valid():
#             form.save()
#             return redirect('beneficiary_detail', pk=dfi.beneficiary.pk)
#     else:
#         form = DFIForm(instance=dfi)

#     return render(request, 'dfi_form.html', {'form': form})

# @login_required
# def dfi_delete(request, pk):
#     dfi = get_object_or_404(DFI, pk=pk)
#     beneficiary_pk = dfi.beneficiary.pk

#     if request.method == 'POST':
#         # Handle the confirmation of deletion
#         dfi.delete()
#         return redirect('beneficiary_detail', pk=beneficiary_pk)
#     else:
#         # Display the confirmation page
#         return render(request, 'dfi_delete.html', {'beneficiary_pk': beneficiary_pk})
    



def custom_logout(request):
    logout(request)
    return redirect(reverse('login'))  # 'login' is the name of the login URL


