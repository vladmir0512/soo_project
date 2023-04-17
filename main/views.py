from django.views.generic import TemplateView
from django.core.paginator import Paginator
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from time import sleep
from . import models

import numpy as np
import torch
import time
import vk_api
import traceback

# Create your views here.
#123123


class HomePageView(TemplateView):
	template_name = 'main/home.html'
	
	def get_context_data(self, **kwargs):
		
		context = super(HomePageView, self).get_context_data(**kwargs)

		# Добавляем посты
		list_of_posts = []
		posts = models.Post.objects.all()
		for post in posts:
			id_post = post.id_post
			text = post.post_text
			ref = post.post_ref
			try:
				toxic = models.Toxic_Post.objects.get(id_post=id_post)
				post_dict ={
						"text": text,
						"ref": ref,
						"toxic": toxic.toxic,
						"number": toxic.number
					}
			except Exception as e:
				post_dict ={
						"text": text,
						"ref": ref,

					}	
				
				if e == "Toxic_Post matching query does not exist":
					print("Не существует Toxic_Post с таким id_post")
		
					post_dict["toxic"] = "?"
					post_dict["number"] = "?"

				
			list_of_posts.append(post_dict)
			
		paginator = Paginator(list_of_posts, 2)
		page_number = self.request.GET.get('page')
		context['posts'] = list_of_posts
		page_obj = paginator.get_page(page_number)
		context['paginate']=page_obj
		return context


class AboutPageView(TemplateView):
	template_name = 'main/about.html'

 
class Parcer:

	'''
 	# Основной парсер
		def __init__(self):
  
			self.group_id = '26284064'
  
			self.post_lim = 20
  
			self.token = "698e97510f36f88ced18449a9aa25c9663b8e2eeb1f42a857c3c5c2a65be69d5d90b645e12313d090aad7"

			self.session = vk_api.VkApi(token=self.token)

			self.vk = self.session.get_api()
  	'''

	def __init__(self):
		self.group_id = '26284064' #id группы ТАСС
		self.post_lim = 20
		self.token = "698e97510f36f88ced18449a9aa25c9663b8e2eeb1f42a857c3c5c2a65be69d5d90b645e12313d090aad7"
		self.session = vk_api.VkApi(token=self.token)
		self.vk = self.session.get_api()



	def get_posts(self, group_id : str ='-1'):
		'''
		Эта функция - первая часть парсера. Здесь мы получаем посты по заданному id_post.


		По умолчанию group_id - self.group_id.

  		'''
		if group_id == "-1":
			group_id = self.group_id


		for post in range(self.post_lim):
			
			if group_id == '26284064' and post == 0:
				continue		

			wall = self.session.method(
				'wall.get',
    			{
           			"owner_id": '-' + group_id,
        			"count": 1,
          			"offset": post
             	}
    		)
   
			post_id = group_id + '_' + str(wall['items'][0]['id']) 

			if getSamePostId(post_id):
				continue

			postlink = (
       					"https://vk.com/public" +
               			str(group_id) + "?w=wall" +
						str('-'+group_id) +
      					"_" + str(wall['items'][0]['id'])
           				)
   
			time = 0
   
			addPost(
					post_id,
					wall['items'][0]['text'],
					postlink,
					time,
					0, # ПОЧЕМУ ТУТ 0
					wall['items'][0]['date']
    			)
   
			addToxicPost(id_post=models.Post, count=False, number=0)


			
			try:
				self.get_comments(group_id, id_post=post_id)
				print(f"Получаем комменты по посту id {post_id}.")
			except Exception as e:
				print(e)	


	
	def get_comments(self, group_id : str ='-1', id_post : str = "-1"):
		'''
		Эта функция - вторая часть парсера. Здесь мы получаем комментарии и персоны по заданному id_post.


		По умолчанию group_id - self.group_id.
  
		По умолчанию id_post - пост с самым старым временем проверки.

  		'''
		
		if group_id == "-1":
			group_id = self.group_id
		if id_post == "-1":
			id_post = getOldCheckPostId()

  
		global family, alcohol, smoke, political
		
		post_id_full = id_post
		post_id = str(post_id_full.split("_")[1])
		comments = self.session.method('wall.getComments',
                                 		{
                                       		"owner_id": "-" + group_id,
											"post_id": post_id,
											"extended": 1
           								})
		time_check_first = int(time.time())
  
		addCheckPost(post_id_full, time_check_first)
  
		for comment in comments["items"]:
			try:
				from_id = comment["from_id"]
				
				if from_id <= 0:
					continue

				comment_id = str(group_id) + "_" + str(comment['id'])
				user = self.session.method("users.get",
                               {
									"user_ids": from_id, "fields": "city,country,education,occupation,bdate,personal,relation,interests"})

				try:
					samePerson = getSamePersonId(from_id)
				except Exception:
					print('Ошибка добавления коммента :\n', traceback.format_exc())

				# Проверка на то, есть ли этот человек в бд, и если его нет, выполняем парсинг его данных и их добавление:
				if not samePerson:
					name = user[-1]['first_name']
					lastname = user[-1]['last_name']

					try:
						if "city" in user[-1]:
							city = user[-1]["city"]
							city = city["title"]
						else:
							city = '0'

					except Exception:
						print('Ошибка:\n', traceback.format_exc())

					try:

						if "country" in user[-1]:
							country = user[-1]["country"]
							country = country["title"]

						else:
							country = '0'

					except Exception:
						print('Ошибка:\n', traceback.format_exc())

					try:
						if "education" in user[-1]:
							education = user[-1]["education"]
							education = education["university_name"]

						else:
							education = '0'

					except Exception:
						print('Ошибка:\n', traceback.format_exc())

					try:

						if "occupation" in user[-1]:
							occupation = user[-1]["occupation"]
							occupation = occupation["name"]

						else:
							occupation = '0'

					except Exception:
						print('Ошибка:\n', traceback.format_exc())

					try:

						if "relation" in user[-1]:
							family_int = int(user[-1]["relation"])
							if family_int == 1:
								family = "не женат/не замужем"
							elif family_int == 2:
								family = "есть друг/есть подруга"
							elif family_int == 3:
								family = "помолвлен/помолвлена"
							elif family_int == 4:
								family = "женат/замужем"
							elif family_int == 5:
								family = "всё сложно"
							elif family_int == 6:
								family = "в активном поиске"
							elif family_int == 7:
								family = "влюблён/влюблена"
							elif family_int == 8:
								family = "в гражданском браке"
							elif family_int == 0:
								family = "0"
						else:
							family = 0
							

					except Exception:
						print('Ошибка:\n', traceback.format_exc())

					try:
						if 'bdate' in user[-1]:
							birthday = user[-1]['bdate']
						else:
							birthday = '0'
					except Exception:
						print('Ошибка:\n', traceback.format_exc())

					try:

						if "personal" in user[-1]:
							
							if "alcohol" in user[-1]['personal']:
							
								alcohol_int = user[-1]['personal']["alcohol"]

								if alcohol_int == 1:
									alcohol = "резко негативное"
								elif alcohol_int == 2:
									alcohol = "негативное"
								elif alcohol_int == 3:
									alcohol = "компромиссное"
								elif alcohol_int == 4:
									alcohol = "нейтральное"
								elif alcohol_int == 5:
									alcohol = "положительное"
								
								else:
									print("\"alcohol\" not in [1,2,3,4,5], setting alcohol = \"0\"")
									alcohol = "0"
							else:
								print("\"alcohol\" not in user[-1]['personal'], setting alcohol = \"0\"")
								alcohol = "0"
									
							if "smoking" in user[-1]['personal']:
								
								smoke_int = user[-1]['personal']["smoking"]

								if smoke_int == 1:
									smoke = "резко негативное"
								elif smoke_int == 2:
									smoke = "негативное"
								elif smoke_int == 3:
									smoke = "компромиссное"
								elif smoke_int == 4:
									smoke = "нейтральное"
								elif smoke_int == 5:
									smoke = "положительное"
									
								else:
									print("\"smoke\" not in [1,2,3,4,5], setting smoking = \"0\"")
									smoke = "0"
							else:
								print("\"smoke\" not in user[-1]['personal'], setting smoke = \"0\"")
								smoke = "0"  
								
							if "political" in user[-1]['personal']:
								political_int = user[-1]['personal']["political"]

								if political_int == 1:
									political = "коммунистические"
								elif political_int == 2:
									political = "социалистические"
								elif political_int == 3:
									political = "умеренные"
								elif political_int == 4:
									political = "либеральные"
								elif political_int == 5:
									political = "консервативные."
								elif political_int == 6:
									political = "монархические"
								elif political_int == 7:
									political = "ультраконсервативные"
								elif political_int == 8:
									political = "индифферентные"
								elif political_int == 9:
									political = "либертарианские"
								else:
									print("\"political\" not in [1,2,3,4,5,6,7,8,9], setting political = \"0\"")
									political = "0"         
							else:
								print("\"political\" not in user[-1]['personal'], setting political = \"0\"")
								political = "0"                
							
							
						else:
							print("\"personal\" not in user[-1], setting alcohol = \"0\"")
							alcohol = "0"
							political = "0"  
							smoke = "0"
	
								
							
				
					
					except Exception:
						
						print('Ошибка:\n', traceback.format_exc())

				

				

					try:
						if "interests" in user[-1]:
							interests = user[-1]['interests']
						else:
							interests = "0"
					except Exception:
						print('Ошибка:\n', traceback.format_exc())
				
					# Добавляем в бд информацию по человеку
					addPerson(from_id, name, lastname, city, country, education,
								occupation, family, birthday, alcohol, smoke, political, interests)

				try:
					sameComment = getSameCommentId(from_id)
				except Exception:
					print('Ошибка:\n', traceback.format_exc())
				
				try:
					comment_text = comment["text"]
				except Exception:
					print('Ошибка:\n', traceback.format_exc())

				
				if sameComment:
					print("Same comment, skip...")
					continue
		
				if not comment_text:
					print(f"Saddenly, no text in comment id {comment_id}skip...")
					continue
				
				try:
					addComment(id_comment=comment_id, id_post=id_post, id_person=from_id,
								comment=comment["text"], comment_date=comment["date"])
					#changeFlag для токсик_поста,где id_post=id_post
				except Exception:
					print('Ошибка:\n', traceback.format_exc())

				try:
					addToxicComment(text2toxicity(comment["text"]))
				except Exception:
					print('Ошибка:\n', traceback.format_exc())

				

				# try:
				#     orm.changeFlag()
				# except Exception:
				#     print('Ошибка:\n', traceback.format_exc())

			except Exception:
				print('Ошибка:\n', traceback.format_exc())


def toxc():
    '''
    # Токсичность для парсера
	Получение комментариев постоянно, по принципу очереди.
 
 	Берет пост где не брались давно комментарии и получает их.
  
	Если есть новый комментарий – то флаг у токсичности поста возвести.
 
	Получить пост из БД  (сортировка)
    '''
    try:
        # получить комменты, которые есть в comments, но которых нет в toxic_comments
        comments_and_ids = toxicGetComment()
        list_of_comments = []
        id_and_toxic = tuple()
        for comment in comments_and_ids:
            list_of_comments.append(comment.comment)

        toxic_list = text2toxicity(list_of_comments)

        id_and_toxic = (comments_and_ids), (toxic_list)

        for toxic_comment in toxic_list:
            number = list(toxic_list).index(toxic_comment)
            id_comment = id_and_toxic[0][number]
            toxic = id_and_toxic[1][number]
            addToxicComment(id_comment, toxic)
            
            # получить айди поста через коммент

    except Exception as e:
        if str(type(e)) == "<class 'IndexError'>":
            print("Toxicity already calculated.")
            return False
        else:
            print('Ошибка:\n', traceback.format_exc())
            return False




def addCheckPost(id_post : str, time_check_first : int):  # возвращает True или False
    try:
        models.Post.objects.filter(id_post=id_post).update(time_check_first=time_check_first)
        print(f"Временная метка проверки поста id {id_post} обновлена.")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())

        return False
    return True

def addPost(id_post : str, post_text : str, post_ref : str, time_check_first : int, time_last_comment : int, post_date : int):
	try:
		a = models.Post(id_post=id_post, post_text=post_text, post_ref=post_ref, time_check_first=time_check_first, time_last_comment=time_last_comment, post_date=post_date)
		a.save()
		
	
	except Exception as e:
		print("Возникло исключение пр добавлении нового поста: \n",e)
		


def addToxicComment(id_comment = models.Comment, id_post = models.Post, toxic=0):
	try:
		
		models.Comment(id_comment=id_comment,
					id_post=id_post,
					toxic=toxic
					).save()

		print(f"Добавлен токсик коммент id {id_comment}.")
	except Exception as e:
		print("Токсик коммент не добавлен.", e)

def addToxicPost(id_post, toxic=0.5, count : bool=False, number=0):
	try:
		
		toxic_list = models.Toxic_Comment.objects.get(id_post=id_post)
		if not toxic_list[1]:
			return toxic_list[1]
		else:
			toxic_list=toxic_list[0]

		pre_round_toxic_list = []
  
		for toxic in toxic_list:
			round_toxic_list.append(toxic.toxic)
   
   
		round_toxic_list = round(np.mean(pre_round_toxic_list), 2)
		number = len(pre_round_toxic_list)
		models.Toxic_Post(
      					id_post=id_post,
						toxic=round_toxic_list,
						count=count,
						number=number
		).save()

		
  
		print(f"Добавлен токсик пост id {id_post}.")
	except Exception as e:
		print("Токсик пост не добавлен.", e)
  
         
def getSamePostId(id_post : str):
	try:
		models.Post.objects.get(id_post=id_post)
	except Exception as e:
		if str(e) == "Post matching query does not exist.":
			print("Нет этого поста. Добавляем.")
			return False
		else:
			print("Возникло исключение при получении похожего поста: \n",e)
			return False
	return True

def getSamePersonId(id_person : str): # возвращает True или False
	try:
		models.Person.objects.get(id_person=id_person)
	except Exception as e:
		if str(e) == "Person matching query does not exist.":
			print("Нет этого человека. Добавляем.")
			return False
		else:
			print("Возникло исключение при получении существования поста: \n",e)
			return False
	return True
    
   
def getOldCheckPostId():
    try:
        oldCheck = models.Post.objects.order_by("time_check_first")[0].id_post
        print(f"Найден самый старый пост с id {oldCheck}.")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        return False
    return str(oldCheck)

def addPerson(id_person : str, first_name : str, second_name : str, city : str,
                country : str, education : str, occupation : str, family : str,
                birthday : str, alcohol : str, smoke : str, political : str, interests : str):  # возвращает True или False
    try:
        models.Person.objects.create(  
                        id_person=id_person, # логин (идентификатор ВК)
                        first_name=first_name,
                        second_name=second_name,
                        city=city,
                        country=country,
                        education=education,
                        occupation=occupation,
                        family=family,
                        birthday=birthday,
                        alcohol=alcohol,
                        smoke=smoke,
                        political=political,
                        interests=interests
                    )

        print(f"Человек добавлен id {id_person}")
    except Exception as e:
        print("Человек не добавлен.", e)
        return False
    return True

def getSameCommentId(id_comment : str):
	try:
		models.Comment.objects.get(id_comment=id_comment)
	except Exception as e:
		if str(e) == "Comment matching query does not exist.":
			print("Нет этого человека. Добавляем.")
			return False
		else:
			print("Возникло исключение при получении существования человека.: \n",e)
			return False
	return True
   

def addComment(id_comment : str ,id_post : models.Post, id_person : models.Person, comment: str, comment_date : int):
	try:
		pos = models.Post.objects.get_or_create(id_post=id_post)
		if not pos[1]:
			return pos[1]
		else:
			pos=pos[0]

		per = models.Person.objects.get_or_create(id_person=id_person)
		if not per[1]:
			return per[1]
		else:
			per=per[0]
		models.Comment(id_comment=id_comment,
					id_post=models.Post,
					id_person=models.Person,
					comment=comment,
					comment_date=comment_date
					).save()

		print(f"Добавлен коммент id {id_comment}.")
	except Exception as e:
		print("Коммент не добавлен.", e)


def text2toxicity(text : str | list ) -> list:
	'''
	Подаем на вход значение или массив текстовых значений.
 
	На выходе получаем список.
	'''
    
	model_checkpoint = 'cointegrated/rubert-tiny-toxicity'
	tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
	model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
	if torch.cuda.is_available():
		model.cuda()
	""" Calculate toxicity of a text (if aggregate=True) or a vector of toxicity aspects (if aggregate=False)"""
	with torch.no_grad():
		inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(model.device)
		proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()
	if isinstance(text, str):
		proba = proba[0]    
	return 1 - proba.T[0] * (1 - proba.T[-1])


