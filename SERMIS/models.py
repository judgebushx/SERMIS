from django.db import models

from django.core.exceptions import ValidationError 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime

class Group(models.Model):
        
    DISTRICT_CHOICES = (
        ('Koboko','Koboko'),
        ('Lamwo','Lamwo'),
        ('Isingiro','Isingiro'),
        ('Kamwenge','Kamwenge'),
    )
    SETTLEMENT_CHOICES = (
        ('Lobule', 'Lobule'),
        ('Palabek', 'Palabek'),
        ('Nakivale', 'Nakivale'),
        ('Oruchinga', 'Oruchinga'),
        ('Rwamwanja', 'Rwamwanja'),

    )
    LOCATIONSTATUS_CHOICES = (
        ('Inside Settlement', 'Inside Settlement'),
        ('Outside Settlement', 'Outside Settlement'),
    )

    GRPFORMATION_CHOICES = (
        ('Organically formed by community members', 'Organically formed by community members'),
        ('Formed by an organisation/NGO', 'Formed by an organisation/NGO'),
    )
    YESNO_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')                     
    )
    RECIEVEDSUPPORT_CHOICES = (
        ('Recieved support from WFP', 'Recieved support from WFP'),
        ('Never recieved support from WFP', 'Never recieved support from WFP')                     
    )
    PARTNER_CHOICES = (
         ('None', 'None'),
        ('ACF', 'ACF'),
        ('ALIGHT', 'ALIGHT'),
        ('AVSC', 'AVSC'),
        ('CONVOID', 'CONVOID'),
        ('DRDIP', 'DRDIP'),
        ('Equity Bank', 'Equity Bank'),
        ('FRC', 'FRC'),
        ('Government through DRDIP', 'Government through DRDIP'),
        ('HIJRA', 'HIJRA'),
        ('HFU', 'HFU'),
        ('Isingiro DLG', 'Isingiro DLG'),
        ('Nsamis (pigglets) 2022', 'Nsamis (pigglets) 2022'),
        ('OPM', 'OPM'),
        ('OPPORTUNITY BANK', 'OPPORTUNITY BANK'),
        ('OXFAM', 'OXFAM'),
        ('RIPPLE EFFECT', 'RIPPLE EFFECT'),
        ('SACU', 'SACU'),
        ('SEND A COW', 'SEND A COW'),
        ('Shared Action Africa', 'Shared Action Africa'),
        ('UNDP', 'UNDP'),
        ('Usabiti- Digitalization of savings, records', 'Usabiti- Digitalization of savings, records'),
        ('VEDCO', 'VEDCO'),
        ('WFP', 'WFP'),
        ('UWESO', 'UWESO'),
    )

    SUPPORT_RECEIVED_CHOICES = (
         ('Livestock', 'Livestock'),
        ('Group savings', 'Group savings'),
        ('credit/loans', 'credit/loans'),
        ('group farming.', 'group farming.'),
        ('Savings box', 'Savings box'),
        ('Book keeping', 'Book keeping'),
        ('startup capital', 'startup capital'),
        ('AMS training', 'AMS training'),
        ('Seedlings/farm inputs', 'Seedlings/farm inputs'),
        ('Agric/farming training', 'Agric/farming training'),
        ('VSLA/livelihood training', 'VSLA/livelihood training'),
        ('GFA', 'GFA'),
    )
    GROUPTYPE_CHOICES = (
        ('General Group', 'General Group'),
        ('Youth Group', 'Youth Group'),
        ('Women Group', 'Women Group'),
    )
    STATUS_CHOICES = (
        ('Refugees', 'Refugees'),
        ('National', 'National'),
        ('Mixed', 'Mixed'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    group_name = models.CharField(max_length=25)
    group_type = models.CharField(max_length=35, choices=GROUPTYPE_CHOICES)
    status_of_members = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Refugees')
    chairperson_name = models.CharField(max_length=25)
    chairperson_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    chairperson_contact = models.CharField(max_length=9)
    alternate_contact = models.CharField(max_length=9)
    district = models.CharField(max_length=15, choices=DISTRICT_CHOICES)
    settlement = models.CharField(max_length=20, choices=SETTLEMENT_CHOICES)
    location_status = models.CharField(max_length=25, choices=LOCATIONSTATUS_CHOICES)
    date_formed = models.DateField()
    formation_method = models.CharField(max_length=50, choices=GRPFORMATION_CHOICES)
   
   
    total_members_count = models.PositiveIntegerField(editable=False)
    male_members_count = models.PositiveIntegerField(editable=False)
    female_members_count = models.PositiveIntegerField(editable=False)
    num_refugees_count = models.PositiveIntegerField(editable=False)
    male_refugees_count = models.PositiveIntegerField(editable=False)
    female_refugees_count = models.PositiveIntegerField(editable=False)
    num_youth_count = models.PositiveIntegerField(editable=False)
    male_youth_count = models.PositiveIntegerField(editable=False)
    female_youth_count = models.PositiveIntegerField(editable=False)
    num_disabilities_count = models.PositiveIntegerField(editable=False)

    
    
    
    received_support_from_wfp = models.CharField(max_length=50, choices=RECIEVEDSUPPORT_CHOICES)
    received_assistance_from_other_partner = models.CharField(max_length=3, choices=YESNO_CHOICES)
    other_partner_assistance = models.CharField(max_length=255, choices=PARTNER_CHOICES)
    support_received = models.CharField(max_length=50, choices=SUPPORT_RECEIVED_CHOICES)
    crop_farming = models.CharField(max_length=3, choices=YESNO_CHOICES)
    animal_farming = models.CharField(max_length=3, choices=YESNO_CHOICES)
    savings_and_loans = models.CharField(max_length=3, choices=YESNO_CHOICES)
    involved_in_crafts = models.CharField(max_length=3, choices=YESNO_CHOICES)
    tech_vocational_skills = models.CharField(max_length=3, choices=YESNO_CHOICES)
    engaged_in_trading = models.CharField(max_length=3, choices=YESNO_CHOICES)
    incomes_last_12_months = models.PositiveIntegerField()
    group_assets_value = models.PositiveIntegerField()
    group_loans = models.PositiveIntegerField()
    group_has_bank_account = models.CharField(max_length=3, choices=YESNO_CHOICES)
    current_incomes = models.PositiveIntegerField()
    gps_for_group = models.CharField(max_length=60)


    @property
    def total_members(self):
        return self.beneficiary_set.count()

    @property
    def male_members(self):
        return self.beneficiary_set.filter(gender_of_participant='Male').count()

    @property
    def female_members(self):
        return self.beneficiary_set.filter(gender_of_participant='Female').count()

    @property
    def num_refugees(self):
        return self.beneficiary_set.filter(~Q(nationality='Uganda')).count()

    @property
    def male_refugees(self):
        return self.beneficiary_set.filter(~Q(nationality='Uganda') & Q(gender_of_participant='Male')).count()

    @property
    def female_refugees(self):
        return self.beneficiary_set.filter(~Q(nationality='Uganda') & Q(gender_of_participant='Female')).count()

    @property
    def num_youth(self):
        return self.beneficiary_set.filter(participant_age__lte=30).count()

    @property
    def male_youth(self):
        return self.beneficiary_set.filter(participant_age__lte=30, gender_of_participant='Male').count()

    @property
    def female_youth(self):
        return self.beneficiary_set.filter(participant_age__lte=30, gender_of_participant='Female').count()

    @property
    def num_disabilities(self):
        return self.beneficiary_set.filter(disablity_of_hhh='Living with a disability').count()


    def get_beneficiaries(self):
        return Beneficiary.objects.filter(group=self)


    
    def update_member_counts(self):
        beneficiaries = self.get_beneficiaries()

        self.total_members_count = beneficiaries.count()
        self.male_members_count = beneficiaries.filter(gender_of_participant='Male').count()
        self.female_members_count = beneficiaries.filter(gender_of_participant='Female').count()
        self.num_refugees_count = beneficiaries.exclude(nationality='Uganda').count()
        self.male_refugees_count = beneficiaries.exclude(nationality='Uganda', gender_of_participant='Male').count()
        self.female_refugees_count = beneficiaries.exclude(nationality='Uganda', gender_of_participant='Female').count()
        self.num_youth_count = beneficiaries.filter(participant_age__lte=30).count()
        self.male_youth_count = beneficiaries.filter(participant_age__lte=30, gender_of_participant='Male').count()
        self.female_youth_count = beneficiaries.filter(participant_age__lte=30, gender_of_participant='Female').count()
        self.num_disabilities_count = beneficiaries.filter(disablity_of_hhh='Living with a disability').count()

    def save(self, *args, **kwargs):        
        super().save(*args, **kwargs)
        self.update_member_counts()

    def __str__(self):
        return self.group_name


class Beneficiary(models.Model):
    YESNO_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    )
    DISTRICT_CHOICES = (
        ('Koboko', 'Koboko'),
        ('Lamwo', 'Lamwo'),
        ('Isingiro', 'Isingiro'),
        ('Kamwenge', 'Kamwenge'),
    )
    SETTLEMENT_CHOICES = (
        ('Lobule', 'Lobule'),
        ('Palabek', 'Palabek'),
        ('Nakivale', 'Nakivale'),
        ('Oruchinga', 'Oruchinga'),
        ('Rwamwanja', 'Rwamwanja'),

    )
    NATIONALITY_CHOICES = (
        ('Uganda', 'Uganda'),
        ('Congo', 'Congo'),
        ('Sundan', 'Sundan'),
        ('South Sudan', 'South Sudan'),
    )
    REGION_CHOICES = (
         ('South West', 'South West'),
         ('West Nile', 'West Nile'),
         ('Karamoja', 'Karamoja')
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
            )
    RELHH_CHOICES = (
        ('Head of household', 'Head of household'),
        ('Spouse/partner', 'Spouse/partner'),
        ('Son/daughter', 'Son/daughter'),
        ('Brother/sister', 'Brother/sister'),
        ('Father/mother', 'Father/mother'),
    )
    MARITALSTATUS_CHOICES = (
         ('Married', 'Married'),
         ('Single', 'Single'),
         ('Divorced', 'Divorced'),
         ('Widowed', 'Widowed'),
        )
    EDUCLEVEL_CHOICES =  (
        ('Illiterate', 'Illiterate'),
        ('Primaryn education', 'Primaryn education'),
        ('Secondary/High school education', 'Secondary/High school education'),
        ('Teritary education', 'Teritary education'),
    )
    DISABILITY_CHOICES = (
         ('Able bodied', 'Able bodied'),
         ('Living with a disability', 'Living with a disability'),
    )
    RELIGION_CHOICES = (
         ('Christian', 'Christian'),
         ('Muslim', 'Muslim'),
         ('Traditional African religion', 'Traditional African religion'),
         ('Atheist', 'Atheist'),
    )
    STATUS_CHOICES = (
         ('Enrolled', 'Enrolled'),
         ('Temporarily Suspended', 'Temporarily Suspended'),
         ('Exited', 'Exited'),
         ('Graduated', 'Graduated'),
         ('Deceased', 'Deceased'),
         ('Repatriated', 'Repatriated')
         
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)   
    region = models.CharField(max_length=35, choices=REGION_CHOICES)
    district = models.CharField(max_length=35, choices=DISTRICT_CHOICES)
    settlement = models.CharField(max_length=35, choices=SETTLEMENT_CHOICES)    
    nationality = models.CharField(max_length=35, choices=NATIONALITY_CHOICES)
    household_id = models.CharField(max_length=12)
    name_of_household_head = models.CharField(max_length=50)
    household_head_phone = models.IntegerField(validators=[MaxValueValidator(999999999, message="9 digits maximum" )]  )
    participant_individual_id = models.CharField(max_length=12)
    name_of_participant = models.CharField(max_length=50)
    gender_of_participant = models.CharField(max_length=10, choices=GENDER_CHOICES)
    participant_age = models.IntegerField(validators=[MaxValueValidator(99, message="Maximum age should be 99 years or less."), MinValueValidator(0, message="Age cannot be negative."),])
    # participant_photo = models.ImageField(upload_to='beneficiary_photos/', null=True, blank=True)
    participant_phone =  models.IntegerField(validators=[MaxValueValidator(999999999, message="9 digits maximum" )]  )
    relationship_with_household_head = models.CharField(max_length=100, choices=RELHH_CHOICES)
    gender_hhh = models.CharField(max_length=35, choices=GENDER_CHOICES, verbose_name="Gender of HH Head")
    age_of_hhh = models.IntegerField(validators=[MaxValueValidator(99, message="Maximum age should be 99 years or less."), MinValueValidator(0, message="Age cannot be negative."),], verbose_name="Age of HH Head")
    disablity_of_hhh = models.CharField(max_length=35, choices=DISABILITY_CHOICES)
    marital_status = models.CharField(max_length=35, choices=MARITALSTATUS_CHOICES)
    education_level = models.CharField(max_length=35, choices=EDUCLEVEL_CHOICES)
    religion = models.CharField(max_length=35, choices=RELIGION_CHOICES)
    beneficiary_status = models.CharField(max_length=35, choices=STATUS_CHOICES, default='Enrolled')
    created_at = models.DateTimeField(default=timezone.now)        
    


    def update_group_member_counts(sender, instance, **kwargs):
        group = instance.group
        beneficiaries = Beneficiary.objects.filter(group=group)

        group.total_members = beneficiaries.count()
        group.male_members = beneficiaries.filter(gender_of_participant='Male').count()
        group.female_members = beneficiaries.filter(gender_of_participant='Female').count()
        group.num_refugees = beneficiaries.filter(nationality__ne='Uganda').count()
        group.male_refugees = beneficiaries.filter(nationality__ne='Uganda', gender_of_participant='Male').count()
        group.female_refugees = beneficiaries.filter(nationality__ne='Uganda', gender_of_participant='Female').count()
        group.num_youth = beneficiaries.filter(participant_age__lte=30).count()
        group.male_youth = beneficiaries.filter(participant_age__lte=30, gender_of_participant='Male').count()
        group.female_youth = beneficiaries.filter(participant_age__lte=30, gender_of_participant='Female').count()
        group.num_disabilities = beneficiaries.filter(disablity_of_hhh='Living with a disability').count()

        group.save()
   
    def __str__(self):
            return self.name_of_participant
    
class SAGEBeneficiary(models.Model):
    STATUS_CHOICES = (
        ('Enrolled', 'Enrolled'),
        ('Re-enrolled', 'Re-enrolled'),
        ('Exited', 'Exited'),
        ('Temporarily transferred to TSFP', 'Temporarily transferred to TSFP'),
    )

    IDtype_CHOICES = (
        ('NIN', 'NIN'),
        ('Attestation Individual Number', 'Attestation Individual Number'),
        ('KSRN Number', 'KSRN Number'),
        ('Next of Kin NIN', 'Next of Kin NIN'),
        ('Next of Kin AIN', 'Next of Kin AIN'),
        ('Other government issued ID', 'Other government issued ID'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    profiling_date = models.DateTimeField(default=timezone.now)
    nationality = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_beneficiaries_nationality')
    region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_beneficiaries_region')
    district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_beneficiaries_district')
    settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_beneficiaries_settlement')
    candidate_name = models.CharField(max_length=50)
    candidate_dob = models.DateField()
    candidate_gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    household_id = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_beneficiaries_household_id')
    ID_type = models.CharField(max_length=30, choices=IDtype_CHOICES, default='NIN')
    candidate_individual_id = models.CharField(max_length=12)
    group_representative = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_beneficiaries_group_representative')
    beneficiary_status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    # Additional fields to store actual names
    actual_nationality = models.CharField(max_length=35, blank=True)
    actual_region = models.CharField(max_length=35, blank=True)
    actual_district = models.CharField(max_length=35, blank=True)
    actual_settlement = models.CharField(max_length=35, blank=True)


# @receiver(post_save, sender=SAGEBeneficiary)
# def update_actual_names(sender, instance, created, **kwargs):
#     if created:
#         beneficiary_instance = instance.nationality
#         if beneficiary_instance:
#             instance.actual_nationality = beneficiary_instance.nationality
#         beneficiary_instance = instance.region
#         if beneficiary_instance:
#             instance.actual_region = beneficiary_instance.region
#         beneficiary_instance = instance.district
#         if beneficiary_instance:
#             instance.actual_district = beneficiary_instance.district
#         beneficiary_instance = instance.settlement
#         if beneficiary_instance:
#             instance.actual_settlement = beneficiary_instance.settlement
#         instance.save()

  


class NutricashBeneficiary(models.Model):
    YESNO_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    STATUS_CHOICES = (
        ('Enrolled', 'Enrolled'),
        ('Re-enrolled', 'Re-enrolled'),
        ('Exited', 'Exited'),
        ('Temporarily transferred to TSFP', 'Temporarily transferred to TSFP'),
    )

    IDtype_CHOICES = (
        ('NIN', 'NIN'),
        ('Attestation Individual Number', 'Attestation Individual Number'),
        ('KSRN Number', 'KSRN Number'),
        ('Next of Kin NIN', 'Next of Kin NIN'),
        ('Next of Kin AIN', 'Next of Kin AIN'),
        ('Other government issued ID', 'Other government issued ID'),
    )

    PREGLACT_CHOICES = (
        ('Pregnant', 'Pregnant'),
        ('Lactating', 'Lactating'),
        ('Pregnant & Lactating', 'Pregnant & Lactating'),
    )

    profiling_date = models.DateTimeField(default=timezone.now)
    nutricash_beneficiary_name = models.CharField(max_length=30)
    nationality = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='nutricash_beneficiary_nationality')
    region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='nutricash_beneficiaries_region')
    district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='nutricash_beneficiaries_district')
    settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='nutricash_beneficiaries_settlement')
    ID_type = models.CharField(max_length=30, choices=IDtype_CHOICES, default='NIN')
    ID_number = models.CharField(max_length=16)
    group_representative = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='nutricash_beneficiaries_group_representative')
    age = models.IntegerField(validators=[MaxValueValidator(99, message="2 digits maximum" )])
    enrollment_gestational_age = models.IntegerField(validators=[MaxValueValidator(99, message="2 digits maximum" )])
    expected_delivery_date = models.DateField()
    pregnant_or_lactating = models.CharField(max_length=22, choices=PREGLACT_CHOICES)
    beneficiary_status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    

    # Additional fields to store actual names
    actual_nationality = models.CharField(max_length=35, blank=True)
    actual_region = models.CharField(max_length=35, blank=True)
    actual_district = models.CharField(max_length=35, blank=True)
    actual_settlement = models.CharField(max_length=35, blank=True)


    exit_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate the exit date by adding 24 months to the expected delivery date
        if self.expected_delivery_date:
            self.exit_date = self.expected_delivery_date + timezone.timedelta(days=730)
        else:
            self.exit_date = None
        
        super().save(*args, **kwargs)



class SPNutricashDetails(models.Model):
    YESNO_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    DISTRICT_CHOICES = (
        ('Koboko', 'Koboko'),
        ('Lamwo', 'Lamwo'),
        ('Isingiro', 'Isingiro'),
        ('Kamwenge', 'Kamwenge'),
    )
    SETTLEMENT_CHOICES = (
        ('Lobule', 'Lobule'),
        ('Palabek', 'Palabek'),
        ('Nakivale', 'Nakivale'),
        ('Oruchinga', 'Oruchinga'),
        ('Rwamwanja', 'Rwamwanja'),
    )
    PREGLACT_CHOICES = (
        ('Pregnant', 'Pregnant'),
        ('Lactating', 'Lactating'),
        ('Pregnant & Lactating', 'Pregnant & Lactating'),
    )

    COMPONENT_CHOICES = (
        ('SEMC', 'SEMC'),
        ('SP', 'SP'),
        ('LPD', 'LPD'),
        ('DFI', 'DFI'),
    )
    CP_CHOICES = (
        ('WFP', 'WFP'),
        ('AFI', 'AFI'),
        ('KRC', 'KRC'),
        ('ACF', 'ACF'),
        ('FHI', 'FHI'),
        ('MTI', 'MTI'),
        ('LWF', 'LWF'),
        ('FHU', 'FHU'),
    )

    provider = models.CharField(max_length=20, choices=CP_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False, related_name='nutricash_group')
    disbursement_date = models.DateField()
    nutricash_beneficiary_name = models.ForeignKey(NutricashBeneficiary, on_delete=models.CASCADE, related_name='nutricash_beneficiaryname')
    nationality  = models.ForeignKey(NutricashBeneficiary, on_delete=models.CASCADE, related_name='nutricash_nationality')        
    region = models.ForeignKey(NutricashBeneficiary, on_delete=models.CASCADE, related_name='nutricash_region')
    district = models.ForeignKey(NutricashBeneficiary, on_delete=models.CASCADE, related_name='nutricash_district')
    settlement = models.ForeignKey(NutricashBeneficiary, on_delete=models.CASCADE, related_name='nutricash_settlement')
    ID_type = models.ForeignKey(NutricashBeneficiary, on_delete=models.CASCADE, related_name='nutricash_id_type')
    ID_number = models.ForeignKey(NutricashBeneficiary, on_delete=models.CASCADE, related_name='nutricash_id_number')       
    pregnant_or_lactating = models.CharField(max_length=22, choices=PREGLACT_CHOICES)
    transfer_value = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
    group_representative = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='nutricash_group_representative')
    component = models.CharField(max_length=10, default='SP')

    # Actual field names
    actual_nationality = models.CharField(max_length=40)  # Store actual nationality
    actual_region = models.CharField(max_length=40)  # Store actual region
    actual_district = models.CharField(max_length=40)  # Store actual district
    actual_settlement = models.CharField(max_length=40)  # Store actual settlement
    actual_ID_type = models.CharField(max_length=40)  # Store actual ID type
    actual_ID_number = models.CharField(max_length=40)  # Store actual ID number

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being saved for the first time
            if not self.group_id:
                self.group = self.nutricash_beneficiary_name.group_representative.group
           
            beneficiary_instance = self.nutricash_beneficiary_name

            if beneficiary_instance:
                self.actual_nationality = beneficiary_instance.nationality.nationality
                self.actual_region = beneficiary_instance.region.region
                self.actual_district = beneficiary_instance.district.district
                self.actual_settlement = beneficiary_instance.settlement.settlement
                self.actual_ID_type = beneficiary_instance.ID_type
                self.actual_ID_number = beneficiary_instance.ID_number
        super().save(*args, **kwargs)


class FinlitBeneficiary(models.Model):
        STATUS_CHOICES = (
            ('Enrolled', 'Enrolled'),
            ('Re-enrolled', 'Re-enrolled'),
            ('Exited', 'Exited'),
            ('Temporarily transferred to TSFP', 'Temporarily transferred to TSFP'),
        ) 
        IDtype_CHOICES = (
            ('NIN', 'NIN'),
            ('Attestation Individual Number', 'Attestation Individual Number'),
            ('KSRN Number', 'KSRN Number'),
            ('Next of Kin NIN', 'Next of Kin NIN'),
            ('Next of Kin AIN', 'Next of Kin AIN'),
            ('Other government issued ID', 'Other government issued ID'),
        )
        GENDER_CHOICES = (
             ('Male', 'Male'),
             ('Female', 'Female')
        )
        

        profiling_date = models.DateTimeField(default=timezone.now)
        nationality = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='finlit_beneficiaries_nationality')
        region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='finlit_beneficiaries_region')
        district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='finlit_beneficiaries_district')
        settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='finlit_beneficiaries_settlement')   
        candidate_name = models.CharField(max_length=50)
        candidate_age = models.IntegerField(validators=[MaxValueValidator(99, message="2 digits maximum" )])
        candidate_gender = models.CharField(max_length=8, choices=GENDER_CHOICES) 
        household_id = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='finlit_beneficiaries_household_id')
        ID_type = models.CharField(max_length=30, choices=IDtype_CHOICES, default='NIN')  
        candidate_individual_id = models.CharField(max_length=12)
        group_representative = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='finlit_beneficiaries_group_representative')
        beneficiary_status = models.CharField(max_length=32, choices=STATUS_CHOICES)
        created_at = models.DateTimeField(default=timezone.now) 

        actual_nationality = models.CharField(max_length=35, blank=True)
        actual_region = models.CharField(max_length=35, blank=True)
        actual_district = models.CharField(max_length=35, blank=True)
        actual_settlement = models.CharField(max_length=35, blank=True)


class FinLitDetails(models.Model):
   
        YESNO_CHOICES = (
            ('Yes', 'Yes'),
            ('No', 'No'),
            )
        GENDER_CHOICES = (
                ('Male', 'Male'),
                ('Female', 'Female'),
            )
        DISTRICT_CHOICES = (
            ('Koboko', 'Koboko'),
            ('Lamwo', 'Lamwo'),
            ('Isingiro', 'Isingiro'),
            ('Kamwenge', 'Kamwenge'),
        )
        SETTLEMENT_CHOICES = (
            ('Lobule', 'Lobule'),
            ('Palabek', 'Palabek'),
            ('Nakivale', 'Nakivale'),
            ('Oruchinga', 'Oruchinga'),
            ('Rwamwanja', 'Rwamwanja'),

        )
        NATIONALITY_CHOICES = (
            ('Uganda', 'Uganda'),
            ('Congo', 'Congo'),
            ('Sundan', 'Sundan'),
            ('South Sudan', 'South Sudan'),
        )
        REGION_CHOICES = (
            ('South West', 'South West'),
            ('West Nile', 'West Nile'),
            ('Karamoja', 'Karamoja')
        )
        COMPONENT_CHOICES = (
            ('SEMC', 'SEMC'),
            ('SP', 'SP'),
            ('LPD', 'LPD'),
            ('DFI', 'DFI'),
        )
        DFISOFTCOMPONENT_CHOICES = (
            ('Basic financial literacy training received', 'Basic financial literacy training received'),
            ('Advanced financial literacy trainings received', 'Advanced financial literacy trainings received'),
            ('Digital literacy training received', 'Digital literacy training received'),
        )     
        CP_CHOICES = (
            ('WFP', 'WFP'),
            ('AFI', 'AFI'),
            ('KRC', 'KRC'),
            ('ACF', 'ACF'),
            ('FHI', 'FHI'),
            ('MTI', 'MTI'),
            ('LWF', 'LWF'),
            ('FHU', 'FHU'),
        )

        provider = models.CharField(max_length=10, choices=CP_CHOICES)
        finlit_candidate_name = models.ForeignKey(FinlitBeneficiary, on_delete=models.CASCADE, related_name='finlit_candidate')
        group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='finlit_group')        
        value_date = models.DateField()
        nationality  = models.ForeignKey(FinlitBeneficiary, on_delete=models.CASCADE, related_name='finlit_nationality')        
        region = models.ForeignKey(FinlitBeneficiary, on_delete=models.CASCADE, related_name='finlit_region')
        district = models.ForeignKey(FinlitBeneficiary, on_delete=models.CASCADE, related_name='finlit_district')
        settlement = models.ForeignKey(FinlitBeneficiary, on_delete=models.CASCADE, related_name='finlit_settlement')
        DFI_Software_component_received = models.CharField(max_length=100, choices=DFISOFTCOMPONENT_CHOICES, verbose_name="Software Component received")
        group_representative = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='finlit_details_group_representative')
        component = models.CharField(max_length=10, default='LPD')

        # Actual field names
        actual_nationality = models.CharField(max_length=35) 
        actual_region = models.CharField(max_length=35)  # Store actual region name
        actual_district = models.CharField(max_length=35)  # Store actual district name
        actual_settlement = models.CharField(max_length=35)  # Store actual settlement name
        actual_group = models.CharField(max_length=100)  # Store actual group name

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.finlit_candidate_name.group_representative.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "FinLit Details"

        def __str__(self):
            return f"FinLit Details for {self.finlit_candidate_name}"
        






class SEMCCommunityParticipation(models.Model):
    DISTRICT_CHOICES = (
        ('Koboko', 'Koboko'),
        ('Lamwo', 'Lamwo'),
        ('Isingiro', 'Isingiro'),
        ('Kamwenge', 'Kamwenge'),
    )
    SETTLEMENT_CHOICES = (
        ('Lobule', 'Lobule'),
        ('Palabek', 'Palabek'),
        ('Nakivale', 'Nakivale'),
        ('Oruchinga', 'Oruchinga'),
        ('Rwamwanja', 'Rwamwanja'),
    )
    NATIONALITY_CHOICES = (
        ('Uganda', 'Uganda'),
        ('Congo', 'Congo'),
        ('Sudan', 'Sudan'),
        ('South Sudan', 'South Sudan'),
    )
    REGION_CHOICES = (
        ('South West', 'South West'),
        ('West Nile', 'West Nile'),
        ('Karamoja', 'Karamoja')
    )
    TOPIC_CHOICES = (
        ('Gender', 'Gender'),
        ('WASH', 'WASH'),
        ('Communication and life skills', 'Communication and life skills')
    )

    CP_CHOICES = (
        ('WFP', 'WFP'),
        ('AFI', 'AFI'),
        ('KRC', 'KRC'),
        ('ACF', 'ACF'),
        ('FHI', 'FHI'),
        ('MTI', 'MTI'),
        ('LWF', 'LWF'),
        ('FHU', 'FHU'),
    )

    provider = models.CharField(max_length=20, choices=CP_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False, related_name='community_participation_group')
    meeting_date = models.DateField()        
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='community_participation_beneficiary')
    region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='community_participation_region')
    district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='community_participation_district')
    settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='community_participation_settlement')        
    topic_of_discussion = models.CharField(max_length=100, choices=TOPIC_CHOICES)
    component = models.CharField(max_length=10, default='SEMC')
    
    # Actual field names
    actual_group = models.CharField(max_length=100)  # Store actual group name
    actual_region = models.CharField(max_length=35)  # Store actual region name
    actual_district = models.CharField(max_length=35)  # Store actual district name
    actual_settlement = models.CharField(max_length=35)  # Store actual settlement name

    def save(self, *args, **kwargs):
        # If the group and beneficiary are not already set, set them automatically
        if not self.group_id:
            self.group = self.beneficiary.group

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Community Participation Details"

    def __str__(self):
        return f"Community Participation Details for {self.beneficiary.name_of_participant}"   



class SEMCSBCC(models.Model):
    DISTRICT_CHOICES = (
        ('Koboko', 'Koboko'),
        ('Lamwo', 'Lamwo'),
        ('Isingiro', 'Isingiro'),
        ('Kamwenge', 'Kamwenge'),
    )
    SETTLEMENT_CHOICES = (
        ('Lobule', 'Lobule'),
        ('Palabek', 'Palabek'),
        ('Nakivale', 'Nakivale'),
        ('Oruchinga', 'Oruchinga'),
        ('Rwamwanja', 'Rwamwanja'),
    )
    NATIONALITY_CHOICES = (
        ('Uganda', 'Uganda'),
        ('Congo', 'Congo'),
        ('Sudan', 'Sudan'),
        ('South Sudan', 'South Sudan'),
    )
    REGION_CHOICES = (
        ('South West', 'South West'),
        ('West Nile', 'West Nile'),
        ('Karamoja', 'Karamoja')
    )
    TOPIC_CHOICES = (
        ('Gender', 'Gender'),
        ('WASH', 'WASH'),
        ('Communication and life skills', 'Communication and life skills')
    )
    CP_CHOICES = (
        ('WFP', 'WFP'),
        ('AFI', 'AFI'),
        ('KRC', 'KRC'),
        ('ACF', 'ACF'),
        ('FHI', 'FHI'),
        ('MTI', 'MTI'),
        ('LWF', 'LWF'),
        ('FHU', 'FHU'),
    )

    provider = models.CharField(max_length=20, choices=CP_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False, related_name='sbcc_group')
    meeting_date = models.DateField()
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sbcc_beneficiary')
    region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sbcc_region')
    district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sbcc_district')
    settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sbcc_settlement')         
    topic_of_discussion = models.CharField(max_length=100, choices=TOPIC_CHOICES)    
    component = models.CharField(max_length=10, default='SEMC')
    
    # Actual field names
    actual_group = models.CharField(max_length=100)  # Store actual group name
    actual_region = models.CharField(max_length=35)  # Store actual region name
    actual_district = models.CharField(max_length=35)  # Store actual district name
    actual_settlement = models.CharField(max_length=35)  # Store actual settlement name

    def save(self, *args, **kwargs):
        # If the group and beneficiary are not already set, set them automatically
        if not self.group_id:
            self.group = self.beneficiary.group

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "SBCC Details"

    def __str__(self):
        return f"SBCC Details for {self.beneficiary.name_of_household_head}"   




class SEMCMentoringCoaching(models.Model):
    DISTRICT_CHOICES = (
        ('Koboko', 'Koboko'),
        ('Lamwo', 'Lamwo'),
        ('Isingiro', 'Isingiro'),
        ('Kamwenge', 'Kamwenge'),
    )
    SETTLEMENT_CHOICES = (
        ('Lobule', 'Lobule'),
        ('Palabek', 'Palabek'),
        ('Nakivale', 'Nakivale'),
        ('Oruchinga', 'Oruchinga'),
        ('Rwamwanja', 'Rwamwanja'),
    )
    NATIONALITY_CHOICES = (
        ('Uganda', 'Uganda'),
        ('Congo', 'Congo'),
        ('Sudan', 'Sudan'),
        ('South Sudan', 'South Sudan'),
    )
    REGION_CHOICES = (
        ('South West', 'South West'),
        ('West Nile', 'West Nile'),
        ('Karamoja', 'Karamoja')
    )
    TOPIC_CHOICES = (
        ('On farm', 'On farm'),
        ('Non farm', 'Non farm'),        
    )
    CP_CHOICES = (
        ('WFP', 'WFP'),
        ('AFI', 'AFI'),
        ('KRC', 'KRC'),
        ('ACF', 'ACF'),
        ('FHI', 'FHI'),
        ('MTI', 'MTI'),
        ('LWF', 'LWF'),
        ('FHU', 'FHU'),
    )

    provider = models.CharField(max_length=20, choices=CP_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False, related_name='mentoring_coaching_group')
    meeting_date = models.DateField()
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='mentoring_coaching_beneficiary')
    region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='mentoring_coaching_region')
    district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='mentoring_coaching_district')
    settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='mentoring_coaching_settlement')       
    mentor_name =  models.CharField(max_length=30)
    topic_of_discussion = models.CharField(max_length=100, choices=TOPIC_CHOICES)
    component = models.CharField(max_length=10, default='SEMC')
    
    # Actual field names
    actual_group = models.CharField(max_length=100)  # Store actual group name
    actual_region = models.CharField(max_length=35)  # Store actual region name
    actual_district = models.CharField(max_length=35)  # Store actual district name
    actual_settlement = models.CharField(max_length=35)  # Store actual settlement name

    def save(self, *args, **kwargs):
        # If the group and beneficiary are not already set, set them automatically
        if not self.group_id:
            self.group = self.beneficiary.group

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Mentoring and Coaching Details"

    def __str__(self):
        return f"Mentoring and Coaching Details for {self.beneficiary.name_of_participant}"   



       
        

class SPGFA(models.Model):
    YESNO_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    DISTRICT_CHOICES = (
        ('Koboko', 'Koboko'),
        ('Lamwo', 'Lamwo'),
        ('Isingiro', 'Isingiro'),
        ('Kamwenge', 'Kamwenge'),
    )
    SETTLEMENT_CHOICES = (
        ('Lobule', 'Lobule'),
        ('Palabek', 'Palabek'),
        ('Nakivale', 'Nakivale'),
        ('Oruchinga', 'Oruchinga'),
        ('Rwamwanja', 'Rwamwanja'),
    )
    NATIONALITY_CHOICES = (
        ('Uganda', 'Uganda'),
        ('Congo', 'Congo'),
        ('Sudan', 'Sudan'),
        ('South Sudan', 'South Sudan'),
    )
    REGION_CHOICES = (
        ('South West', 'South West'),
        ('West Nile', 'West Nile'),
        ('Karamoja', 'Karamoja')
    )        
    COMPONENT_CHOICES = (
        ('SEMC', 'SEMC'),
        ('SP', 'SP'),
        ('LPD', 'LPD'),
        ('DFI', 'DFI'),
    )

    CP_CHOICES = (
        ('WFP', 'WFP'),
        ('AFI', 'AFI'),
        ('KRC', 'KRC'),
        ('ACF', 'ACF'),
        ('FHI', 'FHI'),
        ('MTI', 'MTI'),
        ('LWF', 'LWF'),
        ('FHU', 'FHU'),
    )

    provider = models.CharField(max_length=20, choices=CP_CHOICES)
    disbursement_date = models.DateField()
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='gfa_beneficiary')        
    region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='gfa_region')
    district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='gfa_district')
    settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='gfa_settlement') 
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False, related_name='gfa_group')
    household_beneficiary_name = models.CharField(max_length=25)
    transfer_value = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
    component = models.CharField(max_length=10, default='SP')

    # Actual field names
    actual_region = models.CharField(max_length=35)  # Store actual region name
    actual_district = models.CharField(max_length=35)  # Store actual district name
    actual_settlement = models.CharField(max_length=35)  # Store actual settlement name
    actual_group = models.CharField(max_length=100)  # Store actual group name

    def save(self, *args, **kwargs):
        # If the group and beneficiary are not already set, set them automatically
        if not self.group_id:
            self.group = self.beneficiary.group

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "GFA Details"

    def __str__(self):
        return f"GFA Details for {self.beneficiary.name_of_household_head}"











                # self.actual_nationality = self.nutricash_beneficiary_name.nationality
                # self.actual_region = self.nutricash_beneficiary_name.region
                # self.actual_district = self.nutricash_beneficiary_name.district
                # self.actual_settlement = self.nutricash_beneficiary_name.settlement
                # self.actual_ID_type = self.nutricash_beneficiary_name.ID_type
                # self.actual_ID_number = self.nutricash_beneficiary_name.ID_number

        # super().save(*args, **kwargs)


    
# @receiver(post_save, sender=SPNutricashDetails)
# def update_actual_names(sender, instance, created, **kwargs):
#     beneficiary_instance = instance.nutricash_beneficiary_name
#     if beneficiary_instance:
#         instance.actual_region = beneficiary_instance.region
#         instance.actual_district = beneficiary_instance.district
#         instance.actual_settlement = beneficiary_instance.settlement
#         instance.actual_ID_type = beneficiary_instance.ID_type
#         instance.actual_ID_number = beneficiary_instance.ID_number
#         instance.actual_nationality = beneficiary_instance.nationality
#         instance.save()


class SPSAGEdetails(models.Model):
        YESNO_CHOICES = (
            ('Yes', 'Yes'),
            ('No', 'No'),
            )
        GENDER_CHOICES = (
                ('Male', 'Male'),
                ('Female', 'Female'),
            )
        DISTRICT_CHOICES = (
            ('Koboko', 'Koboko'),
            ('Lamwo', 'Lamwo'),
            ('Isingiro', 'Isingiro'),
            ('Kamwenge', 'Kamwenge'),
        )
        SETTLEMENT_CHOICES = (
            ('Lobule', 'Lobule'),
            ('Palabek', 'Palabek'),
            ('Nakivale', 'Nakivale'),
            ('Oruchinga', 'Oruchinga'),
            ('Rwamwanja', 'Rwamwanja'),

        )
        NATIONALITY_CHOICES = (
            ('Uganda', 'Uganda'),
            ('Congo', 'Congo'),
            ('Sundan', 'Sundan'),
            ('South Sudan', 'South Sudan'),
        )
        REGION_CHOICES = (
            ('South West', 'South West'),
            ('West Nile', 'West Nile'),
            ('Karamoja', 'Karamoja')
        )
        COMPONENT_CHOICES = (
            ('SEMC', 'SEMC'),
            ('SP', 'SP'),
            ('LPD', 'LPD'),
            ('DFI', 'DFI'),
        )
        CP_CHOICES = (
            ('WFP', 'WFP'),
            ('AFI', 'AFI'),
            ('KRC', 'KRC'),
            ('ACF', 'ACF'),
            ('FHI', 'FHI'),
            ('MTI', 'MTI'),
            ('LWF', 'LWF'),
            ('FHU', 'FHU'),
        )

        
        def validate_sage_beneficiary_age(value):
            if value < 80 or value > 100:
                raise ValidationError('Household beneficiary age must be between 80 and 100 inclusive.')
            
        provider = models.CharField(max_length=20, choices=CP_CHOICES)
        name_of_participant = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_participant')
        group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='sage_group')        
        disbursement_date = models.DateField()
        nationality = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_nationality')
        region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_region')
        district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_district')
        ID_type = models.ForeignKey(SAGEBeneficiary, on_delete=models.CASCADE, related_name='sage_id_type')
        candidate_individual_id = models.ForeignKey(SAGEBeneficiary, on_delete=models.CASCADE, related_name='sage_id_number') 
        settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='sage_settlement')
        sage_beneficiary_name = models.ForeignKey(SAGEBeneficiary, on_delete=models.CASCADE, related_name='sage_beneficiary')
        sage_beneficiary_dob = models.ForeignKey(SAGEBeneficiary, on_delete=models.CASCADE, related_name='sage_dob')
        sage_beneficiary_age = models.IntegerField(validators=[validate_sage_beneficiary_age])
        transfer_value = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
        component = models.CharField(max_length=10, default='SP')

        # Actual field names
        actual_nationality = models.CharField(max_length=35)
        actual_region = models.CharField(max_length=35)  # Store actual region name
        actual_district = models.CharField(max_length=35)  # Store actual district name
        actual_settlement = models.CharField(max_length=35)  # Store actual settlement name
        actual_group = models.CharField(max_length=100)  # Store actual group name
        actual_ID_type = models.CharField(max_length=40)  # Store actual ID type
        actual_candidate_individual_id = models.CharField(max_length=40)  # Store actual ID number


        def save(self, *args, **kwargs):
                # If the group and beneficiary are not already set, set them automatically
                if not self.group_id:
                    self.group = self.name_of_participant.group

            # Calculate age based on the candidate's date of birth if it's provided
                if self.sage_beneficiary_dob:
                    # Access the date of birth from the associated SAGEBeneficiary instance
                    dob = self.sage_beneficiary_dob.candidate_dob

                    # Calculate the age
                    age = datetime.today().year - dob.year

                    # Check if the birthday has occurred this year already
                    if (dob.month, dob.day) > (datetime.today().month, datetime.today().day):
                        age -= 1  # Subtract 1 if birthday hasn't occurred yet this year

                    self.sage_beneficiary_age = age
                else:
                    # Handle case when date of birth is not provided
                    self.sage_beneficiary_age = None

                super().save(*args, **kwargs)
                
        class Meta:
            verbose_name_plural = "SAGE Details"

        def __str__(self):
            return f"SAGE Details for {self.sage_beneficiary_name}"

# # Receiver to update actual field names
# @receiver(post_save, sender=SPSAGEdetails)
# def update_actual_names(sender, instance, created, **kwargs):
#     if created:
#         beneficiary_instance = instance.beneficiary
#         if beneficiary_instance:
#             instance.actual_region = beneficiary_instance.region
#             instance.actual_district = beneficiary_instance.district
#             instance.actual_settlement = beneficiary_instance.settlement
#             instance.actual_group = beneficiary_instance.group.group_name
#         instance.save()   

class LPDOnFarm(models.Model):
   
        YESNO_CHOICES = (
            ('Yes', 'Yes'),
            ('No', 'No'),
            )
        GENDER_CHOICES = (
                ('Male', 'Male'),
                ('Female', 'Female'),
            )
        DISTRICT_CHOICES = (
            ('Koboko', 'Koboko'),
            ('Lamwo', 'Lamwo'),
            ('Isingiro', 'Isingiro'),
            ('Kamwenge', 'Kamwenge'),
        )
        SETTLEMENT_CHOICES = (
            ('Lobule', 'Lobule'),
            ('Palabek', 'Palabek'),
            ('Nakivale', 'Nakivale'),
            ('Oruchinga', 'Oruchinga'),
            ('Rwamwanja', 'Rwamwanja'),

        )
        NATIONALITY_CHOICES = (
            ('Uganda', 'Uganda'),
            ('Congo', 'Congo'),
            ('Sundan', 'Sundan'),
            ('South Sudan', 'South Sudan'),
        )
        REGION_CHOICES = (
            ('South West', 'South West'),
            ('West Nile', 'West Nile'),
            ('Karamoja', 'Karamoja')
        )
        COMPONENT_CHOICES = (
            ('SEMC', 'SEMC'),
            ('SP', 'SP'),
            ('LPD', 'LPD'),
            ('DFI', 'DFI'),
        )
        COMPONENTRECEIVED_CHOICES = (
            ('None', 'None'),
            ('Acquired access to land', 'Acquired access to land'),
            ('Conducting large scale production (1 acre and above)', 'Conducting large scale production (1 acre and above)'),
            ('Adoption of climate smart production', 'Adoption of climate smart production'),
            ('Acquired access to water for production', 'Acquired access to water for production'),
            ('Conducting back yard gardening', 'Conducting back yard gardening'),
            ('On-farm PHM practices', 'On-farm PHM practices'),
        )       
        CP_CHOICES = (
            ('WFP', 'WFP'),
            ('AFI', 'AFI'),
            ('KRC', 'KRC'),
            ('ACF', 'ACF'),
            ('FHI', 'FHI'),
            ('MTI', 'MTI'),
            ('LWF', 'LWF'),
            ('FHU', 'FHU'),
        )

        provider = models.CharField(max_length=20, choices=CP_CHOICES)
        name_of_participant = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_onfarm_participant')
        group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lpd_onfarm_group')        
        value_date = models.DateField()
        region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_onfarm_region')
        district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_onfarm_district')
        settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_onfarm_settlement')
        Onfarm_component_received = models.CharField(max_length=100, choices=COMPONENTRECEIVED_CHOICES, verbose_name="On-Farm Component received")
        component = models.CharField(max_length=10, default='LPD')
        
        # Actual field names
        actual_region = models.CharField(max_length=35)  # Store actual region name
        actual_district = models.CharField(max_length=35)  # Store actual district name
        actual_settlement = models.CharField(max_length=35)  # Store actual settlement name
        actual_group = models.CharField(max_length=100)  # Store actual group name

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "LPD On-Farm Details"

        def __str__(self):
            return f"LPD On-Farm Details for {self.beneficiary.name_of_household_head}"

# # Receiver to update actual field names
# @receiver(post_save, sender=LPDOnFarm)
# def update_actual_names(sender, instance, created, **kwargs):
#     if created:
#         beneficiary_instance = instance.beneficiary
#         if beneficiary_instance:
#             instance.actual_region = beneficiary_instance.region
#             instance.actual_district = beneficiary_instance.district
#             instance.actual_settlement = beneficiary_instance.settlement
#             instance.actual_group = beneficiary_instance.group.group_name
#         instance.save()    

class LPDOffFarm(models.Model):
   
        YESNO_CHOICES = (
            ('Yes', 'Yes'),
            ('No', 'No'),
            )
        GENDER_CHOICES = (
                ('Male', 'Male'),
                ('Female', 'Female'),
            )
        DISTRICT_CHOICES = (
            ('Koboko', 'Koboko'),
            ('Lamwo', 'Lamwo'),
            ('Isingiro', 'Isingiro'),
            ('Kamwenge', 'Kamwenge'),
        )
        SETTLEMENT_CHOICES = (
            ('Lobule', 'Lobule'),
            ('Palabek', 'Palabek'),
            ('Nakivale', 'Nakivale'),
            ('Oruchinga', 'Oruchinga'),
            ('Rwamwanja', 'Rwamwanja'),

        )
        NATIONALITY_CHOICES = (
            ('Uganda', 'Uganda'),
            ('Congo', 'Congo'),
            ('Sundan', 'Sundan'),
            ('South Sudan', 'South Sudan'),
        )
        REGION_CHOICES = (
            ('South West', 'South West'),
            ('West Nile', 'West Nile'),
            ('Karamoja', 'Karamoja')
        )
        COMPONENT_CHOICES = (
            ('SEMC', 'SEMC'),
            ('SP', 'SP'),
            ('LPD', 'LPD'),
            ('DFI', 'DFI'),
        )
        SOFTCOMPONENT_CHOICES = (
            ('None', 'None'),
            ('Training-Post harvest management', 'Training-Post harvest management'),
            ('Market linkages(Big buyers)', 'Market linkages -Big buyers'),
            ('Bulking - Storage infrastructure/tonnage', 'Bulking- Storage infrastructure/tonnage'),
        )      
        HARDCOMPONENT_CHOICES = (
            ('None', 'None'),
            ('Hermetic silos', 'Hermetic silos'),
            ('Mills', 'Mills'),
            ('Threshers', 'Threshers'),
            ('Transport facilities etc', 'Transport facilities etc'),
        )     

        CP_CHOICES = (
            ('WFP', 'WFP'),
            ('AFI', 'AFI'),
            ('KRC', 'KRC'),
            ('ACF', 'ACF'),
            ('FHI', 'FHI'),
            ('MTI', 'MTI'),
            ('LWF', 'LWF'),
            ('FHU', 'FHU'),
        )

        provider = models.CharField(max_length=20, choices=CP_CHOICES)        
        name_of_participant = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_offfarm_participant')
        group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lpd_offfarm_group')        
        value_date = models.DateField()
        region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_offfarm_region')
        district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_offfarm_district')
        settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_offfarm_settlement')
        Offfarm_Software_component_received = models.CharField(max_length=100, choices=SOFTCOMPONENT_CHOICES, verbose_name="Software Component received")
        Offfarm_Hardware_component_received = models.CharField(max_length=100, choices=HARDCOMPONENT_CHOICES, verbose_name="Hardware Component received")
        component = models.CharField(max_length=10, default='LPD')
        
        # Actual field names
        actual_region = models.CharField(max_length=35)  # Store actual region name
        actual_district = models.CharField(max_length=35)  # Store actual district name
        actual_settlement = models.CharField(max_length=35)  # Store actual settlement name
        actual_group = models.CharField(max_length=100)  # Store actual group name

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "LPD Off-Farm Details"

        def __str__(self):
            return f"LPD Off-Farm Details for {self.beneficiary.name_of_household_head}"
        
# # Receiver to update actual field names
# @receiver(post_save, sender=LPDOffFarm)
# def update_actual_names(sender, instance, created, **kwargs):
#     if created:
#         beneficiary_instance = instance.beneficiary
#         if beneficiary_instance:
#             instance.actual_region = beneficiary_instance.region
#             instance.actual_district = beneficiary_instance.district
#             instance.actual_settlement = beneficiary_instance.settlement
#             instance.actual_group = beneficiary_instance.group.group_name
#         instance.save()


class LPDNonFarm(models.Model):
   
        YESNO_CHOICES = (
            ('Yes', 'Yes'),
            ('No', 'No'),
            )
        GENDER_CHOICES = (
                ('Male', 'Male'),
                ('Female', 'Female'),
            )
        DISTRICT_CHOICES = (
            ('Koboko', 'Koboko'),
            ('Lamwo', 'Lamwo'),
            ('Isingiro', 'Isingiro'),
            ('Kamwenge', 'Kamwenge'),
        )
        SETTLEMENT_CHOICES = (
            ('Lobule', 'Lobule'),
            ('Palabek', 'Palabek'),
            ('Nakivale', 'Nakivale'),
            ('Oruchinga', 'Oruchinga'),
            ('Rwamwanja', 'Rwamwanja'),

        )
        NATIONALITY_CHOICES = (
            ('Uganda', 'Uganda'),
            ('Congo', 'Congo'),
            ('Sundan', 'Sundan'),
            ('South Sudan', 'South Sudan'),
        )
        REGION_CHOICES = (
            ('South West', 'South West'),
            ('West Nile', 'West Nile'),
            ('Karamoja', 'Karamoja')
        )
        COMPONENT_CHOICES = (
                ('SEMC', 'SEMC'),
                ('SP', 'SP'),
                ('LPD', 'LPD'),
                ('DFI', 'DFI'),
            )
        NFSOFTCOMPONENT_CHOICES = (
            ('None', 'None'),
            ('Skill acquisition training', 'Skill acquisition training'),
            ('Apprenticeship', 'Apprenticeship'),
            
        )      
        NFHARDCOMPONENT_CHOICES = (
            ('None', 'None'),
            ('Start-up capital received', 'Start-up capital received'),
        )     
        CP_CHOICES = (
            ('WFP', 'WFP'),
            ('AFI', 'AFI'),
            ('KRC', 'KRC'),
            ('ACF', 'ACF'),
            ('FHI', 'FHI'),
            ('MTI', 'MTI'),
            ('LWF', 'LWF'),
            ('FHU', 'FHU'),
        )

        provider = models.CharField(max_length=20, choices=CP_CHOICES)
        name_of_participant = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_nonfarm_participant')
        group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lpd_nonfarm_group')        
        value_date = models.DateField()
        region = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_nonfarm_region')
        district = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_nonfarm_district')
        settlement = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name='lpd_nonfarm_settlement')
        nonfarm_Software_component_received = models.CharField(max_length=100, choices=NFSOFTCOMPONENT_CHOICES, verbose_name="Software Component received")
        nonfarm_Hardware_component_received = models.CharField(max_length=100, choices=NFHARDCOMPONENT_CHOICES, verbose_name="Hardware Component received")
        component = models.CharField(max_length=10, default='LPD')
        
        # Actual field names
        actual_region = models.CharField(max_length=35)  # Store actual region name
        actual_district = models.CharField(max_length=35)  # Store actual district name
        actual_settlement = models.CharField(max_length=35)  # Store actual settlement name
        actual_group = models.CharField(max_length=100)  # Store actual group name

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "LPD Non-Farm Details"

        def __str__(self):
            return f"LPD Non-Farm Details for {self.beneficiary.name_of_household_head}"



