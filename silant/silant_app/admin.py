from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(MachineModel)
admin.site.register(Engine)
admin.site.register(Transmission)
admin.site.register(DrivingAxle)
admin.site.register(ControlledAxle)
admin.site.register(MaintenanceType)
admin.site.register(Failure)
admin.site.register(RecoveryMethod)
admin.site.register(ServiceCompany)
admin.site.register(Machine)
admin.site.register(Maintenance)
admin.site.register(Claims)


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


class UserAdmin(UserAdmin):
    inlines = (UserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
