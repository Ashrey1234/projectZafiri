from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
# Division Model
class Division(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('researcher','Researcher'),
        ('assistant','Assistant'),
        ('head_division','Head of Division'),
        ('head_department','Head of Department'),
        ('director', 'Director'),  # kama unataka pia director awe role
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    division = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True, blank=True)

    # Fix reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myapp_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myapp_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # Fix reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myapp_user_set',  # Change here
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myapp_user_permissions_set',  # Change here
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Proposal Model
class Proposal(models.Model):
    class ProposalType(models.TextChoices):
        RESEARCH = 'Research'
        PROJECT = 'Project'

    class ProposalStatus(models.TextChoices):
        PENDING = 'Pending'
        APPROVED = 'Approved'
        REJECTED = 'Rejected'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=ProposalType.choices)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='proposals')
    status = models.CharField(max_length=10, choices=ProposalStatus.choices, default=ProposalStatus.PENDING)
    submission_date = models.DateTimeField(auto_now_add=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

# Research Project Model
class ResearchProject(models.Model):
    class RPStatus(models.TextChoices):
        PENDING = 'Pending'
        APPROVED = 'Approved'
        REJECTED = 'Rejected'

    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='research_projects')
    content = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='research_projects')
    status = models.CharField(max_length=10, choices=RPStatus.choices, default=RPStatus.PENDING)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Research Project for Proposal: {self.proposal.title}"

# Report Model
class Report(models.Model):
    class ReportStatus(models.TextChoices):
        PENDING = 'Pending'
        APPROVED = 'Approved'
        REJECTED = 'Rejected'

    research_project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='reports')
    content = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')
    status = models.CharField(max_length=10, choices=ReportStatus.choices, default=ReportStatus.PENDING)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for Research Project: {self.research_project.proposal.title}"

# Approval Model
class Approval(models.Model):
    class SubmissionType(models.TextChoices):
        PROPOSAL = 'Proposal'
        RESEARCH_PROJECT = 'ResearchProject'
        REPORT = 'Report'
        ETHICAL_REQUEST = 'EthicalRequest'

    class ApprovalStatus(models.TextChoices):
        APPROVED = 'Approved'
        REJECTED = 'Rejected'
        PENDING = 'Pending'

    submission_type = models.CharField(max_length=20, choices=SubmissionType.choices)
    submission_id = models.PositiveIntegerField()
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approvals')
    role = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.submission_type} approval by {self.approver} - {self.status}"

# Comment Model
class Comment(models.Model):
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on approval {self.approval.id}"

# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('read','Read'), ('unread','Unread')], default='unread')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

# External User Model
class ExternalUser(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    institution = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

# Ethical Request Model
class EthicalRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = 'Pending'
        APPROVED = 'Approved'
        REJECTED = 'Rejected'

    user = models.ForeignKey(ExternalUser, on_delete=models.CASCADE, related_name='ethical_requests')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    document_path = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=RequestStatus.choices, default=RequestStatus.PENDING)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Review Model
class Review(models.Model):
    request = models.ForeignKey(EthicalRequest, on_delete=models.CASCADE, related_name='reviews')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    decision = models.CharField(max_length=10, choices=[('Approved','Approved'), ('Rejected','Rejected')])
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.request.title} by {self.reviewed_by}"

# Ethical Certificate Model
class EthicalCertificate(models.Model):
    request = models.ForeignKey(EthicalRequest, on_delete=models.CASCADE, related_name='certificates')
    file_path = models.CharField(max_length=500)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_certificates')
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.request.title}"
