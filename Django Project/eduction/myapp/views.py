from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html')

def error(request):
    return render(request,'404.html')

def about(request):
    return render(request,'about.html')

def blog_single(request):
    return render(request,'blog_single.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')

def course_details(request):
    return render(request,'course_details.html')

def course(request):
    return render(request,'course.html')

def faq(request):
    return render(request,'faq.html')

def index2(request):
    return render(request,'index2.html')

def ins_details(request):
    return render(request,'ins_details.html')

def instructor(request):
    return render(request,'instructor.html')

def pricing(request):
    return render(request,'pricing.html')

def thank_you(request):
    return render(request,'thank-you.html')