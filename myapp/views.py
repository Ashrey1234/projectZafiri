from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Role ya user
        role = user.role
        
        # Dashboard redirect kulingana na role
        if role == 'admin':
            redirect_to = '/admin-dashboard'
        else:
            redirect_to = '/user-dashboard'
        
        return Response({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.username,
            'role': role,
            'redirect_to': redirect_to  # Hii ndiyo muhimu
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=401)


# Internal Users
class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny] 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Proposals & Research Projects
class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResearchProjectViewSet(viewsets.ModelViewSet):
    queryset = ResearchProject.objects.all()
    serializer_class = ResearchProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

# Approvals & Comments
class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

# External Users & Ethical Requests
class ExternalUserViewSet(viewsets.ModelViewSet):
    queryset = ExternalUser.objects.all()
    serializer_class = ExternalUserSerializer
    permission_classes = [permissions.AllowAny]  # external users can register

class EthicalRequestViewSet(viewsets.ModelViewSet):
    queryset = EthicalRequest.objects.all()
    serializer_class = EthicalRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

class EthicalCertificateViewSet(viewsets.ModelViewSet):
    queryset = EthicalCertificate.objects.all()
    serializer_class = EthicalCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
