from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DivisionViewSet, UserViewSet, ProposalViewSet, ResearchProjectViewSet,
    ReportViewSet, ApprovalViewSet, CommentViewSet, NotificationViewSet,
    ExternalUserViewSet, EthicalRequestViewSet, ReviewViewSet, EthicalCertificateViewSet,
    login_view  # ⚠️ Import login_view hapa
)

# Create DRF router
router = DefaultRouter()

# Internal users and workflow
router.register(r'divisions', DivisionViewSet)
router.register(r'users', UserViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'research-projects', ResearchProjectViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'approvals', ApprovalViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'notifications', NotificationViewSet)

# External users & ethical requests
router.register(r'external-users', ExternalUserViewSet)
router.register(r'ethical-requests', EthicalRequestViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'ethical-certificates', EthicalCertificateViewSet)

# App URL patterns
urlpatterns = [
    path('login/', login_view),  # login endpoint
    path('', include(router.urls)),  # All other API endpoints
]
