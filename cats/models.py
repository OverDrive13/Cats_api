from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Achievement(models.Model):
    """Достижения."""
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Cat(models.Model):
    """Коты."""
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
        )
    achievements = models.ManyToManyField(Achievement, through='AchievementCat')
    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
        )

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    """Достижения кота."""

    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'


class Review(models.Model):
    """Отзыв."""

    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(10, ),
            MinValueValidator(1, )
        ]
    )
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta(RelatedName.Meta):
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.text[:10]} {self.author} {self.pub_date}'


class Breed(models.Model):
    """Порода."""

    name = models.CharField(max_length=150, verbose_name='Название породы')

    def __str__(self):
        return self.name
