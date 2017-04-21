from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from symposion.proposals.models import ProposalSection

from pyconca2017.users.services import UserService


@login_required
def submit_proposal(request):
    user = request.user
    proposal_service = UserService()
    proposal_service.get_or_create_speaker(user)

    return redirect('proposal_submit')


class CFPView(TemplateView):
    template_name = 'cfp_main.html'

    def get_context_data(self, **kwargs):

        kinds = []
        for proposal_section in ProposalSection.available():
            for kind in proposal_section.section.proposal_kinds.all():
                kinds.append(kind.slug)

        return {
            "kinds": kinds,
        }
