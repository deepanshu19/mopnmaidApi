from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, ClientSerializer
from pydoc import cli
from django.shortcuts import redirect, render
from . models import user, state, city, area, client, address, religion, caste, services, helper, serviceProvided, chargesArea, maidRequest, maidRequestDetails, timeDetails, demo, booking, payments, workingHours, feedback, complaint, holidayRequest, ratings, helperPaymentDetails
# Create your views here.


@api_view(['GET'])
def getClientData(request):
    clients = client.objects.all()
    users = user.objects.all()
    clientserializer = ClientSerializer(clients, many=True)
    userserializer = UserSerializer(users, many=True)
    return Response([userserializer.data, clientserializer.data])


@api_view(['GET'])
def getClient(request, emailId):
    users = user.objects.get(email=emailId)
    clients = client.objects.get(c_id=users.user_id)
    userserializer = UserSerializer(users, many=False)
    clientserializer = ClientSerializer(clients, many=False)
    return Response([userserializer.data, clientserializer.data])


@api_view(['POST'])
def clientRegisterApi(request):
    data = request.data
    userObj = user.objects.create(
        primary_contact=data["primary_contact"],
        email=data["email"],
        pwd=data["pwd"],
        user_type=2,
    )
    clientObj = client.objects.create(
        user=userObj,
        fname=data["fname"],
        lname=data["lname"],
        secondary_contact=None,
        delete_flag=0
    )

    serializer = ClientSerializer(clientObj, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updateClient(request, emailId):
    data = request.data
    users = user.objects.get(email=emailId)
    users.email = data["email"]
    users.primary_contact = data["primary_contact"]
    users.pwd = data["pwd"]
    users.save(update_fields=["email", "primary_contact", "pwd"])
    clients = client.objects.get(user_id=users.user_id)
    clients.fname = data["fname"]
    clients.lname = data["lname"]
    clients.save(update_fields=["fname", "lname"])
    userser = UserSerializer(users, data=request.data)
    clientser = ClientSerializer(clients, data=request.data)
    if userser.is_valid():
        userser.save()
    if clientser.is_valid():
        clientser.save()
    return Response([userser.data, clientser.data])


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if(username == "admin" and password == "admin"):
            return render(request, "index.html")
        else:
            return render(request, "sign_in/login.html")


def login(request):
    return render(request, "sign_in/login.html")


'''
def edit_profile(request):
    userData = user.objects.get(user_type=1)
    if request.method == 'POST':
        userData.email = request.POST.get('email')
        userData.pwd = request.POST.get('password')
        userData.save()
    return render(request, "main/edit_profile.html", {'user': userData})
'''


def res_services(request):
    serviceData = services.objects.filter(
        delete_flag=False).exclude(service_type=2)
    return render(request, "main/res_services.html", {'services': serviceData})


def add_res_services(request):
    if request.method == 'POST':
        service = services()
        service.service_name = request.POST.get('servicename')
        service.service_type = 1
        service.criteria_of_charge = request.POST.get('criteriaofcharge')
        service.description = request.POST.get('servicedescription')
        service.delete_flag = False
        if len(request.FILES) != 0:
            service.service_img = request.FILES['img']
        service.save()
        return redirect("res_services")
    return render(request, "main/add_res_services.html")


def update_res_services(request, key):
    serviceData = services.objects.filter(
        delete_flag=False).exclude(service_type=2)
    if request.method == 'POST':
        service = services.objects.get(service_id=key)
        service.service_name = request.POST.get('servicename')
        service.criteria_of_charge = request.POST.get('criteriaofcharge')
        service.description = request.POST.get('servicedescription')
        if len(request.FILES) != 0:
            service.service_img = request.FILES['img']
        service.save(update_fields=[
                     'service_name', 'criteria_of_charge', 'description', 'service_img'])
        # return redirect("res_services")
    return render(request, "main/res_services.html", {'services': serviceData})


def delete_res_services(request, key):
    if request.method == 'POST':
        service = services.objects.get(service_id=key)
        service.delete_flag = True
        service.save(update_fields=['delete_flag'])
        # if len(service.service_img) > 0:
        #     os.remove(service.service_img.path)
        # service.delete()
    serviceData = services.objects.filter(
        service_type=1).exclude(delete_flag=True)
    return render(request, "main/res_services.html", {'services': serviceData})


def comm_services(request):
    serviceData = services.objects.filter(
        delete_flag=False).exclude(service_type=1)
    return render(request, "main/comm_services.html", {'services': serviceData})


def add_comm_services(request):
    if request.method == 'POST':
        service = services()
        service.service_name = request.POST.get('servicename')
        service.service_type = 2
        service.criteria_of_charge = request.POST.get('criteriaofcharge')
        service.description = request.POST.get('servicedescription')
        service.delete_flag = False
        if len(request.FILES) != 0:
            service.service_img = request.FILES['img']
        service.save()
        return redirect("comm_services")
    return render(request, "main/add_comm_services.html")


def update_comm_services(request, key):
    serviceData = services.objects.filter(
        delete_flag=False).exclude(service_type=1)
    if request.method == 'POST':
        service = services.objects.get(service_id=key)
        service.service_name = request.POST.get('servicename')
        service.criteria_of_charge = request.POST.get('criteriaofcharge')
        service.description = request.POST.get('servicedescription')
        if len(request.FILES) != 0:
            service.service_img = request.FILES['img']
        service.save(update_fields=[
                     'service_name', 'criteria_of_charge', 'description', 'service_img'])
        # return redirect("res_services")
    return render(request, "main/comm_services.html", {'services': serviceData})


def delete_comm_services(request, key):
    if request.method == 'POST':
        service = services.objects.get(service_id=key)
        service.delete_flag = True
        service.save(update_fields=['delete_flag'])
        # if len(service.service_img) > 0:
        #     os.remove(service.service_img.path)
        # service.delete()
    serviceData = services.objects.filter(
        service_type=2).exclude(delete_flag=True)
    return render(request, "main/comm_services.html", {'services': serviceData})


def register_helper(request):
    if request.method == "POST":
        userdata = user()
        userdata.primary_contact = request.POST.get("primarycontact")
        userdata.user_type = 3
        userdata.save()

        curstatedata = state()
        curstatedata.state_name = request.POST.get("cstate")
        curstatedata.save()
        curcitydata = city(state=curstatedata)
        curcitydata.city_name = request.POST.get("ccity")
        curcitydata.save()
        curareadata = area(city=curcitydata)
        curareadata.area_name = request.POST.get("carea")
        curareadata.zipcode = request.POST.get("czipcode")
        curareadata.save()
        religiondata = religion()
        religiondata.religion_name = request.POST.get("religion")
        religiondata.save()
        castedata = caste(religion=religiondata)
        castedata.caste_name = request.POST.get("caste")
        castedata.save()
        perstatedata = state()
        perstatedata.state_name = request.POST.get("pstate")
        perstatedata.save()
        percitydata = city(state=perstatedata)
        percitydata.city_name = request.POST.get("pcity")
        percitydata.save()
        perareadata = area(city=percitydata)
        perareadata.area_name = request.POST.get("parea")
        perareadata.zipcode = request.POST.get("pzipcode")
        perareadata.save()

        spl_service_name = request.POST.get('speciality')
        splservices = services.objects.get(service_name=spl_service_name)
        splservices.save()
        helperdata = helper(user=userdata, caste=castedata, temp_area=curareadata,
                            perm_area=perareadata, special_service=splservices)

        helperdata.fname = request.POST.get('firstname')
        helperdata.lname = request.POST.get('lastname')
        helperdata.gender = request.POST.get('gender')
        helperdata.dob = request.POST.get('date')
        if len(request.FILES) != 0:
            helperdata.photo = request.FILES['img']

        helperdata.secondary_contact = request.POST.get("secondarycontact")

        helperdata.temp_house_no = request.POST.get("chouseno")
        helperdata.temp_line_one = request.POST.get("cline1")
        helperdata.temp_landmark = request.POST.get("clandmark")
        helperdata.temp_line_two = request.POST.get("cline2")

        helperdata.perm_house_no = request.POST.get("phouseno")
        helperdata.perm_line_one = request.POST.get("pline1")
        helperdata.perm_landmark = request.POST.get("plandmark")
        helperdata.perm_line_two = request.POST.get("pline2")
        helperdata.delete_flag = False
        helperdata.save()
        timeslot1 = workingHours(h=helperdata)
        timeslot1.time_slot = 1
        timeslot1.start_hour = request.POST.get('s1start')
        timeslot1.end_hour = request.POST.get('s1end')
        timeslot1.delete_flag = False
        timeslot1.save()
        timeslot2 = workingHours(h=helperdata)
        timeslot2.time_slot = 2
        timeslot2.start_hour = request.POST.get('s2start')
        timeslot2.end_hour = request.POST.get('s2end')
        timeslot2.delete_flag = False
        timeslot2.save()
        timeslot3 = workingHours(h=helperdata)
        timeslot3.time_slot = 3
        timeslot3.start_hour = request.POST.get('s3start')
        timeslot3.end_hour = request.POST.get('s3end')
        timeslot3.delete_flag = False
        timeslot3.save()
        servicename = request.POST.getlist('servicechk')
        for sname in servicename:
            chkservicesdata = services.objects.get(service_name=sname)
            chkservicesdata.save()
        serviceProvideddata = serviceProvided(
            service=chkservicesdata, h=helperdata)
        serviceProvideddata.delete_flag = False
        serviceProvideddata.save()

    serviceData = services.objects.all()
    return render(request, "helper/register_helper.html", {'service': serviceData})


def work_details(request):
    return render(request, "helper/work_details.html")


def manage_helper(request):
    helperdata = helper.objects.filter(delete_flag=False)
    serviceData = services.objects.all()
    return render(request, "helper/manage_helper.html", {'helper': helperdata})


def edit_helper(request, hid):
    helperdata = helper.objects.get(h_id=hid)
    serv_prov = serviceProvided.objects.get(h=helperdata)
    serviceData = services.objects.all()
    wh1 = workingHours.objects.get(h=helperdata, time_slot=1)
    wh2 = workingHours.objects.get(h=helperdata, time_slot=2)
    wh3 = workingHours.objects.get(h=helperdata, time_slot=3)
    return render(request, "helper/edit_helper.html", {'helper': helperdata, 'service': serviceData, 'serv_prov': serv_prov, 'working_hour': wh1})


def delete_helper(request, hid):
    if request.method == 'POST':
        helperdata = helper.objects.get(h_id=hid)
        helperdata.delete_flag = True
        helperdata.save(update_fields=['delete_flag'])
    helperdata = helper.objects.filter(delete_flag=False)
    return render(request, "helper/manage_helper.html")


def edit_work_details(request):
    return render(request, "helper/edit_work_details.html")


def schedule(request):
    return render(request, "helper/schedule.html")


def conf_details(request):
    return render(request, "helper/conf_details.html")


def edit_conf_details(request):
    return render(request, "helper/edit_conf_details.html")


def salary_details(request):
    return render(request, "helper/salary_details.html")


def holiday_details(request):
    return render(request, "helper/holiday_details.html")


def charges(request):
    cityData = city.objects.all()
    areaData = area.objects.all()
    serviceData = services.objects.all()
    return render(request, "main/charges.html", {'city': cityData, 'area': areaData, 'services': serviceData})


def new_charges(request):
    if request.method == 'POST':
        servicename = request.POST.get('service')
        cityname = request.POST.get('city')
        areaname = request.POST.get('area')
        charges = chargesArea.objects.filter(
            service_name=servicename, city_name=cityname, area_name=areaname)
    return render(request, "main/charges.html", {'charges': charges})


def ratings(request):
    return render(request, "helper/ratings.html")


def feedback(request):
    return render(request, "extra/feedback.html")


def view_feedback(request):
    return render(request, "extra/view_feedback.html")


def complaint(request):
    return render(request, "extra/complaint.html")


def view_complaint(request):
    return render(request, "extra/view_complaint.html")


def holiday_req(request):
    return render(request, "extra/holiday_req.html")


def view_holiday_req(request):
    return render(request, "extra/view_holiday_req.html")


def register_client(request):
    if request.method == 'POST':
        userdata = user()
        userdata.primary_contact = request.POST.get("primarycontact")
        userdata.email = request.POST.get("emailaddress")
        # userdata.pwd = "123"
        userdata.user_type = 2
        userdata.save()
        clientdata = client(user=userdata)
        clientdata.fname = request.POST.get("firstname")
        clientdata.lname = request.POST.get("lastname")
        clientdata.secondary_contact = request.POST.get("secondarycontact")
        clientdata.delete_flag = 0
        clientdata.save()

    return render(request, "client/register_client.html")


def manage_client(request):
    clientdata = client.objects.filter(delete_flag=False)
    return render(request, "client/manage_client.html", {'client': clientdata})


def update_manage_client(request, userid, cid):
    if request.method == 'POST':
        userdata = user(user_id=userid, primary_contact=request.POST.get(
            "primarycontact"), email=request.POST.get("email"))
        clientdata = client(c_id=cid, user=userdata)
        clientdata.fname = request.POST.get("firstname")
        clientdata.lname = request.POST.get("lastname")
        userdata.save(update_fields=['primary_contact', 'email'])
        clientdata.save(update_fields=['fname', 'lname'])
    clientdata = client.objects.filter(delete_flag=False)
    return render(request, "client/manage_client.html", {'client': clientdata})


def delete_manage_client(request, cid):
    if request.method == 'POST':
        clientdata = client(c_id=cid)
        clientdata.delete_flag = True
        clientdata.save(update_fields=['delete_flag'])
    clientdata = client.objects.filter(delete_flag=False)
    return render(request, "client/manage_client.html", {'client': clientdata})


def add_maidreq(request, cid):
    clientdata = client.objects.get(c_id=cid)
    # userdata = user.objects.get(user_id=uid)
    fname = clientdata.fname
    lname = clientdata.lname
    contact = clientdata.user.primary_contact
    context = {'username': fname+" "+lname, 'contact': contact}
    return render(request, "client/add_maidreq.html", context)


def maid_req(request):
    return render(request, "client/maid_req.html")


def demo_details(request):
    return render(request, "client/demo_details.html")


def demofor_req(request):
    return render(request, "client/demofor_req.html")


def maidfor_demo(request):
    return render(request, "client/maidfor_demo.html")


def bookings(request):
    return render(request, "client/bookings.html")


def payments(request):
    return render(request, "client/payments.html")


def edit_maidreq(request):
    return render(request, "client/edit_maidreq.html")
