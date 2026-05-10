import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from campaigns.models import Campaign
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with 1000+ realistic Saudi digital campaigns'

    def handle(self, *args, **kwargs):
        fake = Faker(['ar_SA'])
        
        self.stdout.write('جاري مسح البيانات القديمة...')
        Campaign.objects.all().delete()
        
        platforms = ['X', 'TikTok', 'Snapchat', 'Instagram']
        categories = ['Awareness', 'Commercial', 'National', 'Sports']
        theories = [
            'نظرية الاستخدامات والإشباعات (Uses and Gratifications)',
            'نظرية ترتيب الأولويات (Agenda Setting)',
            'نظرية الغرس الثقافي (Cultivation Theory)',
            'نظرية التذييل الإعلامي (Media Priming)',
            'نظرية التأطير الإعلامي (Framing Theory)'
        ]
        
        cities = ['الرياض', 'جدة', 'الدمام', 'مكة المكرمة', 'المدينة المنورة', 'أبها', 'تبوك', 'حائل']
        
        campaign_types = [
            'حملة توعوية عن {topic}',
            'إطلاق منتج {product} في {city}',
            'فعالية {event} الوطنية',
            'ترويج لـ {brand} عبر {platform}'
        ]
        
        topics = ['الصحة العامة', 'البيئة', 'القيادة الآمنة', 'التحول الرقمي', 'التوفير المالي']
        products = ['تطبيق ذكي', 'سيارة كهربائية', 'عطر فاخر', 'ساعة ذكية']
        events = ['موسم الرياض', 'مهرجان جدة', 'يوم التأسيس', 'اليوم الوطني']
        brands = ['شركة الاتصالات', 'مصرف الراجحي', 'نيوم', 'أرامكو']

        self.stdout.write(f'جاري توليد 1000 سجل...')
        
        campaigns_to_create = []
        for i in range(1000):
            platform = random.choice(platforms)
            category = random.choice(categories)
            city = random.choice(cities)
            
            # Generate logical dates
            start_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 500))
            end_date = start_date + timedelta(days=random.randint(7, 60))
            
            # Name generation
            name_tpl = random.choice(campaign_types)
            name = name_tpl.format(
                topic=random.choice(topics),
                product=random.choice(products),
                city=city,
                event=random.choice(events),
                brand=random.choice(brands),
                platform=platform
            )
            
            # Logical Metrics
            reach = random.randint(10000, 5000000)
            engagement_rate = random.uniform(0.01, 0.15)
            engagement = int(reach * engagement_rate)
            
            theory = random.choice(theories)
            
            # Scientific Evaluation
            evaluation = f"بناءً على تحليل {theory}، أظهرت الحملة في {city} "
            evaluation += f"قدرة فائقة على الوصول لـ {reach:,} شخص. "
            evaluation += fake.paragraph(nb_sentences=3)

            campaigns_to_create.append(Campaign(
                name=f"{name} - {i+1}",
                category=category,
                platform=platform,
                start_date=start_date.date(),
                end_date=end_date.date(),
                reach=reach,
                engagement=engagement,
                media_theory=theory,
                scientific_evaluation=evaluation
            ))

            if len(campaigns_to_create) >= 100:
                Campaign.objects.bulk_create(campaigns_to_create)
                campaigns_to_create = []
                self.stdout.write(f'تم إدراج {i+1} سجل...')

        if campaigns_to_create:
            Campaign.objects.bulk_create(campaigns_to_create)

        self.stdout.write(self.style.SUCCESS('تم توليد 1000 سجل بنجاح! المنصة الآن جاهزة للتحليل المعقد.'))
