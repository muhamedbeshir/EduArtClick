from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
from v1.db.models import Transaction


class TransactionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = ('db.view_transaction')
	model = Transaction
	context_object_name = 'transactions'
	template_name = 'admin/transaction/transaction_list.html'
	#paginate_by = 10

	