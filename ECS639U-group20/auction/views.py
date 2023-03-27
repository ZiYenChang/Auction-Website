from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
import json
import os

from .models import User, Question, Answer, Item, Bid
from .forms import SignUpForm

#import the emailing function
from .email import sendSimpleEmail

def spa_view(request):
    """
        Function to the SPA
    """
    return render(request, "auction/spa/index.html", {})


def signup(request):
    '''
        View function to let a user sign up
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            print("Info about user:" + request.POST.get('email'))
            sendSimpleEmail(request.POST.get('email'))
            auth_login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    '''
        View function to let a user log in
    '''
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                response = redirect('/')
                return response
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def questions_api(request):
    '''
        View api function for all questions of an item
    '''
    if request.method == 'GET':
        return JsonResponse({
            'questions': [
                question.to_dict()
                for question in Question.objects.all()
            ]
        })

    elif request.method == 'POST':
        body = json.loads(request.body)
        item_question = Item.objects.get(id=body['item'])
        user_question = User.objects.get(id=body['user'])
        question = Question.objects.create(
            question_body = body['question_body'],
            question_time = body['question_time'],
            item = item_question,
            user = user_question
            )

        return JsonResponse(question.to_dict())

def question_api(request: HttpRequest, question_id: int) -> HttpResponse:
    '''
        View api function for one question of an item
    '''
    question = get_object_or_404(Question, id=question_id)
    print(question)
    if request.method == 'GET':
        print(question.to_dict)
        return JsonResponse(question.to_dict())

    if request.method == 'PUT':
        body = json.loads(request.body)
        question.answer = body['answer']
        question.save()

        return JsonResponse(question.to_dict())

def answers_api(request):
    '''
        View api function for the answer of one question
    '''
    if request.method == 'GET':
        return JsonResponse({
            'answers': [
                answer.to_dict()
                for answer in Answer.objects.all()
            ]
        })
    
    elif request.method == 'POST':
        body = json.loads(request.body)
        question = get_object_or_404(Question, id=body['question'])
        owner = User.objects.get(id=body['user'])
        answer = Answer.objects.create(
            answer_body = body['answer_body'],
            answer_time = body['answer_time'],
            user = owner
            )
        
        question.answer= answer
        question.save()
        
        return JsonResponse(answer.to_dict())

def user_api(request):
    '''
        View api function for one user
    '''
    print("This is the current session user")
    print(request.user)
    if request.method == 'GET':
        return JsonResponse({ 
            "user": request.user.to_dict()
        })
    
    if request.method == 'PUT':
        userPut = get_object_or_404(User, id = request.user.id)
        body = json.loads(request.body)
        userPut.username = body["username"]
        userPut.email = body["email"]
        userPut.date_of_birth = body["date_of_birth"]
        userPut.city = body["city"]

        userPut.save()

        return JsonResponse(
            {"userPut": [userPut.to_dict()]}
        )

    if request.method == "POST":
        userPost = get_object_or_404(User, id = request.user.id)
        userPost.profile_image = request.FILES.get('profile_image')

        userPost.save()
        return JsonResponse(
            {"userPost": [userPost.to_dict()]}
        )


def item_api(request: HttpRequest, item_id: int) -> HttpResponse:
    '''
        View api function for one question of an item
    '''
    item = get_object_or_404(Item, id=item_id)
    print(item)
    if request.method == 'GET':
        print(item.to_dict)
        return JsonResponse(item.to_dict())

def bids_api(request):
    '''
        View api function for the items listed
    '''
    print("I'm trying to get bids")
    if request.method == 'GET':
        return JsonResponse({
            'bids': [
                bid.to_dict()
                for bid in Bid.objects.all()
            ]
        })

    elif request.method == 'POST':
        body = json.loads(request.body)
        item_bid = Item.objects.get(id=body['item'])
        user_bid = User.objects.get(id=body['user'])
        bid = Bid.objects.create(
            bid_amount = body['bid_amount'],
            bid_time = body['bid_time'],
            item = item_bid,
            user = user_bid
            )

        return JsonResponse(bid.to_dict())

def newitem_api(request):
    if request.method == 'GET':
        return JsonResponse({
            'items': [
                item.to_dict()
                for item in Item.objects.all()
            ]
        })

    if request.method == 'POST':
        # body=json.loads(request.body)
        # user_item = get_object_or_404(User, id = request.user.id)
        print("in post")
        print(request.user)
        print(request.FILES)
        owner = get_object_or_404(User, id = request.user.id)

        item = Item.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            deadline=request.POST.get('deadline'),
            starting_price=request.POST.get('starting_price'),
            picture=request.FILES.get('picture'),
            user=owner
        )
        return JsonResponse(item.to_dict())


def search_api(request):
    ''' search an item '''
    if request.method == 'POST':
        search_str=json.loads(request.body).get('searchText')

        searching = Item.objects.filter(title__icontains=search_str)  |  Item.objects.filter(description__icontains=search_str)

        data=searching.values()
        return JsonResponse(list(data), safe=False) 
    