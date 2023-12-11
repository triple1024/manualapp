from internapp.models import Document, Manual

manual_instance = Manual.objects.first()

# Manual_instance が存在する場合のみ実行
if manual_instance:
    problematic_documents = Document.objects.filter(manual=None)

    for document in problematic_documents:
        document.manual = manual_instance
        document.save()
else:
    print("Documentに割り当てるManualが存在しません。")
