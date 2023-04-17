from django.db import models

#Create models


class Post(models.Model):
    """
    # Посты
        - id_post = models.TextField(unique=True, primary_key=True)
    
        - post_text = models.TextField()
        
        - post_ref = models.TextField()
        
        - time_check_first = models.IntegerField()
        
        - time_last_comment = models.IntegerField()
        
        - post_date = models.IntegerField()
    
    """
    
    
    class Meta:
        db_table = 'posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        
    
    id_post = models.TextField(unique=True, primary_key=True)
    post_text = models.TextField()
    post_ref = models.TextField()
    time_check_first = models.IntegerField()
    time_last_comment = models.IntegerField()
    post_date = models.IntegerField()

class Person(models.Model):
    """
    # Персоны
        - id_person = models.TextField(unique=True, primary_key=True) # логин (идентификатор ВК)
        - first_name = models.TextField()
        - second_name = models.TextField()
        - city = models.TextField()
        - country = models.TextField()
        - education = models.TextField()
        - occupation = models.TextField()
        - family = models.TextField()
        - birthday = models.TextField()
        - alcohol = models.TextField()
        - smoke = models.TextField()
        - political = models.TextField()
        - interests = models.TextField()
    
    """
    class Meta:
        db_table = 'persons'
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'
    id_person = models.TextField(unique=True, primary_key=True) # логин (идентификатор ВК)
    first_name = models.TextField()
    second_name = models.TextField()
    city = models.TextField()
    country = models.TextField()
    education = models.TextField()
    occupation = models.TextField()
    family = models.TextField()
    birthday = models.TextField()
    alcohol = models.TextField()
    smoke = models.TextField()
    political = models.TextField()
    interests = models.TextField()


class Comment(models.Model):
    """
    # Комментарии
    - id_comment = models.TextField(unique=True, primary_key=True) 
    - id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    - id_person = models.ForeignKey(Person, on_delete=models.CASCADE)
    - comment = models.TextField()
    - comment_date = models.IntegerField()
    """
    
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    id_comment = models.TextField(unique=True, primary_key=True) 
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.IntegerField()
	

class Toxic_Comment(models.Model):
    """
    # Токсичные комментарии
    - id_comment = models.OneToOneField(Comment, on_delete=models.CASCADE, unique=True, primary_key=True)
    - id_post = models.OneToOneField(Post,unique=True, on_delete=models.CASCADE)
    - toxic = models.FloatField()
    """
    class Meta:
        db_table = 'toxic_comments'
        verbose_name = 'Токсичный комментарий'
        verbose_name_plural = 'Токсичные комментарии'

    id_comment = models.OneToOneField(Comment, on_delete=models.CASCADE, unique=True, primary_key=True)
    id_post = models.OneToOneField(Post,unique=True, on_delete=models.CASCADE)
    toxic = models.FloatField()


class Toxic_Post(models.Model):
    """
    # Токсичные посты
    - id_post = models.OneToOneField(Post,unique=True, primary_key=True, on_delete=models.CASCADE)
    - toxic = models.FloatField()
    - count = models.BooleanField()
    - number = models.IntegerField()

    """
    class Meta:
        db_table = 'toxic_posts'
        verbose_name = 'Токсичный пост'
        verbose_name_plural = 'Токсичные посты'
        
    id_post = models.OneToOneField(Post,unique=True, primary_key=True, on_delete=models.CASCADE)
    toxic = models.FloatField()
    count = models.BooleanField()
    number = models.IntegerField()


	 
# class Plot(models.Model):
# 	plotType =HStoreField
# 	- тип (Hscore) – json хранить все схожие id постов, Array.
# 	- мешок слов
# 	- вектор … цифрой
# 	'''
