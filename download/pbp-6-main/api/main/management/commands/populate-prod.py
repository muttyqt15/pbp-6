import json
from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = "Populate the database from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):
        json_file_path = options["json_file"]

        with open(json_file_path, "r") as file:
            data = json.load(file)

        for item in data:
            model = apps.get_model(item["model"])
            fields = item["fields"]

            # Handle foreign key fields
            for field_name, value in fields.items():
                field = model._meta.get_field(field_name)
                if (
                    field.is_relation and field.many_to_one
                ):  # Check if the field is a foreign key
                    try:
                        # Get the related object
                        related_model = field.related_model
                        fields[field_name] = related_model.objects.get(pk=value)
                    except ObjectDoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Related object for {field_name} with pk {value} not found."
                            )
                        )

            # Create and save the instance
            obj = model(**fields)
            obj.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully added {item}"))
