from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text
import json


mydb = create_engine('mysql+pymysql://' + 'root' + ':' + 'password' + '@' + '49.205.199.235' + ':' + str(3306) + '/' + 'shivadb_new' , echo=False)
try:
    conn = mydb.connect()
except Exception as err:
    print(err)



def index(request):
    template = loader.get_template("result_Home.html")
    # results = VisaGetlist.objects.all()
    context = {'user': 'arun'}
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)

from .forms import LoginForm
from .models import LoginModel

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        # Check if the user with the given mobile_number or email already exists
        mobile_number = form.data.get('mobile_number')
        email = form.data.get('email')

        existing_user = None

        if mobile_number:
            existing_user = LoginModel.objects.filter(mobile_number=mobile_number).first()
        elif email:
            existing_user = LoginModel.objects.filter(email=email).first()

        if existing_user:
            # print(existing_user)
            # when  existing_user found then sesion store the user and go to back page 
            # # User with the given mobile_number or email already exists
            # form.add_error(None, 'User with this mobile number or email already exists.')
            request.session['user_id'] = existing_user.id
            return render(request, 'result_Home.html', {'form': form})

        # Proceed with form validation if the user does not already exist
        if form.is_valid():
            # Form is valid, continue processing
            form.save()
            return render(request, 'result_login.html', {'form': form})  # Replace 'success_url' with the actual URL or name of the success page
        else:
            # Form is not valid, include form in the context to preserve values
            return render(request, 'result_login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'result_login.html', {'form': form})

def logout_view(request):
    current_page = request.get_full_path()
    # Remove the 'user_id' from the session
    if 'user_id' in request.session:
        del request.session['user_id']

    # Redirect to a different page after logout, for example, the home page
    return render(request, 'result_Home.html')


def cart(request):
    template = loader.get_template("result_Cart.html")
    # results = VisaGetlist.objects.all()
    context = {'user': 'arun'}
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)


def list_product(request):
    template = loader.get_template("list_product.html")
    # results = VisaGetlist.objects.all()
    try:
        generated_org_id = request.session['generated_org_id']
        json_result,json_result_1,item_rows = check_generated_org_id(request)
    except:
        json_result,json_result_1,item_rows = None, None, None
    print(json_result)
    context = {'logo_url': json_result,'org_name': json_result_1,'item_rows':item_rows}
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)



def list_product_details(request):
    template = loader.get_template("result_ProductDetails.html")
    print("result_ProductDetails.html")
    # results = VisaGetlist.objects.all()
    try:
        generated_org_id = request.session['generated_org_id']
        json_result,json_result_1,item_rows = check_generated_org_id(request)
    except:
        json_result,json_result_1,item_rows = None, None, None
    print(json_result)
    context = {'logo_url': json_result,'org_name': json_result_1,'item_rows':item_rows}
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)



def forget_password(request):
    template = loader.get_template("result_Forget.html")
    # results = VisaGetlist.objects.all()
    context = {'user': 'arun'}
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)

def check_generated_org_id(_request):

    # Get generated_org_id from session
    generated_org_id = _request.session.get('generated_org_id')
    print(
        generated_org_id
    )
    # SQL query
    # SQL query for user_app_generate_org_id
    user_query = text(f'SELECT * FROM user_app_generate_org_id WHERE generated_org_id = {generated_org_id}')
    # Execute the queries
    user_result = conn.execute(user_query).fetchall() 
    # Convert the results to lists of dictionaries
    user_rows = [dict(row) for row in user_result]
    json_result_1 = user_rows[0]['org_name']
    # SQL query for itemtype
    item_query = text("SELECT * FROM shivadb_new.itemtype WHERE org_id = :org_id")
    item_result = conn.execute(item_query, org_id=json_result_1).fetchall()
    

    item_rows = [dict(row) for row in item_result]

    # Convert the list of dictionaries to JSON
    json_result = "https://saasapps.in:2082/media/"+user_rows[0]['src']

    # Convert the list of dictionaries to JSON
    
    print(item_rows)


    # You can now return the JSON result or use it as needed
    return json_result, json_result_1, item_rows

def generated_org_id(request, generated_org_id):
    print("here")
    # Store generated_org_id in session
    request.session['generated_org_id'] = generated_org_id
    try:
        json_result,json_result_1,item_rows = check_generated_org_id(request)
    except:
        json_result,json_result_1,item_rows = None, None, None
    print(json_result)
    context = {'logo_url': json_result,'org_name': json_result_1,'item_rows':item_rows}
    # Redirect to the home page or any other page you desire
    return render(request, 'result_Home.html', context)






