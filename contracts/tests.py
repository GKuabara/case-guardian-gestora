from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Contract, Parcel

class ContractAPITestCase(APITestCase):

    def setUp(self):
        # Create test data
        self.contract1 = Contract.objects.create(
            issue_date="2025-01-01",
            birth_date="2000-01-01",
            amount=10000,
            document_number="12345678901",
            country="Brazil",
            state="SP",
            city="São Carlos",
            phone_number="11123456789",
            contract_rate=3.5
        )
        self.contract2 = Contract.objects.create(
            issue_date="2025-02-03",
            birth_date="1990-01-01",
            amount=20000,
            document_number="98765432101",
            country="Brazil",
            state="RJ",
            city="Rio de Janeiro",
            phone_number="21987654321",
            contract_rate=4.5
        )
        Parcel.objects.create(contract_id=self.contract1, parcel_number=1, due_date="2025-03-01", parcel_amount=5000)
        Parcel.objects.create(contract_id=self.contract1, parcel_number=2, due_date="2025-04-01", parcel_amount=5000)
        Parcel.objects.create(contract_id=self.contract2, parcel_number=1, due_date="2025-05-01", parcel_amount=20000)

    def test_create_contract(self):
        url = reverse('contracts:contracts-create')
        data = {
            "issue_date": "2025-03-01",
            "birth_date": "1985-01-01",
            "amount": 15000,
            "document_number": "11122233344",
            "country": "Brazil",
            "state": "MG",
            "city": "Belo Horizonte",
            "phone_number": "31987654321",
            "contract_rate": 5.0,
            "parcels": [
                {"due_date": "2025-06-01", "parcel_amount": 7500},
                {"due_date": "2025-07-01", "parcel_amount": 7500}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.count(), 3)
        self.assertEqual(Parcel.objects.count(), 5)

    def test_list_contracts_filter_by_id(self):
        url = reverse('contracts:contracts-list')
        response = self.client.get(url, {'contract_id': self.contract1.contract_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['contract_id'], self.contract1.contract_id)

    def test_list_contracts_filter_by_document_number(self):
        url = reverse('contracts:contracts-list')
        response = self.client.get(url, {'document_number': '12345678901'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['document_number'], '12345678901')

    def test_list_contracts_filter_by_issue_date(self):
        url = reverse('contracts:contracts-list')
        response = self.client.get(url, {'issue_date': '2025-01-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['issue_date'], '2025-01-01')

    def test_list_contracts_filter_by_issue_year(self):
        url = reverse('contracts:contracts-list')
        response = self.client.get(url, {'year': 2025})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['issue_date'], '2025-01-01')
        self.assertEqual(response.data[1]['issue_date'], '2025-02-03')

    def test_list_contracts_filter_by_issue_year_moth(self):
        url = reverse('contracts:contracts-list')
        response = self.client.get(url, {'year': 2025, 'month': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['issue_date'], '2025-01-01')

    def test_list_contracts_filter_by_state(self):
        url = reverse('contracts:contracts-list')
        response = self.client.get(url, {'state': 'SP'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['state'], 'SP')

    def test_contract_summary(self):
        url = reverse('contracts:contracts-summary')
        response = self.client.get(url, {'state': 'SP'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_amount_disbursed'], 10000)
        self.assertEqual(response.data['total_number_of_contracts'], 1)
        self.assertEqual(response.data['avg_contract_rate'], 3.5)
        self.assertEqual(response.data['total_receivable'], 10000)

    def test_contract_summary_multiple_filters(self):
        url = reverse('contracts:contracts-summary')
        response = self.client.get(url, {
            'state': 'RJ',
            'document_number': '98765432101'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_amount_disbursed'], 20000)
        self.assertEqual(response.data['total_number_of_contracts'], 1)
        self.assertEqual(response.data['avg_contract_rate'], 4.5)
        self.assertEqual(response.data['total_receivable'], 20000)

    def test_contract_summary_no_results(self):
        url = reverse('contracts:contracts-summary')
        response = self.client.get(url, {'state': 'MG'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_amount_disbursed'], None)
        self.assertEqual(response.data['total_number_of_contracts'], 0)
        self.assertEqual(response.data['avg_contract_rate'], None)
        self.assertEqual(response.data['total_receivable'], 0)
