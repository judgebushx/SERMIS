from django import forms
from .models import Group, Beneficiary, SEMCMentoringCoaching, SEMCCommunityParticipation, SEMCSBCC, SPGFA, SPNutricashDetails, SPSAGEdetails, LPDOnFarm, LPDOffFarm, LPDNonFarm, DFI, NutricashBeneficiary
from django.core.validators import MaxValueValidator, MinValueValidator


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'date_formed': forms.DateInput(attrs={'type': 'date'}),            
        }

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        
        fields = '__all__'
        exclude = ['group', 'created_at']
        widgets = {
            # 'participant_photo': forms.FileInput(attrs={'accept': 'image/*', 'capture': 'camera'})
        }
    def clean_household_id(self):
            print("clean_household_id method called")
            id_number = self.cleaned_data['household_id']

            # If the instance is new (not already in the database),
            # check for duplicate ID_number
            if not self.instance.pk and Beneficiary.objects.filter(household_id=id_number).exists():
                existing_person = Beneficiary.objects.get(household_id=id_number)
                if existing_person.beneficiary_status != 'Exited':
                    raise forms.ValidationError("A person with this ID number already exists, but the status is not 'Exited'.")
            elif self.instance.pk:  # If editing an existing instance
                # Check for duplicate ID_number excluding the current instance
                existing_person = Beneficiary.objects.filter(household_id=id_number).exclude(pk=self.instance.pk).first()
                if existing_person and existing_person.beneficiary_status != 'Exited':
                    raise forms.ValidationError("A person with this ID number already exists, but the status is not 'Exited'.")

            return id_number    

class NutricashBeneficiaryForm(forms.ModelForm):
    class Meta:
        model = NutricashBeneficiary
        exclude = ['group_representative', 'region', 'district',
                   'settlement', 'group_representative', 'nationality',
                   'actual_nationality', 'actual_region', 'actual_district',
                   'actual_settlement', 'created_at'
                   
                   ]
        fields = '__all__'
        widgets = {
            'profiling_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),  
        } 


class SEMCMentoringCoachingForm(forms.ModelForm):
    class Meta:
        model = SEMCMentoringCoaching
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),            
        }


class SEMCCommunityParticipationForm(forms.ModelForm):
    class Meta:
        model = SEMCCommunityParticipation
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),            
        }


class SEMCSBCCForm(forms.ModelForm):
    class Meta:
        model = SEMCSBCC
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),            
        }
class SPGFAForm(forms.ModelForm):
    class Meta:
        model = SPGFA
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'disbursement_date': forms.DateInput(attrs={'type': 'date'}), 
        }        

class SPNutricashForm(forms.ModelForm):
    class Meta:
        model = SPNutricashDetails
        exclude = ['group', 'group_representative', 
                   'nutricash_beneficiary_name', 'nationality', 
                   'region', 'district', 'settlement', 'ID_type', 'ID_number',
                   'group_representative', 'actual_nationality', 'actual_region', 
                   'actual_district', 'actual_settlement', 'actual_ID_type', 
                   'actual_ID_number'
                   ]
        fields = '__all__'
        
        widgets = {
            'disbursement_date': forms.DateInput(attrs={'type': 'date'}), 
        }

        


class SPSAGEForm(forms.ModelForm):
    class Meta:
        model = SPSAGEdetails
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'disbursement_date': forms.DateInput(attrs={'type': 'date'}), 
        }            

class LPDOnFarmForm(forms.ModelForm):
    class Meta:
        model = LPDOnFarm
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'value_date': forms.DateInput(attrs={'type': 'date'}), 
        }    

class LPDOffFarmForm(forms.ModelForm):
    class Meta:
        model = LPDOffFarm
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'value_date': forms.DateInput(attrs={'type': 'date'}), 
        }

class LPDNonFarmForm(forms.ModelForm):
    class Meta:
        model = LPDNonFarm
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'value_date': forms.DateInput(attrs={'type': 'date'}), 
        } 

class DFIForm(forms.ModelForm):
    class Meta:
        model = DFI
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'value_date': forms.DateInput(attrs={'type': 'date'}), 
        }                    


