from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Post,Comment
# Create your views here.


def home(request):
    if not request.session.has_key('username'):
           return redirect('/')    

    posts=Post.objects.all()

    if request.method=="GET":
        return render(request,'home.html',{"name":request.session["username"],'posts':posts})

    pos=Post.objects.create(user=User.objects.get(name=request.session['username']),content=request.POST['post'],genre=request.POST['genre'])
    pos.save()
    return redirect('/home')


def post(request,id=1):
    if not request.session.has_key('username'):
        return redirect('/') 

    p=Post.objects.get(id=id)
    cs=Comment.objects.filter(post=id)
        
    if request.method=="GET":
       return render(request,'post.html',{'p':p,'cs':cs})  

    com=Comment.objects.create(user=User.objects.get(name=request.session['username']),content=request.POST['comment'],post=p)
    com.save()
    return redirect('/post/{}'.format(id))


def myposts(request):
     if not request.session.has_key('username'):
        return redirect('/') 

    if request.method=="GET":
        posts=Post.objects.filter(user=User.objects.get(name=request.session["username"]),genre__contains=request.GET.get("genre",""))
        return render(request,'myposts.html',{"posts":posts})
    
    if Post.objects.filter(id=request.POST["id"]).exists():
        new=Post.objects.get(id=request.POST["id"])
        if len(request.POST["post"])>0:
            new.content=request.POST["post"]
        if len(request.POST["genre"])>0:
            new.genre=request.POST["genre"]
        new.save()
    return redirect('/myposts')

def mycomments(request):
     if not request.session.has_key('username'):
        return redirect('/') 
        
    comments=Comment.objects.filter(post__in=Post.objects.filter(user=User.objects.get(name=request.session["username"])))
    return render(request,'mycomments.html',{'comments':comments})


def login(request):
    if request.method=='GET':
        return render(request,'login.html',{'message':''})

    global current
    current=User('','')    
    
    if len(request.POST["password"])==0 or len(request.POST["username"])==0:
        return render(request,'login.html',{'message':'Some fields are missing'})

    if not(User.objects.filter(name=request.POST["username"]).exists()):
        return render(request,'login.html',{'message':'Username is incorrect'})

    if User.objects.get(name=request.POST["username"]).password!=request.POST["password"]:
        return render(request,'login.html',{'message':'Password is incorrect'})
  
    request.session['username']=request.POST["username"]
    return redirect('/home')    


def reg(request):
    if request.method=='GET':
        return render(request,'reg.html',{'error':''})
    
    if len(request.POST["password"])==0 or len(request.POST["cp"])==0 or len(request.POST["username"])==0:
            return render(request,'reg.html',{'error':'Some fields are missing'})

    if(request.POST["password"]!=request.POST["cp"]):
        return render(request,'reg.html',{'error':'Password not confirmed'})

    names=User.objects.all()
    for p in names:
        if p.name==request.POST["username"]:
            return render(request,'reg.html',{'error':'Username already exists'})

    u=User.objects.create(name=request.POST["username"],password=request.POST["password"])
    u.save()
    return render(request,'reg.html',{'error':'Registered Successfully!'})

