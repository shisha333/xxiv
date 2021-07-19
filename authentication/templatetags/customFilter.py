import random
import string
import csv
from django.shortcuts import get_object_or_404
from django import template
from django.shortcuts import HttpResponse
from xxivapp.models import Payment,Stock,Product,Order,Discount,Taxes,Customer
from django.utils  import timezone
from authentication.models import User
from django.db.models import Count, Sum

from xxivapp.models import (
   Payment,Stock,Product,Order,Discount,Taxes,Customer,CustomOrder

)
register = template.Library()

@register.filter
def get_items(parameter_list):
    """
    docstring
    """
    items = Product.objects.all()
    return items

@register.filter
def random_background(text):
    colors = ['primary', 'success', 'danger', 'warning']
    return random.choice(colors)

@register.filter
def display(name, names):
    print("name")
    print("names")
    return "https://google.com"
    
@register.filter
def get_daily_order(bundle_id):
    time = timezone.now()
    orders = Order.objects.filter(created_at=time).filter(bundle=bundle_id)
    return orders

@register.filter
def count_queryset(queryset):
    return queryset.count()

@register.filter
def get_user_objects(user_id):
    user = User.objects.filter(id=user_id).first()
    return user

@register.filter
def get_bundle_by_location(district):
    locations = []
    districts_orders = Order.objects.all()[0:0]
    orders = Order.objects.all()
    
    for location in orders:
        if location not in locations:
            locations.append(location)
        else:
            pass
    for location in locations:
        districts_orders = Order.objects.all().filter(agent__district=district)
    
    return queryset.count()

@register.filter
def get_bundle_cover(bundle_name):
    if bundle_name == "ICYANGA" or bundle_name == "icyanga":
        return "/public/bundlepics/ICYANGA.png"
    elif bundle_name == "UBUZIMA" or bundle_name == "ubuzima":
        return "/public/bundlepics/UBUZIMA.png"
    elif bundle_name == "UBWUZU" or bundle_name == "ubwuzu":
        return "/public/bundlepics/UBWUZU.png"
    elif bundle_name == "TWIHAZE" or bundle_name == "Css":
        return "/public/bundlepics/TWIHAZE.png"
    elif bundle_name == "UMUFUNGO W'UMUHINZI" or bundle_name == "Css":
        return "/public/bundlepics/Food Bundle Image3.png"


@register.filter
def random_background(text):
    colors = ['primary', 'success', 'redness', 'warning']
    return random.choice(colors)

@register.filter
def get_price_of_item(item):
    item = Product.objects.get(id=item)
    return item.price

@register.filter
def get_path(request):
    path = request.path_info+'export/'
    return path

@register.filter
def get_path(request):
    path = request.path_info+'export/'
    return path
    
@register.filter
def times(number):
    return range(number)

@register.filter
def add(a, b):
    return a + b

@register.filter
def substract(a, b):
    return a - b

@register.filter
def multiply(a, b):
    return a * b

@register.filter
def devide(a, b):
    return a / b

@register.filter
def get_total_bundle_cost(n):
    items = []
    bundles = Bundle.objects.all()
    total_bundle_cost = 0
    bundle_cost = 0
    for bundle in bundles:
        time = timezone.now()
        orders = Order.objects.filter(created_at=time).filter(status=1).filter(bundle_id=bundle).values('bundle').annotate(number_of_count=Count('id'))
        cost = 0
        cost_of_bundle_productivity = BundleCost.objects.filter(id=1).first()
        if cost_of_bundle_productivity:
            bundle_cost = cost_of_bundle_productivity.cost()
        else:
            bundle_cost = 0
        for bundle_item in BundleItems.objects.filter(bundle_id=bundle):
            if bundle_item not in items:
                items.append(bundle_item)
                cost_per_piece = bundle_item.item.price / bundle_item.item.pieces + bundle_item.item.transport 
                cost += (cost_per_piece*bundle_item.number)
            else:
                continue
            
        for order in orders:
            total_bundle_cost += (cost*order['number_of_count'])
    return "%.2f"%(total_bundle_cost + bundle_cost)

@register.filter
def get_total_bundle_change(n):
    bundles = Bundle.objects.all()
    total_bundle_change = 0
    for bundle in bundles:
        
        cost_of_bundle = 0
        for bundle_item in BundleItems.objects.filter(bundle_id=bundle):
            cost_per_piece = bundle_item.item.price / bundle_item.item.pieces
            cost_of_bundle += (cost_per_piece*bundle_item.number)
            
        fixed_price = PriceVariation.objects.filter(bundle_id=bundle).reverse().first()
        if fixed_price is None:
            fixed_bundle_price = 0
        else:
            fixed_bundle_price = fixed_price.fixed
            
        time = timezone.now()
        orders = Order.objects.filter(created_at=time).filter(status=1).filter(bundle_id=bundle)
        
        total_bundle_change += ( (fixed_bundle_price-cost_of_bundle) * len(orders) )
        
        return "%.2f"%total_bundle_change

@register.filter
def total_bundle_profit_rate(n):
    # bundle CHANGE
    bundles = Bundle.objects.all()
    total_bundle_change = 0
    for bundle in bundles:
        
        cost_of_bundle = 0
        for bundle_item in BundleItems.objects.filter(bundle_id=bundle):
            cost_per_piece = bundle_item.item.price / bundle_item.item.pieces
            cost_of_bundle += (cost_per_piece*bundle_item.number)
            
        fixed_price = PriceVariation.objects.filter(bundle_id=bundle).reverse().first()
        if fixed_price is None:
            fixed_bundle_price = 0
        else:
            fixed_bundle_price = fixed_price.fixed
            
        time = timezone.now()
        orders = Order.objects.filter(created_at=time).filter(status=1).filter(bundle_id=bundle)
        
        total_bundle_change += ( (fixed_bundle_price-cost_of_bundle) * len(orders) )
        
    # BUNDLE COST
    total_bundle_cost = 0
    for bundle in bundles:
        time = timezone.now()
        orders = Order.objects.filter(created_at=time).filter(status=1).filter(bundle_id=bundle).values('bundle').annotate(number_of_count=Count('id'))
        cost = 0
        for bundle_item in BundleItems.objects.filter(bundle_id=bundle):
            cost_per_piece = bundle_item.item.price / bundle_item.item.pieces
            cost += (cost_per_piece*bundle_item.number)
            
        for order in orders:
            total_bundle_cost += (cost*order['number_of_count'])
    if total_bundle_cost == 0:
        rate = (total_bundle_change*100)/1
    else:
        rate = (total_bundle_change*100)/total_bundle_cost
    
    return "%.2f"%rate

@register.filter
def get_total_amount_of_farmer(farmer):
    stocks = Stock.objects.filter(request__farmer=farmer)
    sub_total = 0
    for stock in stocks:
        sub_total += stock.quantity_received * stock.request.item.price
        
    return sub_total

def get_bundle_item_make_loss_or_profit(bundle_id):
    bundle = Bundle.objects.filter(id=bundle_id).first()
    
    item_for_low_profit = {"id":0, "name":"name","price_in_bundle":0, "low_profit_rate":0}
    item_for_high_profit = {"id":0, "name":"name","price_in_bundle":0, "high_profit_rate":0}
    
    low_price = 0
    high_price = 0
    
    bundle_items = BundleItems.objects.filter(bundle=bundle)
    
    for bundle_item in bundle_items:
        cost_per_piece = (bundle_item.item.price / bundle_item.item.pieces) + (bundle_item.item.transport / bundle_item.item.pieces)
        profit_per_piece = bundle_item.item.profit / bundle_item.item.pieces
        price_per_piece = cost_per_piece + profit_per_piece
        
        item_market_price = price_per_piece * bundle_item.number
        # market_price += item_market_price
        
        # price = (bundle_item.item.price / bundle_item.item.pieces) * bundle_item.number
        price = item_market_price
        if low_price == high_price and high_price == 0 and low_price == 0:
            high_price = price
            low_price = price
            
            item_for_low_profit.update(
                {
                    "id":bundle_item.item.id, "name":bundle_item.item,"price_in_bundle":price
                }
            )
            
            item_for_high_profit.update(
                {
                    "id":bundle_item.item.id, "name":bundle_item.item,"price_in_bundle":price
                }
            )
            
        elif price > low_price:
            if price > high_price:
                high_price = price
                item_for_high_profit.update(
                    {
                        "id":bundle_item.item.id, "name":bundle_item.item,"price_in_bundle":price
                    }
                )
            else:
                pass
        elif price < low_price:
            if price < low_price:
                low_price = price
                item_for_low_profit.update(
                    {
                        "id":bundle_item.item.id, "name":bundle_item.item,"price_in_bundle":price
                    }
                )
            else:
                pass
    fixed_price  = float(bundle.fixed_price())
    if fixed_price:
        low_profit_rate = (low_price * 100)/fixed_price
        high_profit_rate = (high_price * 100)/fixed_price
    else:
        low_profit_rate = high_profit_rate = 0
    
    item_for_low_profit.update(
        {
            "low_profit_rate":low_profit_rate
        }
    )
    item_for_high_profit.update(
        {
            "high_profit_rate":high_profit_rate
        }
    )
    
    return item_for_low_profit, item_for_high_profit

