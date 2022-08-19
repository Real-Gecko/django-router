from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'List all routes in project'

    def handle(self, *args, **options):
        from django_router import router

        for pattern in router.urlpatterns:
            self.stdout.write(self.style.SUCCESS(f'"{pattern.pattern._route}", namespace: {pattern.namespace}, app_name: {pattern.app_name}'))
            for subpattern in pattern.url_patterns:
                _route = subpattern.pattern._route if hasattr(subpattern.pattern,'_route') else subpattern.pattern._regex
                self.stdout.write(self.style.SUCCESS(f'\t"{_route}", {subpattern.lookup_str}, {subpattern.name}'))
