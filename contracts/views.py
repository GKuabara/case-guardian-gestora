from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg, Count
from django.http import HttpResponse
from .models import Contract, Parcel
from .serializers import ContractSerializer


def index(request):
    latest_question_list = Contract.objects.order_by('issue_date')[:5]
    output = ', '.join([q.document_number for q in latest_question_list])
    return HttpResponse(output)


class ContractCreateAPIView(APIView):
    def post(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractListAPIView(APIView):
    def get(self, request):
        filters = {
            'contract_id': request.query_params.get('contract_id'),
            'document_number': request.query_params.get('document_number'),
            'issue_date': request.query_params.get('issue_date'),
            'issue_date__month': request.query_params.get('month'),
            'issue_date__year': request.query_params.get('year'),
            'state': request.query_params.get('state'),
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        contracts = Contract.objects.filter(**filters)
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractSummaryAPIView(APIView):
    def get(self, request):
        filters = {
            'document_number': request.query_params.get('document_number'),
            'issue_date__day': request.query_params.get('day'),
            'issue_date__month': request.query_params.get('month'),
            'issue_date__year': request.query_params.get('year'),
            'state': request.query_params.get('state'),
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        summary = Contract.objects.filter(**filters).aggregate(
            total_amount_disbursed = Sum('amount'),
            total_number_of_contracts = Count('contract_id'),
            avg_contract_rate = Avg('contract_rate'),
        )
        total_receivable = Parcel.objects.filter(
            contract_id__in=Contract.objects.filter(**filters)
        ).aggregate(total_receivable=Sum('parcel_amount'))[
            'total_receivable'
        ]

        summary['total_receivable'] = total_receivable or 0
        return Response(summary)
