from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class ServiceCompany(BaseModel):
    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_service = models.BooleanField(default=False, blank=True, verbose_name='Является сотрудником сервисной компании')
    service_company = models.ForeignKey(ServiceCompany, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Сервисная компания')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class MachineModel(BaseModel):
    class Meta:
        verbose_name = 'Модель техники'
        verbose_name_plural = 'Модели техники'


class Engine(BaseModel):
    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модели двигателей'


class Transmission(BaseModel):
    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модели трансмиссий'


class DrivingAxle(BaseModel):
    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модели ведущего моста'


class ControlledAxle(BaseModel):
    class Meta:
        verbose_name = 'Модель управляемого моста'
        verbose_name_plural = 'Модели управляемого моста'


class MaintenanceType(BaseModel):
    class Meta:
        verbose_name = 'Вид технического обслуживания'
        verbose_name_plural = 'Виды технических обслуживаний'


class Failure(BaseModel):
    class Meta:
        verbose_name = 'Характер отказа'
        verbose_name_plural = 'Характеры отказа'


class RecoveryMethod(BaseModel):
    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановления'


class Machine(models.Model):
    machine_number = models.CharField(max_length=50, unique=True, verbose_name='Зав. № машины')
    machine_model = models.ForeignKey(MachineModel, related_name='machines', on_delete=models.CASCADE, verbose_name='Модель техники')
    engine_model = models.ForeignKey(Engine, related_name='machines', on_delete=models.CASCADE, verbose_name='Модель двигателя')
    engine_id = models.CharField(max_length=50, verbose_name='Зав. № двигателя')
    transmission_model = models.ForeignKey(Transmission, related_name='machines', on_delete=models.CASCADE, verbose_name='Модель трансмиссии')
    transmission_id = models.CharField(max_length=50, verbose_name='Зав. № трансмиссии')
    driving_axle_model = models.ForeignKey(DrivingAxle, related_name='machines', on_delete=models.CASCADE, verbose_name='Модель ведущего моста')
    driving_axle_id = models.CharField(max_length=50, verbose_name='Зав. № ведущего моста')
    controlled_axle_model = models.ForeignKey(ControlledAxle, related_name='machines', on_delete=models.CASCADE, verbose_name='Модель управляемого моста')
    controlled_axle_id = models.CharField(max_length=50, verbose_name='Зав. № управляемого моста')
    delivery_contract = models.CharField(max_length=255, verbose_name='Договор поставки №, дата')
    factory_shipment_date = models.DateField(default=timezone.now, verbose_name='Дата отгрузки с завода')
    end_consumer = models.CharField(max_length=100, verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес поставки (эксплуатации)')
    specification = models.TextField(verbose_name='Комплектация (доп. опции)')
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    def __str__(self):
        return f'{self.machine_number}'

    class Meta:
        ordering = ['factory_shipment_date']
        db_table = 'machines'
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, verbose_name='Вид ТО')
    maintenance_date = models.DateField(default=timezone.now, verbose_name='Дата проведения ТО')
    operating_time = models.PositiveIntegerField(verbose_name='Наработка, м/час')
    work_order_number = models.CharField(max_length=100, verbose_name='№ заказ-наряда')
    work_order_date = models.DateField(default=timezone.now, verbose_name='Дата заказ-наряда')
    machine = models.ForeignKey(Machine, related_name='maintenance', on_delete=models.CASCADE, verbose_name='Машина')
    maintenance_provider = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Организация, проводившая ТО')

    def __str__(self):
        return f'{self.maintenance_date}'

    class Meta:
        ordering = ['maintenance_date']
        db_table = 'maintenance'
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Технические обслуживания'


class Claims(models.Model):
    equipment_failure_date = models.DateField(default=timezone.now, verbose_name='Дата отказа')
    operating_time = models.PositiveIntegerField(verbose_name='Наработка, м/час')
    failure_point = models.ForeignKey(Failure, on_delete=models.CASCADE, verbose_name='Узел отказа')
    equipment_failure_description = models.TextField(verbose_name='Описание отказа')
    equipment_recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.CASCADE, verbose_name='Способ восстановления')
    used_spare_parts = models.TextField(blank=True, verbose_name='Используемые запасные части')
    recovery_date = models.DateField(default=timezone.now, verbose_name='Дата восстановления')
    downtime_of_equipment = models.IntegerField(verbose_name='Время простоя техники')
    machine = models.ForeignKey(Machine, related_name='claims', on_delete=models.CASCADE, verbose_name='Mашина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Cервисная компания')

    def __str__(self):
        return f'{self.failure_point}'

    def save(self, *args, **kwargs):
        self.downtime_of_equipment = (self.recovery_date - self.equipment_failure_date).total_seconds() / 3600
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['equipment_failure_date']
        db_table = 'claims'
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'
