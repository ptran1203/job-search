from django.db import models
import datetime

class SpiderReport(models.Model):
    """
    report crawling process
    """
    src_map = ['undefinded','topitwork', 'itviec']
    # 1 -> topitwork
    # 2 -> itviec
    src_type = models.IntegerField(default=0)
    run_at = models.DateTimeField(auto_now=True)
    crawled_pages = models.IntegerField(default=0)
    # total secondss
    running_time = models.IntegerField(default=0)

    def __str__(self):
        return 'run in: ' + str(self.running_time)

    def get_running_time(self):
        return datetime.timedelta(seconds=self.running_time)

    def get_source_name(self):
        return self.src_map[self.src_type]
