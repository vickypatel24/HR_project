
from urllib.parse import urlencode
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from core.models import Course, Person, Grade
from django.db.models import Avg, Sum, Min, Max
from django.utils.translation import gettext_lazy as _

# Register your models here.


class AgeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('age type')

    parameter_name = 'age_type'

    def lookups(self, request, model_admin):
        return (
            ('senior', _('SENIOR')),
            ('young', _('YOUNG')),
            ('minor', _('MINOR')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'senior':
            return queryset.filter(age__gt=35)
        elif self.value() == 'young':
            return queryset.filter(age__gt=17, age__lt=36)
        elif self.value() == 'minor':
            return queryset.filter(age__lt=18)

class PerformanceFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Performance')

    parameter_name = 'Performance'

    def lookups(self, request, model_admin):
        return (
            ('average', _('AVERAGE')),
            ('good', _('GOOD')),
            ('excellent', _('EXCELLENT')),
        )

    def queryset(self, request, queryset):
        performance = queryset.values('id').annotate(performance=Avg('grade__grade'))
        if self.value() == 'average':
            performance = performance.filter(performance__lt=51).distinct()
        elif self.value() == 'good':
            performance = performance.filter(performance__gt=50, performance__lte=75).distinct()
        elif self.value() == 'excellent':
            performance = performance.filter(performance__gt=75).distinct()
        # print(performance.values_list('id', flat=True))
        return queryset.filter(id__in=performance.values_list('id', flat=True))


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'age_type', 'gender', 'person_average', 'performance', 'course_name', 'person_sum', 'min_grade', 'max_grade')
    search_fields = ('first_name__startswith',)
    list_filter = (AgeFilter, PerformanceFilter, 'courses')
    readonly_fields = ('age', )

    def full_name(self, person_obj):
        return f'{person_obj.first_name} {person_obj.last_name}'
        # return person_obj.first_name + " " + person_obj.last_name

    def course_name(self, person_obj):
        # return list(person_obj.courses.all().values_list('name',flat=True))
        course_list = person_obj.courses.all().values('name', 'id', 'color')
        # grade_list = person_obj.Grade__grade.all().values('person_grade')
        # print(grade_list)
        s = ''
        for x in course_list:
            course_id = x['id']
            person_id = person_obj.id
            # print(course_id)
            # print(person_obj.id)
            grade=Grade.objects.filter(person_id=person_id, course_id=course_id).values('grade')
            # print(grade)
            if grade:
                marks = grade[0]['grade']
            else:
                marks = 0
            s = s + f'<a href="/admin/core/course/{x["id"]}/change/" style="color:{x["color"]};">{x["name"]} - {marks}</a>' + " ,"
        return mark_safe(s.strip(","))
        # return format_html(f'<a href="admin/core/course/1/change/>"{person_obj.courses}</a>')
        # if person_obj.age < 18:
            # return format_html('<b style="color:yellow;">{}</b>','MINOR')


    def age_type(self, person_obj):
        if person_obj.age < 18:
            return format_html(f'<a href="/admin/core/person/?age__lt=18">{"MINOR"}</a>')
        elif person_obj.age < 35:
            return format_html(f'<a href="/admin/core/person/?age__gte=18&age__lt=35">{"YOUNG"}</a>')
        elif person_obj.age > 35:
            return format_html(f'<a href="/admin/core/person/?age__gt=35">{"SENIOR"}</a>')
        return person_obj.age

    # def course_name(self, person_obj):
    #     return list(person_obj.courses.all().values_list('name', flat=True))
    #     courses_list = person_obj.courses.all().values('name', 'id')
    #     print(courses_list)
    #     return format_html('<a href="/admin/core/course/1/change/"')

    # def full_name(self,person_obj):
    #     return format_html(f'<a href = "admin/core/person/{person_obj.id}/change/">{person_obj.first_name}{person_obj.last_name}</a>')

    def performance(self, person_obj):
        performance = Grade.objects.filter(person=person_obj).aggregate(Avg('grade'))
        if performance['grade__avg'] <= 50:
            return format_html(f'<a href="/admin/core/grade/?grade__lt=51">{"AVERAGE"}</a>')
        elif performance['grade__avg'] <= 75:
            return format_html(f'<a href="/admin/core/grade/?grade__gt=50&grade__lt=76">{"GOOD"}</a>')
        elif performance['grade__avg'] > 75:
            return format_html(f'<a href="/admin/core/grade/?grade__gt=75">{"EXCELLENT"}</a>')


    def person_average(self,person_obj):
        result = Grade.objects.filter(person=person_obj).aggregate(Avg('grade'))
        # r = result['grade__avg']
        if result['grade__avg'] <= 50:
            return format_html('<b style="color:red;">{}</b>', result['grade__avg'])
        elif result['grade__avg'] <= 75:
            return format_html('<b style="color:yellow;">{}</b>', result['grade__avg'])
        elif result['grade__avg'] > 75:
            return format_html('<b style="color:green;">{}</b>', result['grade__avg'])
    person_average.short_description = 'AVERAGE'


    def person_sum(self,person_obj):
        result_sum = Grade.objects.filter(person=person_obj).aggregate(Sum('grade'))
        # print(result)
        return result_sum['grade__sum']
    person_sum.short_description = 'SUM'
    # def person_average(self,obj):
    #     result = Grade.objects.filter(person=obj).aggregate(Avg('grade'))
    #     return format_html('<b><i>{}</i></b>',result['grade__avg'])


    def min_grade(self, person_obj):
        result_min = Grade.objects.filter(person=person_obj).aggregate(Min('grade'))
        return result_min['grade__min']
    min_grade.short_description = 'MIN'

    def max_grade(self, person_obj):
        result_max = Grade.objects.filter(person=person_obj).aggregate(Max('grade'))
        return result_max['grade__max']
    max_grade.short_description = 'MAX'




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'view_student_link', 'color')
    list_filter = ("name", )

    def view_student_link(self,obj):
        count = obj.person_list.count()
        url = (
                reverse("admin:core_person_changelist")
                + "?"
                + urlencode({"courses__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Students</a>', url, count)

    view_student_link.short_description = "Students"

    def color(self, obj):
        color = f'{obj.color}'
        if color == "Red":
            return format_html('<b style="color:red;">{}</b>', color)
        elif color == "Green":
            return format_html('<b style="color:green;">{}</b>', color)
        elif color == "Yellow":
            return format_html('<b style="color:yellow;">{}</b>', color)
        elif color == "Orange ":
            return format_html('<b style="color:orange;">{}</b>', color)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('person', 'person_grade')

    def person_grade(self,g_obj):
        return f'{g_obj.course} - {g_obj.grade}'

    # def grade_total(self, grade_obj):
    #     grade_list = grade_obj.grade.all().values('grade')
    #     print('grade_list')


