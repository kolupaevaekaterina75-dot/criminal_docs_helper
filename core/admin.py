from django.contrib import admin
from .models import (
    Participant,
    DocumentType,
    Employee,
    Witness,
    Document,
    Specialist
)

admin.site.register(Participant)
admin.site.register(DocumentType)
admin.site.register(Employee)
admin.site.register(Witness)
admin.site.register(Specialist)

class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'case_number',
        'issue_date',
        'investigator',
        'status',
        'location'
    )
    
    list_filter = (
        'status',
        'issue_date',
        'investigator'
    )
    
    search_fields = (
        'case_number',
        'participant__full_name',
        'content'
    )
    
    readonly_fields = ('file_path',)  # Поле только для чтения
    
    fieldsets = (
        (None, {
            'fields': (
                'case_number',
                'doc_type',
                'participant',
                'investigator',
                'status'
            )
        }),
        ('Основная информация', {
            'fields': (
                'issue_date',
                'location',
                'content'
            )
        }),
        ('Участники', {
            'fields': (
                'witness1',
                'witness2',
                'specialist'
            )
        })
    )

admin.site.register(Document, DocumentAdmin)