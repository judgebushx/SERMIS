from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Beneficiary
from django.urls import reverse
from .models import SEMCMentoringCoaching, SEMCCommunityParticipation, SEMCSBCC, SPGFA, SPNutricash, SPSAGE, LPDOnFarm, LPDOffFarm, LPDNonFarm, DFI
from .forms import GroupForm, BeneficiaryForm, SEMCMentoringCoachingForm, SEMCCommunityParticipationForm, SEMCSBCCForm, SPGFAForm, SPNutricashForm, SPSAGEForm, LPDOnFarmForm, LPDOffFarmForm, LPDNonFarmForm, DFIForm
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





# Group Views--------------------------------------------------------------------------
@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    beneficiaries = group.get_beneficiaries()

    group_create_url = reverse('group_create')
   
    return render(request, 'group_detail.html', {'group': group, 'group_create': group_create, 'beneficiaries': beneficiaries})


@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'group_form.html', {'form': form})


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
    semcmentoringcoaching_details = SEMCMentoringCoaching.objects.filter(beneficiary=beneficiary)
    semccommunityparticipation_details = SEMCCommunityParticipation.objects.filter(beneficiary=beneficiary)
    semcsbcc_details = SEMCSBCC.objects.filter(beneficiary=beneficiary)
    spgfa_details = SPGFA.objects.filter(beneficiary=beneficiary)
    spnutricash_details = SPNutricash.objects.filter(beneficiary=beneficiary)
    spsage_details = SPSAGE.objects.filter(beneficiary=beneficiary)
    lpdonfarm_details = LPDOnFarm.objects.filter(beneficiary=beneficiary)
    lpdofffarm_details = LPDOffFarm.objects.filter(beneficiary=beneficiary)
    lpdnonfarm_details = LPDNonFarm.objects.filter(beneficiary=beneficiary)
    dfi_details = DFI.objects.filter(beneficiary=beneficiary)    
    
    return render(
        request, 'beneficiary_detail.html', {'beneficiary': beneficiary,
                                            'semcmentoringcoaching_details': semcmentoringcoaching_details,
                                            'semccommunityparticipation_details': semccommunityparticipation_details,
                                            'semcsbcc_details': semcsbcc_details,
                                            'spgfa_details': spgfa_details,
                                            'spnutricash_details': spnutricash_details,
                                            'spsage_details': spsage_details,
                                            'lpdonfarm_details': lpdonfarm_details,
                                            'lpdofffarm_details': lpdofffarm_details,
                                            'lpdnonfarm_details': lpdnonfarm_details,
                                            'dfi_details': dfi_details,                                            

                                              }
        )
@login_required
def beneficiary_create(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, request.FILES)

        # Proceed with form processing if image data is not present
        if form.is_valid():
            # Access the captured image data
            webimg_data = request.POST.get('webimg')
            
            # Convert base64 image data to a file and associate it with the form
            if webimg_data:
                format, imgstr = webimg_data.split(';base64,') 
                ext = format.split('/')[-1]

                # Create a ContentFile from the base64 data
                image_data = ContentFile(base64.b64decode(imgstr), name=f'webimg.{ext}')

                # Associate the image data with the form
                #form.cleaned_data['participant_photo'] = image_data
                form.instance.participant_photo = image_data

            beneficiary = form.save(commit=False)
            beneficiary.group = group
            beneficiary.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = BeneficiaryForm()

    return render(request, 'beneficiary_form.html', {'form': form})

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
    return render(request, 'beneficiary_confirm_delete.html', {'beneficiary': beneficiary})


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


#SPNutricash views-----------------------------------------------------------------------------------------------

@login_required
def spnutricash_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = SPNutricashForm(request.POST)
        if form.is_valid():
            spnutricash = form.save(commit=False)
            spnutricash.beneficiary = beneficiary
            spnutricash.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = SPNutricashForm()

    return render(request, 'spnutricash_form.html', {'form': form})

@login_required
def spnutricash_update(request, pk):
    spnutricash = get_object_or_404(SPNutricash, pk=pk)
    
    if request.method == 'POST':
        form = SPNutricashForm(request.POST, instance=spnutricash)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=spnutricash.beneficiary.pk)
    else:
        form = SPNutricashForm(instance=spnutricash)

    return render(request, 'spnutricash_form.html', {'form': form})

@login_required
def spnutricash_delete(request, pk):
    spnutricash = get_object_or_404(SPNutricash, pk=pk)
    beneficiary_pk = spnutricash.beneficiary.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        spnutricash.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'spnutricash_delete.html', {'beneficiary_pk': beneficiary_pk})
    
    #SPSAGE views-----------------------------------------------------------------------------------------------

@login_required
def spsage_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = SPSAGEForm(request.POST)
        if form.is_valid():
            spsage = form.save(commit=False)
            spsage.beneficiary = beneficiary
            spsage.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = SPSAGEForm()

    return render(request, 'spsage_form.html', {'form': form})

@login_required
def spsage_update(request, pk):
    spsage = get_object_or_404(SPSAGE, pk=pk)
    
    if request.method == 'POST':
        form = SPSAGEForm(request.POST, instance=spsage)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=spsage.beneficiary.pk)
    else:
        form = SPSAGEForm(instance=spsage)

    return render(request, 'spsage_form.html', {'form': form})

@login_required
def spsage_delete(request, pk):
    spsage = get_object_or_404(SPSAGE, pk=pk)
    beneficiary_pk = spsage.beneficiary.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        spsage.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'spsage_delete.html', {'beneficiary_pk': beneficiary_pk})
    

#LPDOnFarm views-----------------------------------------------------------------------------------------------
@login_required
def lpdonfarm_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = LPDOnFarmForm(request.POST)
        if form.is_valid():
            lpdonfarm = form.save(commit=False)
            lpdonfarm.beneficiary = beneficiary
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
            return redirect('beneficiary_detail', pk=lpdonfarm.beneficiary.pk)
    else:
        form = LPDOnFarmForm(instance=lpdonfarm)

    return render(request, 'lpdonfarm_form.html', {'form': form})

@login_required
def lpdonfarm_delete(request, pk):
    lpdonfarm = get_object_or_404(LPDOnFarm, pk=pk)
    beneficiary_pk = lpdonfarm.beneficiary.pk

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
            return redirect('beneficiary_detail', pk=lpdofffarm.beneficiary.pk)
    else:
        form = LPDOffFarmForm(instance=lpdofffarm)

    return render(request, 'lpdofffarm_form.html', {'form': form})

@login_required
def lpdofffarm_delete(request, pk):
    lpdofffarm = get_object_or_404(LPDOffFarm, pk=pk)
    beneficiary_pk = lpdofffarm.beneficiary.pk

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
            return redirect('beneficiary_detail', pk=lpdnonfarm.beneficiary.pk)
    else:
        form = LPDNonFarmForm(instance=lpdnonfarm)

    return render(request, 'lpdnonfarm_form.html', {'form': form})

@login_required
def lpdnonfarm_delete(request, pk):
    lpdnonfarm = get_object_or_404(LPDNonFarm, pk=pk)
    beneficiary_pk = lpdnonfarm.beneficiary.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        lpdnonfarm.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'lpdnonfarm_delete.html', {'beneficiary_pk': beneficiary_pk})


#DFI views-----------------------------------------------------------------------------------------------
@login_required
def dfi_create(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)

    if request.method == 'POST':
        form = DFIForm(request.POST)
        if form.is_valid():
            dfi = form.save(commit=False)
            dfi.beneficiary = beneficiary
            dfi.save()
            return redirect('beneficiary_detail', pk=beneficiary.pk)
    else:
        form = DFIForm()

    return render(request, 'dfi_form.html', {'form': form})

@login_required
def dfi_update(request, pk):
    dfi = get_object_or_404(DFI, pk=pk)
    
    if request.method == 'POST':
        form = DFIForm(request.POST, instance=dfi)
        if form.is_valid():
            form.save()
            return redirect('beneficiary_detail', pk=dfi.beneficiary.pk)
    else:
        form = DFIForm(instance=dfi)

    return render(request, 'dfi_form.html', {'form': form})

@login_required
def dfi_delete(request, pk):
    dfi = get_object_or_404(DFI, pk=pk)
    beneficiary_pk = dfi.beneficiary.pk

    if request.method == 'POST':
        # Handle the confirmation of deletion
        dfi.delete()
        return redirect('beneficiary_detail', pk=beneficiary_pk)
    else:
        # Display the confirmation page
        return render(request, 'dfi_delete.html', {'beneficiary_pk': beneficiary_pk})
    



def custom_logout(request):
    logout(request)
    return redirect(reverse('login'))  # 'login' is the name of the login URL


