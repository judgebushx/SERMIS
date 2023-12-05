from django.db import models

from django.core.exceptions import ValidationError 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count


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
        return self.beneficiary_set.exclude(nationality='Uganda').count()

    @property
    def male_refugees(self):
        return self.beneficiary_set.exclude(nationality='Uganda', gender_of_participant='Male').count()

    @property
    def female_refugees(self):
        return self.beneficiary_set.exclude(nationality='Uganda', gender_of_participant='Female').count()

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
        self.update_member_counts()
        super().save(*args, **kwargs)

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

    group = models.ForeignKey(Group, on_delete=models.CASCADE)   
    region = models.CharField(max_length=100, choices=REGION_CHOICES)
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
    settlement = models.CharField(max_length=100, choices=SETTLEMENT_CHOICES)    
    nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES)
    household_id = models.CharField(max_length=12)
    name_of_household_head = models.CharField(max_length=100)
    household_head_phone = models.IntegerField(validators=[MaxValueValidator(999999999, message="9 digits maximum" )]  )
    gender_of_participant = models.CharField(max_length=10, choices=GENDER_CHOICES)
    participant_age = models.IntegerField(validators=[MaxValueValidator(99, message="Maximum age should be 99 years or less."), MinValueValidator(0, message="Age cannot be negative."),])
    participant_photo = models.ImageField(upload_to='beneficiary_photos/', null=True, blank=True)
    relationship_with_household_head = models.CharField(max_length=100, choices=RELHH_CHOICES)
    gender_hhh = models.CharField(max_length=100, choices=GENDER_CHOICES, verbose_name="Gender of HH Head")
    age_of_hhh = models.IntegerField(validators=[MaxValueValidator(99, message="Maximum age should be 99 years or less."), MinValueValidator(0, message="Age cannot be negative."),], verbose_name="Age of HH Head")
    disablity_of_hhh = models.CharField(max_length=100, choices=DISABILITY_CHOICES)
    marital_status = models.CharField(max_length=100, choices=MARITALSTATUS_CHOICES)
    education_level = models.CharField(max_length=100, choices=EDUCLEVEL_CHOICES)
    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES)        
    household_own_any_livestock = models.CharField(max_length=100, choices=YESNO_CHOICES)


    def update_group_member_counts(sender, instance, **kwargs):
        group = instance.group
        beneficiaries = Beneficiary.objects.filter(group=group)

        group.total_members = beneficiaries.count()
        group.male_members = beneficiaries.filter(gender_of_participant='Male').count()
        group.female_members = beneficiaries.filter(gender_of_participant='Female').count()
        group.num_refugees = beneficiaries.filter(nationality='Refugee').count()
        group.male_refugees = beneficiaries.filter(nationality='Refugee', gender_of_participant='Male').count()
        group.female_refugees = beneficiaries.filter(nationality='Refugee', gender_of_participant='Female').count()
        group.num_youth = beneficiaries.filter(participant_age__lte=30).count()
        group.male_youth = beneficiaries.filter(participant_age__lte=30, gender_of_participant='Male').count()
        group.female_youth = beneficiaries.filter(participant_age__lte=30, gender_of_participant='Female').count()
        group.num_disabilities = beneficiaries.filter(disablity_of_hhh='Living with a disability').count()

        group.save()
   
    def __str__(self):
            return self.name_of_household_head
    
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
            ('Sundan', 'Sundan'),
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
        group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
        meeting_date = models.DateField()        
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=100, choices=SETTLEMENT_CHOICES)        
        topic_of_discussion = models.CharField(max_length=100, choices=TOPIC_CHOICES)
        component = models.CharField(max_length=10, default='SEMC')

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)


        class Meta:
            verbose_name_plural = "Community Participation Details"

        def __str__(self):
            return f"Community Participation Details for {self.beneficiary.name_of_household_head}"    

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
            ('Sundan', 'Sundan'),
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
        group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)   
        meeting_date = models.DateField()
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=100, choices=SETTLEMENT_CHOICES)        
        topic_of_discussion = models.CharField(max_length=100, choices=TOPIC_CHOICES)    
        component = models.CharField(max_length=10, default='SEMC')
        
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
            ('Sundan', 'Sundan'),
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
        group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
        meeting_date = models.DateField()
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=100, choices=SETTLEMENT_CHOICES)        
        mentor_name =  models.CharField(max_length=30)
        topic_of_discussion = models.CharField(max_length=100, choices=TOPIC_CHOICES)
        component = models.CharField(max_length=10, default='SEMC')
        
        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "Mentoring and Coaching Details"

        def __str__(self):
            return f"Mentoring and Coaching Details for {self.beneficiary.name_of_household_head}"   
        

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

        provider = models.CharField(max_length=20, choices=CP_CHOICES)
        disbursement_date = models.DateField()
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)        
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=20, choices=SETTLEMENT_CHOICES)
        group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
        household_beneficiary_name = models.CharField(max_length=25)
        transfer_value = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
        component = models.CharField(max_length=10, default='SP')
        
        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)
        
        class Meta:
            verbose_name_plural = "GFA Details"

        def __str__(self):
            return f"GFA Details for {self.beneficiary.name_of_household_head}"
        
class SPNutricash(models.Model):
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
            ('Uganda' 'Uganda'),
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

        provider = models.CharField(max_length=20, choices=CP_CHOICES)
        disbursement_date = models.DateField()
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)        
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=20, choices=SETTLEMENT_CHOICES)
        group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
        household_beneficiary_name = models.CharField(max_length=25)
        pregnant_mother= models.CharField(max_length=4, choices = YESNO_CHOICES, default='No')
        lactating_mother = models.CharField(max_length=4, choices = YESNO_CHOICES, default='No')
        transfer_value = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
        component = models.CharField(max_length=10, default='SP')

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "Nutricash Details"

        def __str__(self):
            return f"Nutricash Details for {self.beneficiary.name_of_household_head}"

class SPSAGE(models.Model):
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

        
        def validate_household_beneficiary_age(value):
            if value < 80 or value > 100:
                raise ValidationError('Household beneficiary age must be between 80 and 100 inclusive.')
            
        provider = models.CharField(max_length=20, choices=CP_CHOICES)
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
        group = models.ForeignKey(Group, on_delete=models.CASCADE)        
        disbursement_date = models.DateField()
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=20, choices=SETTLEMENT_CHOICES)
        household_beneficiary_name = models.CharField(max_length=25)
        household_beneficiary_age = models.IntegerField(validators=[validate_household_beneficiary_age])
        transfer_value =models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
        component = models.CharField(max_length=10, default='SP')

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)
                
        class Meta:
            verbose_name_plural = "SAGE Details"

        def __str__(self):
            return f"SAGE Details for {self.beneficiary.name_of_household_head}"
        

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
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
        group = models.ForeignKey(Group, on_delete=models.CASCADE)        
        value_date = models.DateField()
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=20, choices=SETTLEMENT_CHOICES)
        Onfarm_component_received = models.CharField(max_length=100, choices=COMPONENTRECEIVED_CHOICES, verbose_name="On-Farm Component received")
        component = models.CharField(max_length=10, default='LPD')

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "LPD On-Farm Details"

        def __str__(self):
            return f"LPD On-Farm Details for {self.beneficiary.name_of_household_head}"
        

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
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
        group = models.ForeignKey(Group, on_delete=models.CASCADE)        
        value_date = models.DateField()
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=20, choices=SETTLEMENT_CHOICES)
        Offfarm_Software_component_received = models.CharField(max_length=100, choices=SOFTCOMPONENT_CHOICES, verbose_name="Software Component received")
        Offfarm_Hardware_component_received = models.CharField(max_length=100, choices=HARDCOMPONENT_CHOICES, verbose_name="Hardware Component received")
        component = models.CharField(max_length=10, default='LPD')

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "LPD Off-Farm Details"

        def __str__(self):
            return f"LPD Off-Farm Details for {self.beneficiary.name_of_household_head}"
        

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
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
        group = models.ForeignKey(Group, on_delete=models.CASCADE)        
        value_date = models.DateField()
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        settlement = models.CharField(max_length=20, choices=SETTLEMENT_CHOICES)
        nonfarm_Software_component_received = models.CharField(max_length=100, choices=NFSOFTCOMPONENT_CHOICES, verbose_name="Software Component received")
        nonfarm_Hardware_component_received = models.CharField(max_length=100, choices=NFHARDCOMPONENT_CHOICES, verbose_name="Hardware Component received")
        component = models.CharField(max_length=10, default='LPD')

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "LPD Non-Farm Details"

        def __str__(self):
            return f"LPD Non-Farm Details for {self.beneficiary.name_of_household_head}"
        
class DFI(models.Model):
   
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

        provider = models.CharField(max_length=20, choices=CP_CHOICES)
        beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
        group = models.ForeignKey(Group, on_delete=models.CASCADE)        
        value_date = models.DateField()
        region = models.CharField(max_length=20, choices=REGION_CHOICES)
        district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
        settlement = models.CharField(max_length=20, choices=SETTLEMENT_CHOICES)
        DFI_Software_component_received = models.CharField(max_length=100, choices=DFISOFTCOMPONENT_CHOICES, verbose_name="Software Component received")
        component = models.CharField(max_length=10, default='LPD')

        def save(self, *args, **kwargs):
            # If the group and beneficiary are not already set, set them automatically
            if not self.group_id:
                self.group = self.beneficiary.group

            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = "DFI Non-Farm Details"

        def __str__(self):
            return f"DFI Details for {self.beneficiary.name_of_household_head}"