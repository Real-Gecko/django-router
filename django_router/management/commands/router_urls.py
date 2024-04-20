from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "List all routes in project that look like `urls.py`"

    def handle(self, *args, **options):
        from django_router import router

        for pattern in router.urlpatterns:
            imports = set()
            routes = list()
            for subpattern in pattern.url_patterns:
                route = "    "
                route += (
                    f'path("{subpattern.pattern._route}"'
                    if hasattr(subpattern.pattern, "_route")
                    else f're_path("{subpattern.pattern._regex}"'
                )
                route += f", {subpattern.lookup_str}"
                route += f', name="{subpattern.name}"),\n'
                routes.append(route)
                imports.add(
                    f"import {'.'.join(subpattern.lookup_str.split('.')[:-1])}\n"
                )
            output = f"# {pattern.namespace}/urls.py\n\n"
            for imp in imports:
                output += imp
            output += "from django.urls import path, re_path\n\n"
            output += "urlpatterns = [\n"
            for route in routes:
                output += route
            output += "]\n"
            self.stdout.write(output)
