# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Artist.slug'
        db.add_column('artists_artist', 'slug', self.gf('django.db.models.fields.SlugField')(default=1, max_length=100, db_index=True), keep_default=False)

        # Deleting field 'ArtistWorkPhoto.imagemodel_ptr'
        db.delete_column('artists_artistworkphoto', 'imagemodel_ptr_id')

        # Adding field 'ArtistWorkPhoto.id'
        db.add_column('artists_artistworkphoto', 'id', self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True), keep_default=False)

        # Adding field 'ArtistWorkPhoto.title'
        db.add_column('artists_artistworkphoto', 'title', self.gf('django.db.models.fields.CharField')(default=1, max_length=50), keep_default=False)

        # Adding field 'ArtistWorkPhoto.description'
        db.add_column('artists_artistworkphoto', 'description', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'ArtistWorkPhoto.original_image'
        db.add_column('artists_artistworkphoto', 'original_image', self.gf('django.db.models.fields.files.ImageField')(default=1, max_length=100), keep_default=False)

        # Adding field 'ArtistWorkPhoto.slug'
        db.add_column('artists_artistworkphoto', 'slug', self.gf('autoslug.fields.AutoSlugField')(default=1, unique_with=(), max_length=100, populate_from=None, db_index=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Artist.slug'
        db.delete_column('artists_artist', 'slug')

        # Adding field 'ArtistWorkPhoto.imagemodel_ptr'
        db.add_column('artists_artistworkphoto', 'imagemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(default=1, related_name='artists_artistworkphoto', unique=True, primary_key=True, to=orm['galleries.ImageModel']), keep_default=False)

        # Deleting field 'ArtistWorkPhoto.id'
        db.delete_column('artists_artistworkphoto', 'id')

        # Deleting field 'ArtistWorkPhoto.title'
        db.delete_column('artists_artistworkphoto', 'title')

        # Deleting field 'ArtistWorkPhoto.description'
        db.delete_column('artists_artistworkphoto', 'description')

        # Deleting field 'ArtistWorkPhoto.original_image'
        db.delete_column('artists_artistworkphoto', 'original_image')

        # Deleting field 'ArtistWorkPhoto.slug'
        db.delete_column('artists_artistworkphoto', 'slug')


    models = {
        'artists.artist': {
            'Meta': {'object_name': 'Artist'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        'artists.artistworkphoto': {
            'Meta': {'object_name': 'ArtistWorkPhoto'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artists.Artist']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '100', 'populate_from': 'None', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
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
        'auth.user': {
            'Meta': {'object_name': 'User'},
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
        }
    }

    complete_apps = ['artists']
