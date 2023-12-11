from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
# from django.views import View
from .models import Process, Document, Work
from django.db import IntegrityError
# from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

# 新規登録
def signupfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '' ,password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('admin:login'))
        except IntegrityError:
            return render(request, 'signup.html', {'Error':'このユーザーはすでに登録されています。'})
    return render(request, 'signup.html', {'some':100})

# ログイン
def loginfunc(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # ログインしているかどうかでリダイレクト先を変更
            if request.user.is_authenticated:
                return redirect('/work/')  # ログイン後のリダイレクト先を/work/に変更
            else:
                return redirect('/admin/login/?next=/admin/')
    return render(request, 'work.html', {})

# ログアウト
def logoutfunc(request):
    logout(request)
    return redirect('login')

# 関連する手順の取得
@csrf_exempt
@require_http_methods(['GET'])
def get_related_processes(request):
    if request.method == 'GET':
        print('GET request received')
        selected_work_ids = request.GET.getlist('work_ids[]', [])

        # 選択された作業に関連する手順を取得
        related_processes = Process.objects.filter(work_set__id__in=selected_work_ids)

        # 関連する手順のデータを整形
        process_data = [{'id': process.id, 'title': process.title} for process in related_processes]

        return JsonResponse({'related_processes': process_data})
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

#作業リスト
class Workview(ListView):
    template_name = 'work.html'
    model = Work
    context_object_name = 'workin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Print文を追加
        print("workin value:", context['workin'])

        workin_data = [{'work_name': work.work, 'related_processes': work.works_for_processes.all()} for work in context['workin']]

        # 'related_work' を 'related_processes' に変更
        for data in workin_data:
            data['related_work'] = data['related_processes'].first().work_set.first() if data['related_processes'].first() else None

        context['workin'] = workin_data

        return context

# 作業の手順リスト
class Carelist(ListView):
    template_name = 'list.html'
    model = Work
    context_object_name = 'carelist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        work = get_object_or_404(Work, pk=pk)

        # 関連データも一緒に取得する
        context['selected_work'] = work

        # 関連する手順を取得
        context['related_processes'] = work.works_for_processes.all()

        return context

# 詳細表示
class CareDetail(DetailView):
    template_name = 'detail.html'
    model = Document
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document = self.get_object()

        # 関連するマニュアルや手順を取得
        context['related_documents'] = document.relation.all()

        # 関連する手順を取得
        context['related_processes'] = document.process_set.all()

        # 前の手順と次の手順を取得
        context['previous_processes'] = Process.objects.filter(move__in=context['related_processes'])
        context['next_processes'] = Process.objects.filter(previous__in=context['related_processes'])

        return context

# 手順詳細表示
class ProcessDetailView(DetailView):
    model = Process
    template_name = 'process.html'
    context_object_name = 'process'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        process = self.object

        # 関連するマニュアル・手順にアクセスするために正しい関連名を使用する
        context['related_documents'] = process.documents.all()
        context['next_processes'] = process.move.all()
        context['previous_processes'] = process.previous.all()

        context['care_detail_url'] = reverse('care_detail', kwargs={'pk': process.id})


        return context



