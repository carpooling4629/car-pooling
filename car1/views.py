from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import pyrebase
from django.contrib import auth
from django.core.cache import cache

firebaseConfig = {
    "apiKey": "AIzaSyADhXzPY5vHvpngz2A1ajYgLAnTuvFbUHs",
    "authDomain": "car-pooling-4629.firebaseapp.com",
    "databaseURL": "https://car-pooling-4629.firebaseio.com",
    "projectId": "car-pooling-4629",
    "storageBucket": "car-pooling-4629.appspot.com",
    "messagingSenderId": "999103793856",
    "appId": "1:999103793856:web:56abe91bd51b4488c5bb25",
    "measurementId": "G-JE36MHB704"
};

firebase=pyrebase.initialize_app(firebaseConfig)
authen=firebase.auth()
database=firebase.database()

def home(request):
    if 'mail' in request.session:
        url = database.child("UserDetails").child(request.session['rollno']).child("url").get().val()
        if request.method == 'POST':
            print("abc")
            if (request.POST.get('trip_submit')):
                start_location = request.POST.get('start_location')
                destination = request.POST.get('destination')
                trip_date = request.POST.get('trip_date')
                start_time = request.POST.get('start_time')
                no_of_seats = request.POST.get('no_of_seats')
                vehicle_number=request.POST.get('vehicle_number')
                print(trip_date)

                try:
                    if not database.child("LiftDatabase").child(trip_date).child(request.session['rollno']).get().val():
                        data = {"destination":destination,"start":start_location,"time":start_time,"date":trip_date,"seats":int(no_of_seats),"vehicle_number":vehicle_number}
                        database.child("TripDatabase").child(trip_date).child(request.session['rollno']).push(data)
                        print("if")
                        return render(request, 'web/tripdetails.html', {"message": "Trip added successfully","pic":url})
                    else:
                        print("else")
                        return render(request,'web/tripdetails.html',{"message":"You have requested for lift ","pic":url})
                except Exception as e:
                    # return render(request,'web/signup.html',{"message":"Error Occured"})
                    print(e)
                print("out")
                return render(request,'web/tripdetails.html',{"pic":url})



            if (request.POST.get('lift_submit')):
                lift_date = request.POST.get('lift_date')
                start=request.POST.get('start_location')
                destination=request.POST.get('destination')
                # print(lift_date)
                # print("abc")
                # print(start)
                # print(destination)
                request.session['lift_date'] = lift_date
                request.session['start_location'] = start
                request.session['destination'] = destination
                if not database.child("TripDatabase").child(lift_date).child(request.session['rollno']).get().val():
                    if database.child("TripDatabase").child(lift_date).get().val():
                        users = {}
                        for i in database.child("TripDatabase").child(lift_date).get().val():

                            for j in database.child("TripDatabase").child(lift_date).child(i).get().val():
                                user = []
                                print(j)
                                print(database.child("TripDatabase").child(lift_date).child(i).child(j).child(
                                    "seats").get().val())
                                if int(database.child("TripDatabase").child(lift_date).child(i).child(j).child(
                                        "seats").get().val()) > 0:
                                    user.append(i)
                                    user.append(database.child("UserDetails").child(i).child("name").get().val())
                                    user.append(database.child("UserDetails").child(i).child("gender").get().val())

                                    user.append(
                                        database.child("TripDatabase").child(lift_date).child(i).child(j).child(
                                            "start").get().val())
                                    user.append(database.child("TripDatabase").child(lift_date).child(i).child(j).child(
                                        "destination").get().val())
                                    user.append(
                                        database.child("TripDatabase").child(lift_date).child(i).child(j).child(
                                            "time").get().val())
                                    user.append(
                                        database.child("TripDatabase").child(lift_date).child(i).child(j).child(
                                            "seats").get().val())
                                    users[j] = user

                        return render(request, 'web/lift_view.html', {"start":request.session['start_location'],"destination":request.session['destination'],"users": users,"pic":url})
                    else:
                        return render(request, 'web/2.html', {"message": "No user exists","pic":url})
                else:
                    return render(request, 'web/2.html', {"message": "You have registered for lift provider","pic":url})
            if (request.POST.get('request')):
                request_rollno=request.POST.get('rollno')
                print(request_rollno)
                request_id = request.POST.get('request')
                mail=request.session['mail']
                sep=mail.split("@")
                rno=sep[0].split(".")
                print(rno)
                try:
                    if database.child("TripDatabase").child(request.session['lift_date']).child(request_rollno).child(request_id).child("request_list").child(rno[1]).get().val() or database.child("TripDatabase").child(request.session['lift_date']).child(request_rollno).child(request_id).child("lift_takers").child(rno[1]).get().val():
                        return render(request, 'web/2.html',{"message":"Already Requested","pic":url})
                    else:
                        data = {"status":0,"trip_provider":request_rollno,"ref_id":request_id,"start_location":request.session['start_location'],"destination":request.session['destination']}
                        database.child("LiftDatabase").child(request.session['lift_date']).child(rno[1]).push(data)
                        sender = ""
                        for i in database.child("LiftDatabase").child(request.session['lift_date']).child(rno[1]).get().val():
                            if request_id == database.child("LiftDatabase").child(request.session['lift_date']).child(rno[1]).child(i).child("ref_id").get().val():
                                sender = i
                                print(sender)
                                break

                        database.child("TripDatabase").child(request.session['lift_date']).child(request_rollno).child(request_id).child("request_list").child(rno[1]).set(sender)
                        #return render(request, 'web/2.html',{"message":"Successfully booked the seat"})
                except Exception as e:
                    #return render(request,'web/lift_view.html',{"message":"Error Occured"})
                    print(e)

                print(request_id)
        return render(request, 'web/2.html', {"message": request.session['mail'],"pic":url})
    return redirect("/")




def signin(request):
    if request.method == 'POST':
        if (request.POST.get('submit')):
            email = request.POST.get('mailid')
            pwd = request.POST.get('password')
            try:
                user=authen.sign_in_with_email_and_password(email,pwd)
                #auth.login(request, user)
            except Exception as e:
                return render(request, 'web/login.html', {"message": "invalid credentials"})
            request.session['mail']=email
            sep = email.split("@")
            rno = sep[0].split(".")
            request.session['rollno']=rno[1]
            print(request.session['rollno'])
            print(user['idToken'])
            request.session['userid']=str(user['idToken'])
            print(request.session['userid'])
            if 'userid' in request.session:
                print("1")
                return redirect("home/")
    return render(request, 'web/login.html')

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    auth.logout(request)
    try:
        print(request.session['userid'])
        del request.session['userid']
        #request.session.clear()
    except KeyError as e:
        print(e)
        pass
    return redirect("/")



def signup(request):
    if request.method=='POST':
        if (request.POST.get('submit')):
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            rollno =int( request.POST.get('rollno'))
            department = request.POST.get('department')
            gender= request.POST.get('gender')
            address = request.POST.get('address')
            cmailid = request.POST.get('mailid')
            password = request.POST.get('password')
            phoneno = request.POST.get('phoneno')
            vnumber = request.POST.get("password2")
            name=fname+lname
            try:
                user=authen.create_user_with_email_and_password(cmailid, password)
                authen.send_email_verification(user['idToken'])
            except Exception as e:
                return render(request, 'web/signup.html', {"message": "mail id already exist"})
            try:
                # if database.order_by_child("rollno").equal_to(rollno).limit_to_first(1).get():
                #     print("already exist")
                # else:
                #if database.child(rollno).
                if not database.child("UserDetails").child(rollno).get().val():
                    data={"name":name,"rollno":rollno,"gender":gender,"department":department,"mailid":cmailid,"phone_number":phoneno,"address":address,"url":"https://x1.xingassets.com/assets/frontend_minified/img/users/nobody_m.original.jpg"}
                    database.child("UserDetails").child(rollno).set(data)
                    return render(request, 'web/signup.html',{"message":"Registered Successfully"})
                else:
                    return render(request, 'web/signup.html', {"message": "Roll number already exists"})
            except Exception as e:
                # return render(request,'web/signup.html',{"message":"Error Occured"})
                print(e)
    return render(request,'web/signup.html')


def forgot_password(request):
    if request.method=='POST':
        if (request.POST.get('submit')):
            emailid = request.POST.get('emailid')
            authen.send_password_reset_email(emailid)
            return redirect("/", {"message": "password reset link has been sent to your respective mail address"})
            #return render(request, 'web/1.html', {"message": "password reset link has been sent to your respective mail address"})
        # return render(request, 'web/1.html',{"message": "error occured try again"})
    return render(request, 'web/forgot_password.html')



def update(request):
    if 'mail' in request.session:
        url = database.child("UserDetails").child(request.session['rollno']).child("url").get().val()
        if request.method=='POST':
            if (request.POST.get('submit')):
                name=request.POST.get('name')
                rollno =int( request.POST.get('rollno'))
                department = request.POST.get('department')
                gender= request.POST.get('gender')
                address = request.POST.get('address')
                cmailid = request.POST.get('cmailid')
                phoneno = request.POST.get('phoneno')
                try:
                    if database.child("UserDetails").child(rollno).get().val():
                        data = {"name": name, "rollno": request.session['rollno'], "gender": gender, "department": department,
                                "mailid": cmailid, "phone_number": phoneno, "address": address}
                        database.child("UserDetails").child(rollno).update(data)
                        return redirect('/profile')
                    else:
                        return render(request, 'web/signup.html', {"message": "Roll number does not exist"})
                except Exception as e:
                    print(e)

        user = []
        rollno = request.session['rollno']
        user.append(database.child("UserDetails").child(rollno).child("name").get().val())
        user.append(rollno)
        user.append(database.child("UserDetails").child(rollno).child("gender").get().val())
        user.append(database.child("UserDetails").child(rollno).child("department").get().val())
        user.append(database.child("UserDetails").child(rollno).child("phone_number").get().val())
        user.append(database.child("UserDetails").child(rollno).child("mailid").get().val())
        user.append(database.child("UserDetails").child(rollno).child("address").get().val())
        return render(request,'web/update_profile.html',{"user":user,"pic":url})
    return redirect('/')
#
# def trip(request):
#     if 'mail' in request.session:
#         if request.method == 'POST':
#             if (request.POST.get('submit')):
#                 start_location = request.POST.get('start_location')
#                 destination = request.POST.get('destination')
#                 trip_date = request.POST.get('trip_date')
#                 start_time = request.POST.get('start_time')
#                 no_of_seats = request.POST.get('no_of_seats')
#                 vehicle_number=request.POST.get('vehicle_number')
#                 print(trip_date)
#
#                 try:
#                     if not database.child("LiftDatabase").child(trip_date).child(request.session['rollno']).get().val():
#                         data = {"destination":destination,"start":start_location,"time":start_time,"date":trip_date,"seats":int(no_of_seats),"vehicle_number":vehicle_number}
#                         database.child("TripDatabase").child(trip_date).child(request.session['rollno']).push(data)
#                         print("if")
#                         return render(request, 'web/tripdetails.html', {"message": "Trip added successfully","pic":url})
#                     else:
#                         print("else")
#                         return render(request,'web/tripdetails.html',{"message":"You have requested for lift ","pic":url})
#                 except Exception as e:
#                     # return render(request,'web/signup.html',{"message":"Error Occured"})
#                     print(e)
#                 print("out")
#                 return render(request,'web/tripdetails.html')
#     return redirect("/")
# def lift(request):
#     if 'mail' in request.session:
#         if request.method == 'POST':
#             if (request.POST.get('submit')):
#                 lift_date = request.POST.get('lift_date')
#                 print(lift_date)
#                 print("abc")
#                 request.session['lift_date']=lift_date
#                 if database.child("TripDatabase").child(lift_date).child(request.session['rollno']).get().val():
#                     if database.child("TripDatabase").child(lift_date).get().val():
#                         users = {}
#                         for i in database.child("TripDatabase").child(lift_date).get().val():
#
#                             for j in database.child("TripDatabase").child(lift_date).child(i).get().val():
#                                 user = []
#                                 print(j)
#                                 print(database.child("TripDatabase").child(lift_date).child(i).child(j).child(
#                                         "seats").get().val())
#                                 if int(database.child("TripDatabase").child(lift_date).child(i).child(j).child("seats").get().val())> 0 :
#                                     user.append(i)
#                                     user.append(database.child("UserDetails").child(i).child("name").get().val())
#                                     user.append(database.child("UserDetails").child(i).child("gender").get().val())
#                                     user.append(database.child("TripDatabase").child(lift_date).child(i).child(j).child(
#                                         "destination").get().val())
#                                     user.append(
#                                         database.child("TripDatabase").child(lift_date).child(i).child(j).child("start").get().val())
#                                     user.append(
#                                         database.child("TripDatabase").child(lift_date).child(i).child(j).child("time").get().val())
#                                     user.append(
#                                         database.child("TripDatabase").child(lift_date).child(i).child(j).child("seats").get().val())
#                                     users[j] = user
#                         return render(request,'web/lift_view.html',{"users":users,"pic":url})
#                     else:
#                         return render(request, 'web/lift_view.html', {"message": "No user exists","pic":url})
#                 else:
#                     return render(request,'web/lift_view.html', {"message": "You have registered for lift provider","pic":url})
#
#             if (request.POST.get('request')):
#                 request_rollno=request.POST.get('rollno')
#                 print(request_rollno)
#                 request_id = request.POST.get('request')
#                 mail=request.session['mail']
#                 sep=mail.split("@")
#                 rno=sep[0].split(".")
#                 print(rno)
#                 try:
#                     if database.child("TripDatabase").child(request.session['lift_date']).child(request_rollno).child(request_id).child("request_list").child(rno[1]).get().val() or database.child("TripDatabase").child(request.session['lift_date']).child(request_rollno).child(request_id).child("lift_takers").child(rno[1]).get().val():
#                         return render(request, 'web/lift_view.html',{"message":"Already Requested"})
#                     else:
#                         data = {"status":0,"trip_provider":request_rollno,"ref_id":request_id,"start_location":request.session['start_location'],"destination":request.session['destination']}
#                         database.child("LiftDatabase").child(request.session['lift_date']).child(rno[1]).push(data)
#                         sender = ""
#                         for i in database.child("LiftDatabase").child(request.session['lift_date']).child(rno[1]).get().val():
#                             if request_id == database.child("LiftDatabase").child(request.session['lift_date']).child(rno[1]).child(i).child("ref_id").get().val():
#                                 sender = i
#                                 print(sender)
#                                 break
#
#                         database.child("TripDatabase").child(request.session['lift_date']).child(request_rollno).child(request_id).child("request_list").child(rno[1]).set(sender)
#                         return render(request, 'web/lift_view.html',{"message","Successfully booked the seat","pic":url})
#                 except Exception as e:
#                     #return render(request,'web/lift_view.html',{"message":"Error Occured"})
#                     print(e)
#
#                 print(request_id)
#         return render(request,'web/lift_view.html')
#     return redirect("/")


def cancel_ride_request(request):
    if 'mail' in request.session:
        url = database.child("UserDetails").child(request.session['rollno']).child("url").get().val()
        if request.method == 'POST':
            mail = request.session['mail']
            sep = mail.split("@")
            rno = sep[0].split(".")
            print(rno)
            if (request.POST.get('submit')):
                lift_date = request.POST.get('lift_date')
                print(lift_date)
                print("abc")
                request.session['lift_cancel_date'] = lift_date
                if database.child("LiftDatabase").child(lift_date).child(rno[1]).get().val():
                    users = {}
                    for i in database.child("LiftDatabase").child(lift_date).child(rno[1]).get().val():
                        user = []
                        trip_provider=database.child("LiftDatabase").child(lift_date).child(rno[1]).child(i).child("trip_provider").get().val()
                        ref_id=database.child("LiftDatabase").child(lift_date).child(rno[1]).child(i).child("ref_id").get().val()
                        user.append(trip_provider)
                        user.append(database.child("UserDetails").child(trip_provider).child("name").get().val())
                        user.append(database.child("TripDatabase").child(lift_date).child(trip_provider).child(ref_id).child(
                            "destination").get().val())
                        user.append(
                            database.child("TripDatabase").child(lift_date).child(trip_provider).child(ref_id).child(
                                "start").get().val())
                        user.append(
                            database.child("TripDatabase").child(lift_date).child(trip_provider).child(ref_id).child(
                                "time").get().val())
                        users[i] = user
                    return render(request, 'web/trip_booking_details.html', {"users": users,"pic":url})
                else:
                    return render(request, 'web/trip_booking_details.html', {"message": "No user exists","pic":url})

            if (request.POST.get('cancel_request')):
                ref_id = request.POST.get('cancel_request')
                mail = request.session['mail']
                sep = mail.split("@")
                rno = sep[0].split(".")
                print(rno)
                try:
                    trip_provider=database.child("LiftDatabase").child(request.session['lift_cancel_date']).child(
                            rno[1]).child(ref_id).child("trip_provider").get().val()
                    trip_ref_id = database.child("LiftDatabase").child(request.session['lift_cancel_date']).child(
                        rno[1]).child(ref_id).child("ref_id").get().val()
                    if (database.child("LiftDatabase").child(request.session['lift_cancel_date']).child(rno[1]).child(ref_id).child("status").get().val()) ==1:
                        seats=int(database.child("TripDatabase").child(request.session['lift_cancel_date']).child(trip_provider).child(trip_ref_id).child("seats").get().val())+1
                        database.child("TripDatabase").child(request.session['lift_cancel_date']).child(
                            trip_provider).child(trip_ref_id).child("seats").set(seats)
                    database.child("LiftDatabase").child(request.session['lift_cancel_date']).child(rno[1]).child(ref_id).remove()
                    if database.child("TripDatabase").child(request.session['lift_cancel_date']).child(trip_provider).child(trip_ref_id).child("request_list").child(rno[1]).get().val():
                        database.child("TripDatabase").child(request.session['lift_cancel_date']).child(
                            trip_provider).child(trip_ref_id).child("request_list").child(rno[1]).remove()
                    if database.child("TripDatabase").child(request.session['lift_cancel_date']).child(trip_provider).child(trip_ref_id).child("lift_takers").child(rno[1]).get().val():
                        database.child("TripDatabase").child(request.session['lift_cancel_date']).child(
                            trip_provider).child(trip_ref_id).child("lift_takers").child(rno[1]).remove()
                    return render(request, 'web/trip_booking_details.html', {"message": "Cancelled the Request","pic":url})

                except Exception as e:
                    # return render(request,'web/signup.html',{"message":"Error Occured"})
                    print(e)

        return render(request, 'web/trip_booking_details.html')
    return redirect("/")


def accept_lift_request(request):
    if 'mail' in request.session:
        url = database.child("UserDetails").child(request.session['rollno']).child("url").get().val()
        if request.method == 'POST':

            mail = request.session['mail']
            sep = mail.split("@")
            rno = sep[0].split(".")
            print(rno)
            if (request.POST.get('submit')):
                lift_date = request.POST.get('lift_date')
                request.session['lift_date']=lift_date
                print(lift_date)
                users={}
                if database.child("TripDatabase").child(lift_date).child(rno[1]).get().val():
                    for i in  database.child("TripDatabase").child(lift_date).child(rno[1]).get().val():
                        user=[]
                        if database.child("TripDatabase").child(lift_date).child(rno[1]).child(i).child("request_list").get().val():
                            for j in database.child("TripDatabase").child(lift_date).child(rno[1]).child(i).child("request_list").get().val():
                                rid=database.child("TripDatabase").child(lift_date).child(rno[1]).child(i).child("request_list").child(j).get().val()
                                user.append(j)
                                user.append(database.child("UserDetails").child(j).child("name").get().val())
                                user.append(database.child("UserDetails").child(j).child("gender").get().val())
                                user.append(database.child("UserDetails").child(j).child("department").get().val())
                                user.append(database.child("LiftDatabase").child(lift_date).child(j).child(rid).child("destination").get().val())
                                user.append(database.child("TripDatabase").child(lift_date).child(rno[1]).child(i).child("time").get().val())
                            users[i]=user
                    if len(users)<=0:
                        return render(request, 'web/lift_accepting_list.html', {"message": "NO request","pic":url})
                    else:
                        return render(request, 'web/lift_accepting_list.html', {"users": users,"pic":url})
                else:
                    return redirect('/home')
            if (request.POST.get('accept_request')):
                rollno = request.POST.get('rollno')
                rid=request.POST.get('accept_request')
                print(rollno)
                print(rid)
                print(request.session['lift_date'])
                if int(database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(
                        rid).child("seats").get().val()) > 0 and database.child("LiftDatabase").child(
                        request.session['lift_date']).child(rollno).child(
                        database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(
                            rid).child("request_list").child(rollno).get().val()).child("status").get().val() != 1:

                    req_rid=database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(rid).child("request_list").child(rollno).get().val()
                    database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(rid).child("lift_takers").child(rollno).set(req_rid)
                    seats=int(database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(rid).child("seats").get().val())-1
                    database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(rid).child("seats").set(seats)
                    database.child("LiftDatabase").child(request.session['lift_date']).child(rollno).child(req_rid).child("status").set(1)
                    database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(rid).child("request_list").child(rollno).remove()
                else:
                    return render(request, 'web/lift_accepting_list.html',{"message":"max seat capacity or the user already got a ride"})

                    # seats = int(database.child("TripDatabase").child(request.session['lift_date']).child(request_rollno).child(
                    #     request_id).child("seats").get().val())
                    # seats = seats - 1
                    #
                    # database.child("TripDatabase").child(request.session['lift_date']).child(request_rollno).child(
                    #     request_id).child(
                    #     "seats").set(seats)
            if (request.POST.get('decline_request')):
                rollno = request.POST.get('rollno')
                rid=request.POST.get('decline_request')
                print(rollno)
                print(rid)
                sender_rid=database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(rid).child("request_list").child(rollno).get().val()
                database.child("LiftDatabase").child(request.session['lift_date']).child(rollno).child(sender_rid).remove()
                database.child("TripDatabase").child(request.session['lift_date']).child(rno[1]).child(rid).child("request_list").child(rollno).remove()
                return render(request, 'web/lift_accepting_list.html',
                              {"message": "declined the request"})
        return render(request,'web/lift_accepting_list.html')

    return  redirect("/")



def firebase1(request):
    if request.method == 'POST':
        if (request.POST.get('submit')):
            lift_date = request.POST.get('start_address')
            lift_date1 = request.POST.get('dest_address')
            print(lift_date)
            print(lift_date1)
    return render(request,"web/testui.html")


def display_profile(request):
    if 'mail' in request.session:

        if request.method == 'POST':
            print("efg")
            if (request.POST.get('image_request')):
                print("abc")
                storage=firebase.storage()

                pic =request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save("static\\"+pic.name, pic)

                uploaded_file_url = fs.url("static\\"+filename)
                print(uploaded_file_url)
                token=storage.child(request.session['rollno']).put(filename)
                # data = {"photo": url}
                # database.child("UserDetais").child(request.session['rollno']).set(data)
                print(token['downloadTokens'])
                url=(storage.child(request.session['rollno']).get_url(token['downloadTokens']))
                database.child("UserDetails").child(request.session['rollno']).child("url").set(str(url))
                fs.delete(filename)
        user=[]
        rollno=request.session['rollno']
        url = database.child("UserDetails").child(rollno).child("url").get().val()
        user.append(database.child("UserDetails").child(rollno).child("name").get().val())
        user.append(rollno)
        user.append(database.child("UserDetails").child(rollno).child("gender").get().val())
        user.append(database.child("UserDetails").child(rollno).child("department").get().val())
        user.append(database.child("UserDetails").child(rollno).child("mailid").get().val())
        user.append(database.child("UserDetails").child(rollno).child("address").get().val())
        user.append(database.child("UserDetails").child(rollno).child("phone_number").get().val())
        print(url)
        return render(request, "web/profile.html", {"user": user,"pic":url})
    return redirect('/')