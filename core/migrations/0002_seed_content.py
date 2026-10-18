from django.db import migrations


def load(apps, schema_editor):
    from core.seed import run
    run(apps)


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [migrations.RunPython(load, migrations.RunPython.noop)]
