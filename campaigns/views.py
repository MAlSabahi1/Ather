from django.shortcuts import render, redirect, get_object_or_404
from .models import Campaign, UserSearchHistory
from .forms import CampaignForm
from django.db.models import Sum, Count, Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import random

def landing(request):
    if request.user.is_authenticated:
        return redirect('campaigns:search_home')
    return render(request, 'campaigns/landing.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('campaigns:search_home')
    else:
        form = UserCreationForm()
    return render(request, 'campaigns/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('campaigns:search_home')
    else:
        form = AuthenticationForm()
    return render(request, 'campaigns/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('campaigns:landing')

@login_required
def dashboard(request):
    # Get only searches performed by this specific user
    history = UserSearchHistory.objects.filter(user=request.user).select_related('campaign')
    
    if not history.exists():
        return render(request, 'campaigns/restricted_access.html')

    # Calculate stats from the campaigns linked in the history
    total_campaigns = history.count()
    total_reach = sum(item.campaign.reach for item in history)
    total_engagement = sum(item.campaign.engagement for item in history)

    context = {
        'history': history,
        'total_campaigns': total_campaigns,
        'total_reach': total_reach,
        'total_engagement': total_engagement,
    }
    return render(request, 'campaigns/dashboard.html', context)

@login_required
def search_home(request):
    return render(request, 'campaigns/search_home.html')

@login_required
def scanner(request):
    query = request.GET.get('q', '')
    platform = request.GET.get('platform', 'X')
    return render(request, 'campaigns/scanner.html', {'query': query, 'platform': platform})

@login_required
def search_results(request):
    query = request.GET.get('q', '')
    platform = request.GET.get('platform', 'X')
    
    if not query:
        return redirect('campaigns:search_home')

    # Check if this user searched this before
    history = UserSearchHistory.objects.filter(user=request.user, search_query__iexact=query, platform=platform).first()
    
    if history:
        campaign = history.campaign
        display_name = query
    else:
        campaign = Campaign.objects.filter(name__icontains=query, platform=platform).first()
        
        if not campaign:
            all_campaigns = Campaign.objects.all()
            if all_campaigns.exists():
                campaign = random.choice(all_campaigns)
            else:
                return render(request, 'campaigns/search_home.html', {'error': 'قاعدة البيانات فارغة.'})
        
        # Save to history for THIS user
        UserSearchHistory.objects.get_or_create(
            user=request.user,
            search_query=query,
            platform=platform,
            defaults={'campaign': campaign}
        )
        display_name = query

        display_name = query

    return render(request, 'campaigns/search_results.html', {
        'campaign': campaign,
        'display_name': display_name,
        'query': query
    })

# Previous views (add_campaign etc.)
def add_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            reach = campaign.reach
            engagement = campaign.engagement
            if reach > 0:
                engagement_rate = (engagement / reach) * 100
                if engagement_rate > 10:
                    suggested_theory = "نظرية الاستخدامات والإشباعات (Uses and Gratifications)"
                    evaluation = f"تم تحقيق معدل تفاعل مرتفع ({engagement_rate:.1f}%)، مما يشير إلى نجاح الحملة في تلبية احتياجات الجمهور وإشباع رغباتهم المعرفية أو الترفيهية."
                elif reach > 1000000 and engagement_rate <= 10:
                    suggested_theory = "نظرية ترتيب الأولويات (Agenda Setting)"
                    evaluation = f"رغم التفاعل المتوسط ({engagement_rate:.1f}%)، إلا أن الوصول الضخم تجاوز المليون، مما يعزز قدرة الحملة على جعل القضية ضمن أولويات الرأي العام."
                else:
                    suggested_theory = "النظرية الإعلامية التقليدية"
                    evaluation = "الحملة في مستويات أداء قياسية."
                if not campaign.media_theory: campaign.media_theory = suggested_theory
                if not campaign.scientific_evaluation: campaign.scientific_evaluation = evaluation
            campaign.save()
            return redirect('campaigns:dashboard')
    else:
        form = CampaignForm()
    return render(request, 'campaigns/add_campaign.html', {'form': form})
