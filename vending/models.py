from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Machine(models.Model):
    CHOICES = [
        ('Milk', 'Milk'),
        ('Juice', 'Juice'),
        ('Cooking oil', 'Cooking oil'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(blank=True, null=True, max_length=255)
    serial_number = models.CharField(max_length=255, unique=True)
    machine_type = models.CharField(max_length=255, choices=CHOICES, blank=True, null=True, default='Milk')
    total_volume = models.FloatField(default=0.000)
    total_amount = models.FloatField(default=0.000)
    initial_tokens = models.PositiveIntegerField(default=15)  # Updated to 15 tokens
    remaining_tokens = models.PositiveIntegerField(default=15)  # Updated to 15 tokens
    days_used = models.PositiveIntegerField(default=0)
    cost_per_day = models.FloatField(default=3.0)  # Each day costs 3 Ksh
    tokens_per_month = models.PositiveIntegerField(default=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vending_machine')
    last_processed_date = models.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.name} - {self.serial_number}'

    def process_daily_usage(self):
        current_date = datetime.now().date()
        if (current_date - self.last_processed_date).days >= 1:
            self.days_used += 1
            self.total_amount += self.cost_per_day
            self.remaining_tokens -= 1  # One token per day
            self.last_processed_date = current_date
            self.save()


class Transaction(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField(default=0.000)
    date = models.DateTimeField(auto_now_add=True)
    volume = models.FloatField(default=0.000)
    token_used = models.FloatField(default=1)
    total_amount = models.FloatField(default=0.000)
    total_volume = models.FloatField(default=0.000)

    def __str__(self):
        return f'{self.machine.name} - {self.date} - {self.amount}'

    def remaining_tokens(self):
        self.machine.total_amount = self.total_amount
        self.machine.total_volume = self.total_volume
        self.machine.remaining_tokens = self.machine.initial_tokens - self.token_used
        self.machine.save()
        return True

class Refill(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='refills')
    date = models.DateTimeField(auto_now_add=True)
    payment_made = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default='Pending')
    token_pack = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.machine.name} - {self.date}'

    def refill_tokens(self):
        if self.payment_made and self.status == 'Approved':
            if self.token_pack == 'Starter Pack':
                self.machine.remaining_tokens += 25
                self.machine.save()
            elif self.token_pack == 'Popular Pack':
                self.machine.remaining_tokens += 50
                self.machine.save()
            elif self.token_pack == 'Bulk Pack':
                self.machine.remaining_tokens += 100
                self.machine.save()
