from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.urls import reverse
from v1.db.application.application import Application
from v1.db.models import Commission
from v1.db.user.profile import AggentUserProfile
from v1.web.views.admin.commission.forms import AgentCommissionForm
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F
from django.contrib.auth.models import Group
from django.db.models.functions import ExtractYear, ExtractMonth



class CommissionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = ('db.view_commission')
	model = Commission
	context_object_name = 'commissions'
	template_name = 'admin/commission/commission_list.html'
	# paginate_by = 10


class AddAgentCommission(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_commission')
	form_class = AgentCommissionForm
	template_name = 'admin/commission/add_commission.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:commission_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add Commission"
		return context

	def form_valid(self, form):
		messages.success(self.request, 'Successfully Added.')
		return super(AddAgentCommission, self).form_valid(form)


class EditAgentCommission(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_commission')
	model = Commission
	form_class = AgentCommissionForm
	template_name = 'admin/commission/add_commission.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:commission_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['title'] = 'Edit Commission'
		#context['event'] = event
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(EditAgentCommission, self).form_valid(form)


class DeleteAgentCommission(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_commission')
	model = Commission
	template_name = 'admin/master/delete_city.html'
	pk_url_kwarg = 'pk'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:commission_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page'] = 'Delete Agent Commission'
		context['content'] = 'Are you sure you want to delete ?'
		return context


class AgentCommissionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = ('db.view_commission')
	model = Commission
	context_object_name = 'results'
	template_name = 'admin/commission/agent_commission_list.html'
	# paginate_by = 10

	def get_queryset(self):
		context = []
		agent_users = Group.objects.get(name="aggent").user_set.values_list('id')
		agent_users = [au[0] for au in agent_users]
		print('[+] All agent users :: ', agent_users)

		applications = Application.objects.filter(ap_status=1)
		year_applications = applications.values('year').annotate(count=Count('id')).order_by('-year')
		for _application in year_applications:
			year = _application.get('year')
			print(year)
			mod_applications = applications.filter(year=year).values('user', 'ap_currency').annotate(user_count=Count('user'), app_total=Sum('ap_grand_total'), year_count=Count('year')).order_by('-user')
			print(applications, mod_applications)
			for application in mod_applications:
				user_id = application.get('user')
				# check agent user
				if user_id in agent_users:
					# Get commission rate
					app_count = application.get('user_count')
					app_grand_total = application.get('app_total')
					app_ap_currency = application.get('ap_currency')
					app_year = year
					
					# commission = Commission.objects.filter(min_application__gte=0, max_application__lte=app_count, is_active=True).order_by('commission_rate').first()
					commissions = Commission.objects.filter(is_active=True).order_by('commission_rate')
					commission_rate = 0
					for commission in commissions:
						min_application = commission.min_application
						max_application = commission.max_application
						if app_count in range(min_application, max_application):
							commission_rate = commission.commission_rate
							break
					
					commission_amount = (app_grand_total * commission_rate)/100
					commission_amount = round(float(commission_amount), 2)
					context.append(
						{
							'agent': User.objects.get(pk=user_id).email,
							'no_of_application': app_count,
							'commission_rate': commission_rate,
							'year': app_year,
							'currency': app_ap_currency,
							'app_amount': app_grand_total,
							'commission_amount': commission_amount,
						},
					)

		return context