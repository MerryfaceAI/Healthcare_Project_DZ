from django.core.management.base import BaseCommand
from patients.models.core import Patient, Address, Contact, Insurance
from patients.models.clinical import Condition, Allergy, Immunization
from patients.models.encounter import Encounter, Observation, Procedure
from patients.models.billing import Prescription
from faker import Faker
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
import random

class Command(BaseCommand):
    help = 'Seed the database with realistic fake patient data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        Patient.objects.all().delete()

        conditions = ["Hypertension", "Type 2 Diabetes", "Asthma", "Chronic Kidney Disease"]
        reactions = ["Rash", "Anaphylaxis", "Swelling"]
        vaccines = ["COVID-19", "Hepatitis B", "Influenza"]
        procedures = ["Appendectomy", "Coronary Bypass", "Knee Replacement"]

        for _ in range(100):
            # Create address, contact, insurance
            addr = Address.objects.create(
                line1=fake.street_address(),
                line2=fake.secondary_address(),
                city=fake.city(),
                state=fake.state(),
                postal_code=fake.postcode(),
                country=fake.country()
            )
            contact = Contact.objects.create(
                phone=fake.phone_number(),
                email=fake.unique.email()
            )
            insurance = Insurance.objects.create(
                provider=fake.company(),
                policy_number=fake.uuid4(),
                group_number=fake.lexify(text='G????'),
                valid_until=fake.future_date(end_date='+1y')
            )

            # Create patient
            patient = Patient.objects.create(
                medical_record_number=fake.unique.bothify(text='MR#####'),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
                gender=random.choice(['M', 'F', 'O', 'U']),
                address=addr,
                contact=contact,
                insurance=insurance
            )

            # Clinical: Conditions, Allergies, Immunizations
            Condition.objects.create(
                patient=patient,
                name=random.choice(conditions),
                description=fake.text(),
                onset_date=fake.date_between(start_date='-5y', end_date='-1y')
            )
            Allergy.objects.create(
                patient=patient,
                substance=random.choice(["Penicillin", "Nuts", "Shellfish"]),
                reaction=random.choice(reactions),
                severity=random.choice(["Mild", "Moderate", "Severe"])
            )
            Immunization.objects.create(
                patient=patient,
                vaccine=random.choice(vaccines),
                date_given=fake.date_between(start_date='-3y', end_date='today'),
                lot_number=fake.bothify(text='LOT####')
            )

            # Encounter + Observation + Procedure
            encounter = Encounter.objects.create(
                patient=patient,
                encounter_type=random.choice(['inpatient', 'outpatient', 'emergency']),
                start_time=make_aware(fake.date_time_between(start_date='-6mo')),
                end_time=make_aware(fake.date_time_between(start_date='-6mo', end_date='now')),
                reason=fake.sentence(),
                notes=fake.paragraph()
            )
            Observation.objects.create(
                encounter=encounter,
                code=random.choice(["LOINC-1234", "LOINC-5678"]),
                value=str(random.randint(90, 160)),
                unit="mmHg",
                observed_at=make_aware(datetime.now())
            )
            Procedure.objects.create(
                encounter=encounter,
                procedure_code=random.choice(["CPT-99213", "ICD10-XYZ"]),
                description=random.choice(procedures),
                performed_at=make_aware(fake.date_time_between(start_date='-3mo'))
            )

            # Prescription
            Prescription.objects.create(
                patient=patient,
                medication=fake.lexify(text='Drug-???'),
                dosage="1 tablet",
                start_date=datetime.today().date(),
                end_date=datetime.today().date() + timedelta(days=7),
                instructions="Take after meals"
            )

        self.stdout.write(self.style.SUCCESS("✅ Seeded 100 patients with related records."))
