from django.shortcuts import render,HttpResponse,redirect
# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from home.models import Registration,UserBookData
from django.contrib.auth.models import User,auth
from django.contrib import messages
from aidiet import settings
import requests
from django.core.mail import send_mail
from django.conf import settings
import json
import random
import os
from together import Together

def signup(request):
    # return HttpResponse("This is home page")
    return render(request,'signup.html')


# def login(request):
#     if request.method=="POST":
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']


#         Registratio=Registration(first_name=first_name,last_name=last_name,email=email,password=password)
#         Registratio.save()
#         return render(request,'login.html')
#     return render(request,'login.html')

def login(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the email already exists in the database
        if Registration.objects.filter(email=email).exists():
            # Email already exists, do not save and return an error or simply return nothing
            
            return render(request, 'login.html', {'error': 'Email already exists'})
        else:
            # Email does not exist, save the new record
            new_registration = Registration(first_name=first_name, last_name=last_name, email=email, password=password)
            
            new_registration.save()
            send_mail(
                    subject='Login Successful',
                    message=f'Login Successful',
                    from_email='agrawalharsh0522@gmail.com',  # Use the email you set in settings.py
                    recipient_list=[email],
                    fail_silently=False,
            )
            return render(request,'login.html')
            
    return render(request,'login.html')

def process_login(request):
    if request.method=="POST":
        check_email=request.POST['email']
        check_password=request.POST['password']

        try:
            user = Registration.objects.get(email=check_email)
            if user.password == check_password:
                # Login successful, send an email to the user
                # send_mail(
                #     subject='Login Successful',
                #     message=f'Hello You have successfully logged in.',
                #     from_email='agrawalharsh0522@gmail.com',  # Use the email you set in settings.py
                #     recipient_list=[check_email],
                #     fail_silently=False,
                # )
                # request.session.set_expiry(3)
                request.session['first_name'] = user.first_name
                request.session['email']=user.email
                return redirect("/home")
            else:
                messages.error(request, 'Incorrect Password!!')
                return redirect('/login')
                # return render(request,'login.html',{'error':'INcorrect Password!!'})


        # Problem faced in this code urls not matching  ---- DONE
        except Registration.DoesNotExist:
            messages.error(request, 'Email not exist, PLease Create an account first!!')
            # return redirect('/')
            # return messages.error(request,'Email not exist')
    
    return render(request,'login.html')

        
def home(request):
    result=request.session.get('result')
    email = request.session.get('email')

    
    
    #  Personalized user operation

    Incomplete = UserBookData.objects.filter(email=email,is_completed=False)
    incomplete_list = [
      {'id': a_project.BookId,
       'name': a_project.BookName
      }
      for a_project in Incomplete 
    ]

    Complete=UserBookData.objects.filter(email=email,is_completed=True)
    complete_list = [
      {'id': a_project.BookId,
       'name': a_project.BookName
      }
      for a_project in Complete 
    ]

    context={
        'username':username,
        'email':email,
        'incomplete_books':incomplete_list,
        'completed_books':complete_list,
        'result':result
    }

    return render(request,'home.html',context)  #perfect

def AddNewBook(request):
    email=request.session.get('email')
    if request.method=="POST":
        BookName = request.POST['BookName']
        BookId=random.randint(0,999999)
        NewBook = UserBookData(email=email,BookId=BookId,BookName=BookName,is_completed=False)
            
        NewBook.save()

        return redirect("/home")
    return redirect("/home")

def MarkAsCompleted(request,book_id):
    
    if request.method=="POST":
        user = UserBookData.objects.get(BookId=book_id)

        user.is_completed=True
        user.save()

        return redirect("/home")




    return redirect("/home")


def Recommended(request):
    email=request.session.get('email')
    print(email)
    if request.method=="POST":
        Complete=UserBookData.objects.filter(email=email,is_completed=True)
        completedbook=""
        for a_project in Complete:
            completedbook=completedbook+","+a_project.BookName
        
        print(completedbook)

        client = Together(api_key="YOUR API KEY")
        stream = client.chat.completions.create(
              model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
              messages=[{"role": "user", "content": "I completed this"+ completedbook +"books. pLease suggest me other books based on this"}],
              stream=True,
        )
        # response = client.chat.completions.create(
        #     model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        #     messages=[],
        #     max_tokens=512,
        #     temperature=0.7,
        #     top_p=0.7,
        #     top_k=50,
        #     repetition_penalty=1,
        #     stop=["<|eot_id|>","<|eom_id|>"],
        #     stream=True
        # )
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end='', flush=True)

# Render the result in the templat
    # request.session['result']=full_response
        request.session['result'] = full_response
        print(full_response)
        return redirect("/home")
    

    



        
        


    


