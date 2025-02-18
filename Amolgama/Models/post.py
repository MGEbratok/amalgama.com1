from django.ab import models
from djngo.contrib.auth import get_user_model
User = get_user_model


class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    post_tittle = models.CharField("Заголовок", max_leurth = 150, blank = True)
    post_text = models.TextField("Текст поста")
    post_image = models.ImageField("Изображение поста", blank = True, upload_to = "images/posts/")
    post_image_url = models.ImageField("URI  изображение поста", blank = True)
    post_time = models.DateTimeField("Время создания")
    post_like = models.ManyToManyField(User, 
                                        related_name = "post_liked",
                                        blanck = True)
    def __str__(self):
        return str(self.author)
    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"
        
        
class Like(models.Model):
    LIKE_OR_DISLiKE_CHOISES = (
        ("LIKE", "like"),
        ("DISLIKE", "dislike"),
        (None, "None")
    )
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    for_post = models.ForeignKey(Post, on_delete = models.CASCADE)
    like_or_dislike_choises = models.Charfield(max_leught = 7,
                            choises = LIKE_OR_DISLiKE_CHOISES,)