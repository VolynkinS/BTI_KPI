from django.contrib import admin

from kpi.models import Kpi, Criteria, Indicator, Category, UserAnswer, Condition, Condition3


@admin.register(Kpi)
class KpiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('kpi',)


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('criteria__kpi',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'point')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'percent_min', 'percent_max')
    list_display_links = ('id', 'percent_min', 'percent_max')
    search_fields = ('percent_min', 'percent_max')


@admin.register(Condition3)
class Condition3Admin(admin.ModelAdmin):
    list_display = ('id', 'amount_min', 'amount_max')
    list_display_links = ('id', 'amount_min', 'amount_max')
    search_fields = ('amount_min', 'amount_max')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'indicator', 'point', 'approve')
    list_display_links = ('id', 'user', 'indicator')
    search_fields = ('indicator__name',)
    list_filter = ('approve', 'user', )
    fields = ('user', 'get_criteria', 'indicator', 'point', 'text', 'approve')
    readonly_fields = ('user', 'get_criteria', 'indicator', 'point', 'text')


