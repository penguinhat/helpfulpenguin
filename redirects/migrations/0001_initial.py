# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArchivedRedirect'
        db.create_table('redirects_archivedredirect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('expiry', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('redirects', ['ArchivedRedirect'])

        # Adding model 'LiveRedirect'
        db.create_table('redirects_liveredirect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('word_list', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('expiry', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('redirects', ['LiveRedirect'])


    def backwards(self, orm):
        # Deleting model 'ArchivedRedirect'
        db.delete_table('redirects_archivedredirect')

        # Deleting model 'LiveRedirect'
        db.delete_table('redirects_liveredirect')


    models = {
        'redirects.archivedredirect': {
            'Meta': {'object_name': 'ArchivedRedirect'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiry': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'redirects.liveredirect': {
            'Meta': {'object_name': 'LiveRedirect'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'expiry': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'word_list': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['redirects']