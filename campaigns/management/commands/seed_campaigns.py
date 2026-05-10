from django.core.management.base import BaseCommand
from campaigns.models import Campaign
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with sample campaigns'

    def handle(self, *args, **kwargs):
        Campaign.objects.all().delete()
        
        campaigns = [
            {
                'name': 'يوم التأسيس السعودي 2024',
                'platform': 'X',
                'start_date': date.today() - timedelta(days=30),
                'end_date': date.today() - timedelta(days=20),
                'reach': 1500000,
                'engagement': 250000,
                'media_theory': 'نظرية ترتيب الأولويات (Agenda Setting)',
                'scientific_evaluation': 'نجحت الحملة في تعزيز الهوية الوطنية من خلال التركيز على الرموز التاريخية، مما أدى إلى تصدر الوسم للترند العالمي.'
            },
            {
                'name': 'رؤية 2030 - جودة الحياة',
                'platform': 'TikTok',
                'start_date': date.today() - timedelta(days=15),
                'end_date': date.today() + timedelta(days=15),
                'reach': 3200000,
                'engagement': 850000,
                'media_theory': 'نظرية الاستخدامات والإشباعات (U&G)',
                'scientific_evaluation': 'استهدفت الحملة فئة الشباب بمحتوى تفاعلي قصير، محققة إشباعاً معرفياً وترفيهياً حول المبادرات الجديدة.'
            },
            {
                'name': 'موسم الرياض - تخيل أكثر',
                'platform': 'Snapchat',
                'start_date': date.today() - timedelta(days=60),
                'end_date': date.today() - timedelta(days=5),
                'reach': 5000000,
                'engagement': 1200000,
                'media_theory': 'نظرية التذييل الإعلامي (Media Priming)',
                'scientific_evaluation': 'استخدمت الحملة عدسات تفاعلية لتعزيز تجربة المستخدم، مما خلق انطباعاً إيجابياً مسبقاً قبل زيارة الفعاليات.'
            }
        ]

        for data in campaigns:
            Campaign.objects.create(**data)
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded sample campaigns'))
