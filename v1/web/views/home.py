from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'web/home.html'


class AboutView(TemplateView):
    template_name = 'web/about.html'


class ServicesView(TemplateView):
    template_name = 'web/services.html'


class ServiceDetailsView(TemplateView):
    template_name = 'web/service_details.html'


class CoursesView(TemplateView):
    template_name = 'web/courses.html'


class CourseDetailsView(TemplateView):
    template_name = 'web/course_details.html'


class ProjectsView(TemplateView):
    template_name = 'web/projects.html'


class ProjectDetailsView(TemplateView):
    template_name = 'web/project_details.html'


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


class EventsView(TemplateView):
    template_name = 'web/events.html'


class EventDetailsView(TemplateView):
    template_name = 'web/event_details.html'


class ShopView(TemplateView):
    template_name = 'web/shop.html'


class ShopDetailsView(TemplateView):
    template_name = 'web/shop_details.html'


class ContactView(TemplateView):
    template_name = 'web/contact.html'


class ThankYouView(TemplateView):
    template_name = 'web/thank_you.html'
