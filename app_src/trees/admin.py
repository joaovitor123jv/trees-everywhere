from django.contrib import admin

from .models import Tree, PlantedTree


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name']
    search_fields = ['name', 'scientific_name']

@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ['tree', 'user', 'account', 'planted_at']
    search_fields = ['tree__id', 'user__id', 'account__id']
    readonly_fields = ['planted_at']
    list_filter = ['account', 'planted_at']
