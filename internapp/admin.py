from django.contrib import admin
from internapp.models import Document, Manual, Process, Work
from django.http import HttpResponseRedirect
from django.urls import reverse


# カスタムした管理画面設定
admin.site.site_header = 'InternApp管理画面'
admin.site.index_title = 'データ管理'
admin.site.site_url = '/work/'


class MyAdminSite(admin.AdminSite):

    def index(self, request, extra_context=None):
        if not request.user.is_authenticated:
            # ログインしていない場合はログインページにリダイレクト
            return HttpResponseRedirect(reverse('admin:login'))
        else:
            # ログインしている場合はホーム画面にリダイレクト
            return HttpResponseRedirect(reverse('admin:index_home'))

# Documentモデルの管理画面設定
class DocumentAdmin(admin.ModelAdmin):
    list_filter = ('relation', 'process_set')
    list_display = ('manual', 'display_relation', 'display_process_set')
    list_display_links = ('display_relation', 'display_process_set')
    filter_horizontal = ('relation', 'process_set')
    actions_on_top = False
    actions_on_bottom = True
    list_display_links = None
    list_editable = ('manual', )
    list_per_page = 30

    #カスタムメソッド
    def display_relation(self, obj):
        return ', '.join([str(relation) for relation in obj.relation.all()])
    display_relation.short_description = '関連マニュアル'

    def display_process_set(self, obj):
        return ', '.join([str(process) for process in obj.process_set.all()])
    display_process_set.short_description = '手順'

    search_fields = ['relation__name', 'process_set__title','text']

    def response_post_save_change(self, request, obj):
        """
        Override the response after successfully saving changes to a Document object.
        """
        if "_popup" in request.GET:  # ポップアップの場合
            return super().response_post_save_change(request, obj)
        else:
            return HttpResponseRedirect(reverse('admin:index'))


# Documentモデルをインライン表示
class DocumentInline(admin.StackedInline):
    model = Document
    extra = 1

# Manual モデルの管理画面設定
class ManualAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [DocumentInline]
    extra = 1
    actions_on_top = False
    actions_on_bottom = True
    list_per_page = 30

# Process モデルの管理画面設
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_work_set')
    list_filter = ('work_set', )
    filter_horizontal = ('work_set', 'previous', 'move')
    actions_on_top = False
    actions_on_bottom = True
    list_per_page = 30

    #カスタムメソッド
    def display_work_set(self, obj):
        return ', '.join([str(work_set) for work_set in obj.work_set.all()])
    display_work_set.short_description = '作業'

    search_fields = ['title', 'display_work_set']

# Work モデルの管理画面設定
class WorkAdmin(admin.ModelAdmin):
    list_display = ('work',)
    actions_on_top = False
    actions_on_bottom = True
    list_per_page = 30

# カスタムした管理画面インスタンス
admin_site = MyAdminSite(name='myadmin')

# カスタムした管理画面にモデルを登録
admin_site.register(Document, DocumentAdmin)
admin_site.register(Manual, ManualAdmin)
admin_site.register(Process, ProcessAdmin)
admin_site.register(Work, WorkAdmin)

# 通常の管理画面にモデルを登録
admin.site.register(Document, DocumentAdmin)
admin.site.register(Manual, ManualAdmin)
admin.site.register(Process,  ProcessAdmin)
admin.site.register(Work, WorkAdmin)


