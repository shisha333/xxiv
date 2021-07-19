from django.contrib import auth
from django.contrib.auth.models import  PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        first_name = first_name
        last_name = self.last_name
        user = self.model(first_name, last_name,email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(first_name, last_name, email, password, **extra_fields)

    def create_superuser(self, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(first_name, last_name, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    first_name = models.CharField(_('First Name'), max_length=30)
    last_name = models.CharField(_('Last Name'), max_length=150)
    
    category_choices = (
        ('coordinator', _("BUSINESS MANAGER")),
        ('internal-territory', _("INTERNAL TERRITORY MANAGER")),
        ('extarnal-territory', _("EXTARNAL TERRITORY MANAGER")),
        ('aggregator', "AGGREGATOR"),
        ('sales-agent', _("SALES AGENT")),
    )
    
    gender_choices = (
        ('m', _("Male")),
        ('f', _("Female")),
    )
    
    status_choices = (
        ('pending', _("Pending")),
        ('approved', _("Approved")),
        ('rejected', _("Rejected")),
    )
    
    phone = models.PositiveIntegerField(_("Phone"), null=True, blank=False)
    email = models.EmailField(_('E-mail'), unique=True)
    category = models.CharField(_("Category"), max_length=100,null=True,blank=True,choices=category_choices)
    gender = models.CharField(_("Gender"), max_length=100,null=True,blank=True,choices=gender_choices)
    is_staff = models.BooleanField(
        _('Status'),
        default=False,
        help_text=_("Designates whether the user can connect to this administration site."),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Indicates whether this user should be treated as active. '
            'Deselect this instead of deleting accounts.'
        ),
    )
    status = models.CharField(_("Approval"), max_length=20, choices=status_choices, default='pending')
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
    
    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        if self.category == "sales-agent":
            return "%s"%(self.phone)
        else:
            return full_name.strip()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_email(self):
        """
        Return the email.
        """
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    # class Meta(AbstractUser.Meta):
    #     swappable = ''AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(
		"authentication.User",
		max_length=255,
		null=True,
		blank=True,
		on_delete = models.CASCADE,
		db_column = "user",
		related_name = "profile", 
		)
    address = models.CharField(_("Full Adress"), max_length=255, null=True, blank=True,help_text="Address like RN4,NM 320, PO.BOX 340 Kigali")
    district = models.ForeignKey(
            "District",
            verbose_name=("District"),
            on_delete = models.CASCADE
        )
    sector = models.ForeignKey(
        "Sector",
        verbose_name=("Sector"),
        on_delete = models.CASCADE
    )
    cell = models.ForeignKey(
        "Cell",
        null=True,
        blank=True,
        verbose_name=("Cell"),
        on_delete = models.CASCADE
    )
    # initial_quantity = models.PositiveIntegerField(_("Initial quantity to deliver"), null=True, blank=True)
    tin = models.PositiveIntegerField(_("TIN Number"), null=True, blank=True)
    pin = models.PositiveIntegerField(_("PIN"), default=12345, null=True, blank=True)
    dob = models.DateField(_("Date of birth"), auto_now=False,auto_now_add=False,null=True,blank=True)
    nid = models.BigIntegerField(_("National ID"), null=True, blank=True)
    about = models.TextField(_("About user"),  null=True, blank=True,help_text="Short description about user")

    # def image_tag(self):
    #     from django.utils.html import escape
    #     return u'<img src="%s" />' % escape("user/profile_pictures/")
    # profile_picture.short_description = 'Image'
    # profile_picture.allow_tags = True
    
    objects = models.Manager()
    
    def __str__(self):
        return ""

    
class Province(models.Model):
    name = models.CharField(_("province"), max_length=50)
    
    class Meta:
        db_table = "provinces"
        verbose_name = _("province")
        verbose_name_plural = _("provinces")
    
        def __str__(self):
            return self.name
        
    def __str__(self):
        return self.name

class District(models.Model):
    
    name = models.CharField(_("district"), max_length=50)
    province = models.ForeignKey(
        "Province", 
        db_column = 'province',
        verbose_name=_("Province"), 
        on_delete=models.CASCADE
        )

    class Meta:
        db_table = "districts"
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return self.name

class Sector(models.Model):
    name = models.CharField(_("sector"), max_length=50)
    district = models.ForeignKey(
        "District", 
        db_column = 'district',
        verbose_name=_("District"), 
        on_delete=models.CASCADE)

    class Meta:
        db_table = 'sectors'
        verbose_name = _('sector')
        verbose_name_plural = _('Sectors')
    
    def __str__(self):
        return self.name
        
class Cell(models.Model):
    
    name = models.CharField(_("Cell"), max_length=50)
    
    sector = models.ForeignKey(
        "Sector", 
        db_column = 'sector',
        verbose_name=_("Sectors"), 
        on_delete=models.CASCADE
        )

    class Meta:
        db_table = "cells"
        verbose_name = _("Cell")
        verbose_name_plural = _("Cells")

    def __str__(self):
        return self.name
    
class Village(models.Model):
    name = models.CharField(_("Village"), max_length=50)
    cell = models.ForeignKey(
        "Cell", 
        db_column = 'cell',
        verbose_name=_("Cell"), 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'villages'
        verbose_name = 'Village'
        verbose_name_plural = 'Villages'

