from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from examapp.models import Quetion, result

from django.contrib import auth

# Create your views here.

def giveMePage1(request):
    return render(request,'examapp/quetionmanagement.html')

def giveMePage2(request):
    return render(request,'examapp/resultanalysis.html')

def giveMePage3(request):
    return render(request,'examapp/admindashboard.html')


def showRemainingTime(request):

       request.session['duration'] = request.session['duration'] - 1
       return HttpResponse(request.session['duration'])



def search(request,pageno):
       
    endindex=int(pageno)*3
    startindex=endindex-3

    queryset=result.objects.filter(subject=request.session['subject'])[startindex:endindex]

    print(queryset)

    count=request.session['count']

    list=[]

    for i in range(0,count):
        list.append(i+1)

    print(list)

    return render(request,'examapp/search.html',{'results':queryset,'listofint':list})
        
    
def search1(request):

     subject=request.GET["subject"]
     request.session['subject']=subject
     noofrecords=result.objects.filter(subject=subject).count()
     i=noofrecords
     count=0

     while i>0:
         count=count+1
         i=i-3
    
     print(f"noofrecords is {noofrecords} and noofpages is {count}")

     request.session['count']=count

     queryset=result.objects.filter(subject=subject)[0:3]
     print(queryset)

     l=[]
     for i in range(0,count):
        l.append(i+1)
     print(l)

     return render(request,'examapp/search.html',{'results':queryset,'listofint':l})


def startTest(request):

    subjectname=request.GET["subject"]
    
    request.session["subject"]=subjectname

    queryset=Quetion.objects.filter(subject=subjectname)


    
    quetionobject=queryset[0]

    return render(request,'examapp/quetion.html',{'quetion':quetionobject})


def nextQuetion(request):

    if 'op' in request.GET:

        dict=request.session["answers"]
        dict[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]

        print(dict)
    
    quetionlist=Quetion.objects.filter(subject=request.session["subject"])

    if (request.session["qindex"]<len(quetionlist)-1):


       request.session["qindex"]=request.session["qindex"]+1

       quetionobject=quetionlist[request.session["qindex"]]

       qno=quetionobject.qno
       qno=str(qno)

       dictionary=request.session["answers"]

       if qno in dictionary:

            questiondetails=dictionary[qno]

            previousanswer=questiondetails[3]

       else:
            previousanswer=''

       return render(request,'examapp/quetion.html',{'quetion':quetionobject,'previousanswer':previousanswer})
    
    else:

        return render(request,'examapp/quetion.html',{'quetion':quetionlist[len(quetionlist)-1],'message':'quetion over.please click on previous or end exam'})
    


    
def previousQuetion(request):

    if 'op' in request.GET:

        dict=request.session["answers"]
        dict[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]

        print(dict)
    quetionlist=Quetion.objects.filter(subject=request.session["subject"])

    if (request.session["qindex"]>0):


       request.session["qindex"]=request.session["qindex"]-1

       quetionobject=quetionlist[request.session["qindex"]]

       qno=quetionobject.qno
       qno=str(qno)

       dictionary=request.session["answers"]

       if qno in dictionary:
           quetiondetails=dictionary[qno]
           previousanswer=quetiondetails[3]

       else:
           previousanswer=''
              

       return render(request,'examapp/quetion.html',{'quetion':quetionobject,'previousanswer':previousanswer})
    
    else:

        return render(request,'examapp/quetion.html',{'quetion':quetionlist[0],'message':'quetion over.please click on next or end exam'})
    

def endexam(request):
          
     if 'op' in request.GET:
        
        dictionary=request.session["answers"]

        dictionary[request.GET["qno"]] = [request.GET["qno"],request.GET["qtext"],request.GET["answer"],request.GET["op"]] 

        print(dictionary)

     dictionary=request.session["answers"]

     listoflist=dictionary.values()


     for list in listoflist:
         if list[2]==list[3]:
             request.session["score"]=request.session["score"]+1
    
     finalscore=request.session["score"]
     username=request.session["username"]
     subjectname=request.session["subject"]

     result.objects.create(username=username,score=finalscore,subject=subjectname)

     print(connection.queries) 

     auth.logout(request) # it will remove all keys from session

     return render(request,'examapp/score.html',{'username':username,'score':finalscore,'listoflist':listoflist})

    
def addQuetion(request):

    Quetion.objects.create(qno=request.GET["qno"],subject=request.GET["subject"],answer=request.GET["answer"],qtext=request.GET["qtext"],op1=request.GET["op1"],op2=request.GET["op2"],op3=request.GET["op3"],op4=request.GET["op4"])
    
    return render(request,"examapp/quetionmanagement.html",{'message':'question added'})


def viewQuetion(request):
   
    question=Quetion.objects.get(qno=request.GET["qno"],subject=request.GET["subject"])

    print(connection.queries)

    return render(request,"examapp/quetionmanagement.html",{'question':question})


def updateQuetion(request):

    question=Quetion.objects.filter(qno=request.GET["qno"],subject=request.GET["subject"])

    question.update(qtext=request.GET["qtext"],answer=request.GET["answer"],op1=request.GET["op1"],op2=request.GET["op2"],op3=request.GET["op3"],op4=request.GET["op4"])
    
    print(connection.queries)

    return render(request,"examapp/quetionmanagement.html",{'message':"Record Updated"})


def deleteQuetion(request):

    queryset=Quetion.objects.filter(qno=request.GET["qno"],subject=request.GET["subject"])
    
    queryset.delete()

    print(connection.queries)

    return render(request,"examapp/quetionmanagement.html",{'message':"Record Deleted"})    


    
