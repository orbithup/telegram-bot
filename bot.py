import imaplib
import email
from email.header import decode_header
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re

# بيانات الإيميل
EMAIL_USER = "orbithup.1@outlook.sa"
EMAIL_PASS = "jmsjbitartdmisoe"
IMAP_SERVER = "outlook.office365.com"

# توكن البوت
BOT_TOKEN = "8457375862:AAH6EUM0qn6PsXE7gtC1qlPx1cUoMMFYlis"

# دالة لجلب آخر كود من الإيميل
def get_latest_code():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        _, search_data = mail.search(None, "ALL")
        mail_ids = search_data[0].split()
        latest_email_id = mail_ids[-1]
        _, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # قراءة المحتوى
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        # البحث عن كود (أرقام فقط)
        code_match = re.search(r"\b\d{4,8}\b", body)
        if code_match:
            return code_match.group(0)
        return "ما لقيت كود."
    except Exception as e:
        return f"خطأ: {e}"

# أمر /code في البوت
async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = get_latest_code()
    await update.message.reply_text(f"أحدث كود هو: {code}")

# تشغيل البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("code", code_command))

print("البوت شغال...")
app.run_polling()