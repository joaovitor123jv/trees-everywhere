from django.contrib import admin

from .models import Tree, PlantedTree


class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    extra = 0
    readonly_fields = ['planted_at', 'user', 'account']


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'scientific_name']
    search_fields = ['name', 'scientific_name']
    inlines = [PlantedTreeInline]


@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ['id', 'tree', 'user', 'account', 'planted_at']
    search_fields = ['tree__id', 'user__id', 'account__id']
    readonly_fields = ['planted_at']
    list_filter = ['account', 'planted_at', 'tree__scientific_name']
