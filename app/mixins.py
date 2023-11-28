from django.contrib.auth.mixins import AccessMixin


class IsStudentMixin(AccessMixin):
    """Verify that the current user is student, otherwise no_permission."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_tutor:
            return self.handle_no_permission()  # maybe just raise  Http404
        return super().dispatch(request, *args, **kwargs)


class IsTutorMixin(AccessMixin):
    """Verify that the current user is student, otherwise no_permission."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_tutor:
            return self.handle_no_permission()  # maybe just raise  Http404
        return super().dispatch(request, *args, **kwargs)
