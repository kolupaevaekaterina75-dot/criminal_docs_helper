from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


class Participant(models.Model):
    ROLE_CHOICES = [
        ('suspect', 'Подозреваемый'),
        ('OUR', 'Оперуполномоченный'),
        ('victim', 'Потерпевший'),
        ('witness', 'Свидетель'),
        ('lawyer', 'Защитник (адвокат)'),
        ('investigator', 'Следователь'),
        ('UUP', 'Участковый уполномоченный'),
        ('expert', 'Эксперт'),
        ('other', 'Иное лицо'),
    ]

    SIDE_CHOICES = [
        ('prosecution', 'Сторона обвинения'),
        ('defense', 'Сторона защиты'),
        ('other', 'Иные лица'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    birth_place = models.CharField(max_length=255, verbose_name="Место рождения")
    address = models.TextField(verbose_name="Адрес проживания")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    citizenship = models.CharField(max_length=100, verbose_name="Гражданство")
    education = models.CharField(max_length=100, verbose_name="Образование")
    marital_status = models.CharField(max_length=50, verbose_name="Семейное положение")
    employment = models.CharField(max_length=255, verbose_name="Место работы/учебы")
    work_phone = models.CharField(max_length=20, verbose_name="Рабочий телефон")
    military_duty = models.CharField(max_length=100, verbose_name="Отношение к воинской обязанности")
    criminal_record = models.TextField(verbose_name="Наличие судимости")
    document_type = models.CharField(max_length=100, verbose_name="Тип документа")
    document_number = models.CharField(max_length=20, verbose_name="Номер документа")
    signature = models.CharField(max_length=100, verbose_name="Подпись")

    created_at = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)

    class Meta:
        verbose_name = _('Участник уголовного дела')
        verbose_name_plural = _('Участники уголовного дела')
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    # Метод регистрации по телефону (бизнес‑логика на уровне модели — опционально)
    @classmethod
    def register_by_phone(cls, full_name, phone, role, side='other'):
        if not phone.strip():
            raise ValidationError({'phone': _('Телефон обязателен для регистрации')})
        obj, created = cls.objects.get_or_create(
            phone=phone.strip(),
            defaults={'full_name': full_name.strip(), 'role': role, 'side': side}
        )
        if not created:
            # Если участник уже есть — можно обновить ФИО/роль/сторону при необходимости
            obj.full_name = full_name
            obj.role = role
            obj.side = side
            obj.save()
        return obj

    # Назначение статуса (стороны и роли)
    def assign_status(self, role=None, side=None):
        if role:
            if role not in dict(self.ROLE_CHOICES):
                raise ValidationError({'role': _('Недопустимая роль')})
            self.role = role
        if side:
            if side not in dict(self.SIDE_CHOICES):
                raise ValidationError({'side': _('Недопустимая сторона')})
            self.side = side
        self.save()


class DocumentType(models.Model):
    """Справочник видов уголовно‑процессуальных документов"""
    code = models.SlugField(_('Код'), unique=True, help_text=_('Например: protocol_interrogation, indictment'))
    name = models.CharField(_('Название вида документа'), max_length=255)
    description = models.TextField(_('Описание'), blank=True)

    class Meta:
        verbose_name = _('Вид документа')
        verbose_name_plural = _('Виды документов')
        ordering = ['name']

    def __str__(self):
        return self.name


class Document(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('ready', 'Готов к подписанию'),
        ('signed', 'Подписан'),
        ('sent', 'Направлен'),
        ('archived', 'В архиве'),
    ]

    participant = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name=_('Кто составил')
    )
    doc_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        verbose_name=_('Вид документа')
    )

    case_date = models.DateField(_('Дата дела'), help_text=_('Дата возбуждения/начала дела'))
    case_number = models.CharField(_('Номер дела'), max_length=100)
    article_uk_rf = models.CharField(
        _('Статья УК РФ'),
        max_length=100,
        help_text=_('Например: 158 ч. 2 п. «в»')
    )

    content = models.TextField(_('Содержание документа'), blank=True)
    issue_date = models.DateField(_('Дата составления документа'), default=date.today)
    creator_full_name = models.CharField(_('ФИО составителя'), max_length=255)
    recipient_position = models.CharField("Должность получателя", max_length=255)
    information_source = models.TextField("Источник получения информации")
    crime_description = models.TextField("Описание преступления")

    destination = models.CharField(_('Куда направляется'), max_length=255, blank=True)
    items_seized = models.TextField(_('Что изъято'), blank=True)
    statements = models.TextField(_('Заявления'), blank=True)
    tech_equipment = models.TextField(_('Техсредства'), blank=True)
    address = models.CharField(_('Адрес'), max_length=255, blank=True)
    to_do = models.TextField(_('Что необходимо / выполнено'), blank=True)

    author = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="reports"
    )

    location = models.CharField("Место составления", max_length=255)
    investigator = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="voluntary_surrenders"
    )
    place = models.CharField("Место проведения", max_length=255)
    time = models.TimeField("Время")
    authority_name = models.CharField("Наименование органа", max_length=255)
    crime_description = models.TextField("Описание преступления")
    read_method = models.CharField("Способ ознакомления", max_length=50)
    recorded_correctly = models.CharField("Запись соответствует", max_length=50)
    remarks = models.TextField("Замечания", blank=True)

    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    file_path = models.FilePathField(
        _('Путь к файлу .docx'),
        path='media/documents',
        allow_files=True,
        allow_folders=False,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_('Дата создания записи'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Уголовно‑процессуальный документ')
        verbose_name_plural = _('Уголовно‑процессуальные документы')
        ordering = ['-issue_date', '-created_at']

    def __str__(self):
        return f"{self.doc_type.name} №{self.case_number} от {self.issue_date}"

    def clean(self):
        """Базовая валидация полей на уровне модели"""
        if self.case_date > self.issue_date:
            raise ValidationError({
                'issue_date': _('Дата составления документа не может быть раньше даты дела')
            })