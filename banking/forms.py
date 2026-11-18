from django.contrib.auth.models import User
from django import forms


class TransferForm(forms.Form):

    recipient_name = forms.CharField(
        max_length=100,
        label="Recipient Name"
    )

    bank_name = forms.ChoiceField(
        choices=[
            ('Access Bank', 'Access Bank'),
            ('First Bank', 'First Bank'),
            ('GTBank', 'GTBank'),
            ('UBA', 'UBA'),
            ('Zenith Bank', 'Zenith Bank'),
            ('Moniepoint MFB', 'Moniepoint MFB'),
            ('Fidelity Bank', 'Fidelity Bank'),
            ('Opay', 'Opay'),
        ],
        label="Select Bank"
    )

    account_number = forms.CharField(
        max_length=10,
        min_length=10,
        label="Account Number"
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=1,
        label="Transfer Amount"
    )
    

class AirtimeForm(forms.Form):
    network = forms.ChoiceField(
        choices=[
            ('MTN', 'MTN'),
            ('Airtel', 'Airtel'),
            ('Glo', 'Glo'),
            ('9mobile', '9mobile'),
        ],
        label="Select Network"
    )

    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        label="Phone Number"
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=50,
        label="Airtime Amount"
    )


class DataBundleForm(forms.Form):
    network = forms.ChoiceField(
        choices=[
            ('MTN', 'MTN'),
            ('Airtel', 'Airtel'),
            ('Glo', 'Glo'),
            ('9mobile', '9mobile'),
        ],
        label="Select Network"
    )

    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        label="Phone Number"
    )

    data_plan = forms.ChoiceField(
        choices=[
            ('500MB', '500MB - ₦500'),
            ('1GB', '1GB - ₦1,000'),
            ('2GB', '2GB - ₦2,000'),
            ('5GB', '5GB - ₦4,000'),
            ('10GB', '10GB - ₦8,000'),
        ],
        label="Select Data Plan"
    )


class ElectricityForm(forms.Form):
    provider = forms.ChoiceField(
        choices=[
            ('AEDC', 'Abuja Electricity (AEDC)'),
            ('IKEDC', 'Ikeja Electric (IKEDC)'),
            ('EKEDC', 'Eko Electricity (EKEDC)'),
            ('IBEDC', 'Ibadan Electricity (IBEDC)'),
            ('EEDC', 'Enugu Electricity (EEDC)'),
        ],
        label="Select Electricity Provider"
    )

    meter_type = forms.ChoiceField(
        choices=[
            ('Prepaid', 'Prepaid'),
            ('Postpaid', 'Postpaid'),
        ],
        label="Meter Type"
    )

    meter_number = forms.CharField(
        max_length=13,
        min_length=10,
        label="Meter Number"
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=500,
        label="Payment Amount"
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {
            'email': 'Email Address',
        }

class TVSubscriptionForm(forms.Form):
    provider = forms.ChoiceField(
        choices=[
            ('DStv', 'DStv'),
            ('GOtv', 'GOtv'),
            ('StarTimes', 'StarTimes'),
        ],
        label="Select TV Provider"
    )

    smartcard_number = forms.CharField(
        max_length=15,
        min_length=8,
        label="Smartcard/IUC Number"
    )

    package = forms.ChoiceField(
        choices=[
            ('Basic', 'Basic'),
            ('Standard', 'Standard'),
            ('Premium', 'Premium'),
        ],
        label="Select Subscription Package"
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=500,
        label="Subscription Amount"
    )

class WaterBillForm(forms.Form):
    provider = forms.ChoiceField(
        choices=[
            ('Abuja Water Board', 'Abuja Water Board'),
            ('Lagos Water Corporation', 'Lagos Water Corporation'),
            ('Kano Water Board', 'Kano Water Board'),
        ],
        label="Select Water Provider"
    )

    customer_number = forms.CharField(
        max_length=20,
        min_length=5,
        label="Customer Account Number"
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=500,
        label="Payment Amount"
    )