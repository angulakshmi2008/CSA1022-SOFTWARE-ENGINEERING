from django.db import models

class Campus(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="Unique campus identifier code, e.g. MAIN, ENG")
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='Chennai')
    timezone = models.CharField(max_length=50, default='UTC')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'campuses'
        ordering = ['name']
        verbose_name_plural = 'Campuses'

    def __str__(self):
        return f"{self.name} ({self.code})"
