from django.shortcuts import redirect


def deco_login(fun):
    def wrapper(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return fun(self, request, *args, **kwargs)
        return redirect('main:login')
    return wrapper

def deco_url_admin(fun):
    def wrapper(self,request,*args,**kwargs):
        if request.user.is_admin or request.user.is_staff:
            return fun(self, request, *args, **kwargs)
        return redirect('main:page-not-found')
    return wrapper


def deco_url_student(fun):
    def wrapper(self,request,*args,**kwargs):
        if request.user.is_student or request.user.is_staff:
            return fun(self, request, *args, **kwargs)
        return redirect('main:page-not-found')
    return wrapper