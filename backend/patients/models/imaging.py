from django.db import models
from .core import Patient


class ImagingStudy(models.Model):
    class ImagingType(models.TextChoices):
        XRAY = 'X-ray', 'X-ray'
        MRI = 'MRI', 'MRI'
        CT = 'CT', 'CT Scan'
        ULTRASOUND = 'Ultrasound', 'Ultrasound'
        OTHER = 'Other', 'Other'

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='imaging_studies'
    )
    study_type = models.CharField(
        max_length=20,
        choices=ImagingType.choices,
        verbose_name="Imaging Modality"
    )
    study_date = models.DateField()
    description = models.TextField(blank=True)
    radiologist = models.CharField(max_length=100)
    image_file = models.FileField(
        upload_to='radiology/images/',
        blank=True,
        null=True,
        help_text="Optional uploaded image"
    )
    dicom_reference = models.CharField(
        max_length=255,
        blank=True,
        help_text="DICOM UID or PACS system reference"
    )

    def __str__(self):
        return f"{self.study_type} for {self.patient} on {self.study_date}"
