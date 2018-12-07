from django_inlines.inlines import InlineBase, ModelInline
from core.models import User


class QuineInline(InlineBase):
    """
    A simple inline that returns itself.
    """
    def render(self):
        bits = []
        if self.variant:
            bits.append(':%s' % self.variant)
        else:
            bits.append('')
        if self.value:
            bits.append(self.value)
        for k, v in list(self.kwargs.items()):
            bits.append("%s=%s" % (k,v))
        else:
            return "{{ quine%s }}" % " ".join(bits)


class DoubleInline(InlineBase):
    """
    A simple inline that doubles itself.
    """
    def render(self):
        value = self.value
        multiplier = 2
        if 'multiplier' in self.kwargs:
            try:
                multiplier = int(self.kwargs['multiplier'])
            except ValueError:
                pass
        try:
            value = int(self.value)
        except ValueError:
            pass
        return value*multiplier


class KeyErrorInline(InlineBase):
    """
    An inline that raises a KeyError. For regression testing.
    """
    def render(self):
        empty = {}
        return empty['this will fail']


class UserInline(ModelInline):
    """
    A inline for the mock user model.
    """
    model = User
