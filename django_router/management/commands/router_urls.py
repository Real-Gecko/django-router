from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "List all routes in project that look like `urls.py`"

    def handle(self, *args, **options):
        from django_router import router

        for pattern in router.urlpatterns:
            # self.stdout.write(self.style.SUCCESS(f'"{pattern.pattern._route}", namespace: {pattern.namespace}, app_name: {pattern.app_name}'))
            self.stdout.write(self.style.NOTICE(f"# {pattern.namespace}/urls.py"))
            self.stdout.write(
                self.style.SUCCESS(f"from django.urls import path, re_path")
            )
            self.stdout.write(self.style.SUCCESS(f'app_name = "{pattern.app_name}"'))
            self.stdout.write(self.style.SUCCESS(f"urlpatterns = ["))
            for subpattern in pattern.url_patterns:
                _route = (
                    f'path("{subpattern.pattern._route}"'
                    if hasattr(subpattern.pattern, "_route")
                    else f're_path("{subpattern.pattern._regex}"'
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\t{_route}, {subpattern.lookup_str}, name="{subpattern.name}")'
                    )
                )
            self.stdout.write(self.style.SUCCESS(f"]\n"))
