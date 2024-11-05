from mainapp.models import Status
class TitleStatusMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleStatusMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context["statuses"] = Status.objects.all()
        return context