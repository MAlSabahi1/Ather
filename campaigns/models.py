from django.db import models

class Campaign(models.Model):
    PLATFORM_CHOICES = [
        ('X', 'X (Twitter)'),
        ('TikTok', 'TikTok'),
        ('Snapchat', 'Snapchat'),
        ('Instagram', 'Instagram'),
    ]

    CATEGORY_CHOICES = [
        ('Awareness', 'توعوية'),
        ('Commercial', 'تجارية'),
        ('National', 'وطنية'),
        ('Sports', 'رياضية'),
    ]

    name = models.CharField(max_length=255, verbose_name="اسم الحملة")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Awareness', verbose_name="نوع الحملة")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name="المنصة")
    start_date = models.DateField(verbose_name="تاريخ البدء")
    end_date = models.DateField(verbose_name="تاريخ الانتهاء")
    reach = models.PositiveIntegerField(default=0, verbose_name="عدد الوصول (Reach)")
    engagement = models.PositiveIntegerField(default=0, verbose_name="عدد التفاعل (Engagement)")
    media_theory = models.CharField(max_length=255, verbose_name="النظرية الإعلامية")
    scientific_evaluation = models.TextField(verbose_name="التقييم العلمي")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def engagement_rate(self):
        if self.reach > 0:
            return round((self.engagement / self.reach) * 100, 1)
        return 0

    @property
    def success_rate(self):
        # We simulate a success rate based on engagement efficiency
        if self.reach > 0:
            return min(int(self.engagement_rate * 5), 100)
        return 0

    @property
    def platform_display(self):
        return dict(self.PLATFORM_CHOICES).get(self.platform, self.platform)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "حملة"
        verbose_name_plural = "الحملات"
        ordering = ['-created_at']

from django.contrib.auth.models import User

class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="المستخدم")
    search_query = models.CharField(max_length=255, verbose_name="كلمة البحث")
    platform = models.CharField(max_length=20, default='X', verbose_name="المنصة المختارة")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name="الحملة المرتبطة")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تاريخ البحث"
        verbose_name_plural = "تاريخ البحث"
        unique_together = ('user', 'search_query', 'platform')
