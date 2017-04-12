from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from pyconca2017.users.services import UserService


@login_required
def submit_proposal(request):
    user = request.user
    proposal_service = UserService()
    proposal_service.get_or_create_speaker(user)

    return redirect('proposal_submit')
