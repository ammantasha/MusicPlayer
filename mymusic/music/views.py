from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.views.generic import ListView,View,CreateView,UpdateView,TemplateView,DeleteView,DetailView
from .models import Album,Song
from .myforms import Mylogin,Register,AddAlbum,Addsong
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.

#def index(request):
 #   d=Album.objects.all()
  #  print(d)
   # return render(request,'music/master.html',{'d':d})

'''class index(ListView):
    template_name = 'music/home.html'
    context_object_name='data'
    def get_queryset(self):
        return Album.objects.all()'''

class index(TemplateView):
    def get(self,request,*args,**kwargs):
        d=Album.objects.all()
        if request.user.is_authenticated:
            return render(request,'music/home1.html',{'data':d})
        else:
            return render(request,'music/home.html',{'data':d})

'''def detail(request,pk):
    a=get_object_or_404(Album,pk=int(pk))
    ht=''
    for i in  a.song_set.all():
        ht+='<h1>'+i.title+'</h1>''<br>'
    return render(request,'music/song.html',{'val':a})'''

def detail(request,pk):
    a=get_object_or_404(Album,pk=int(pk))
    context={'val':a}
    context['user']=request.user
    if request.user.is_authenticated:
        context['master']='music/master1.html'
        return render(request,'music/song.html',context)
    else:
        context['master']='music/master.html'
        return render(request,'music/song.html',context)


'''def loginpage(request):
    form=Mylogin(request.POST or None)
    if form.is_valid():
        u = form.cleaned_data['UserName']
        p = form.cleaned_data['Password']
        v=authenticate(username=u,password=p)
        if v is not None:
            login(request,v)
        return HttpResponse('logged in '+ u)
    return render(request,'music/login.html',{'form':form})'''

class loginpage(View):
    def get(self,request):
        form=Mylogin(None)
        return render(request,'music/login.html',{'form':form})
    def post(self,request):
        form=Mylogin(request.POST)
        if form.is_valid():
            u = form.cleaned_data['UserName']
            p = form.cleaned_data['Password']
            v = authenticate(username=u, password=p)
            n = request.GET.get('next',None)
            if v is not None:
                login(request,v)
                if n:
                    return redirect(n)
                else:
                    return redirect('music:index')


        return render(request,'music/login.html',{'form':form})

class signup(CreateView):
    def get(self,request):
        form=Register(None)
        return render(request,'music/register.html',{'form':form})
    def post(self,request):
        form=Register(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            p=form.cleaned_data['Password']
            data.set_password(p)
            data.save()
            return redirect('music:login')
        return render(request,'music/register.html',{'form':form})

class Addalbum(LoginRequiredMixin,View):
    login_url = 'music:login'
    def get(self,request):
        form=AddAlbum(None)
        return render(request,'music/addalbum.html',{'form':form})
    def post(self,request):
        form=AddAlbum(request.POST,request.FILES)
        form.save()
        return redirect('music:index')

class UpdateAlbum(LoginRequiredMixin,UpdateView):
    login_url = 'music:login'
    template_name = 'music/addalbum.html'
    model = Album
    fields = ['title','artist','genre','year','image']
    def form_valid(self, form):
        form.save()
        return redirect('music:index')

'''class AddSong(View):
    def form(self,request):
        form=Addsong(None)
        return render(request,'music/addalbum.html',{'form':form})
    def post(self,request):
        form=Addsong(request.POST,request.FILES)
        form.save()
        return redirect('index')'''

class AddSong(LoginRequiredMixin,CreateView):
    login_url = 'music:login'
    template_name = 'music/addalbum.html'
    context_object_name = 'form'
    model = Song
    fields = ['title','artist','genre','sfile','image']
    def form_valid(self, form):
        i=self.kwargs.get('pk')
        a=Album.objects.get(pk=int(i))
        data=form.save(commit=False)
        data.al_id=a
        data.save()
        return redirect('music:detail',a.id)


class UpdateSong(LoginRequiredMixin,UpdateView):
    login_url = 'music:login'
    template_name = 'music/addalbum.html'
    context_object_name = 'form'
    model = Song
    fields = ['title','artist','genre','sfile','image']
    def form_valid(self, form):
        form.save()
        a=Song.objects.get(id=int(self.kwargs.get('pk')))
        return redirect('music:detail',a.al_id.id)

def Signout(request):
    logout(request)
    return redirect('music:index')

class DelAlbum(LoginRequiredMixin,DeleteView):
    login_url = 'music:login'
    template_name = 'music/delete.html'
    model = Album
    success_url = reverse_lazy('music:index')

class DelSong(LoginRequiredMixin,DeleteView):
    login_url = 'music:login'
    template_name = 'music/delete.html'
    model = Song
    def get_success_url(self):
        a=self.object.al_id
        return reverse_lazy('music:detail',kwargs={'pk':a.id})


def search(request):
    query=request.GET.get('search')
    if query:
        match=Album.objects.filter(title__startswith=query)
        print(match)
        if len(match)!=0:
            return render(request,'music/home.html',{'data':match})
        else:

            return render(request,'music/searchhome.html')


def search1(request):
    query=request.GET.get('search1')

    '''if query:
        match=Album.objects.filter(title__startswith=query)
        return render(request,'music/home1.html',{'data':match})'''
    if query:
        match = Album.objects.filter(title__startswith=query)
        print(match)
        if len(match) != 0:
            return render(request, 'music/home1.html', {'data': match})
        else:
            return render(request, 'music/searchhome1.html')

