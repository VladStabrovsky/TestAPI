from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from django.http import HttpResponse
from django.shortcuts import render

import datetime
import csv
import re
import os

from API.models import *
# Create your views here.

def index(request):
    return render(request, 'API/index.html')
class user_credits(APIView):
    def get(self, request, user_id):
        credits_queryset = Credits.objects.filter(user = user_id)
        response = {'credits': []}
        for credit in credits_queryset:
            payments_queryset = Payments.objects.filter(credit = credit)
            credit_data = {}
            credit_data['issuance_date'] = credit.issuance_date
            credit_data['return_date'] = credit.return_date
            credit_data['body'] = credit.body
            credit_data['percent'] = credit.percent
            if credit.actual_return_date == None:
                overdue_days = (datetime.date.today() - datetime.date(year=credit.return_date.year, month=credit.return_date.month, day=credit.return_date.day)).days
                credit_data['close'] = False
                credit_data['overdue_days'] = overdue_days
                credit_data['payments_sum_body'] = sum(payment.sum for payment in payments_queryset.filter(type__name='тіло'))
                credit_data['payments_sum_percent'] = sum(payment.sum for payment in payments_queryset.filter(type__name='відсотки'))
            else:
                credit_data['close'] = True
                credit_data['payments_sum'] = sum(payment.sum for payment in payments_queryset)
            response['credits'].append(credit_data)
        return Response(response)

class plans_insert(APIView):
    def post(self, request):
        file = request.data['file']
        plans = csv.DictReader(file.read().decode().splitlines(), delimiter='\t')
        response = {'plans':[]}
        for plan in plans:
            day = int(plan["period"].split(".")[0])
            period = f'{plan["period"].split(".")[2]}-{plan["period"].split(".")[1]}-{plan["period"].split(".")[0]}'
            if len(Plans.objects.filter(period=period, category__name=plan['category'])) != 0:
                response['plans'].append({**plan, **{   'success': False,
                                                        'message':'План присутній в базі даних'}})
                continue
            if day != 1:
                response['plans'].append({**plan, **{'success': False,
                                                     'message': 'Невірна дата'}})
                continue
            if plan['sum'] == '':
                response['plans'].append({**plan, **{'success': False,
                                                     'message': 'Відсутнє значення суми'}})
                continue
            Plans.objects.create(period=period,
                                 sum=float(plan['sum']),
                                 category_id=Dictionary.objects.get(name=plan['category']).pk)
            response['plans'].append({**plan, **{'success': True,
                                                 'message': 'Додано в базу даних'}})
        return Response(response)

class plans_performance(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        if date is None:
            return Response({'message':'Невказана дата'}, status=400)
        response = {'plans':[]}
        check_date = datetime.date(year=int(date.split(".")[2]), month=int(date.split(".")[1]), day=int(date.split(".")[0]))
        plans_queryset = Plans.objects.filter(period__lte=check_date)
        for plan in plans_queryset:
            plan_data = {}
            plan_data['period'] = plan.period
            plan_data['category'] = plan.category.name
            plan_data['sum'] = plan.sum
            response['plans'].append(plan_data)
            if plan.category == Dictionary.objects.get(name='видача'):
                if plan.period.month == check_date.month and plan.period.year == check_date.year:
                    credits_queryset = Credits.objects.filter(issuance_date__gte=plan.period, issuance_date__lte=check_date)
                else:
                    credits_queryset = Credits.objects.filter(issuance_date__month=plan.period.month, issuance_date__year=plan.period.year)
                plan_data['credits_sum'] = sum(credit.body for credit in credits_queryset)
                plan_data['percent'] = round(plan_data['credits_sum']/plan_data['sum'],3)
            elif plan.category == Dictionary.objects.get(name='збір'):
                if plan.period.month == check_date.month and plan.period.year == check_date.year:
                    payments_queryset = Payments.objects.filter(payment_date__gte=plan.period, payment_date__lte=check_date)
                else:
                    payments_queryset = Payments.objects.filter(payment_date__month=plan.period.month, payment_date__year=plan.period.year)
                plan_data['payments_sum'] = sum(payment.sum for payment in payments_queryset)
                plan_data['percent'] = round(plan_data['payments_sum']/plan_data['sum'],3)
        return Response(response)

class year_performance(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        if year is None:
            return Response({'message': 'Невказан рік'}, status=400)
        response = {'months':[]}
        issuance_year_sum = sum(credit.body for credit in Credits.objects.filter(issuance_date__year=year))
        payments_year_sum = sum(payment.sum for payment in Payments.objects.filter(payment_date__year=year))
        for month in range(1, 13):
            print(month)
            month_data = {}
            month_data['period'] = f'{month}.{year}'
            credits_queryset = Credits.objects.filter(issuance_date__month=month, issuance_date__year=year)
            month_data['issuance_count'] = credits_queryset.count()
            month_data['issuance_sum'] = sum(credit.body for credit in credits_queryset)
            if issuance_year_sum > 0:
                month_data['year_issuance_percent'] = round(month_data['issuance_sum'] / issuance_year_sum,3)

            payments_queryset = Payments.objects.filter(payment_date__month=month, payment_date__year=year)
            month_data['payments_count'] = payments_queryset.count()
            month_data['payments_sum'] = sum(payment.sum for payment in payments_queryset)
            if payments_year_sum > 0:
                month_data['year_payments_percent'] = round(month_data['payments_sum'] / payments_year_sum,3)

            plans = Plans.objects.filter(period__month=month, period__year=year)
            if plans.count() == 0:
                response['months'].append(month_data)
                continue
            issuance_plan = plans.filter(category__name='видача')
            if issuance_plan.count() != 0:
                month_data['issuance_plan_sum'] = issuance_plan.first().sum
                if month_data['issuance_plan_sum'] > 0:
                    month_data['issuance_percent'] = round(month_data['issuance_sum'] / month_data['issuance_plan_sum'],3)
            payments_plan = plans.filter(category__name='збір')
            if payments_plan.count() != 0:
                month_data['payments_plan_sum'] = payments_plan.first().sum
                if month_data['payments_plan_sum'] > 0:
                    month_data['payments_percent'] = round(month_data['payments_sum'] / month_data['payments_plan_sum'],3)
            response['months'].append(month_data)
        return Response(response)
