from django.contrib import admin
from .models import ChatMessage

# admin.site.register(ChatMessage)
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    # অ্যাডমিন টেবিল ভিউতে কোন কোন কলাম দেখাবে
    list_display = ('id_short', 'pickup_request_short', 'sender', 'message_excerpt', 'is_read', 'created_at')
    
    # ডানপাশে ফিল্টার করার অপশন (যেমন: ডেট বা রিড স্ট্যাটাস অনুযায়ী)
    list_filter = ('is_read', 'created_at', 'sender')
    
    # সার্চ বক্সের মাধ্যমে খোঁজার সুবিধা
    search_fields = ('message', 'sender__email', 'pickup_request__id')
    
    # শুধু রিড-অনলি করে রাখার জন্য (চাইলে অ্যাডমিন থেকে মেসেজ এডিট বন্ধ রাখতে পারেন)
    readonly_fields = ('created_at',)

    # কাস্টম মেথড: আইডি ছোট করে দেখানোর জন্য
    def id_short(self, obj):
        return str(obj.id)[:8] + "..."
    id_short.short_description = "Message ID"

    # কাস্টম মেথড: পিকআপ আইডি ছোট করে দেখানোর জন্য
    def pickup_request_short(self, obj):
        return str(obj.pickup_request.id)[:8] + "..."
    pickup_request_short.short_description = "Pickup ID"

    # কাস্টম মেথড: মেসেজ অনেক বড় হলে প্রথম ৩০টা ক্যারেক্টার দেখাবে
    def message_excerpt(self, obj):
        return obj.message[:30] + "..." if len(obj.message) > 30 else obj.message
    message_excerpt.short_description = "Message"