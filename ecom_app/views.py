from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text
import json
from urllib.parse import urlparse

# mydb = create_engine('mysql+pymysql://' + 'root' + ':' + 'password' + '@' + '49.205.199.235' + ':' + str(3306) + '/' + 'shivadb_new' , echo=False)
# try:
#     conn = mydb.connect()
# except Exception as err:
#     print(err)

def use_sqlalchemy(query,params={}):
    try:
        # Using SQLAlchemy for a specific task
        engine = create_engine('mysql+pymysql://root:Snc&!123@127.0.0.1:3306/shivadb_new', echo=False)
        conn = engine.connect()

        _query = text(f"{query}")
        _result = conn.execute(_query,params).fetchall()
        # print('#_result',_result)
        _rows = [dict(row._asdict()) for row in _result]

        print("item_result", _result, _rows)
        return _rows
    
    except Exception as err:
        print("mysql connection error",err)
        return rows
    finally:
        print("#############################result done#####################################")
        conn.close()



def get_org_id(request):
    current_url = request.build_absolute_uri()
    parsed_url = urlparse(current_url)
    input_org = 'synnergyze.com'#parsed_url.netloc
    item_query = "SELECT * FROM shivadb_new.user_app_generate_org_id"
    list_item_row = use_sqlalchemy(item_query)
    result_dict = None
    for item in list_item_row:
        if input_org.lower() in item['org_name'].lower() or item['org_name'].lower() in input_org.lower():
            result_dict = item
            request.session['generated_org_id'] = result_dict['generated_org_id']
            break
    # print(result_dict)

def index(request):
    get_org_id(request)
    template = loader.get_template("result_Home.html")
    # results = VisaGetlist.objects.all()
    try:
        generated_org_id = request.session['generated_org_id']
        json_result,json_result_1,item_rows,item_sub_row = check_generated_org_id(request)
    except:
        json_result,json_result_1,item_rows,item_sub_row  = None, None, None,None
    # print(json_result)
    context = {'logo_url': json_result,'org_name': json_result_1,'item_rows':item_rows,"item_sub_row":item_sub_row }
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


def list_product(request, item_type_name):
    # print("item-name",item_type_name)
    item_subtype = request.GET.get('item_subtype', None)
    # print("item_subtype",item_subtype)
    template = loader.get_template("list_product.html")
    # results = VisaGetlist.objects.all()
    try:
        generated_org_id = request.session['generated_org_id']
        json_result,json_result_1,item_rows,item_sub_row = check_generated_org_id(request)

    except:
        json_result,json_result_1,item_rows,item_sub_row  = None, None, None,None
    try:
        # print("######",item_subtype)
        if item_subtype:
            item_query = text(
                """
                SELECT *,nd.Selling_Price-nd.Selling_Price*nd.Item_Discount/100 as discount_price
                FROM shivadb_new.newitemdetails AS nd
                LEFT JOIN shivadb_new.newitemdetailsimage AS ni ON nd.org_id = ni.org_id
                                            AND nd.item_type = ni.item_type
                                            AND nd.item_name = ni.item_name
                WHERE nd.org_id = :org_id
                AND nd.item_type = :item_type
                AND nd.item_subtype = :item_subtype;
                """
            )
            # text("SELECT * FROM newitemdetails WHERE org_id = :org_id and item_type = :item_type and item_subtype = :item_subtype")
            params = {'org_id': json_result_1, 'item_type': item_type_name, 'item_subtype': item_subtype}
        else:
            # print("####", 'item_query')
            item_query = text(
                """
                SELECT *,nd.Selling_Price-nd.Selling_Price*nd.Item_Discount/100 as discount_price
                FROM shivadb_new.newitemdetails AS nd
                LEFT JOIN shivadb_new.newitemdetailsimage AS ni ON nd.org_id = ni.org_id
                                            AND nd.item_type = ni.item_type
                                            AND nd.item_name = ni.item_name
                WHERE nd.org_id = :org_id
                AND nd.item_type = :item_type;
                """
            )
            # text("SELECT * FROM newitemdetails WHERE org_id = :org_id and item_type = :item_type")
            params = {'org_id': json_result_1, 'item_type': item_type_name}
        list_item_row = use_sqlalchemy(item_query,params)
      
        # print("item_result",list_item_row) 
    except:
        print("error")
    # print(json_result)
    context = {'logo_url': json_result,'org_name': json_result_1,'item_rows':item_rows,"item_sub_row":item_sub_row,"list_item_row":list_item_row }
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)



def list_product_details(request):
    template = loader.get_template("result_ProductDetails.html")
    try:
        json_result,json_result_1,item_rows,item_sub_row = check_generated_org_id(request)
    except:
        json_result,json_result_1,item_rows,item_sub_row = None, None, None,None
    
    item_name = request.GET.get('item_name', None)
    item_type_name = request.GET.get('item_type', None)
    item_subtype = request.GET.get('item_subtype', None)
    print(
        item_name,"$",
        item_type_name,"$",
        item_subtype,"$",
    )
    try:
        # print("######",item_subtype)
        if item_subtype:
            item_query = text(
                """
                SELECT *,nd.Selling_Price-nd.Selling_Price*nd.Item_Discount/100 as discount_price
                FROM shivadb_new.newitemdetails AS nd
                LEFT JOIN shivadb_new.newitemdetailsimage AS ni ON nd.org_id = ni.org_id
                                            AND nd.item_type = ni.item_type
                                            AND nd.item_name = ni.item_name
                WHERE nd.org_id = :org_id
                AND nd.item_type = :item_type
                AND nd.item_subtype = :item_subtype
                AND nd.item_name = :item_name;
                """
            )
            # text("SELECT * FROM newitemdetails WHERE org_id = :org_id and item_type = :item_type and item_subtype = :item_subtype")
            params = {'org_id': json_result_1, 'item_type': item_type_name, 'item_subtype': item_subtype,'item_name':item_name}
        else:
            # print("####", 'item_query')
            item_query = text(
                """
                SELECT *,nd.Selling_Price-nd.Selling_Price*nd.Item_Discount/100 as discount_price
                FROM shivadb_new.newitemdetails AS nd
                LEFT JOIN shivadb_new.newitemdetailsimage AS ni ON nd.org_id = ni.org_id
                                            AND nd.item_type = ni.item_type
                                            AND nd.item_name = ni.item_name
                WHERE nd.org_id = :org_id
                AND nd.item_type = :item_type
                AND nd.item_name = :item_name;
                """
            )
            # text("SELECT * FROM newitemdetails WHERE org_id = :org_id and item_type = :item_type")
            params = {'org_id': json_result_1, 'item_type': item_type_name,'item_name':item_name}
        list_item_detail = use_sqlalchemy(item_query,params)
      
        # print("item_result",list_item_row) 
        context = {'item':list_item_detail[0],'logo_url': json_result,'org_name': json_result_1,'item_rows':item_rows,"item_sub_row":item_sub_row}
    except:
        print("error")



        context = {'logo_url': json_result,'org_name': json_result_1,'item_rows':item_rows,"item_sub_row":item_sub_row}
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)



def forget_password(request):
    template = loader.get_template("result_Forget.html")
    # results = VisaGetlist.objects.all()
    context = {'user': 'arun'}
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)

def check_generated_org_id(request):
    generated_org_id = request.session.get('generated_org_id')
    if not generated_org_id:
        return None, None, None,None
    try:
        user_query = text(f'SELECT * FROM user_app_generate_org_id WHERE generated_org_id = "{generated_org_id}"')
        user_rows = use_sqlalchemy(user_query)
        if not user_rows:
            return None, None, None
        json_result_1 = user_rows[0]['org_name']
        item_query = text(f'SELECT * FROM itemtype WHERE org_id = "{json_result_1}"')
        item_rows = use_sqlalchemy(item_query)
        item_sub_query = text(f"SELECT * FROM shivadb_new.itemsubtype WHERE org_id = '{json_result_1}'")
        item_sub_row= use_sqlalchemy(item_sub_query)
        json_result = "https://saasapps.in:2082/media/" + user_rows[0]['src']
        return json_result, json_result_1, item_rows, item_sub_row
    except Exception as e:
        return None, None, None,None

def generated_org_id(request, generated_org_id):
  #  print("here")
    # Store generated_org_id in session
    request.session['generated_org_id'] = generated_org_id
    try:
        json_result,json_result_1,item_rows,item_sub_row = check_generated_org_id(request)
    except:
        json_result,json_result_1,item_rows,item_sub_row = None, None, None,None
    # print(json_result)
    context = {'logo_url': json_result,'org_name': json_result_1,'item_rows':item_rows,"item_sub_row":item_sub_row}
    # Redirect to the home page or any other page you desire
    return render(request, 'result_Home.html', context)






