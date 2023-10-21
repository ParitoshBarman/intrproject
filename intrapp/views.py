from django.shortcuts import render, redirect, HttpResponse
from json import dumps
import requests

# Create your views here.
def index(request):
    sendData = {}
    
    return render(request, 'login.html', sendData)
    

def savedata(request, token):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        street = request.POST.get('street')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        create_customer_url = "https://qa2.sunbasedata.com/sunbase/portal/api/assignment.jsp?cmd=create"

        headers = {
            "Authorization": token
        }
        customer_data = {
            "first_name": f"{first_name}",
            "last_name": f"{last_name}",
            "street": f"{street}",
            "address": f"{address}",
            "city": f"{city}",
            "state": f"{state}",
            "email": f"{email}",
            "phone": f"{phone}"
        }
        customer_response = requests.post(create_customer_url, headers=headers, json=customer_data)

        if customer_response.status_code==201:
            customer_list_url = "https://qa2.sunbasedata.com/sunbase/portal/api/assignment.jsp?cmd=get_customer_list"
            customer_response = requests.get(customer_list_url, headers=headers)

            if customer_response.status_code == 201:
                print("Successful. Status code: 201")
                # print(f"{customer_response.json()}")
            else:
                print("fail")
            sendData = {
                'Authorization' : token,
                'DRRdb' : customer_response.json(),
                'totalEntries' : len(customer_response.json()),
                'fromEntry' : 1,
                'toEntry' : 1+len(customer_response.json())-1
                }
            return render(request, 'drr.html', sendData)





def deletdata(request, slID, token):
    prm = {
        'cmd' : 'delete',
        'uuid' : slID
    }
    delete_url = "https://qa2.sunbasedata.com/sunbase/portal/api/assignment.jsp"

    headers = {
        "Authorization": f"Bearer {token}"
    }
    customer_response = requests.post(delete_url, headers=headers, params=prm)
    # print(f"This is ================== {customer_response.status_code}")
    if customer_response.status_code==200:
        customer_list_url = "https://qa2.sunbasedata.com/sunbase/portal/api/assignment.jsp?cmd=get_customer_list"
        customer_response = requests.get(customer_list_url, headers=headers)

        if customer_response.status_code == 200:
            print("Successful. Status code: 200")
            # print(f"{customer_response.json()}")
        else:
            print("fail")
        sendData = {
            'Authorization' : token,
            'DRRdb' : customer_response.json(),
            'totalEntries' : len(customer_response.json()),
            'fromEntry' : 1,
            'toEntry' : 1+len(customer_response.json())-1
            }

        return render(request, 'drr.html', sendData)
    else:
        return redirect("/")

def loginSuccess(request):
    if request.method == 'POST':
        userID = request.POST.get('username')
        password = request.POST.get('password')
        auth_url = "https://qa2.sunbasedata.com/sunbase/portal/api/assignment_auth.jsp"
        auth_data = {
            "login_id": userID,
            "password": password
        }
        auth_response = requests.post(auth_url, json=auth_data)
        # print(auth_response.json())
        if auth_response.status_code == 200:
            bearer_token = auth_response.json()["access_token"]
            print(f"Authentication successful. Bearer Token: {bearer_token}")
            customer_list_url = "https://qa2.sunbasedata.com/sunbase/portal/api/assignment.jsp?cmd=get_customer_list"

            headers = {
                "Authorization": f"Bearer {bearer_token}"
            }


            customer_response = requests.get(customer_list_url, headers=headers)

            if customer_response.status_code == 200:
                print("Successful. Status code: 200")
                # print(f"{customer_response.json()}")
            else:
                print("fail")
            sendData = {
                'Authorization' : f'Bearer {bearer_token}',
                'DRRdb' : customer_response.json(),
                'totalEntries' : len(customer_response.json()),
                'fromEntry' : 1,
                'toEntry' : 1+len(customer_response.json())-1
                }

            return render(request, 'drr.html', sendData)
        else:
            # print(f"Authentication failed with status code: {auth_response.status_code}")
            return render(request, 'login.html', {"errorData":"Sorry please check"})




def updateForm(request, slID, token):
    print("done...............")
    sendData = {
        'upadeLink' : f"/update/{slID}/{token}"
    }
    return render(request, 'updateform.html', sendData)

def update(request, slID, token):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        street = request.POST.get('street')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        

        headers = {
            "Authorization": token
        }
        customer_data = {
            "first_name": f"{first_name}",
            "last_name": f"{last_name}",
            "street": f"{street}",
            "address": f"{address}",
            "city": f"{city}",
            "state": f"{state}",
            "email": f"{email}",
            "phone": f"{phone}"
        }


        prm = {
            'cmd' : 'update',
            'uuid' : slID
        }
        update_url = "https://qa2.sunbasedata.com/sunbase/portal/api/assignment.jsp"

        headers = {
            "Authorization": f"Bearer {token}"
        }
        update_response = requests.post(update_url, headers=headers, json=customer_data, params=prm)
        # print(f"This is ================== {customer_response.status_code}")
        if update_response.status_code==200:
            customer_list_url = "https://qa2.sunbasedata.com/sunbase/portal/api/assignment.jsp?cmd=get_customer_list"
            customer_response = requests.get(customer_list_url, headers=headers)

            if customer_response.status_code == 200:
                print("Successful. Status code: 200")
                # print(f"{customer_response.json()}")
            else:
                print("fail")
            sendData = {
                'Authorization' : token,
                'DRRdb' : customer_response.json(),
                'totalEntries' : len(customer_response.json()),
                'fromEntry' : 1,
                'toEntry' : 1+len(customer_response.json())-1
                }

            return render(request, 'drr.html', sendData)
        else:
            return redirect("/")