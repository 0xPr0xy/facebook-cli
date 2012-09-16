#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp
import sys
import os
import logging

class Facebook:
	""" 
	Wrapper around fb graph api using fbconsole
	Let's you use facebook from the command line
	"""

	def __init__(self, page, status_id=None):
		""" 
		Authenticate to facebook 
		Save ACCESS_TOKEN to .fb_access_token 
		"""
		logging.basicConfig(filename='fb.log',level=logging.DEBUG)
		self.fb = imp.load_source('fb', '.fbconsole.py')
		self.fb.AUTH_SCOPE = ['publish_stream']
		self.fb.authenticate()

		if page == 'feed':
			self.show_news_feed()
		elif page == 'profile':
			self.show_profile()
		elif page == 'friends':
			self.show_friends()
		elif page == 'likes':
			self.show_likes()
		elif page == 'music':
			self.show_music()
		elif page == 'status':
			self.post_status()
		elif page == 'photo':
			self.post_photo()
		elif page == 'statusfriend':
			self.post_status_to_friend_wall()
		elif page == 'photofriend':
			self.post_photo_to_friend_wall()
		elif page == 'delete' and status_id is not None:
			self.delete_status(status_id)
		elif page == 'clean':
			self.clean()
		else:
			sys.exit('Invalid Keyword\nValid keywords are: feed, profile, friends, likes, music, status, photo, statusfriend, photofriend, delete <POST ID>, clean\n')
	

	def show_news_feed(self):
		"""
		Output newsfeed
		"""
		data = self.fb.graph('/me/home')
		for item in data['data']:
			try:	
				print str(item['from']['name']) +' ID:'+ str(item['id']) + ':\n' + str(item['message']) + '\n' + str(item['comments']['count']) + '\n'
			except Exception as e:
				logging.exception(e)


	def show_profile(self):
		"""
		Output posts on your wall
		"""
		data = self.fb.graph('/me/posts')
		for item in data['data']:
			try:	
				print 'TIME:' + str(item['created_time']) +' ID:'+ str(item['id']) + '\n' + str(item['message']) + '\n' + str(item['comments']['count']) + '\n'
			except Exception as e:
				logging.exception(e)


	def show_friends(self):
		"""
		Output friends list
		"""
		data = self.fb.graph('/me/friends')
		for item in data['data']:
			try:	
				print str(item['name'])
			except Exception as e:
				logging.exception(e)


	def show_likes(self):
		"""
		Output pages you like
		"""
		data = self.fb.graph('/me/likes')
		for item in data['data']:
			try:	
				print str(item['name'])
			except Exception as e:
				logging.exception(e)


	def show_music(self):
		"""
		Output music you like
		"""
		data = self.fb.graph('/me/music')
		for item in data['data']:
			try:	
				print str(item['name'])
			except Exception as e:
				logging.exception(e)


	def post_status(self):
		"""
		Post status update to your wall
		"""
		try:
			message = raw_input('Type message:\n')
			self.fb.graph_post("/me/feed", {"message":message})
			print 'Post Created: %s' %message
		except Exception as e:
			logging.exception(e)


	def post_photo(self):
		"""
		Post status update with photo to your wall
		"""
		try:
			message = raw_input('Type message:\n')
			photo_location = raw_input('Type photo location:\n')
			self.fb.graph_post("/me/photos", {"message":message,  "source":open(photo_location)})
			print 'Photo Uploaded: %s \nWith Message: %s' %(photo_location,message)
		except Exception as e:
			logging.exception(e)	


	def post_status_to_friend_wall(self):
		"""
		Post status update to a friends wall
		"""
		data = self.fb.graph('/me/friends')
		friend_name = raw_input('Type Friend Name:\n')
		try:
			for item in data['data']:
				if item['name'] == friend_name:
					print 'Friend Found!'
					friend_id = item['id']
					message = raw_input('Type message:\n')
					self.fb.graph_post("/%s/feed" % friend_id, {"message":message})
					print 'Posted %s to: %s' %(message, item['name'])
		except Exception as e:
			logging.exception(e)	


	def post_photo_to_friend_wall(self):
		"""
		Post status update with photo to a friends wall
		"""
		data = self.fb.graph('/me/friends')
		friend_name = raw_input('Type Friend Name:\n')
		try:
			for item in data['data']:
				if item['name'] == friend_name:
					print 'Friend Found!'
					friend_id = item['id']
					message = raw_input('Type message:\n')
					photo_location = raw_input('Type photo location:\n')
					self.fb.graph_post("/%s/photos" % friend_id, {"message":message,  "source":open(photo_location)})
					print 'Posted %s with image %s to: %s' %(message, photo_location, item['name'])
		except Exception as e:
			logging.exception(e)	


	def delete_status(self, id):
		"""
		Delete status update
		"""
		try:
			print id
			self.fb.graph_delete("/"+id)
			print 'deleted'
		except Exception as e:
			logging.exception(e)	


	def clean(self):
		"""
		Clean the local stored ACCESS_TOKEN
		"""
		os.system('rm .fb_access_token')


if len(sys.argv) == 2:
	Facebook(sys.argv[1])
elif len(sys.argv) == 3:
	Facebook(sys.argv[1], sys.argv[2])
else:
	sys.exit('Invalid Keyword\nValid keywords are: feed, profile, friends, likes, music, status, photo, statusfriend, photofriend, delete <POST ID>, clean\n')