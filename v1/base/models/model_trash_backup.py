from django.db import models

class TrashBackupModel(models.Model):
    app_label = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    table_name = models.CharField(max_length=32)
    ref_id = models.IntegerField()
    content = models.TextField()
    created_by = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "mv_trash_backup"