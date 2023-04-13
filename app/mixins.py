from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "/admin/login/"

    def test_func(self) -> bool:
        if request := getattr(self, "request", None):
            return cast(bool, request.user.is_superuser)
        return False
