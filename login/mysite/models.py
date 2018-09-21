from django.db import models

# Create your models here.

class User(models.Model):
    
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = models.CharField(max_length=128,unique=True)#unique=True表示名字唯一不重复
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    #这个参数的默认值也为False，设置为True时，会在model对象第一次被创建时，
    # 将字段的值设置为创建时的时间，以后修改对象时，字段的值不会再更新。
    has_confirmed = models.BooleanField(default=False)
    # User模型新增了has_confirmed字段，这是个布尔值，默认为False，也就是未进行邮件注册；
    def __str__(self):
        return self.name
    
    class Meta:#元数据，对该模型进行附加设置
        db_table = 'User'#设置数据库表名为‘User’
        ordering = ['-c_time']#按照创建时间进行排序
        verbose_name = "用户"#设置模型对象名称
        verbose_name_plural = "用户"#设置模型对象名称的复数形式


class ConfirmString(models.Model):
    # ConfirmString模型保存了用户和注册码之间的关系，一对一的形式；
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"