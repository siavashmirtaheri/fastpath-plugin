# Short posts you can copy

## English (Reddit / Discord / X)

**fastpath is now in the Hermes Agent plugin catalog.** It compresses oversized
tool results before they enter the model context: first 60% + last 40% with an
explicit omission marker (default limit 12,000 chars). An 80k file read sends
~85% fewer characters. Local-only, fail-open, MIT, 12 tests.

```bash
hermes plugins install fastpath
hermes plugins enable fastpath
/fastpath
```

Repo: https://github.com/siavashmirtaheri/fastpath-plugin
Marketplace: https://hermes-agent.nousresearch.com/marketplace/fastpath
Backed by Metadigi: https://metadigi.ir

Also published `fresh-code`, a skill that makes Hermes verify installed
dependency versions and current docs before writing complete, tested code:
https://github.com/siavashmirtaheri/hermes-fresh-code

## English (short X post)

New Hermes plugin: fastpath compresses huge tool results to head 60% + tail 40% with an omission marker — ~85% fewer chars on an 80k file read. Local-only, fail-open, MIT. `hermes plugins install fastpath` → https://github.com/siavashmirtaheri/fastpath-plugin

## فارسی (برای انجمنها)

پلاگین **fastpath** حالا در کاتالوگ رسمی Hermes Agent موجود است. نتایج خیلی بزرگ ابزارها را قبل از ورود به context مدل فشرده میکند: ۶۰٪ ابتدا + ۴۰٪ انتها همراه با علامت صریح حذفشده (پیشفرض ۱۲٬۰۰۰ کاراکتر). برای یک فایل ۸۰ هزار کاراکتری حدود ۸۵٪ کاهش ارسال به مدل. کاملاً محلی، fail-open، MIT و با ۱۲ تست.

نصب:

```bash
hermes plugins install fastpath
hermes plugins enable fastpath
/fastpath
```

لینک: https://github.com/siavashmirtaheri/fastpath-plugin

همچنین Skill جدایی به نام **fresh-code** منتشر کردم که هرمس را قبل از نوشتن کد، به بررسی نسخهٔ نصبشده و مستندات روز وادار میکند:
https://github.com/siavashmirtaheri/hermes-fresh-code
