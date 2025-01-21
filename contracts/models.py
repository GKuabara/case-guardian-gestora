from django.db import models


class Contract(models.Model):
    contract_id = models.BigAutoField(primary_key=True)
    issue_date = models.DateField()
    birth_date = models.DateField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    document_number = models.CharField(max_length=11)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    contract_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.document_number} in {self.issue_date}: R$ {self.amount}'


class Parcel(models.Model):
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='parcels')
    parcel_number = models.PositiveIntegerField()
    parcel_amount = models.DecimalField(max_digits=11, decimal_places=2)
    due_date = models.DateField()

    class Meta:
        unique_together = ('contract_id', 'parcel_number')  # Ensure parcel_number uniqueness per contract

    def __str__(self):
        return f'Contract {self.contract_id} in {self.parcel_number}: R$ {self.parcel_amount}'
    