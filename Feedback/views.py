from django.shortcuts import render, render_to_response
from Feedback.models import *
from django.core.urlresolvers import reverse_lazy
from django.forms.models import inlineformset_factory, model_to_dict,modelformset_factory
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from CRM.models import *
from Registration.models import *
from Feedback.forms import *
from django.http.response import HttpResponse, JsonResponse
from django.forms.formsets import formset_factory
from django.template import RequestContext
from datetime import date, datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from datetime import datetime
from operator import itemgetter
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
from Timeline.models import *
from django.utils import timezone
from django.contrib import messages
from Feedback.filters import *
# Create your views here.




@login_required(login_url="/registration/login/")
def new_feed(request):
    
        msg=""
        user=request.user
        group=Group.objects.get(user=user)
        if group.name=="Customer":
            
            lead_u=lead_user.objects.get(user=user)
            print(lead_u.pk,lead_u.customer)
            lead=Lead.objects.get(pk=lead_u.customer.pk)
            address= UserProfile.objects.get(user=lead.member)
             
            qlist=feedback_question.objects.all()
            qlist1=FeedbackSubquestion.objects.all()
            
            inlineformset=formset_factory(FeedbackFormCust, extra=0)
            print(qlist)
            #qform=inlineformset(initial=[{'question':v.question}for v in qlist,{'sub_question':i.question} for i in qlist1]) 
            qform=inlineformset(initial=[{'question':v.question}for v in qlist])
            qform=inlineformset(initial=[{'sub_question':i.sub_question} for i in qlist1]) 
            #qform=inlineformset()
            print ("qform--------------------------",qform)
            if request.method=="POST":
                print("post")
                
                qform=inlineformset(request.POST)
                i=1
                print(qform.errors)
                if qform.is_valid():
                    for form in qform.forms:
                       print("within valid form",i)
                       i=i+1 
                    print("----------------------valid")
                    j=0
                    lead_u=lead_user.objects.get(user=request.user)
                    lead=Lead.objects.get(pk=lead_u.customer.pk)
                    cust_feedback=Custfeedback()
                    cust_feedback.customer=lead
                    cust_feedback.date=datetime.now().today()
                    cust_feedback.comment=request.POST.get('comment')
                    cust_feedback.save()
                    now = timezone.now()
                    variable=Timeline(comment1="have send a ", comment2="Feddback",action_create=now,user=self.request.user)
                    variable.save()
                    for form in qform.forms:
                        
                        questionfrm=form.cleaned_data['question']
                        answerfrm=form.cleaned_data['answer']
                        sub_questionfrm=form.cleaned_data['sub_question']
                        sub_answerfrm=form.cleaned_data['sub_answer']
                        subquestion=FeedbackSubquestion.objects.get(sub_question=sub_questionfrm)
                        #print("questionfrm : ",questionfrm)
                        #print ("answerfrm : ",answerfrm)
                        #print ("request.user ",request.user)
                        
                        question=feedback_question.objects.get(question=questionfrm)
                        print("question",question)
                        feedback_obj=Custfeedquestion()
                        feedback_obj.feedback_cust=cust_feedback
                        
                        feedback_obj.question=question
                        #qualify_obj.answer=answerfrm
                        feedback_obj.sub_question=subquestion
                        feedback_obj.sub_answer=sub_answerfrm
                        
                        answer2=request.POST.get(str(j)+'-answer2')
                        print("answer2",answer2)
                        print("%%%%%%%%%%%%%%:  ",j)
                        #if answer2 is not None:
                            #qualify_obj.answer=answer2
                        #else:
                        feedback_obj.answer=answer2
                        
                        #customer=request.user ,question=questionfrm,answer=answerfrm
                        feedback_obj.save()
                        j=j+1
                    lead_u=lead_user.objects.get(user=request.user)
                    lea=Lead.objects.get(pk=lead_u.customer.pk)
                    notify.send(request.user,recipient=lea.member,verb=" submitted a feedback")
                    qform=inlineformset()   
                    variables = RequestContext(request, {'qform':qform,'msg1':'Feedback submitted successfully','group':group,'address':address,'l':'1'})
                    return render(request,'Feedback/feedback_form.html',variables)  
                    
                else:
                    print("form invalid")
                    qform=inlineformset(request.POST)
                    variables = RequestContext(request, {'qform':qform,'msg':'Can not submit feedback','group':group,'address':address,'l':'0'})
                    return render_to_response('Feedback/feedback_form.html', variables)
            
            else:
                    print("get")
                    
                    variables = RequestContext(request, {'qform':qform,'group':group,'address':address,'l':'0'})
                    return render_to_response('Feedback/feedback_form.html', variables)
        elif group.name=="Lead":
                    lead_u=lead_user.objects.get(user=user)
                    print(lead_u.pk,lead_u.customer)
                    lead=Lead.objects.get(pk=lead_u.customer.pk)
                    address= UserProfile.objects.get(user=lead.member)
                     
                    qlist=feedback_question.objects.all()
                    qlist1=FeedbackSubquestion.objects.all()
                    
                    inlineformset=formset_factory(FeedbackFormCust, extra=0)
                    print(qlist)
                    #qform=inlineformset(initial=[{'question':v.question}for v in qlist,{'sub_question':i.question} for i in qlist1]) 
                    qform=inlineformset(initial=[{'question':v.question}for v in qlist])
                    qform=inlineformset(initial=[{'sub_question':i.sub_question} for i in qlist1]) 
                    #qform=inlineformset()
                    print ("qform--------------------------",qform)
                    if request.method=="POST":
                        print("post")
                        
                        qform=inlineformset(request.POST)
                        i=1
                        print(qform.errors)
                        if qform.is_valid():
                            for form in qform.forms:
                               print("within valid form",i)
                               i=i+1 
                            print("----------------------valid")
                            j=0
                            lead_u=lead_user.objects.get(user=request.user)
                            lead=Lead.objects.get(pk=lead_u.customer.pk)
                            cust_feedback=Custfeedback()
                            cust_feedback.customer=lead
                            cust_feedback.date=datetime.now().today()
                            cust_feedback.comment=request.POST.get('comment')
                            cust_feedback.save()
                            now = timezone.now()
                            variable=Timeline(comment1="have send a ", comment2="Feddback",action_create=now,user=self.request.user)
                            variable.save()
                            for form in qform.forms:
                                
                                questionfrm=form.cleaned_data['question']
                                answerfrm=form.cleaned_data['answer']
                                sub_questionfrm=form.cleaned_data['sub_question']
                                sub_answerfrm=form.cleaned_data['sub_answer']
                                subquestion=FeedbackSubquestion.objects.get(sub_question=sub_questionfrm)
                                #print("questionfrm : ",questionfrm)
                                #print ("answerfrm : ",answerfrm)
                                #print ("request.user ",request.user)
                                
                                question=feedback_question.objects.get(question=questionfrm)
                                print("question",question)
                                feedback_obj=Custfeedquestion()
                                feedback_obj.feedback_cust=cust_feedback
                                
                                feedback_obj.question=question
                                #qualify_obj.answer=answerfrm
                                feedback_obj.sub_question=subquestion
                                feedback_obj.sub_answer=sub_answerfrm
                                
                                answer2=request.POST.get(str(j)+'-answer2')
                                print("answer2",answer2)
                                print("%%%%%%%%%%%%%%:  ",j)
                                #if answer2 is not None:
                                    #qualify_obj.answer=answer2
                                #else:
                                feedback_obj.answer=answer2
                                
                                #customer=request.user ,question=questionfrm,answer=answerfrm
                                feedback_obj.save()
                                j=j+1
                            lead_u=lead_user.objects.get(user=request.user)
                            lea=Lead.objects.get(pk=lead_u.customer.pk)
                            notify.send(request.user,recipient=lea.member,verb=" submitted a feedback")
                            qform=inlineformset()   
                            variables = RequestContext(request, {'qform':qform,'msg1':'Feedback submitted successfully','group':group,'address':address,'l':'1'})
                            return render(request,'Feedback/feedback_form.html',variables)  
                            
                        else:
                            print("form invalid")
                            qform=inlineformset(request.POST)
                            variables = RequestContext(request, {'qform':qform,'msg':'Can not submit feedback','group':group,'address':address,'l':'0'})
                            return render_to_response('Feedback/feedback_form.html', variables)
                     
                     
                    else:
                            print("get")
                            
                            variables = RequestContext(request, {'qform':qform,'group':group,'address':address,'l':'0'})
                            return render_to_response('Feedback/feedback_form.html', variables)            
        else:
            user=request.user
            print(user.pk)
            lead_list=Lead.objects.filter(member=request.user)
           
            feedback=[]
            obj1=[]
            mag=""
            flag=False
            obj2=None
            l1=0
            feddback_list=None
            if lead_list:
                for leads in lead_list:
                    
                    feddback_list=Custfeedback.objects.filter(customer=leads).order_by('date')
                    #print("feddback_list",feddback_list)
                    if len(feddback_list)>0:
                        for feed in feddback_list:
                            print(feed.date)
                            feedback.append(feed)
                            l1=1
               
                
                for feed in feedback:
                    print("feed",feedback.count(feed)) 
                    if len(obj1)==0:
                        obj1.append(feed)
                        print(obj1)
                    flag=0
                    for ob in obj1:      
                            if ob.customer==feed.customer and ob.date==feed.date : 
                                print("old list customer : ",feed.customer)
                                print("old list date : ",feed.date)
                                print("new list date: ",ob.date)
                                print("new list customer ",feed.date)
                                flag=0
                            else:
                                flag=1
                    if flag==1:                         
                        obj1.append(feed)
                                #obj.append()  """  
                  
                obj1.sort(key=lambda  x: x.date, reverse=True)

# To return a new list, use the sorted() built-in function...
                #newlist = sorted(obj1, key=lambda x: obj1.count(x), reverse=True)
                print("final object : ",feedback)
            if l1==0:
                print("flag true")
                variables=RequestContext(request,{'feedlist':feedback,"group":group,"msg":msg})
                
                
            else:
                print("flag false")
                msg="No feedbacks yet"
                print("************************no feedback")
                
                variables=RequestContext(request,{'feedlist':feedback,"group":group})
                
                
            return render(request,'Feedback/FeedBack_list.html',variables)
    


def get_lead(request):
    user=request.user
    l=lead_user.objects.get(user=user)
    
    data=model_to_dict(l)
    return JsonResponse(data)

def get_feeds(request):
    id=request.GET.get("id")
    date=request.GET.get("date")
    qlist=feedback_question.objects.all()
    sqlist=FeedbackSubquestion.objects.all()
    print(id,date)
    lead=Lead.objects.get(pk=id)
    feed_list=feedback.objects.filter(customer=lead,feedback_date=date)
    print(feed_list)
    i=0
    dict=[]
    for f in feed_list:
       print f.question
       dict.append(model_to_dict(f))
    
    
    return JsonResponse(dict,safe=False)

@login_required(login_url="/registration/login/")
def view_feed(request):
    
        user=request.user
        group=Group.objects.get(user=user)
        id=request.GET.get("id_customer")
        date=request.GET.get("feed_date")
        print(id,date)
        feedback_list=None
        form_list=[]
        #lead=Lead.objects.get(pk=id)
        inlineformset=modelformset_factory(Custfeedquestion,FeedbackFormCust2, extra=0)
        feedback_id1=Custfeedback.objects.get(pk=id,date=date)
        lead=Lead.objects.get(pk=feedback_id1.customer.pk)
        print("feedback _id1---------",feedback_id1.pk)

        feedback_list=Custfeedquestion.objects.filter( feedback_cust=feedback_id1)
        print("list feedback------",feedback_list)
        for ff in feedback_list:
            print("ff id--------",ff.pk)
        qform=inlineformset(queryset=feedback_list)
        return render(request,"Feedback/view_feedback.html",{'qform':qform,'lead':lead,'date':date,'group':group,"feed_main":feedback_id1})

def FeedbackCreate(request):
    user=request.user
    group=Group.objects.get(user=user)
    
    if group.name=="Member":
        
        current_user = request.user
        data=Feedback_Star.objects.filter(member=request.user)
        filter= FeedbackFilter(request.GET, queryset=data)
        return render(request,'Feedback/Feedback_list.html', {'obj':data,'group':group,'filter':filter}) 
    elif group.name=="Company":
        print("group is company")
        if request.method == 'POST':
            current_user = request.user
            cust_company=CustCompany.objects.get(email=current_user.email)
            #var1 = Lead.objects.get(pk=customer.customer.pk) 
             
          
            form = showrating(request.POST)
            if form.is_valid():
                today_date=datetime.today()
                date=today_date.date() 
                deatils=Feedback_Star(rating=form.cleaned_data['rating'],                          
                             comment=form.cleaned_data['comment'],
                             feedback_date=date,
                             company=cust_company,
                             member=cust_company.member,
                             )
                            
                deatils.save()
                print("feedback is saved successfully by:",deatils.company)
                notify.send(current_user,recipient=cust_company.member,verb="Submitted a feedback",app_name="Feedback",activity="update",object_id=deatils.pk)
                return render(request,'Feedback/feedback_form.html',{'group':group,'msg':'Feedback submitted successfully' })
            else:        
                return render('Feedback/feedback_form.html',{'form':form,'group':group} )
    
        else:
            form = showrating()
            variables = RequestContext(request, {'form': form,'group':group})
	    return render(request,'Feedback/feedback_form.html',variables  )

    else:
        
        if request.method == 'POST':
            
            current_user = request.user
                       
            customer=lead_user.objects.get(user=current_user)
            var1 = Lead.objects.get(pk=customer.customer.pk) 
             
          
            form = showrating(request.POST)   
            if form.is_valid():
                today_date=datetime.today()
                date=today_date.date()
                print("date:--------",today_date)
                deatils=Feedback_Star(rating=form.cleaned_data['rating'],             
                             comment=form.cleaned_data['comment'],
                             feedback_date=date,
                             customer=var1,
                             member=var1.member,
                             )            
                deatils.save()
                notify.send(request.user,recipient=var1.member,verb="Submitted a feedback",app_name="Feedback",activity="update",object_id=deatils.pk)

                return render(request,'Feedback/feedback_form.html',{'group':group,'msg':'Feedback submitted successfully' })
            else:
                
                return render('Feedback/feedback_form.html',{'form':form,'group':group} )
    
        else:
           
            form = showrating()   
            variables = RequestContext(request, {'form': form,'group':group})   
            return render(request,'Feedback/feedback_form.html',variables)

@login_required(login_url="/registration/login/")
def show_rating(request):
    query=Feedback_Star.objects.all()
    return render_to_response('Feedback/Feedback_list.html', {'obj':query})
   