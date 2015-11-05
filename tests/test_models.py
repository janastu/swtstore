# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase

from swtstore.classes.utils import urlnorm  # normalize URLs
from swtstore.application import create_app
import test_config as config
from swtstore.classes.database import db
from swtstore.classes.models import Sweet, Context, User


class TestSweet(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config.DefaultConfig())
        return app

    def setUp(self):
        db.create_all()
        user = User("John", "john@smith.com")
        self.what = Context("my-context", {'sample': 'simply'}, user)
        self.who = User("Random Joe Hacker", "rand.joe.hack@hack.com")
        self.where = "http://gnu.org"
        self.how = {
            'attr1': 'val1',
            'attr2': 42,
            'attr3': ['val31', 'val32', 'val33'],
            'attr4': {
                'key41': 'val41',
                'key42': 'val42',
                'key43': 'val43'
            }
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_sweet(self):
        print "test_create_sweet"
        new_sweet = Sweet(self.who, self.what, self.where, self.how)
        new_sweet.persist()

        self.assertTrue(isinstance(new_sweet, Sweet))
        self.assertEqual(new_sweet.who, self.who)

        # try constructing a sweet with missing values
        self.assertRaises(TypeError, Sweet, *[self.who, self.what, self.where])
        self.assertRaises(TypeError, Sweet, *[self.who, self.what, self.how])
        self.assertRaises(TypeError, Sweet, *[self.who, self.where, self.how])
        self.assertRaises(TypeError, Sweet, *[self.what, self.where, self.how])

    def test_update_sweet(self):
        print "test_update_sweet"
        new_sweet = Sweet(self.who, self.what, self.where, self.how)

        # test updated sweet has new how
        new_how = {'attr1': 'val1', 'attr2': 'val2'}
        new_sweet.update(how=new_how)
        self.assertEqual(new_sweet.how, new_how)

        # test it ignores who/what params if updated
        new_user = User('newuser', 'newuser@email.com')
        new_sweet.update(who=new_user)
        self.assertNotEqual(new_sweet.who, new_user)
        self.assertEqual(new_sweet.who, self.who)

    def test_get_by_creator(self):
        print "test_get_by_creator"
        new_sweet1 = Sweet(self.who, self.what, self.where, self.how)
        new_sweet1.persist()
        new_sweet2 = Sweet(self.who, self.what, "http://mit.edu", self.how)
        new_sweet2.persist()
        new_sweet3 = Sweet(self.who, self.what, "http://ucla.edu", self.how)
        new_sweet3.persist()
        user2 = User("Foe", "foe@smo.com")
        new_sweet4 = Sweet(user2, self.what, "http://mit.edu", self.how)
        new_sweet4.persist()
        new_sweet5 = Sweet(user2, self.what, "http://ucla.edu", self.how)
        new_sweet5.persist()

        result = Sweet.getByCreator("Random Joe Hacker")
        self.assertEqual(len(result), 3)
        result = Sweet.getByCreator("Foe")
        self.assertEqual(len(result), 2)
        result = Sweet.getByCreator("No Man")
        self.assertEqual(len(result), 0)

    def test_get_by_context(self):
        print "test_get_by_context"
        ctx = Context('foo', {'sample': 'na'}, self.who)

        new_sweet1 = Sweet(self.who, self.what, self.where, self.how)
        new_sweet1.persist()
        new_sweet2 = Sweet(self.who, self.what, self.where, self.how)
        new_sweet2.persist()
        new_sweet3 = Sweet(self.who, ctx, self.where, self.how)
        new_sweet3.persist()
        new_sweet4 = Sweet(self.who, ctx, self.where, self.how)
        new_sweet4.persist()
        new_sweet5 = Sweet(self.who, ctx, self.where, self.how)
        new_sweet5.persist()

        result = Sweet.getByContext("foo")
        self.assertEqual(len(result), 3)
        result = Sweet.getByContext("my-context")
        self.assertEqual(len(result), 2)
        result = Sweet.getByContext("bar")
        self.assertEqual(len(result), 0)

    def test_get_by_uri(self):
        print "test_get_by_uri"
        new_sweet1 = Sweet(self.who, self.what, self.where, self.how)
        new_sweet1.persist()
        new_sweet2 = Sweet(self.who, self.what, "http://kernel.org", self.how)
        new_sweet2.persist()
        new_sweet3 = Sweet(self.who, self.what, "http://kernel.org", self.how)
        new_sweet3.persist()
        new_sweet4 = Sweet(self.who, self.what, "http://kernel.org", self.how)
        new_sweet4.persist()

        result = Sweet.getByURI(urlnorm("http://kernel.org"))
        self.assertEqual(len(result), 3)
        result = Sweet.getByURI(urlnorm(self.where))
        self.assertEqual(len(result), 1)
        result = Sweet.getByURI(urlnorm("http://google.com"))
        self.assertEqual(len(result), 0)


class TestContext(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config.DefaultConfig())
        return app

    def setUp(self):
        db.create_all()
        self.json_ld = {'attr1': 'val1', 'attr2': 'val2'}
        self.user = User('Joe', 'joe@smith.com')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_context(self):
        print "test_create_context"
        ctx = Context('my-context', self.json_ld, self.user)
        ctx.persist()

        self.assertTrue(isinstance(ctx, Context))
        self.assertEqual(ctx.name, "my-context")

    def test_get_by_name(self):
        print "test_get_by_name"
        ctx = Context('my-context', self.json_ld, self.user)
        ctx.persist()

        result = Context.getByName('my-context')
        self.assertEqual(result.name, 'my-context')

    def test_get_by_creator(self):
        print "test_get_by_creator"
        ctx = Context('my-context', self.json_ld, self.user)
        ctx.persist()

        result = Context.getByCreator(self.user)[0]
        self.assertEqual(result.creator, self.user)

    def test_get_all(self):
        print "test_get_all"
        ctx1 = Context('my-context', self.json_ld, self.user)
        ctx1.persist()
        ctx2 = Context('re-narration', self.json_ld, self.user)
        ctx2.persist()
        ctx3 = Context('somecontext', self.json_ld, self.user)
        ctx3.persist()

        result = Context.getAll()
        self.assertEqual(len(result), 3)


if __name__ == '__main__':
        unittest.main()
