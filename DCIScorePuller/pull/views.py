from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .filters import *
from .tables import *
from .utils.puller import DciScorePuller
from django_tables2 import RequestConfig
from django.http import JsonResponse

# Create your views here.
@login_required
def home(request):
    template = "pull/home.html"
    return render(request, template_name=template)

def about(request):
    template = "pull/about.html"
    return render(request, template_name=template)

def welcome(request):    
    if not request.user.is_authenticated:
        template = "pull/welcome.html"
        return render(request=request, template_name=template)
    else:
        return home(request)

@staff_member_required 
def admin(request):
    template = "pull/admin.html"
    return render(request, template_name=template)

@staff_member_required
def scrape(request):
    puller = DciScorePuller(season=2023)
    puller.get_competitions().format_competition_titles()

    for competition in puller.formatted_shows:

        if not Competition.objects.filter(competition_name=competition).exists():
            
            # get the recap we need to save first, we need the date for the competition model
            recap = puller.get_competition_recap(show=competition)

            # with open(f"./pull/utils/RECAP_JSON/{competition}.json", "w") as f:
            #     tmp_recap = recap
            #     tmp_recap["date"] = tmp_recap["date"].strftime("%Y-%m-%d")
            #     f.write(json.dumps(recap, indent=4))

            # save the competition, retuns the key
            competition_obj = Competition(
                competition_name = competition,
                competition_name_original = recap["Correct Competition Name"],
                competition_date = recap["date"]
            ).save()


            # for each corp, add the scores
            for corp in recap["shows"]:
                corp_check = Corp.objects.filter(name=corp)

                # corp exists, just need its key
                if corp_check.exists():
                    corp_obj = corp_check[0]
                # need to add this corp, and also get its key
                else:
                    corp_obj = Corp(
                        name = corp
                    ).save()

                # GENERAL EFFECT 
                ge_data = recap["shows"][corp]["General Effect"]

                if len(ge_data) == 3:
                    ge_1_1_rpt = RepPerfTotal(
                        rep = ge_data["General Effect 1"]["Rep"],
                        perf = ge_data["General Effect 1"]["Perf"],
                        total = ge_data["General Effect 1"]["Total"]
                    ).save()

                    ge_2_1_rpt = RepPerfTotal(
                        rep = ge_data["General Effect 2"]["Rep"],
                        perf = ge_data["General Effect 2"]["Perf"],
                        total = ge_data["General Effect 2"]["Total"]
                    ).save()

                    ge_total = ge_data["Total"]

                    general_effect = GeneralEffect(
                        general_effect_one_one = ge_1_1_rpt,
                        general_effect_two_one = ge_2_1_rpt,
                        general_effect_total = ge_total
                    ).save()
                else:
                    ge_1_1_rpt = RepPerfTotal(
                        rep = ge_data["General Effect 1 - 1"]["Rep"],
                        perf = ge_data["General Effect 1 - 1"]["Perf"],
                        total = ge_data["General Effect 1 - 1"]["Total"]
                    ).save()

                    ge_1_2_rpt = RepPerfTotal(
                        rep = ge_data["General Effect 1 - 2"]["Rep"],
                        perf = ge_data["General Effect 1 - 2"]["Perf"],
                        total = ge_data["General Effect 1 - 2"]["Total"]
                    ).save()

                    ge_2_1_rpt = RepPerfTotal(
                        rep = ge_data["General Effect 2 - 1"]["Rep"],
                        perf = ge_data["General Effect 2 - 1"]["Perf"],
                        total = ge_data["General Effect 2 - 1"]["Total"]
                    ).save()

                    ge_2_2_rpt = RepPerfTotal(
                        rep = ge_data["General Effect 2 - 2"]["Rep"],
                        perf = ge_data["General Effect 2 - 2"]["Perf"],
                        total = ge_data["General Effect 2 - 2"]["Total"]
                    ).save()

                    ge_total = ge_data["Total"]

                    general_effect = GeneralEffect(
                        general_effect_one_one = ge_1_1_rpt,
                        general_effect_one_two = ge_1_2_rpt,
                        general_effect_two_one = ge_2_1_rpt,
                        general_effect_two_two = ge_2_2_rpt,
                        general_effect_total = ge_total
                    ).save()

                # VISUAL
                vi_data = recap["shows"][corp]["Visual"]

                vp_cat = ContAchvTotal(
                    cont = vi_data["Visual Proficiency"]["Cont"],
                    achv = vi_data["Visual Proficiency"]["Achv"],
                    total = vi_data["Visual Proficiency"]["Total"]
                ).save()

                va_cat = ContAchvTotal(
                    cont = vi_data["Visual Analysis"]["Cont"],
                    achv = vi_data["Visual Analysis"]["Achv"],
                    total = vi_data["Visual Analysis"]["Total"]
                ).save()

                cg_cat = ContAchvTotal(
                    cont = vi_data["Color Guard"]["Cont"],
                    achv = vi_data["Color Guard"]["Achv"],
                    total = vi_data["Color Guard"]["Total"]
                ).save()

                vi_total = vi_data["Total"]

                visual = Visual(
                    visual_proficiency = vp_cat,
                    visual_analysis= va_cat,
                    color_guard = cg_cat,
                    visual_total = vi_total
                ).save()

                # MUSIC
                mu_data = recap["shows"][corp]["Music"]

                mb_cat = ContAchvTotal(
                    cont = mu_data["Music Brass"]["Cont"],
                    achv = mu_data["Music Brass"]["Achv"],
                    total = mu_data["Music Brass"]["Total"],
                ).save()

                ma_cat = ContAchvTotal(
                    cont = mu_data["Music Analysis"]["Cont"],
                    achv = mu_data["Music Analysis"]["Achv"],
                    total = mu_data["Music Analysis"]["Total"],
                ).save()

                mp_cat = ContAchvTotal(
                    cont = mu_data["Music Percussion"]["Cont"],
                    achv = mu_data["Music Percussion"]["Achv"],
                    total = mu_data["Music Percussion"]["Total"],
                ).save()

                mu_total = mu_data["Total"]

                music = Music(
                    music_brass = mb_cat,
                    music_analysis = ma_cat,
                    music_percussion = mp_cat,
                    music_total = mu_total
                ).save()

                new_show = Show(
                    competition = competition_obj,
                    corp = corp_obj,
                    general_effect = general_effect,
                    visual = visual,
                    music = music,
                    total_score = (ge_total +
                                   vi_total +
                                   mu_total)
                ).save()


    return redirect("pull-admin")


@login_required
def show_table(request):
    title = "Show's Table"
    template = "pull/show_table.html"

    shows = Show.objects.all()
    myFilter = ShowFilter(request.GET, queryset=shows)
    shows = myFilter.qs
    table = ShowTable(shows)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    RequestConfig(request).configure(table)

    return render(request, template_name=template, context={"title":title, "table":table, "myFilter":myFilter})

@login_required
def autocomplete_search(request):
    query = request.GET.get('query')
    query_on = request.GET.get('type')
    if query:
        if query_on == "show":
            corps = list(set([show.corp.name for show in Show.objects.all().filter(corp__name__icontains=query)]))
            comps = list(set([show.competition.competition_name_original for show in Show.objects.all().filter(competition__competition_name_original__icontains=query)]))
            return JsonResponse({'status': 200, 'data': corps + comps})
    return JsonResponse({"status":200, "data":[]})