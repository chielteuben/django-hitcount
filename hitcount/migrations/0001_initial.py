# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

try:
    from django.conf import settings
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
except AttributeError:
    AUTH_USER_MODEL = 'auth.User'


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HitCount'
        db.create_table('hitcount_hit_count', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hits', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_hitcount', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hitcount', ['HitCount'])

        # Adding unique constraint on 'HitCount', fields ['content_type', 'object_pk']
        db.create_unique('hitcount_hit_count', ['content_type_id', 'object_pk'])

        # Adding model 'Hit'
        db.create_table('hitcount_hit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[AUTH_USER_MODEL], null=True)),
            ('hitcount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hitcount.HitCount'])),
        ))
        db.send_create_signal('hitcount', ['Hit'])

        # Adding model 'BlacklistIP'
        db.create_table('hitcount_blacklist_ip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
        ))
        db.send_create_signal('hitcount', ['BlacklistIP'])

        # Adding model 'BlacklistUserAgent'
        db.create_table('hitcount_blacklist_user_agent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('hitcount', ['BlacklistUserAgent'])


    def backwards(self, orm):
        # Removing unique constraint on 'HitCount', fields ['content_type', 'object_pk']
        db.delete_unique('hitcount_hit_count', ['content_type_id', 'object_pk'])

        # Deleting model 'HitCount'
        db.delete_table('hitcount_hit_count')

        # Deleting model 'Hit'
        db.delete_table('hitcount_hit')

        # Deleting model 'BlacklistIP'
        db.delete_table('hitcount_blacklist_ip')

        # Deleting model 'BlacklistUserAgent'
        db.delete_table('hitcount_blacklist_user_agent')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        AUTH_USER_MODEL: {
            'Meta': {'object_name': AUTH_USER_MODEL.split('.')[-1]},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'hitcount.blacklistip': {
            'Meta': {'object_name': 'BlacklistIP', 'db_table': "'hitcount_blacklist_ip'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'hitcount.blacklistuseragent': {
            'Meta': {'object_name': 'BlacklistUserAgent', 'db_table': "'hitcount_blacklist_user_agent'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'hitcount.hit': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Hit'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'hitcount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hitcount.HitCount']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % AUTH_USER_MODEL, 'null': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'hitcount.hitcount': {
            'Meta': {'ordering': "('-hits',)", 'unique_together': "(('content_type', 'object_pk'),)", 'object_name': 'HitCount', 'db_table': "'hitcount_hit_count'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_hitcount'", 'to': "orm['contenttypes.ContentType']"}),
            'hits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['hitcount']
