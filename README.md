# 🤖 iTechAcademy (RaBola) Edu Bot

iTechAcademy (RaBola) o'quv markazi uchun rasmiy Telegram boti. Loyiha zamonaviy modulli mikroxizmat (Microservice/Clean Architecture) tamoyillari asosida qayta ishlab chiqilgan, xatolar tuzatilgan va barqarorlik (resilience) ta'minlangan.

---

## 🚀 Loyihadagi Asosiy Muammolar va Ularning Yechimlari

Oldingi versiyada serverda botning o'chib qolishi yoki javob bermay qolishining quyidagi asosiy sabablari aniqlandi va to'liq bartaraf etildi:

1. **Botning qotib qolishi (Testing Handleri xatosi):**
   - *Muammo:* Eng yuqori o'rinda `@bot.message_handler(func=lambda message: True)` handleri turgani va faqat `/start` hamda `/admin` ni tekshirib, qolgan barcha xabarlarni yutib yuborishi natijasida foydalanuvchi menyudagi tugmalarni bosganda bot javob bermay qolardi.
   - *Yechim:* Barcha handlerlar mas'uliyatiga ko'ra ajratildi (`start`, `language`, `menu`, `courses`, `registration`, `admin`) va to'g'ri prioritet bilan ro'yxatdan o'tkazildi.

2. **Serverda bot o'chib qolishi (Startup Crash & Polling Failures):**
   - *Muammo:* Modul darajasida `send_status_update()` chaqirilgan bo'lib, `CANAL_ID` xato bo'lsa yoki bot kanalda bo'lmasa dastur birinchi soniyadayoq qulardi. Shuningdek, Telegram API dagi `ReadTimeout` yoki tarmoq uzilishlarida `bot.polling()` to'xtab qolardi.
   - *Yechim:* Polling **Supervisor Auto-Reconnect Loop** bilan o'raldi. Tarmoq uzilsa ham bot qulab tushmaydi, 5 soniyadan so'ng avtomatik qayta ulanadi. Scheduler xizmati esa xatoliklarni xavfsiz ushlaydigan alohida fonda ishlaydi.

3. **Tilning DB da saqlanmasligi (Memory-Only State):**
   - *Muammo:* Foydalanuvchi tili faqat RAM da (`user_langs = {}`) saqlangani sababli bot qayta ishga tushganda til yo'qolib ketardi.
   - *Yechim:* `users` jadvaliga `language` ustuni qo'shildi. Foydalanuvchi til tanlaganda to'g'ridan-to'g'ri PostgreSQL bazasida saqlanadi va keshlanadi. "Tilni o'zgartirish 🔄" orqali istalgan payt yangilash mumkin.

4. **Ma'lumotlar bazasi uzilishi (Connection Dropping):**
   - *Muammo:* Yagona `psycopg2` aloqasi ishlatilgan, PostgreSQL idle aloqani uzganda bot qulardi.
   - *Yechim:* `psycopg2.pool.ThreadedConnectionPool` asosida Connection Manager yaratildi va avtomatik qayta ulanish (auto-reconnect) ta'minlandi.

5. **Race Condition va KeyError (Global Dictionary):**
   - *Muammo:* `personal_details = {}` global lug'at bo'lib, birdaniga bir necha foydalanuvchi yozsa ma'lumotlar almashib ketardi yoki KeyError berardi.
   - *Yechim:* Har bir `chat_id` uchun thread-safe `StateManager` (FSM) joriy qilindi.

6. **Docker va .env nomutanosibligi:**
   - *Muammo:* `requirements.txt` UTF-16LE da bo'lganligi sababli pip da xatolar yuzaga kelardi. Dockerfile esa keshlanmasdi.
   - *Yechim:* `requirements.txt` toza UTF-8 ga o'tkazildi, `python:3.11-slim` asosidagi optimallashtirilgan `Dockerfile` va to'g'ri networking ega `docker-compose.yml` yaratildi.

---

## 🏗 Yangi Loyiha Arxitekturasi (Microservice / Clean Architecture)

```
itechacademy_edu_bot/
├── app/
│   ├── core/
│   │   ├── config.py         # Type-safe, moslashuvchan ENV konfiguratsiyasi
│   │   └── logger.py         # Markazlashgan strukturalangan loglash
│   ├── database/
│   │   ├── connection.py     # Thread-safe Connection Pool & Auto-reconnect
│   │   ├── migrations.py     # Avtomatik jadvallarni yaratish va yangilash
│   │   └── repositories/
│   │       ├── user_repo.py  # User saqlash, tilni olish va yangilash (DB)
│   │       └── app_repo.py   # O'quvchilar arizalarini bazada saqlash
│   ├── services/
│   │   ├── user_service.py   # Foydalanuvchilar va til keshi servisi
│   │   ├── lead_service.py   # Ariza qabul qilish (DB + Telegram kanal)
│   │   ├── broadcast_service.py # Xavfsiz xabar tarqatish (Rate Limiting)
│   │   └── scheduler_service.py # Xavfsiz status yuborish
│   ├── bot/
│   │   ├── bot_instance.py   # TeleBot instansiyasi
│   │   ├── state.py          # Har bir user uchun alohida FSM StateManager
│   │   ├── keyboards/
│   │   │   ├── reply.py      # Reply klaviaturalar (kurslar, menyu, telefon)
│   │   │   └── inline.py     # Inline klaviaturalar (tillar, tasdiqlash)
│   │   └── handlers/
│   │       ├── start_handler.py        # /start va /help
│   │       ├── language_handler.py     # Tilni o'zgartirish va DB da saqlash
│   │       ├── menu_handler.py         # Asosiy bo'limlar navigatsiyasi
│   │       ├── course_handler.py       # Kurslar tavsifi va tanlash
│   │       ├── registration_handler.py # Ro'yxatdan o'tish (Ism, Telefon, Ariza)
│   │       └── admin_handler.py        # Admin panel, statistika, broadcast
│   └── locales/
│       ├── texts.py          # Ko'p tilli barcha matnlar (uz, ru, en)
│       └── keyboard_texts.py # Tugma matnlari
├── bot.py                    # Boshlang'ich nuqta (Supervisor Polling Loop)
├── Dockerfile                # Optimallashtirilgan Dockerfile
├── docker-compose.yml        # PostgreSQL va Bot servislar
├── requirements.txt          # Kerakli Python kutubxonalari
└── .env.example              # Muhit o'zgaruvchilari namunasi
```

---

## ⚙️ O'rnatish va Ishga Tushirish

### 1. `.env` faylini sozlash
`.env.example` dan nusxa olib `.env` yarating:
```bash
cp .env.example .env
```
Va o'zgaruvchilarni to'ldiring:
```ini
TOKEN=your_bot_token_from_botfather
ADMIN_ID=123456789,987654321
CANAL_ID=-1001234567890

PGHOST=db
PGPORT=5432
PGUSER=postgres
PGPASSWORD=your_secure_password
PGDATABASE=webcervice
```

### 2. Docker Compose orqali ishga tushirish (Tavsiya etiladi)
Loyiha papkasida quyidagi buyruqni bering:
```bash
docker compose up -d --build
```

Konteynerlar holatini tekshirish:
```bash
docker compose ps
```

Bot loglarini jonli kuzatish:
```bash
docker compose logs -f bot
```

### 3. Lokal muhitda (Python venv) ishga tushirish:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

---

## 🎯 Bot Imkoniyatlari

- 🌐 **Ko'p tilli interfeys (Uzbek, Russian, English):**
  - Foydalanuvchi tanlagan til doimiy ravishda PostgreSQL ma'lumotlar bazasida saqlanadi.
  - "Tilni o'zgartirish 🔄" tugmasi orqali xohlagan payt tilni almashtirish mumkin.
- 📚 **Kurslar katalogi:**
  - Barcha kurslar bo'yicha batafsil ma'lumotlar va qulay ro'yxatdan o'tish.
- 📝 **Ariza qabul qilish tizimi:**
  - Foydalanuvchidan ism va telefon raqami so'raladi (Tugma orqali yoki qo'lda).
  - Telefon raqam avtomatik tozalanadi va to'g'riligi tekshiriladi.
  - Ma'lumotlar tasdiqlangach, ma'lumotlar bazasiga (`applications` jadvali) yoziladi va admin kanaliga yuboriladi.
- 🛠 **Admin Paneli:**
  - Foydalanuvchilar va qabul qilingan arizalar soni bo'yicha jonli statistika.
  - Barcha foydalanuvchilarga xavfsiz yangilik tarqatish (Broadcast) - Telegram flood-limit hisobga olingan.
