from django.db import models

class BackupLogModel(models.Model):
    app_label = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    table_name = models.CharField(max_length=32)
    log_type = models.IntegerField()
    ref_id = models.IntegerField()
    content_prev = models.TextField( default= None , null=True )
    content_curr = models.TextField( default= None , null=True )
    created_by = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "mv_backup_log"