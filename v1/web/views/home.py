from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from v1.db.master.country import Country
from v1.db.master.school import School
from v1.db.master.school_course import SchoolCourse
from v1.db.master.school_service import SchoolService

PAGE_SIZE = 24


class HomeView(TemplateView):
    template_name = 'web/home.html'


class AboutView(TemplateView):
    template_name = 'web/about.html'


class ServicesView(TemplateView):
    template_name = 'web/services.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = (SchoolService.objects.filter(status=True)
              .select_related('ref_school', 'ref_school__ref_country', 'ref_school__ref_city')
              .order_by('ref_school__school_name', 'service_name'))
        paginator = Paginator(qs, PAGE_SIZE)
        ctx['page_obj'] = paginator.get_page(self.request.GET.get('page'))
        return ctx


class ServiceDetailsView(TemplateView):
    template_name = 'web/service_details.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['service'] = get_object_or_404(
            SchoolService.objects.select_related('ref_school', 'ref_school__ref_country', 'ref_school__ref_city'),
            pk=kwargs['pk'])
        return ctx


class CoursesView(TemplateView):
    template_name = 'web/courses.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = (SchoolCourse.objects.filter(status=True)
              .select_related('ref_school', 'ref_school__ref_country', 'ref_school__ref_city')
              .order_by('ref_school__school_name', 'title'))
        paginator = Paginator(qs, PAGE_SIZE)
        ctx['page_obj'] = paginator.get_page(self.request.GET.get('page'))
        return ctx


class CourseDetailsView(TemplateView):
    template_name = 'web/course_details.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course = get_object_or_404(
            SchoolCourse.objects.select_related('ref_school', 'ref_school__ref_country', 'ref_school__ref_city'),
            pk=kwargs['pk'])
        ctx['course'] = course
        ctx['other_courses'] = (SchoolCourse.objects.filter(status=True, ref_school=course.ref_school)
                                .exclude(pk=course.pk).order_by('title')[:6])
        return ctx


class ProjectsView(TemplateView):
    template_name = 'web/projects.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['countries'] = (Country.objects
                            .annotate(school_count=Count('rel_ref_country_school',
                                                         filter=Q(rel_ref_country_school__status=True)))
                            .filter(school_count__gt=0)
                            .order_by('-school_count', 'country_name'))
        return ctx


class ProjectDetailsView(TemplateView):
    template_name = 'web/project_details.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        country = get_object_or_404(Country, pk=kwargs['pk'])
        ctx['country'] = country
        ctx['schools'] = (School.objects.filter(status=True, ref_country=country)
                          .select_related('ref_city').order_by('school_name'))
        return ctx


class SchoolsView(TemplateView):
    template_name = 'web/schools.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = (School.objects.filter(status=True)
              .select_related('ref_country', 'ref_city')
              .order_by('ref_country__country_name', 'school_name'))
        paginator = Paginator(qs, PAGE_SIZE)
        ctx['page_obj'] = paginator.get_page(self.request.GET.get('page'))
        return ctx


class SchoolDetailsView(TemplateView):
    template_name = 'web/school_details.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        school = get_object_or_404(School.objects.select_related('ref_country', 'ref_city'), pk=kwargs['pk'])
        ctx['school'] = school
        ctx['courses'] = SchoolCourse.objects.filter(status=True, ref_school=school).order_by('title')
        ctx['services'] = (SchoolService.objects.filter(status=True, ref_school=school)
                           .order_by('service_name'))
        return ctx


class ContactView(View):
    def get(self, request, *args, **kwargs):
        from django.template.response import TemplateResponse
        return TemplateResponse(request, 'web/contact.html')

    def post(self, request, *args, **kwargs):
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        subject = (request.POST.get('subject') or '').strip()
        message = (request.POST.get('message') or '').strip()
        with connection.cursor() as cur:
            cur.execute(
                "INSERT INTO nqraa_contactus "
                "(created_at, updated_at, status, name, email, subject, message, created_by_id) "
                "VALUES (now(), now(), true, %s, %s, %s, %s, 1)",
                [name, email, subject, message],
            )
        return redirect('web:thank_you')


class EventsView(TemplateView):
    template_name = 'web/events.html'


class EventDetailsView(TemplateView):
    template_name = 'web/event_details.html'


class BlogView(TemplateView):
    template_name = 'web/blog.html'


class BlogDetailsView(TemplateView):
    template_name = 'web/blog_details.html'


class FaqView(TemplateView):
    template_name = 'web/faq.html'


class PricingView(TemplateView):
    template_name = 'web/pricing.html'


class TeamView(TemplateView):
    template_name = 'web/team.html'


class TeamDetailsView(TemplateView):
    template_name = 'web/team_details.html'


class ShopView(TemplateView):
    template_name = 'web/shop.html'


class ShopDetailsView(TemplateView):
    template_name = 'web/shop_details.html'


class ThankYouView(TemplateView):
    template_name = 'web/thank_you.html'
