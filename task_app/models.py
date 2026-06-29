from django.db import models
from django.contrib.auth.models import User

import qrcode
from qrcode.image.pil import PilImage
from io import BytesIO
from django.core.files import File

# Create your models here.
stat_ch=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=stat_ch, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    barcode = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # تحقق أولاً إن كان الحقل فارغاً لتوليد الباركود حتى لا يتكرر التوليد عند كل تعديل
        if not self.barcode:
            # منطق توليد الباركود الخاص بك هنا
            qr = qrcode.QRCode(version=1, box_size=5, border=5)
            qr.add_data(f"Task: {self.title}")
            qr.add_data(f"Description: {self.description}")
            qr.add_data(f"Status: {self.status}")
            qr.add_data(f"Created At: {self.created_at}")
            qr.add_data(f"Updated At: {self.updated_at}")
            qr.add_data(f"Date Completed: {self.date_completed}")
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='png')
            
            # حفظ الملف في حقل الباركود
            self.barcode.save(f"qr_{self.title}.png", File(buffer), save=False)
            
        # استدعاء دالة الحفظ الأصلية بالطريقة الصحيحة
        super(Task, self).save(*args, **kwargs)
    def __str__(self):
        return self.title