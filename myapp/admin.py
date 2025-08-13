from django.contrib import admin
from .models import (
    Division, User, Proposal, ResearchProject, Report,
    Approval, Comment, Notification, ExternalUser,
    EthicalRequest, Review, EthicalCertificate
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Custom User Admin
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'division', 'is_staff', 'is_active')
    list_filter = ('role', 'division', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('role', 'division')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'division', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(User, UserAdmin)

# Division Admin
@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Proposal Admin
@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'submitted_by', 'division', 'submission_date')
    list_filter = ('status', 'type', 'division')
    search_fields = ('title', 'submitted_by__username')

# Research Project Admin
@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'submitted_by', 'status', 'submission_date')
    list_filter = ('status',)
    search_fields = ('proposal__title', 'submitted_by__username')

# Report Admin
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('research_project', 'submitted_by', 'status', 'submission_date')
    list_filter = ('status',)
    search_fields = ('research_project__proposal__title', 'submitted_by__username')

# Approval Admin
@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('submission_type', 'submission_id', 'approver', 'role', 'status', 'date')
    list_filter = ('submission_type', 'status', 'role')
    search_fields = ('approver__username',)

# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('approval', 'content', 'created_at')
    search_fields = ('approval__submission_id', 'content')

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'message')

# External User Admin
@admin.register(ExternalUser)
class ExternalUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'institution', 'created_at')
    search_fields = ('full_name', 'email', 'institution')

# Ethical Request Admin
@admin.register(EthicalRequest)
class EthicalRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'user__full_name')

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('request', 'reviewed_by', 'decision', 'date')
    list_filter = ('decision',)
    search_fields = ('request__title', 'reviewed_by__username')

# Ethical Certificate Admin
@admin.register(EthicalCertificate)
class EthicalCertificateAdmin(admin.ModelAdmin):
    list_display = ('request', 'issued_by', 'issued_at')
    search_fields = ('request__title', 'issued_by__username')
