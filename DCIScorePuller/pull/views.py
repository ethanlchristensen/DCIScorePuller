from django.shortcuts import render, redirect
from django.urls import reverse
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
    """
    View to render out the home page
    """

    # get the template name
    template = "pull/home.html"
    # set the title
    title = "Home"
    # create the context
    context = {"title": title}
    # render the template
    return render(request, template_name=template, context=context)


def about(request):
    """
    View to render out the about page
    """

    # get the template name
    template = "pull/about.html"
    # get the title
    title = "About"
    # create the context
    context = {"title": title}
    return render(request, template_name=template, context=context)


def welcome(request):
    """
    View to render out the Welcome Page
    """

    # get the template name
    template = "pull/welcome.html"
    # get the title
    title = "Welcome"
    # create the context
    context = {"title": title}
    # render the template
    return render(request=request, template_name=template, context=context)


@staff_member_required
def admin(request):
    """
    View to render out the DCISP Admin Page (non-django admin)
    """

    # get the template name
    template = "pull/admin.html"
    # get the title
    title = "Admin"
    # create the context
    context = {"title": title}
    # render out the template
    return render(request, template_name=template, context=context)


@staff_member_required
def scrape(request):
    """
    View to scrape the DCI Site for Score data
    """

    # initialize the puller
    puller = DciScorePuller(season=2023)
    # get all the competitions that occured
    puller.get_competitions().format_competition_titles()

    # process each competition
    for competition in puller.formatted_shows:
        # only process if this competiton isn't in the database yet
        if not Competition.objects.filter(competition_name=competition).exists():
            # get the recap we need to save first, we need the date
            # and comp name for the competition model
            recap = puller.get_competition_recap(show=competition)

            # DEBUG
            # with open(f"./pull/utils/RECAP_JSON/{competition}.json", "w") as f:
            #     tmp_recap = recap
            #     tmp_recap["date"] = tmp_recap["date"].strftime("%Y-%m-%d")
            #     f.write(json.dumps(recap, indent=4))

            # save the competition, returns the db obj created
            competition_obj = Competition(
                competition_name=competition,
                competition_name_original=recap["Correct Competition Name"],
                competition_date=recap["date"],
                competition_date_as_string=recap["date"].strftime("%B %d, %Y"),
            ).save()

            # for each corp, add the scores
            for corp in recap["shows"]:
                # check to see if the corp already exsists in corp DB
                corp_check = Corp.objects.filter(name=corp)

                # corp exists, just need its key
                if corp_check.exists():
                    # grab the corp object
                    corp_obj = corp_check[0]
                # need to add this corp, and also get its key
                else:
                    # ssave this corp, returns the db obj created
                    corp_obj = Corp(name=corp).save()

                # GENERAL EFFECT ##################################################################
                # get the GE data from the recap payload
                ge_data = recap["shows"][corp]["General Effect"]

                # we are only dealing with 3 columns
                if len(ge_data) == 3:
                    # create the GE-One object, returns the db obj created
                    ge_1_1_rpt = RepPerfTotal(
                        rep=ge_data["General Effect 1"]["Rep"],
                        perf=ge_data["General Effect 1"]["Perf"],
                        total=ge_data["General Effect 1"]["Total"],
                    ).save()

                    # create the GE-Two object, returns the db obj created
                    ge_2_1_rpt = RepPerfTotal(
                        rep=ge_data["General Effect 2"]["Rep"],
                        perf=ge_data["General Effect 2"]["Perf"],
                        total=ge_data["General Effect 2"]["Total"],
                    ).save()

                    # get the GE Total Score
                    ge_total = ge_data["Total"]

                    # Create the GE Object, linking it to the sub scores
                    # returns the db obj created
                    general_effect = GeneralEffect(
                        general_effect_one_one=ge_1_1_rpt,
                        general_effect_two_one=ge_2_1_rpt,
                        general_effect_total=ge_total,
                    ).save()
                else:
                    # else we are dealing with 5 columns
                    # create the GE-One-1 object, returns the db obj created
                    ge_1_1_rpt = RepPerfTotal(
                        rep=ge_data["General Effect 1 - 1"]["Rep"],
                        perf=ge_data["General Effect 1 - 1"]["Perf"],
                        total=ge_data["General Effect 1 - 1"]["Total"],
                    ).save()

                    # create the GE-One-2 object, returns the db obj created
                    ge_1_2_rpt = RepPerfTotal(
                        rep=ge_data["General Effect 1 - 2"]["Rep"],
                        perf=ge_data["General Effect 1 - 2"]["Perf"],
                        total=ge_data["General Effect 1 - 2"]["Total"],
                    ).save()

                    # create the GE-Two-1 object, returns the db obj created
                    ge_2_1_rpt = RepPerfTotal(
                        rep=ge_data["General Effect 2 - 1"]["Rep"],
                        perf=ge_data["General Effect 2 - 1"]["Perf"],
                        total=ge_data["General Effect 2 - 1"]["Total"],
                    ).save()

                    # create the GE-Two-2 object, returns the db obj created
                    ge_2_2_rpt = RepPerfTotal(
                        rep=ge_data["General Effect 2 - 2"]["Rep"],
                        perf=ge_data["General Effect 2 - 2"]["Perf"],
                        total=ge_data["General Effect 2 - 2"]["Total"],
                    ).save()

                    # get the GE Total
                    ge_total = ge_data["Total"]

                    # Create the GE Object, linking it to the sub scores
                    # returns the db obj created
                    general_effect = GeneralEffect(
                        general_effect_one_one=ge_1_1_rpt,
                        general_effect_one_two=ge_1_2_rpt,
                        general_effect_two_one=ge_2_1_rpt,
                        general_effect_two_two=ge_2_2_rpt,
                        general_effect_total=ge_total,
                    ).save()

                # VISUAL
                vi_data = recap["shows"][corp]["Visual"]

                vp_cat = ContAchvTotal(
                    cont=vi_data["Visual Proficiency"]["Cont"],
                    achv=vi_data["Visual Proficiency"]["Achv"],
                    total=vi_data["Visual Proficiency"]["Total"],
                ).save()

                va_cat = ContAchvTotal(
                    cont=vi_data["Visual Analysis"]["Cont"],
                    achv=vi_data["Visual Analysis"]["Achv"],
                    total=vi_data["Visual Analysis"]["Total"],
                ).save()

                cg_cat = ContAchvTotal(
                    cont=vi_data["Color Guard"]["Cont"],
                    achv=vi_data["Color Guard"]["Achv"],
                    total=vi_data["Color Guard"]["Total"],
                ).save()

                vi_total = vi_data["Total"]

                visual = Visual(
                    visual_proficiency=vp_cat,
                    visual_analysis=va_cat,
                    color_guard=cg_cat,
                    visual_total=vi_total,
                ).save()

                # MUSIC
                # get the music score data
                mu_data = recap["shows"][corp]["Music"]

                # create CAT obj for music brass
                mb_cat = ContAchvTotal(
                    cont=mu_data["Music Brass"]["Cont"],
                    achv=mu_data["Music Brass"]["Achv"],
                    total=mu_data["Music Brass"]["Total"],
                ).save()

                # create CAT obj for music analysis
                ma_one_cat = ContAchvTotal(
                    cont=mu_data["Music Analysis - 1"]["Cont"],
                    achv=mu_data["Music Analysis - 1"]["Achv"],
                    total=mu_data["Music Analysis - 1"]["Total"],
                ).save()

                # if we have more then 4 keys in the music dict, then
                # there was another music analysis
                ma_two_cat = None
                if len(mu_data) != 4:
                    ma_two_cat = ContAchvTotal(
                        cont=mu_data["Music Analysis - 2"]["Cont"],
                        achv=mu_data["Music Analysis - 2"]["Achv"],
                        total=mu_data["Music Analysis - 2"]["Total"],
                    ).save()

                # create CAT obj for music percussion
                mp_cat = ContAchvTotal(
                    cont=mu_data["Music Percussion"]["Cont"],
                    achv=mu_data["Music Percussion"]["Achv"],
                    total=mu_data["Music Percussion"]["Total"],
                ).save()

                # get the total music score
                mu_total = mu_data["Total"]

                # create a music obj
                music = Music(
                    music_brass=mb_cat,
                    music_analysis_one=ma_one_cat,
                    music_analysis_two=ma_two_cat,
                    music_percussion=mp_cat,
                    music_total=mu_total,
                ).save()

                # now we have everything we need for the show
                new_show = Show(
                    competition=competition_obj,
                    corp=corp_obj,
                    general_effect=general_effect,
                    visual=visual,
                    music=music,
                    total_score=(ge_total + vi_total + mu_total),
                ).save()

    return redirect("pull-admin")


@login_required
def show_table(request):
    """
    View to render out the Shows Table
    """

    # get the template name
    template = "pull/show_table.html"
    # get the title
    title = "Show's Table"
    # get all the shows
    shows = Show.objects.all()
    # apply the filter to these shows
    myFilter = ShowFilter(request.GET, queryset=shows)
    # get the resulting queryset after filtering
    shows = myFilter.qs
    # create a table off this queryset
    table = ShowTable(shows)
    # paginate the table
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    # configure the request to handle the table
    RequestConfig(request).configure(table)
    # render out the show table template
    return render(
        request,
        template_name=template,
        context={"title": title, "table": table, "myFilter": myFilter},
    )


@login_required
def autocomplete_search(request):
    """
    View to handle autocomplete search
    """

    # get the query from the search bar
    query = request.GET.get("query")
    # get the source of the query
    source = request.GET.get("type")

    # make sure we got a query
    if query:
        # check where the query came from
        if source == "show":
            # get the corp names the contain the query
            corps = list(
                set(
                    [
                        show.corp.name
                        for show in Show.objects.all().filter(
                            corp__name__icontains=query
                        )
                    ]
                )
            )
            # get the competitions that contain the query
            comps = list(
                set(
                    [
                        show.competition.competition_name_original
                        for show in Show.objects.all().filter(
                            competition__competition_name_original__icontains=query
                        )
                    ]
                )
            )
            # get the dates that contain the query
            comp_dates = list(
                set(
                    [
                        show.competition.competition_date_as_string
                        for show in Show.objects.all().filter(
                            competition__competition_date_as_string__icontains=query
                        )
                    ]
                )
            )
            # return the autocomplete results to suggest to user
            return JsonResponse({"status": 200, "data": corps + comps + comp_dates})
    # return nothing is no conditions were met
    return JsonResponse({"status": 200, "data": []})


@login_required
def rank_chart(request, rank_type):
    """
    View for testing charting scores
    """

    # get the template name
    template = "pull/chart_rank.html"
    # get the title
    title = "Chart Testing"
    # get the shows for a certain Corp
    shows = Show.objects.all()
    # get the top-n value from url
    top = request.GET.get("top")
    if top:
        top = int(top)
    else:
        top = 12
    # create a list of n colors for each corp
    top_n_colors = [
        "#e6194b",
        "#3cb44b",
        "#ffe119",
        "#4363d8",
        "#f58231",
        "#911eb4",
        "#46f0f0",
        "#f032e6",
        "#bcf60c",
        "#fabebe",
        "#008080",
        "#e6beff",
        "#9a6324",
        "#fffac8",
        "#800000",
        "#aaffc3",
        "#808000",
        "#ffd8b1",
        "#000075",
        "#808080",
        "#ffffff",
        "#000000",
    ]

    top_n_background_colors = [
        "#e6194b1A",
        "#3cb44b1A",
        "#ffe1191A",
        "#4363d81A",
        "#f582311A",
        "#911eb41A",
        "#46f0f01A",
        "#f032e61A",
        "#bcf60c1A",
        "#fabebe1A",
        "#0080801A",
        "#e6beff1A",
        "#9a63241A",
        "#fffac81A",
        "#8000001A",
        "#aaffc31A",
        "#8080001A",
        "#ffd8b11A",
        "#0000751A",
        "#8080801A",
        "#ffffff1A",
        "#0000001A",
    ]

    # create the data that will be used for charting
    # get the top 12 corps
    if rank_type == "overall":
        ordered_show_corps = [show.corp.name for show in shows.order_by("total_score")]
    elif rank_type == "general-effect-total":
        ordered_show_corps = [show.corp.name for show in shows.order_by("general_effect__general_effect_total")]
    elif rank_type == "general-effect-one":
        ordered_show_corps = [show.corp.name for show in shows.order_by("general_effect__general_effect_one_one__total")]
    elif rank_type == "general-effect-two":
        ordered_show_corps = [show.corp.name for show in shows.order_by("general_effect__general_effect_two_one__total")]
    elif rank_type == "music-total":
        ordered_show_corps = [show.corp.name for show in shows.order_by("music__music_total")]
    elif rank_type == "music-analysis":
        ordered_show_corps = [show.corp.name for show in shows.order_by("music__music_analysis_one__total")]
    elif rank_type == "music-percussion":
        ordered_show_corps = [show.corp.name for show in shows.order_by("music__music_percussion__total")]
    elif rank_type == "music-brass":
        ordered_show_corps = [show.corp.name for show in shows.order_by("music__music_brass__total")]
    elif rank_type == "visual-total":
        ordered_show_corps = [show.corp.name for show in shows.order_by("visual__visual_total")]
    elif rank_type == "visual-proficiency":
        ordered_show_corps = [show.corp.name for show in shows.order_by("visual__visual_proficiency__total")]
    elif rank_type == "visual-analysis":
        ordered_show_corps = [show.corp.name for show in shows.order_by("visual__visual_analysis__total")]
    elif rank_type == "color-guard":
        ordered_show_corps = [show.corp.name for show in shows.order_by("visual__color_guard__total")]

    top_n = []
    for corp in ordered_show_corps[::-1]:
        if corp not in top_n:
            top_n.append(corp)
        if len(top_n) == top:
            break

    top_n = top_n[::-1]
    # get the chart data for the top 12
    chart_data = {}
    all_dates = []
    for i, corp in enumerate(top_n):
        corp_shows = shows.filter(corp__name=corp).order_by(
            "competition__competition_date"
        )
        dates = [show.competition.competition_date for show in corp_shows]
        for date in dates:
            if date not in all_dates:
                all_dates.append(date)
    
    all_dates = sorted(all_dates)

    for i, corp in enumerate(top_n):
        chart_data[corp] = {}
        corp_shows = shows.filter(corp__name=corp).order_by(
            "competition__competition_date"
        )
        chart_data[corp]["label"] = corp
        dates_main = []
        scores_main = []
        dm_idx = 0
        sm_idx = 0
        dates = [show.competition.competition_date for show in corp_shows]

        if rank_type == "overall":
            scores = [show.total_score for show in corp_shows]
        elif rank_type == "general-effect-total":
            scores = [show.general_effect.general_effect_total for show in corp_shows]
        elif rank_type == "general-effect-one":
            scores = [show.general_effect.general_effect_one_one.total for show in corp_shows]
        elif rank_type == "general-effect-two":
            scores = [show.general_effect.general_effect_two_one.total for show in corp_shows]
        elif rank_type == "music-total":
            scores = [show.music.music_total for show in corp_shows]
        elif rank_type == "music-analysis":
            scores = [show.music.music_analysis_one.total for show in corp_shows]
        elif rank_type == "music-percussion":
            scores = [show.music.music_percussion.total for show in corp_shows]
        elif rank_type == "music-brass":
            scores = [show.music.music_brass.total for show in corp_shows]
        elif rank_type == "visual-total":
            scores = [show.visual.visual_total for show in corp_shows]
        elif rank_type == "visual-proficiency":
            scores = [show.visual.visual_proficiency.total for show in corp_shows]
        elif rank_type == "visual-analysis":
            scores = [show.visual.visual_analysis.total for show in corp_shows]
        elif rank_type == "color-guard":
            scores = [show.visual.color_guard.total for show in corp_shows]

        for date in all_dates:
            if date in dates:
                dates_main.append(dates[dm_idx])
                dm_idx += 1
                scores_main.append(scores[sm_idx])
                sm_idx += 1
            else:
                try:
                    dates_main.append(date)
                    scores_main.append(scores[sm_idx])
                except IndexError:
                    dates_main.append(date)
                    scores_main.append(scores[sm_idx-1])
        chart_data[corp]["data"] = [
            {"x": date, "y": score} for date, score in zip(dates_main, scores_main)
        ]
        chart_data[corp]["color"] = top_n_colors[i % len(top_n_colors)]
        chart_data[corp]["bg_color"] = top_n_background_colors[
            i % len(top_n_background_colors)
        ]

    chart_data["labels"] = all_dates

    # create the context
    context = {"title": title, "shows": shows, "chart_data": chart_data, "top":top, "rank_type":rank_type}
    return render(request, template_name=template, context=context)


@login_required
def competition_chart(request, competition):
    """
    View to render chart for a specific show
    """

    # get the template name
    template = "pull/chart_competition.html"
    # get the competitions
    competition_names = [comp.competition_name for comp in Competition.objects.all().order_by("competition_date")]
    if competition not in competition_names:
        competition = competition_names[-1]
        return redirect(reverse('competition-chart', args=(competition,)))
    # get that competition
    competition = Competition.objects.all().filter(competition_name=competition)[0]
    # get the title
    title = competition.competition_name
    # get the shows for this competition
    shows = Show.objects.all().filter(competition__key=competition.key).order_by("total_score")
    # create a table off this queryset
    table = CompetitionTable(shows)
    # configure the request to handle the table
    RequestConfig(request).configure(table)
    # make the context
    context = {
        "title": title,
        "competition_names": competition_names,
        "competition": competition,
        "shows": shows[::-1],
        "table": table
    }
    # render the template
    return render(request, template_name=template, context=context)
