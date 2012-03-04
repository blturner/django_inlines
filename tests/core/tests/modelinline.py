from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_inlines.inlines import Registry, inline_for_model, InlineInputError, registry, ModelInline
from test_inlines import UserInline
from core.models import User

class ModelInlineTestCase(TestCase):

    fixtures = ['users']

    def setUp(self):
        inlines = Registry()
        inlines.register('user', UserInline)
        self.inlines = inlines

    def testModelInlines(self):
        self.assertEqual(self.inlines.process("{{ user 1 }}"), "Xian")
        self.assertEqual(self.inlines.process("{{ user 1 }} vs {{ user 2 }}"), "Xian vs Evil Xian")

    def testModelInlineVariants(self):
        self.assertEqual(self.inlines.process("{{ user:contact 1 }}"), "Xian, (708) 555-1212, xian@example.com")
        self.assertEqual(self.inlines.process("{{ user:nonexistant_variant 1 }}"), "Xian")


class BadInputModelInlineTestCase(TestCase):

    fixtures = ['users']

    def setUp(self):
        inlines = Registry()
        inlines.register('user', UserInline)
        self.inlines = inlines

    def tearDown(self):
        settings.INLINE_DEBUG = False

    def testAgainstNonexistentObject(self):
        self.assertEqual(self.inlines.process("{{ user 111 }}"), "")

    def testAgainstCrapInput(self):
        self.assertEqual(self.inlines.process("{{ user asdf }}"), "")

    def testErrorRaising(self):
        settings.INLINE_DEBUG = True
        process = self.inlines.process
        self.assertRaises(InlineInputError, process, "{{ user 111 }}",)
        self.assertRaises(InlineInputError, process, "{{ user asdf }}",)

class InlineForModelTestCase(TestCase):

    fixtures = ['users']

    def setUp(self):
        inlines = Registry()
        self.inlines = inlines

    def testInlineForModel(self):
        self.inlines.register('user', inline_for_model(User))
        self.assertEqual(self.inlines.process("{{ user 1 }}"), "Xian")
        self.assertEqual(self.inlines.process("{{ user 1 }} vs {{ user 2 }}"), "Xian vs Evil Xian")

    def testInlineForModelBadInput(self):
        self.assertRaises(ValueError, inline_for_model, "User")


class AdminInlineTestCase(TestCase):
    def setUp(self):
        username = 'ben'
        pwd = 'secret'
        self.user = AuthUser.objects.create_user(username, 'ben@fakemail.com', pwd)
        self.user.is_staff = True
        self.user.save()
        self.client.login(username=username, password=pwd)

        registry.register('user', UserInline)

    def test_inline_is_invalid(self):
        # No inline or target specified
        resp = self.client.get(reverse('get_inline_form'))
        self.assertEqual(resp.status_code, 404)

        # No inline specified
        resp = self.client.get(reverse('get_inline_form'), {'target': 'body_id'})
        self.assertEqual(resp.status_code, 404)

        # No target specified
        resp = self.client.get(reverse('get_inline_form'), {'inline': 'user'})

    def test_get_inline_form(self):
        resp = self.client.get(reverse('get_inline_form'), {'inline': 'user',
                                                                'target': 'body_id'})
        self.assertTemplateUsed(resp, 'admin/django_inlines/inline_form.html')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['target'])
        self.assertTrue(resp.context['ADMIN_MEDIA_PREFIX'])
        self.assertEqual(resp.context['app_label'], 'core/user')
        self.assertContains(resp, ('<img src="%simg/admin/selector-search.gif" width="16" height="16" alt="Lookup" />' % resp.context['ADMIN_MEDIA_PREFIX']))
