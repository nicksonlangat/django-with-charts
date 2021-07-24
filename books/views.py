from django.shortcuts import render
from django.db.models import Count,F,Sum,Avg
from django.db.models.functions import ExtractYear,ExtractMonth
from django.http import JsonResponse
from .models import Book, Purchase
from .utils import (
    months,colorDanger,
    colorPrimary,colorSuccess,
    generate_color_palette,get_year_dict)
# Create your views here.

def display_charts(request):
    return render(request, 'charts.html', {})

def filter_options(request):
    merged_purchases=Purchase.objects.annotate(
        year=ExtractYear(
            'time_created'
        )).values(
            'year'
            ).order_by(
                '-year'
                ).distinct()
    options= [purchase['year'] for purchase in merged_purchases]

    return JsonResponse(data={
        'options':options
    })



def get_annual_sales(request, year):
    purchases=Purchase.objects.filter(time_created__year=year)
    merged_purchases=purchases.annotate(
        price=F('book__price')
    ).annotate(month=ExtractMonth('time_created')).values(
        'month'
    ).annotate(
        average=Sum(
            'book__price'
        )
    ).values(
        'month',
        'average'
    ).order_by('month')
    sales_dict=get_year_dict()
    for merge in merged_purchases:
        sales_dict[months[merge['month']-1]]=round(merge['average'], 2)

    return JsonResponse({
        'title':f'Sales in {year}',
        'data':{
            'labels':list(sales_dict.keys()),
            'datasets':[{
                'label':'Amount (KSHS)',
                'backgroundColor':generate_color_palette(7),
                'borderColor':generate_color_palette(5),
                'data':list(sales_dict.values())
            }]
        }
    })


def payment_success_chart(request, year):
    purchases = Purchase.objects.filter(time_created__year=year)

    return JsonResponse({
        'title': f'Payment success rate in {year}',
        'data': {
            'labels': ['Successful', 'Unsuccessful'],
            'datasets': [{
                'label': 'Amount (KSHS)',
                'backgroundColor': generate_color_palette(12),
                'borderColor': generate_color_palette(9),
                'data': [
                    purchases.filter(is_successful=True).count(),
                    purchases.filter(is_successful=False).count(),
                ],
            }]
        },
    })


def payment_method_chart(request, year):
    purchases = Purchase.objects.filter(time_created__year=year)
    merged_purchases = purchases.values('payment_method').annotate(count=Count('id'))\
        .values('payment_method', 'count').order_by('payment_method')

    payment_method_dict = dict()

    for payment_method in Purchase.PAYMENT_METHODS:
        payment_method_dict[payment_method[1]] = 0

    for group in merged_purchases:
        payment_method_dict[dict(Purchase.PAYMENT_METHODS)[group['payment_method']]] = group['count']

    return JsonResponse({
        'title': f'Payment method rate in {year}',
        'data': {
            'labels': list(payment_method_dict.keys()),
            'datasets': [{
                'label': 'Amount (Number)',
                'backgroundColor': generate_color_palette(len(payment_method_dict)),
                'borderColor': generate_color_palette(len(payment_method_dict)),
                'data': list(payment_method_dict.values()),
            }]
        },
    })

def spend_per_customer_chart(request, year):
    purchases = Purchase.objects.filter(time_created__year=year)
    grouped_purchases = purchases.annotate(price=F('book__price')).annotate(month=ExtractMonth('time_created'))\
        .values('month').annotate(average=Avg('book__price')).values('month', 'average').order_by('month')

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group['month']-1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Spend per customer in {year}',
        'data': {
            'labels': list(spend_per_customer_dict.keys()),
            'datasets': [{
                'label': 'Amount (KSHS)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(spend_per_customer_dict.values()),
            }]
        },
    })





