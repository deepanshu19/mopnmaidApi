import re
from django.db import models

# Create your models here.


class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    primary_contact = models.CharField(max_length=10)
    email = models.CharField(max_length=320, null=True)
    pwd = models.CharField(max_length=64)
    user_type = models.IntegerField()

    def __str__(self):
        return self.email


class state(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=25)

    def __str__(self):
        return self.state_name


class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(
        state, on_delete=models.CASCADE, related_name="state_city")
    city_name = models.CharField(max_length=25)

    def __str__(self):
        return self.city_name


class area(models.Model):
    area_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(
        city, on_delete=models.CASCADE, related_name="city_area")
    zipcode = models.CharField(max_length=6)
    area_name = models.CharField(max_length=100)

    def __str__(self):
        return self.area_name


class client(models.Model):
    c_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="user_client")
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    secondary_contact = models.CharField(max_length=10, null=True)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}{}'.format(self.fname, self.lname)


class address(models.Model):
    addr_id = models.AutoField(primary_key=True)
    c = models.ForeignKey(
        client, on_delete=models.CASCADE, related_name="c_address")
    house_no = models.CharField(max_length=20)
    line_one = models.CharField(max_length=150)
    line_two = models.CharField(max_length=150)
    landmark = models.CharField(max_length=30)
    area = models.ForeignKey(
        area, on_delete=models.CASCADE, related_name="area_address")
    # is_corp = models.IntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}{}'.format(self.c_id, self.area_id)


class religion(models.Model):
    religion_id = models.AutoField(primary_key=True)
    religion_name = models.CharField(max_length=20)

    def __str__(self):
        return self.religion_name


class caste(models.Model):
    caste_id = models.AutoField(primary_key=True)
    religion = models.ForeignKey(
        religion, on_delete=models.CASCADE, related_name="religion_caste")
    caste_name = models.CharField(max_length=30)

    def __str__(self):
        return '{}{}'.format(self.religion_id, self.area_id)


class services(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=10)
    service_img = models.ImageField(blank=True, upload_to='serviceimg')
    service_type = models.IntegerField()
    criteria_of_charge = models.CharField(max_length=15)
    description = models.CharField(max_length=150)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.service_name


class helper(models.Model):
    h_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="user_helper")
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    caste = models.ForeignKey(
        caste, on_delete=models.CASCADE, related_name="caste_helper")
    dob = models.DateField()
   #photo = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, upload_to='helpers')
    secondary_contact = models.CharField(max_length=10)
    acc_no = models.IntegerField(null=True)
    acc_holder_name = models.CharField(max_length=100, null=True)
    branch_name = models.CharField(max_length=50, null=True)
    ifsc_code = models.CharField(max_length=11, null=True)
    aadharcard_no = models.IntegerField(null=True)
    pancard_no = models.IntegerField(null=True)
    aadharcard_img = models.ImageField(
        blank=True, upload_to='adhaarcard', null=True)
    pancard_img = models.ImageField(blank=True, upload_to='pancard', null=True)
    relative_id_proof = models.CharField(max_length=255, null=True)
    temp_house_no = models.CharField(max_length=20)
    temp_line_one = models.CharField(max_length=150)
    temp_line_two = models.CharField(max_length=150)
    temp_landmark = models.CharField(max_length=50)
    temp_area = models.ForeignKey(
        area, on_delete=models.CASCADE, related_name="temp_area_helper")
    perm_house_no = models.CharField(max_length=20)
    perm_line_one = models.CharField(max_length=150)
    perm_line_two = models.CharField(max_length=150)
    perm_landmark = models.CharField(max_length=50)
    perm_area = models.ForeignKey(
        area, on_delete=models.CASCADE, related_name="perm_area_helper",)
    special_service = models.ForeignKey(
        services, on_delete=models.CASCADE, related_name="special_service_helper",)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}{}'.format(self.fname, self.lname)


class serviceProvided(models.Model):
    serv_prov_id = models.AutoField(primary_key=True)
    h = models.ForeignKey(helper, on_delete=models.CASCADE,
                          related_name="h_serviceProvided",)
    service = models.ForeignKey(
        services, on_delete=models.CASCADE, related_name="service_serviceProvided",)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}{}'.format(self.h, self.service)


class chargesArea(models.Model):
    charge_area_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(
        services, on_delete=models.CASCADE, related_name="service_chargesArea")
    area = models.ForeignKey(
        area, on_delete=models.CASCADE, related_name="area_chargesArea")
    charges = models.IntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}{}'.format(self.service, self.area)


class maidRequest(models.Model):
    maid_request_id = models.AutoField(primary_key=True)
    address = models.ForeignKey(
        address, on_delete=models.CASCADE, related_name="address_maidRequest")
    date_of_request = models.DateField(auto_now_add=True)
    time_of_request = models.TimeField(auto_now_add=True)
    gender_pref = models.IntegerField()
    # age_pref = models.IntegerField()
    req_status = models.IntegerField()
    # specification = models.CharField(max_length=150)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.maid_request_id


class maidRequestDetails(models.Model):
    req_details_id = models.AutoField(primary_key=True)
    maid_request = models.ForeignKey(
        maidRequest, on_delete=models.CASCADE, related_name="maid_request_maidRequestDetails")
    service = models.ForeignKey(
        services, on_delete=models.CASCADE, related_name="service_maidRequestDetails")
    # count = models.IntegerField()
    serv_start_date = models.DateField()
    # serv_end_date = models.DateField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.req_details_id


class timeDetails(models.Model):
    time_details_id = models.AutoField(primary_key=True)
    req_details = models.ForeignKey(
        maidRequestDetails, on_delete=models.CASCADE, related_name="req_details_timeDetails")
    full_time = models.IntegerField()
    request_type = models.CharField(max_length=6)
    day_of_week = models.CharField(max_length=9)
    time_slot_1 = models.TimeField()
    time_slot_2 = models.TimeField()
    time_slot_3 = models.TimeField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.time_details_id


class demo(models.Model):
    demo_id = models.AutoField(primary_key=True)
    req_details = models.ForeignKey(
        maidRequestDetails, on_delete=models.CASCADE, related_name="req_details_demo")
    h = models.ForeignKey(
        helper, on_delete=models.CASCADE, related_name="h_demo")
    demo_date = models.DateField()
    demo_time = models.TimeField()
    demo_status = models.IntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.demo_id


class booking(models.Model):
    bkg_id = models.AutoField(primary_key=True)
    req_details = models.ForeignKey(
        maidRequestDetails, on_delete=models.CASCADE, related_name="req_details_booking")
    h = models.ForeignKey(helper, on_delete=models.CASCADE,
                          related_name="h_booking")
    bkg_date = models.DateField()
    bkg_time = models.TimeField()
    bkg_status = models.IntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.bkg_id


class payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    bkg = models.ForeignKey(
        booking, on_delete=models.CASCADE, related_name="bkg_payments")
    payment_date = models.DateField()
    payment_time = models.TimeField()
    amount = models.IntegerField()
    payment_status = models.IntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_id


class workingHours(models.Model):
    working_hours_id = models.AutoField(primary_key=True)
    h = models.ForeignKey(helper, on_delete=models.CASCADE,
                          related_name="h_workingHours")
    time_slot = models.IntegerField(null=True)
    start_hour = models.TimeField(blank=True, null=True)
    end_hour = models.TimeField(blank=True, null=True)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}{}'.format(self.h, self.working_hours_id)


class feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    bkg = models.ForeignKey(
        booking, on_delete=models.CASCADE, related_name="bkg_feedback")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    feedback_date = models.DateField()
    feedback_time = models.TimeField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.feedback_id


class complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    bkg = models.ForeignKey(
        booking, on_delete=models.CASCADE, related_name="bkg_complaint")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    complaint_date = models.DateField()
    complaint_time = models.TimeField()
    complaint_reply = models.CharField(max_length=150)
    complaint_status = models.IntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.complaint_id


class holidayRequest(models.Model):
    holiday_req_id = models.AutoField(primary_key=True)
    h = models.ForeignKey(helper, on_delete=models.CASCADE,
                          related_name="h_holidayRequest")
    date_req = models.DateField()
    time_req = models.TimeField()
    date_holiday = models.DateField()
    duration = models.IntegerField()
    reason = models.CharField(max_length=150)
    audio_req = models.CharField(max_length=255)
    holiday_req_status = models.IntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}{}'.format(self.h, self.holiday_req_id)


class ratings(models.Model):
    rating_id = models.AutoField(primary_key=True)
    feedback = models.ForeignKey(
        feedback, on_delete=models.CASCADE, related_name="feedback_ratings")
    service = models.ForeignKey(
        services, on_delete=models.CASCADE, related_name="service_ratings")
    rating = models.IntegerField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.rating_id


class helperPaymentDetails(models.Model):
    h_payment_details_id = models.AutoField(primary_key=True)
    h = models.ForeignKey(helper, on_delete=models.CASCADE,
                          related_name="h_helperPaymentDetails")
    payment_date = models.DateField()
    payment_amount = models.IntegerField()
    payment_mode = models.CharField(max_length=50)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{}{}'.format(self.h, self.h_payment_details_id)
