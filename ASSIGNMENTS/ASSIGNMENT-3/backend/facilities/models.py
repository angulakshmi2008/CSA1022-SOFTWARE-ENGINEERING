from django.db import models

class FacilityType(models.TextChoices):
    LECTURE_HALL = 'lecture_hall', 'Lecture Hall'
    COMPUTER_LAB = 'computer_lab', 'Computer Laboratory'
    RESEARCH_LAB = 'research_lab', 'Advanced Research Laboratory'
    SEMINAR_HALL = 'seminar_hall', 'Seminar & Conference Hall'
    STUDY_ROOM = 'study_room', 'Collaborative Study Room'

class Facility(models.Model):
    campus = models.ForeignKey(
        'campuses.Campus',
        on_delete=models.CASCADE,
        related_name='facilities'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30, unique=True, help_text="e.g. ENG-ROBO-101")
    facility_type = models.CharField(
        max_length=50,
        choices=FacilityType.choices,
        default=FacilityType.LECTURE_HALL
    )
    capacity = models.PositiveIntegerField(default=30)
    is_restricted = models.BooleanField(
        default=False,
        help_text="Requires departmental approver authorization for booking requests."
    )
    is_active = models.BooleanField(default=True)
    location_details = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'facilities'
        ordering = ['campus', 'name']
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return f"{self.name} [{self.code}] ({self.campus.code})"
