# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Info.birthday'
        db.add_column(u'homepage_info', 'birthday',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Info.bio'
        db.add_column(u'homepage_info', 'bio',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Info.email'
        db.add_column(u'homepage_info', 'email',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Info.jabber'
        db.add_column(u'homepage_info', 'jabber',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Info.skype'
        db.add_column(u'homepage_info', 'skype',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Info.contacts'
        db.add_column(u'homepage_info', 'contacts',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Info.birthday'
        db.delete_column(u'homepage_info', 'birthday')

        # Deleting field 'Info.bio'
        db.delete_column(u'homepage_info', 'bio')

        # Deleting field 'Info.email'
        db.delete_column(u'homepage_info', 'email')

        # Deleting field 'Info.jabber'
        db.delete_column(u'homepage_info', 'jabber')

        # Deleting field 'Info.skype'
        db.delete_column(u'homepage_info', 'skype')

        # Deleting field 'Info.contacts'
        db.delete_column(u'homepage_info', 'contacts')


    models = {
        u'homepage.info': {
            'Meta': {'object_name': 'Info'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['homepage']