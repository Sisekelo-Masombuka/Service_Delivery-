from django.db import models


class FaultReport(models.Model):
    STATUS_RECEIVED = "received"
    STATUS_TRIAGED = "triaged"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_RESOLVED = "resolved"
    STATUS_CHOICES = [
        (STATUS_RECEIVED, "Received"),
        (STATUS_TRIAGED, "Triaged"),
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    ISSUE_POTHOLE = "pothole"
    ISSUE_WATER = "water"
    ISSUE_STREETLIGHT = "streetlight"
    ISSUE_ELECTRICITY = "electricity"
    ISSUE_TRAFFIC = "traffic"
    ISSUE_CHOICES = [
        (ISSUE_POTHOLE, "Pothole"),
        (ISSUE_WATER, "Water leak"),
        (ISSUE_STREETLIGHT, "Streetlight"),
        (ISSUE_ELECTRICITY, "Electricity"),
        (ISSUE_TRAFFIC, "Traffic signals"),
    ]

    tracking_code = models.CharField(max_length=20, unique=True, db_index=True)
    issue_type = models.CharField(max_length=32, choices=ISSUE_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to="fault_uploads/%Y/%m/", blank=True, null=True)
    is_hazard = models.BooleanField(default=False)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default=STATUS_RECEIVED
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tracking_code} ({self.get_issue_type_display()})"
