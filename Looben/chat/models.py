from django.db import models


from accounts.models import Users


class Messages(models.Model):
    
    description = models.TextField()
    sender_name = models.ForeignKey(Users, verbose_name="送信者", on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(Users, verbose_name="受信者", on_delete=models.CASCADE, related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"
    
    class Meta:
        ordering = ('timestamp',)
        verbose_name = 'メッセージリスト'
        verbose_name_plural = 'メッセージリスト'