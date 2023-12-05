from django import forms
from .models import Group, Beneficiary, SEMCMentoringCoaching, SEMCCommunityParticipation, SEMCSBCC, SPGFA, SPNutricash, SPSAGE, LPDOnFarm, LPDOffFarm, LPDNonFarm, DFI

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
        exclude = ['group']
        fields = '__all__'
        widgets = {
            'participant_photo': forms.FileInput(attrs={'accept': 'image/*', 'capture':'camera'})
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
        model = SPNutricash
        exclude = ['group', 'beneficiary']
        fields = '__all__'
        
        widgets = {
            'disbursement_date': forms.DateInput(attrs={'type': 'date'}), 
        }

class SPSAGEForm(forms.ModelForm):
    class Meta:
        model = SPSAGE
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