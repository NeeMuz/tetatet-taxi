"""Переводы интерфейса: ru / uk / en."""

LANGUAGES = [
    ('ru', 'Русский'),
    ('uk', 'Українська'),
    ('en', 'English'),
]

LANGUAGE_CODES = {code for code, _ in LANGUAGES}

TRANSLATIONS = {
    # ── Navigation ──────────────────────────────────────────────────────────
    'nav.home': {'ru': 'Главная', 'uk': 'Головна', 'en': 'Home'},
    'nav.main': {'ru': 'Навигация', 'uk': 'Навігація', 'en': 'Navigation'},
    'nav.orders': {'ru': 'Поездки', 'uk': 'Поїздки', 'en': 'Rides'},
    'nav.history': {'ru': 'История', 'uk': 'Історія', 'en': 'History'},
    'nav.login': {'ru': 'Войти', 'uk': 'Увійти', 'en': 'Log in'},
    'nav.register': {'ru': 'Регистрация', 'uk': 'Реєстрація', 'en': 'Sign up'},
    'nav.logout': {'ru': 'Выйти', 'uk': 'Вийти', 'en': 'Log out'},
    'nav.profile': {'ru': 'Профиль', 'uk': 'Профіль', 'en': 'Profile'},

    # ── Language switcher ─────────────────────────────────────────────────────
    'lang.title': {'ru': 'Язык', 'uk': 'Мова', 'en': 'Language'},
    'lang.sub': {
        'ru': 'Выберите язык интерфейса приложения',
        'uk': 'Оберіть мову інтерфейсу застосунку',
        'en': 'Choose the app interface language',
    },
    'lang.ru_short': {'ru': 'RU', 'uk': 'RU', 'en': 'RU'},
    'lang.uk_short': {'ru': 'UA', 'uk': 'UA', 'en': 'UA'},
    'lang.en_short': {'ru': 'EN', 'uk': 'EN', 'en': 'EN'},

    # ── Profile ─────────────────────────────────────────────────────────────
    'profile.title': {'ru': 'Профиль', 'uk': 'Профіль', 'en': 'Profile'},
    'profile.sub': {'ru': 'Личные данные и фото', 'uk': 'Особисті дані та фото', 'en': 'Personal info and photo'},
    'profile.security': {'ru': 'Безопасность', 'uk': 'Безпека', 'en': 'Security'},
    'profile.security_sub': {'ru': 'Пароль и вход', 'uk': 'Пароль і вхід', 'en': 'Password and sign-in'},
    'profile.security_text': {
        'ru': 'Смена пароля — на отдельной странице, чтобы не путать с данными профиля.',
        'uk': 'Зміна пароля — на окремій сторінці, щоб не плутати з даними профілю.',
        'en': 'Change your password on a separate page, away from profile details.',
    },
    'profile.change_password': {'ru': 'Сменить пароль →', 'uk': 'Змінити пароль →', 'en': 'Change password →'},
    'profile.save': {'ru': 'Сохранить профиль', 'uk': 'Зберегти профіль', 'en': 'Save profile'},
    'profile.phone_required': {
        'ru': 'Добавьте телефон — без него нельзя заказать такси',
        'uk': 'Додайте телефон — без нього не можна замовити таксі',
        'en': 'Add a phone number — required to book a ride',
    },
    'profile.phone_hint': {
        'ru': 'Обязателен для заказа такси',
        'uk': "Обов'язковий для замовлення таксі",
        'en': 'Required to book a ride',
    },
    'profile.avatar_label': {'ru': 'Фото профиля', 'uk': 'Фото профілю', 'en': 'Profile photo'},
    'profile.avatar_choose': {'ru': 'Выбрать фото', 'uk': 'Обрати фото', 'en': 'Choose photo'},
    'profile.avatar_hint': {'ru': 'JPG, PNG — до 5 МБ', 'uk': 'JPG, PNG — до 5 МБ', 'en': 'JPG, PNG — up to 5 MB'},
    'profile.avatar_preview': {'ru': 'Превью', 'uk': 'Попередній перегляд', 'en': 'Preview'},
    'profile.first_name': {'ru': 'Имя *', 'uk': "Ім'я *", 'en': 'First name *'},
    'profile.last_name': {'ru': 'Фамилия', 'uk': 'Прізвище', 'en': 'Last name'},
    'profile.email': {'ru': 'Email *', 'uk': 'Email *', 'en': 'Email *'},
    'profile.phone': {'ru': 'Телефон *', 'uk': 'Телефон *', 'en': 'Phone *'},
    'profile.cards_title': {'ru': 'Мои карты', 'uk': 'Мої картки', 'en': 'My cards'},
    'profile.cards_sub': {
        'ru': 'Выберите основную карту для оплаты поездок',
        'uk': 'Оберіть основну картку для оплати поїздок',
        'en': 'Choose your default card for ride payments',
    },
    'profile.default_badge': {'ru': 'По умолчанию', 'uk': 'За замовчуванням', 'en': 'Default'},
    'profile.edit_card': {'ru': 'Редактировать', 'uk': 'Редагувати', 'en': 'Edit'},
    'profile.make_default': {'ru': 'Сделать основной', 'uk': 'Зробити основною', 'en': 'Set as default'},
    'profile.delete_card': {'ru': 'Удалить', 'uk': 'Видалити', 'en': 'Delete'},
    'profile.delete_confirm': {'ru': 'Удалить точно?', 'uk': 'Видалити точно?', 'en': 'Delete for sure?'},
    'profile.cancel': {'ru': 'Отмена', 'uk': 'Скасувати', 'en': 'Cancel'},
    'profile.no_cards': {'ru': 'Нет сохранённых карт', 'uk': 'Немає збережених карток', 'en': 'No saved cards'},
    'profile.no_cards_hint': {
        'ru': 'Добавьте карту в форме справа',
        'uk': 'Додайте картку у формі праворуч',
        'en': 'Add a card using the form on the right',
    },
    'profile.add_card_title': {'ru': 'Добавить карту', 'uk': 'Додати картку', 'en': 'Add card'},
    'profile.add_card_sub': {
        'ru': 'Номер, CVV, срок и имя — как на банковской карте',
        'uk': 'Номер, CVV, термін і ім\'я — як на банківській картці',
        'en': 'Number, CVV, expiry and name — as on your bank card',
    },
    'profile.card_number': {'ru': 'Номер карты', 'uk': 'Номер картки', 'en': 'Card number'},
    'profile.card_expiry': {'ru': 'Срок действия', 'uk': 'Термін дії', 'en': 'Expiry date'},
    'profile.card_cvv': {'ru': 'CVV', 'uk': 'CVV', 'en': 'CVV'},
    'profile.card_holder': {'ru': 'Имя на карте', 'uk': "Ім'я на картці", 'en': 'Name on card'},
    'profile.card_brand_title': {'ru': 'Тип карты', 'uk': 'Тип картки', 'en': 'Card type'},
    'profile.card_brand_auto': {
        'ru': 'Тип карты определяется автоматически',
        'uk': 'Тип картки визначається автоматично',
        'en': 'Card type is detected automatically',
    },
    'profile.set_default': {
        'ru': 'Сделать картой по умолчанию',
        'uk': 'Зробити карткою за замовчуванням',
        'en': 'Set as default card',
    },
    'profile.add_card_btn': {'ru': 'Добавить карту', 'uk': 'Додати картку', 'en': 'Add card'},
    'profile.save_card': {'ru': 'Сохранить', 'uk': 'Зберегти', 'en': 'Save'},

    # ── Dispatch ──────────────────────────────────────────────────────────────
    'dispatch.badge': {'ru': 'Диспетчерская', 'uk': 'Диспетчерська', 'en': 'Dispatch'},
    'dispatch.online': {'ru': 'Онлайн', 'uk': 'Онлайн', 'en': 'Online'},
    'dispatch.panel_title': {'ru': 'Панель заказов', 'uk': 'Панель замовлень', 'en': 'Orders panel'},
    'dispatch.panel_sub': {
        'ru': 'Всего заказов:',
        'uk': 'Усього замовлень:',
        'en': 'Total orders:',
    },
    'dispatch.sync': {
        'ru': 'синхронизация с админкой',
        'uk': 'синхронізація з адмінкою',
        'en': 'synced with admin',
    },
    'dispatch.search': {
        'ru': 'Поиск по №, имени, адресу...',
        'uk': "Пошук за №, ім'ям, адресою...",
        'en': 'Search by #, name, address...',
    },
    'dispatch.refresh': {'ru': 'Обновить', 'uk': 'Оновити', 'en': 'Refresh'},

    'dispatch.stat.new': {'ru': 'Входящие', 'uk': 'Вхідні', 'en': 'Incoming'},
    'dispatch.stat.accepted': {'ru': 'Едут', 'uk': 'Їдуть', 'en': 'En route'},
    'dispatch.stat.arrived': {'ru': 'На месте', 'uk': 'На місці', 'en': 'Arrived'},
    'dispatch.stat.on_way': {'ru': 'В пути', 'uk': 'У дорозі', 'en': 'On trip'},
    'dispatch.stat.done': {'ru': 'Завершены', 'uk': 'Завершені', 'en': 'Completed'},
    'dispatch.stat.cancelled': {'ru': 'Отменены', 'uk': 'Скасовані', 'en': 'Cancelled'},

    'dispatch.col.new': {'ru': 'Входящие', 'uk': 'Вхідні', 'en': 'Incoming'},
    'dispatch.col.accepted': {'ru': 'Едут к клиенту', 'uk': 'Їдуть до клієнта', 'en': 'Driving to client'},
    'dispatch.col.arrived': {'ru': 'На месте', 'uk': 'На місці', 'en': 'At pickup'},
    'dispatch.col.on_way': {'ru': 'В пути', 'uk': 'У дорозі', 'en': 'On trip'},
    'dispatch.col.done': {'ru': 'Завершены', 'uk': 'Завершені', 'en': 'Completed'},
    'dispatch.col.cancelled': {'ru': 'Отменены', 'uk': 'Скасовані', 'en': 'Cancelled'},
    'dispatch.empty': {'ru': 'Нет заказов', 'uk': 'Немає замовлень', 'en': 'No orders'},

    'dispatch.alert.select_driver': {'ru': 'Выберите водителя', 'uk': 'Оберіть водія', 'en': 'Select a driver'},
    'dispatch.btn.select_driver': {'ru': 'Выберите водителя', 'uk': 'Оберіть водія', 'en': 'Select driver'},
    'dispatch.btn.assign': {'ru': 'Назначить водителя', 'uk': 'Призначити водія', 'en': 'Assign driver'},
    'dispatch.btn.reject': {'ru': 'Отклонить', 'uk': 'Відхилити', 'en': 'Reject'},
    'dispatch.btn.arrived': {'ru': 'На месте', 'uk': 'На місці', 'en': 'Arrived'},
    'dispatch.btn.cancel': {'ru': 'Отменить', 'uk': 'Скасувати', 'en': 'Cancel'},
    'dispatch.btn.start_trip': {'ru': 'Поездка началась', 'uk': 'Поїздка розпочалась', 'en': 'Trip started'},
    'dispatch.btn.complete': {'ru': 'Завершить поездку', 'uk': 'Завершити поїздку', 'en': 'Complete trip'},
    'dispatch.status.done': {'ru': 'Завершён', 'uk': 'Завершено', 'en': 'Completed'},
    'dispatch.status.cancelled': {'ru': 'Отменён', 'uk': 'Скасовано', 'en': 'Cancelled'},
    'dispatch.status.arrived': {'ru': 'На месте', 'uk': 'На місці', 'en': 'Arrived'},

    'dispatch.login.title': {'ru': 'Диспетчерская', 'uk': 'Диспетчерська', 'en': 'Dispatch'},
    'dispatch.login.sub': {
        'ru': 'Вход для операторов — отдельно от приложения пассажиров',
        'uk': 'Вхід для операторів — окремо від застосунку пасажирів',
        'en': 'Operator sign-in — separate from the passenger app',
    },
    'dispatch.login.submit': {'ru': 'Войти в диспетчерскую', 'uk': 'Увійти в диспетчерську', 'en': 'Enter dispatch panel'},
    'dispatch.login.passenger': {'ru': 'Вы пассажир?', 'uk': 'Ви пасажир?', 'en': 'Are you a passenger?'},
    'dispatch.login.passenger_link': {'ru': 'Войти в приложение', 'uk': 'Увійти в застосунок', 'en': 'Open passenger app'},

    'dispatch.error.script_not_loaded': {
        'ru': 'Скрипт не загружен. Нажмите Ctrl+F5.',
        'uk': 'Скрипт не завантажено. Натисніть Ctrl+F5.',
        'en': 'Script not loaded. Press Ctrl+F5.',
    },
    'dispatch.error.action_failed': {
        'ru': 'Ошибка при выполнении действия',
        'uk': 'Помилка під час виконання дії',
        'en': 'Error performing action',
    },
    'dispatch.error.cancel_confirm': {
        'ru': 'Отменить заказ №{id}?',
        'uk': 'Скасувати замовлення №{id}?',
        'en': 'Cancel order #{id}?',
    },
    'dispatch.error.reload_failed': {
        'ru': 'Не удалось обновить (ошибка {status}). Показаны данные с сервера.',
        'uk': 'Не вдалося оновити (помилка {status}). Показані дані з сервера.',
        'en': 'Could not refresh (error {status}). Showing server data.',
    },
    'dispatch.error.network': {
        'ru': 'Ошибка сети. Показаны данные с сервера.',
        'uk': 'Помилка мережі. Показані дані з сервера.',
        'en': 'Network error. Showing server data.',
    },

    # ── Order status labels ───────────────────────────────────────────────────
    'status.new': {'ru': 'Ожидает водителя', 'uk': 'Очікує водія', 'en': 'Waiting for driver'},
    'status.accepted': {'ru': 'Такси едет к вам', 'uk': 'Таксі їде до вас', 'en': 'Taxi is on the way'},
    'status.arrived': {'ru': 'Такси на месте', 'uk': 'Таксі на місці', 'en': 'Taxi has arrived'},
    'status.on_way': {'ru': 'В пути к пункту назначения', 'uk': 'У дорозі до пункту призначення', 'en': 'Heading to destination'},
    'status.done': {'ru': 'Поездка завершена', 'uk': 'Поїздку завершено', 'en': 'Trip completed'},
    'status.cancelled': {'ru': 'Отменён', 'uk': 'Скасовано', 'en': 'Cancelled'},

    # ── Common ────────────────────────────────────────────────────────────────
    'common.show': {'ru': 'Показать', 'uk': 'Показати', 'en': 'Show'},
    'common.hide': {'ru': 'Скрыть', 'uk': 'Приховати', 'en': 'Hide'},
    'common.password': {'ru': 'Пароль', 'uk': 'Пароль', 'en': 'Password'},
    'common.error': {'ru': 'Ошибка', 'uk': 'Помилка', 'en': 'Error'},
    'common.cancel_slide': {'ru': 'Сдвиньте для отмены', 'uk': 'Проведіть для скасування', 'en': 'Slide to cancel'},
    'common.cancel_done': {'ru': 'Отменяем...', 'uk': 'Скасовуємо...', 'en': 'Cancelling...'},
    'common.back_profile': {'ru': '← Назад в профиль', 'uk': '← Назад до профілю', 'en': '← Back to profile'},
    'common.back_home': {'ru': '← Главная', 'uk': '← Головна', 'en': '← Home'},
    'common.email': {'ru': 'Email', 'uk': 'Email', 'en': 'Email'},
    'common.first_name': {'ru': 'Имя', 'uk': "Ім'я", 'en': 'First name'},
    'common.last_name': {'ru': 'Фамилия', 'uk': 'Прізвище', 'en': 'Last name'},
    'common.phone': {'ru': 'Телефон', 'uk': 'Телефон', 'en': 'Phone'},
    'common.online': {'ru': 'Онлайн', 'uk': 'Онлайн', 'en': 'Online'},
    'common.passenger': {'ru': 'Пассажир', 'uk': 'Пасажир', 'en': 'Passenger'},
    'common.open': {'ru': 'Открыть →', 'uk': 'Відкрити →', 'en': 'Open →'},
    'common.order': {'ru': 'Заказать →', 'uk': 'Замовити →', 'en': 'Book →'},
    'common.profile_link': {'ru': 'Профиль →', 'uk': 'Профіль →', 'en': 'Profile →'},
    'common.sending': {'ru': 'Отправляем...', 'uk': 'Надсилаємо...', 'en': 'Sending...'},
    'common.booking': {'ru': 'Оформляем...', 'uk': 'Оформлюємо...', 'en': 'Booking...'},
    'common.tariff': {'ru': 'Тариф:', 'uk': 'Тариф:', 'en': 'Tariff:'},
    'common.dash': {'ru': '—', 'uk': '—', 'en': '—'},

    # ── Landing ───────────────────────────────────────────────────────────────
    'landing.title': {'ru': 'Tetatet — Такси', 'uk': 'Tetatet — Таксі', 'en': 'Tetatet — Taxi'},
    'landing.status': {'ru': 'Сервис доступен · Берлин', 'uk': 'Сервіс доступний · Берлін', 'en': 'Service available · Berlin'},
    'landing.dispatch_banner': {
        'ru': 'Вы вошли как диспетчер — это страница для пассажиров.',
        'uk': 'Ви увійшли як диспетчер — це сторінка для пасажирів.',
        'en': 'You are signed in as a dispatcher — this page is for passengers.',
    },
    'landing.dispatch_link': {'ru': 'В диспетчерскую →', 'uk': 'У диспетчерську →', 'en': 'Go to dispatch →'},
    'landing.tag': {'ru': 'Сервис такси', 'uk': 'Сервіс таксі', 'en': 'Taxi service'},
    'landing.heading': {'ru': 'Закажите', 'uk': 'Замовте', 'en': 'Book a'},
    'landing.heading_accent': {'ru': 'поездку', 'uk': 'поїздку', 'en': 'ride'},
    'landing.desc': {
        'ru': 'Укажите маршрут, выберите тариф и оформите заказ за минуту. История поездок и статус в реальном времени — в личном кабинете.',
        'uk': 'Вкажіть маршрут, оберіть тариф і оформіть замовлення за хвилину. Історія поїздок і статус у реальному часі — в особистому кабінеті.',
        'en': 'Set your route, pick a tariff, and book in under a minute. Trip history and live status — in your account.',
    },
    'landing.cta_book': {'ru': 'Заказать такси', 'uk': 'Замовити таксі', 'en': 'Book a ride'},
    'landing.cta_trips': {'ru': 'Мои поездки', 'uk': 'Мої поїздки', 'en': 'My rides'},
    'landing.cta_login_passenger': {'ru': 'Войти как пассажир', 'uk': 'Увійти як пасажир', 'en': 'Sign in as passenger'},
    'landing.cta_register': {'ru': 'Регистрация', 'uk': 'Реєстрація', 'en': 'Sign up'},
    'landing.cta_start': {'ru': 'Начать', 'uk': 'Почати', 'en': 'Get started'},
    'landing.cta_login': {'ru': 'Войти', 'uk': 'Увійти', 'en': 'Log in'},
    'landing.pill_route': {'ru': 'Маршрут за минуту', 'uk': 'Маршрут за хвилину', 'en': 'Route in a minute'},
    'landing.pill_tariffs': {'ru': '6 тарифов', 'uk': '6 тарифів', 'en': '6 tariffs'},
    'landing.pill_live': {'ru': 'Live-статус', 'uk': 'Live-статус', 'en': 'Live status'},
    'landing.pill_card': {'ru': 'Оплата картой', 'uk': 'Оплата карткою', 'en': 'Card payment'},
    'landing.stat_tariffs': {'ru': 'Тарифов', 'uk': 'Тарифів', 'en': 'Tariffs'},
    'landing.stat_online': {'ru': 'Заказ онлайн', 'uk': 'Замовлення онлайн', 'en': 'Online booking'},
    'landing.stat_updates': {'ru': 'Обновления', 'uk': 'Оновлення', 'en': 'Updates'},

    # ── Auth: login ───────────────────────────────────────────────────────────
    'auth.login.title': {'ru': 'Вход', 'uk': 'Вхід', 'en': 'Log in'},
    'auth.login.sub': {'ru': 'Введите email и пароль', 'uk': 'Введіть email і пароль', 'en': 'Enter your email and password'},
    'auth.login.submit': {'ru': 'Войти', 'uk': 'Увійти', 'en': 'Log in'},
    'auth.login.forgot': {'ru': 'Забыли пароль?', 'uk': 'Забули пароль?', 'en': 'Forgot password?'},
    'auth.login.no_account': {'ru': 'Нет аккаунта?', 'uk': 'Немає акаунта?', 'en': 'No account?'},
    'auth.login.register_link': {'ru': 'Зарегистрироваться', 'uk': 'Зареєструватися', 'en': 'Sign up'},
    'auth.login.visual_title': {
        'ru': 'Добро пожаловать\nв Tetatet',
        'uk': 'Ласкаво просимо\nдо Tetatet',
        'en': 'Welcome\nto Tetatet',
    },
    'auth.login.visual_sub': {
        'ru': 'Такси по Германии — быстро и удобно',
        'uk': 'Таксі по Німеччині — швидко й зручно',
        'en': 'Taxi across Germany — fast and convenient',
    },

    # ── Auth: register ────────────────────────────────────────────────────────
    'auth.register.title': {'ru': 'Регистрация', 'uk': 'Реєстрація', 'en': 'Sign up'},
    'auth.register.sub': {
        'ru': 'Заполните данные для создания аккаунта',
        'uk': 'Заповніть дані для створення акаунта',
        'en': 'Fill in your details to create an account',
    },
    'auth.register.submit': {'ru': 'Создать аккаунт', 'uk': 'Створити акаунт', 'en': 'Create account'},
    'auth.register.has_account': {'ru': 'Уже есть аккаунт?', 'uk': 'Вже є акаунт?', 'en': 'Already have an account?'},
    'auth.register.login_link': {'ru': 'Войти', 'uk': 'Увійти', 'en': 'Log in'},
    'auth.register.visual_title': {
        'ru': 'Поехали!',
        'uk': 'Поїхали!',
        'en': "Let's go",
    },
    'auth.register.visual_sub': {
        'ru': 'Поездки по Германии — создайте аккаунт',
        'uk': 'Поїздки по Німеччині — створіть акаунт',
        'en': 'Rides across Germany — create your account',
    },
    'auth.register.placeholder_first': {'ru': 'Иван', 'uk': 'Іван', 'en': 'John'},
    'auth.register.placeholder_last': {'ru': 'Иванов', 'uk': 'Іванов', 'en': 'Smith'},

    # ── Auth: forgot password ─────────────────────────────────────────────────
    'auth.forgot.title': {'ru': 'Восстановление пароля', 'uk': 'Відновлення пароля', 'en': 'Password recovery'},
    'auth.forgot.sub': {
        'ru': 'Введите ваш email — мы отправим ссылку для сброса пароля.',
        'uk': 'Введіть ваш email — ми надішлемо посилання для скидання пароля.',
        'en': 'Enter your email — we will send a password reset link.',
    },
    'auth.forgot.email_placeholder': {'ru': 'Ваш email', 'uk': 'Ваш email', 'en': 'Your email'},
    'auth.forgot.submit': {'ru': 'Отправить ссылку', 'uk': 'Надіслати посилання', 'en': 'Send link'},
    'auth.forgot.back_login': {'ru': 'Вернуться ко входу', 'uk': 'Повернутися до входу', 'en': 'Back to log in'},

    # ── Auth: change password ─────────────────────────────────────────────────
    'auth.password.title': {'ru': 'Смена пароля', 'uk': 'Зміна пароля', 'en': 'Change password'},
    'auth.password.sub': {
        'ru': 'Введите текущий и новый пароль',
        'uk': 'Введіть поточний і новий пароль',
        'en': 'Enter your current and new password',
    },
    'auth.password.current': {'ru': 'Текущий пароль', 'uk': 'Поточний пароль', 'en': 'Current password'},
    'auth.password.new': {'ru': 'Новый пароль', 'uk': 'Новий пароль', 'en': 'New password'},
    'auth.password.new2': {'ru': 'Повторите новый пароль', 'uk': 'Повторіть новий пароль', 'en': 'Repeat new password'},
    'auth.password.submit': {'ru': 'Обновить пароль', 'uk': 'Оновити пароль', 'en': 'Update password'},

    # ── Home ──────────────────────────────────────────────────────────────────
    'home.title': {'ru': 'Главная', 'uk': 'Головна', 'en': 'Home'},
    'home.greeting_default': {'ru': 'Добрый день', 'uk': 'Добрий день', 'en': 'Good afternoon'},
    'home.heading': {'ru': '{name}, куда поедем?', 'uk': '{name}, куди поїдемо?', 'en': '{name}, where to?'},
    'home.active_trip': {'ru': 'Поездка №{id} — {status}', 'uk': 'Поїздка №{id} — {status}', 'en': 'Ride #{id} — {status}'},
    'home.where_to': {'ru': 'Куда едем?', 'uk': 'Куди їдемо?', 'en': 'Where to?'},
    'home.phone_alert': {
        'ru': 'Добавьте телефон — без него заказ не оформить.',
        'uk': 'Додайте телефон — без нього замовлення не оформити.',
        'en': 'Add a phone number — required to place an order.',
    },
    'home.chip.airport': {'ru': 'Аэропорт BER', 'uk': 'Аеропорт BER', 'en': 'BER Airport'},
    'home.chip.station': {'ru': 'Вокзал', 'uk': 'Вокзал', 'en': 'Train station'},
    'home.stat_done': {'ru': 'Завершённых поездок', 'uk': 'Завершених поїздок', 'en': 'Completed rides'},
    'home.stat_km': {'ru': 'Километров с Tetatet', 'uk': 'Кілометрів з Tetatet', 'en': 'Kilometers with Tetatet'},
    'home.stat_active': {'ru': 'Активных сейчас', 'uk': 'Активних зараз', 'en': 'Active now'},
    'home.section_active': {'ru': 'Сейчас в пути', 'uk': 'Зараз у дорозі', 'en': 'On the way now'},
    'home.rating_label': {'ru': 'Ваш рейтинг', 'uk': 'Ваш рейтинг', 'en': 'Your rating'},
    'home.rating_meta': {'ru': 'Пассажир Tetatet', 'uk': 'Пасажир Tetatet', 'en': 'Tetatet passenger'},
    'home.driver_label': {'ru': 'Водитель едет', 'uk': 'Водій їде', 'en': 'Driver en route'},
    'home.section_recent': {'ru': 'Недавние поездки', 'uk': 'Недавні поїздки', 'en': 'Recent rides'},
    'home.all_history': {'ru': 'Вся история', 'uk': 'Вся історія', 'en': 'Full history'},
    'home.section_map': {'ru': 'Карта рядом', 'uk': 'Карта поруч', 'en': 'Map nearby'},
    'home.map_cta': {'ru': 'Открыть заказ на карте', 'uk': 'Відкрити замовлення на карті', 'en': 'Open booking on map'},

    # ── Greetings (home.js) ───────────────────────────────────────────────────
    'greeting.night': {'ru': 'Доброй ночи', 'uk': 'Доброї ночі', 'en': 'Good night'},
    'greeting.morning': {'ru': 'Доброе утро', 'uk': 'Доброго ранку', 'en': 'Good morning'},
    'greeting.day': {'ru': 'Добрый день', 'uk': 'Добрий день', 'en': 'Good afternoon'},
    'greeting.evening': {'ru': 'Добрый вечер', 'uk': 'Добрий вечер', 'en': 'Good evening'},

    # ── Order page ────────────────────────────────────────────────────────────
    'order.title': {'ru': 'Заказ поездки', 'uk': 'Замовлення поїздки', 'en': 'Book a ride'},
    'order.heading': {'ru': 'Заказ поездок', 'uk': 'Замовлення поїздок', 'en': 'Ride booking'},
    'order.phone_warning_title': {'ru': 'Нужен телефон', 'uk': 'Потрібен телефон', 'en': 'Phone required'},
    'order.phone_warning_text': {
        'ru': 'Добавьте номер в профиле, чтобы заказать такси.',
        'uk': 'Додайте номер у профілі, щоб замовити таксі.',
        'en': 'Add your number in profile to book a ride.',
    },
    'order.phone_warning_profile': {'ru': 'профиле', 'uk': 'профілі', 'en': 'profile'},
    'order.from': {'ru': 'Откуда', 'uk': 'Звідки', 'en': 'From'},
    'order.to': {'ru': 'Куда', 'uk': 'Куди', 'en': 'To'},
    'order.swap': {'ru': 'Поменять', 'uk': 'Поміняти', 'en': 'Swap'},
    'order.my_location': {'ru': 'Моя локация', 'uk': 'Моє місцезнаходження', 'en': 'My location'},
    'order.min_suffix': {'ru': 'мин · подача', 'uk': 'хв · подача', 'en': 'min · pickup'},
    'order.km_suffix': {'ru': 'км · маршрут', 'uk': 'км · маршрут', 'en': 'km · route'},
    'order.select_tariff': {'ru': 'Выберите тариф', 'uk': 'Оберіть тариф', 'en': 'Select tariff'},
    'order.choose_ride': {'ru': 'Выбрать поездку', 'uk': 'Обрати поїздку', 'en': 'Choose a ride'},
    'order.standard': {'ru': 'Стандарт', 'uk': 'Стандарт', 'en': 'Standard'},
    'order.special': {'ru': 'Специальные', 'uk': 'Спеціальні', 'en': 'Special'},
    'order.payment': {'ru': 'Оплата', 'uk': 'Оплата', 'en': 'Payment'},
    'order.cash': {'ru': 'Наличные', 'uk': 'Готівка', 'en': 'Cash'},
    'order.card': {'ru': 'Картой', 'uk': 'Карткою', 'en': 'Card'},
    'order.no_cards': {'ru': 'Нет карт —', 'uk': 'Немає карток —', 'en': 'No cards —'},
    'order.add_card_link': {'ru': 'добавить', 'uk': 'додати', 'en': 'add one'},
    'order.specify_route': {'ru': 'Укажите маршрут', 'uk': 'Вкажіть маршрут', 'en': 'Set your route'},
    'order.need_phone': {'ru': 'Добавьте телефон в профиле', 'uk': 'Додайте телефон у профілі', 'en': 'Add phone in profile'},
    'order.need_card': {'ru': 'Добавьте карту в профиле', 'uk': 'Додайте картку у профілі', 'en': 'Add card in profile'},
    'order.booking': {'ru': 'Оформляем...', 'uk': 'Оформлюємо...', 'en': 'Booking...'},
    'order.book': {'ru': 'Заказать {name} · {price}', 'uk': 'Замовити {name} · {price}', 'en': 'Book {name} · {price}'},
    'order.min_unit': {'ru': 'мин', 'uk': 'хв', 'en': 'min'},
    'order.alert_phone': {
        'ru': 'Добавьте номер телефона в профиле перед заказом.',
        'uk': 'Додайте номер телефону у профілі перед замовленням.',
        'en': 'Add your phone number in profile before booking.',
    },
    'order.alert_card': {
        'ru': 'Сначала добавьте карту в профиле',
        'uk': 'Спочатку додайте картку у профілі',
        'en': 'Add a card in profile first',
    },
    'order.error': {'ru': 'Ошибка заказа', 'uk': 'Помилка замовлення', 'en': 'Booking error'},

    # ── Track page ────────────────────────────────────────────────────────────
    'track.title': {'ru': 'Заказ №{id}', 'uk': 'Замовлення №{id}', 'en': 'Order #{id}'},
    'track.heading': {'ru': 'Поездка №{id}', 'uk': 'Поїздка №{id}', 'en': 'Ride #{id}'},
    'track.hint.new': {
        'ru': 'Диспетчер назначит водителя. Маршрут зафиксирован — изменить нельзя.',
        'uk': 'Диспетчер призначить водія. Маршрут зафіксовано — змінити не можна.',
        'en': 'Dispatch will assign a driver. Route is locked — cannot be changed.',
    },
    'track.hint.accepted': {
        'ru': 'Водитель едет к вам — следите на карте.',
        'uk': 'Водій їде до вас — стежте на карті.',
        'en': 'Driver is on the way — follow on the map.',
    },
    'track.hint.arrived': {
        'ru': 'Такси на месте. Нажмите «Садимся, поехали», когда сядете в машину.',
        'uk': 'Таксі на місці. Натисніть «Сідаємо, їдемо», коли сядете в машину.',
        'en': 'Taxi has arrived. Tap "Let\'s go" when you get in.',
    },
    'track.hint.on_way': {
        'ru': 'Поездка началась — маршрут до пункта назначения.',
        'uk': 'Поїздка розпочалась — маршрут до пункту призначення.',
        'en': 'Trip started — heading to destination.',
    },
    'track.hint.done': {'ru': 'Спасибо за поездку!', 'uk': 'Дякуємо за поїздку!', 'en': 'Thanks for riding!'},
    'track.hint.cancelled': {'ru': 'Заказ отменён.', 'uk': 'Замовлення скасовано.', 'en': 'Order cancelled.'},
    'track.rate_title': {'ru': 'Оцените поездку', 'uk': 'Оцініть поїздку', 'en': 'Rate your ride'},
    'track.rate_sub': {'ru': 'Как вам водитель {name}?', 'uk': 'Як вам водій {name}?', 'en': 'How was driver {name}?'},
    'track.rate_submit': {'ru': 'Отправить оценку', 'uk': 'Надіслати оцінку', 'en': 'Submit rating'},
    'track.rate_thanks': {'ru': 'Спасибо за оценку!', 'uk': 'Дякуємо за оцінку!', 'en': 'Thanks for your rating!'},
    'track.from_label': {'ru': 'Откуда', 'uk': 'Звідки', 'en': 'From'},
    'track.to_label': {'ru': 'Куда', 'uk': 'Куди', 'en': 'To'},
    'track.board': {'ru': 'Садимся, поехали', 'uk': 'Сідаємо, їдемо', 'en': "Let's go"},
    'track.book_again': {'ru': 'Заказать снова', 'uk': 'Замовити знову', 'en': 'Book again'},
    'track.to_history': {'ru': 'К истории', 'uk': 'До історії', 'en': 'To history'},
    'track.to_home': {'ru': 'На главную', 'uk': 'На головну', 'en': 'Go home'},
    'track.eta.approach': {'ru': 'Прибытие через ~{min} мин', 'uk': 'Прибуття через ~{min} хв', 'en': 'Arriving in ~{min} min'},
    'track.eta.driver_here': {'ru': 'Водитель на месте', 'uk': 'Водій на місці', 'en': 'Driver has arrived'},
    'track.eta.destination': {
        'ru': 'До пункта назначения ~{min} мин',
        'uk': 'До пункту призначення ~{min} хв',
        'en': '~{min} min to destination',
    },
    'track.eta.arrived': {'ru': 'Вы на месте', 'uk': 'Ви на місці', 'en': 'You have arrived'},
    'track.eta.complete_countdown': {
        'ru': 'Вы на месте — завершение через {sec} сек',
        'uk': 'Ви на місці — завершення через {sec} сек',
        'en': 'You have arrived — completing in {sec} sec',
    },

    # ── History ───────────────────────────────────────────────────────────────
    'history.title': {'ru': 'Мои поездки', 'uk': 'Мої поїздки', 'en': 'My rides'},
    'history.sub': {'ru': '{count} поездок в истории', 'uk': '{count} поїздок в історії', 'en': '{count} rides in history'},
    'history.active_title': {'ru': 'Активные поездки', 'uk': 'Активні поїздки', 'en': 'Active rides'},
    'history.empty_title': {'ru': 'Поездок пока нет', 'uk': 'Поїздок поки немає', 'en': 'No rides yet'},
    'history.empty_sub': {
        'ru': 'Закажите первую — это займёт меньше минуты',
        'uk': 'Замовте першу — це займе менше хвилини',
        'en': 'Book your first — it takes less than a minute',
    },
    'history.book': {'ru': 'Заказать', 'uk': 'Замовити', 'en': 'Book'},

    # ── Tariff categories ─────────────────────────────────────────────────────
    'tariff.category.standard': {'ru': 'Стандарт', 'uk': 'Стандарт', 'en': 'Standard'},
    'tariff.category.special': {'ru': 'Специальные', 'uk': 'Спеціальні', 'en': 'Special'},

    # ── Tariffs ───────────────────────────────────────────────────────────────
    'tariff.economy.label': {'ru': 'Эконом', 'uk': 'Економ', 'en': 'Economy'},
    'tariff.economy.display': {'ru': 'Economy', 'uk': 'Economy', 'en': 'Economy'},
    'tariff.economy.meta': {'ru': '4 места', 'uk': '4 місця', 'en': '4 seats'},
    'tariff.economy.desc': {'ru': 'Быстрая поездка по городу', 'uk': 'Швидка поїздка містом', 'en': 'Quick city ride'},

    'tariff.comfort.label': {'ru': 'Комфорт', 'uk': 'Комфорт', 'en': 'Comfort'},
    'tariff.comfort.display': {'ru': 'Comfort', 'uk': 'Comfort', 'en': 'Comfort'},
    'tariff.comfort.meta': {'ru': '4 места · просторнее', 'uk': '4 місця · просторіше', 'en': '4 seats · more space'},
    'tariff.comfort.desc': {
        'ru': 'Больше места и тишина в салоне',
        'uk': 'Більше місця й тиша в салоні',
        'en': 'More space and a quiet cabin',
    },

    'tariff.business.label': {'ru': 'Бизнес', 'uk': 'Бізнес', 'en': 'Business'},
    'tariff.business.display': {'ru': 'Business', 'uk': 'Business', 'en': 'Business'},
    'tariff.business.meta': {'ru': 'премиум-класс', 'uk': 'преміум-клас', 'en': 'premium class'},
    'tariff.business.desc': {'ru': 'Премиум-авто и приоритет', 'uk': 'Преміум-авто й пріоритет', 'en': 'Premium car and priority'},

    'tariff.minivan.label': {'ru': 'Минивэн', 'uk': 'Мінівен', 'en': 'Minivan'},
    'tariff.minivan.display': {'ru': 'Minivan', 'uk': 'Minivan', 'en': 'Minivan'},
    'tariff.minivan.meta': {'ru': '6–7 мест · просторно', 'uk': '6–7 місць · просторно', 'en': '6–7 seats · spacious'},
    'tariff.minivan.desc': {
        'ru': 'Больше места для компании и багажа',
        'uk': 'Більше місця для компанії й багажу',
        'en': 'More room for groups and luggage',
    },

    'tariff.cargo.label': {'ru': 'Грузовой', 'uk': 'Вантажний', 'en': 'Cargo'},
    'tariff.cargo.display': {'ru': 'Cargo', 'uk': 'Cargo', 'en': 'Cargo'},
    'tariff.cargo.meta': {'ru': 'до 800 кг', 'uk': 'до 800 кг', 'en': 'up to 800 kg'},
    'tariff.cargo.desc': {
        'ru': 'Перевозка груза и крупных вещей',
        'uk': 'Перевезення вантажу й великих речей',
        'en': 'Moving cargo and large items',
    },

    'tariff.pets.label': {'ru': 'С животными', 'uk': 'З тваринами', 'en': 'Pet-friendly'},
    'tariff.pets.display': {'ru': 'PetRide', 'uk': 'PetRide', 'en': 'PetRide'},
    'tariff.pets.meta': {'ru': 'переноска · плед', 'uk': 'переноска · плед', 'en': 'carrier · blanket'},
    'tariff.pets.desc': {
        'ru': 'Водитель готов к поездке с питомцем',
        'uk': 'Водій готовий до поїздки з улюбленцем',
        'en': 'Driver ready for a trip with your pet',
    },

    'tariff.kids.label': {'ru': 'С детьми', 'uk': 'З дітьми', 'en': 'Family'},
    'tariff.kids.display': {'ru': 'Family', 'uk': 'Family', 'en': 'Family'},
    'tariff.kids.meta': {'ru': 'детское кресло', 'uk': 'дитяче крісло', 'en': 'child seat'},
    'tariff.kids.desc': {
        'ru': 'Кресло и спокойная поездка с ребёнком',
        'uk': 'Крісло й спокійна поїздка з дитиною',
        'en': 'Child seat and a calm ride with kids',
    },

    # ── Payment / card form ───────────────────────────────────────────────────
    'payment.card_number': {'ru': 'Номер карты', 'uk': 'Номер картки', 'en': 'Card number'},
    'payment.expiry': {'ru': 'Срок действия', 'uk': 'Термін дії', 'en': 'Expiry date'},
    'payment.expiry_placeholder': {'ru': 'ММ / ГГ', 'uk': 'ММ / РР', 'en': 'MM / YY'},
    'payment.cvv': {'ru': 'CVV', 'uk': 'CVV', 'en': 'CVV'},
    'payment.holder': {'ru': 'Имя на карте', 'uk': "Ім'я на картці", 'en': 'Name on card'},
    'payment.err.full_number': {
        'ru': 'Введите полный номер карты',
        'uk': 'Введіть повний номер картки',
        'en': 'Enter the full card number',
    },
    'payment.err.expiry_format': {
        'ru': 'Укажите срок действия в формате ММ/ГГ',
        'uk': 'Вкажіть термін дії у форматі ММ/РР',
        'en': 'Enter expiry as MM/YY',
    },
    'payment.err.cvv': {
        'ru': 'Введите CVV (3 цифры)',
        'uk': 'Введіть CVV (3 цифри)',
        'en': 'Enter CVV (3 digits)',
    },

    # ── Map (leaflet-ride-map.js) ─────────────────────────────────────────────
    'map.satellite_title': {'ru': 'Спутник / Карта', 'uk': 'Супутник / Карта', 'en': 'Satellite / Map'},
    'map.satellite_aria': {'ru': 'Переключить вид карты', 'uk': 'Перемкнути вид карти', 'en': 'Toggle map view'},
    'map.locate_title': {'ru': 'Моё местоположение', 'uk': 'Моє місцезнаходження', 'en': 'My location'},
    'map.locate_btn': {'ru': 'Моя локация', 'uk': 'Моє місцезнаходження', 'en': 'My location'},
    'map.click_from': {'ru': 'Кликните на карте — точка A (откуда)', 'uk': 'Клацніть на карті — точка A (звідки)', 'en': 'Click on map — point A (from)'},
    'map.click_to': {'ru': 'Кликните на карте — точка B (куда)', 'uk': 'Клацніть на карті — точка B (куди)', 'en': 'Click on map — point B (to)'},
    'map.hint_destination': {
        'ru': 'Укажите пункт назначения на карте или в поле «Куда»',
        'uk': 'Вкажіть пункт призначення на карті або в полі «Куди»',
        'en': 'Set destination on the map or in the "To" field',
    },
    'map.geo_unavailable': {
        'ru': 'Геолокация недоступна в браузере',
        'uk': 'Геолокація недоступна в браузері',
        'en': 'Geolocation is not available in this browser',
    },
    'map.geo_denied': {
        'ru': 'Не удалось определить местоположение. Разрешите доступ к геолокации.',
        'uk': 'Не вдалося визначити місцезнаходження. Дозвольте доступ до геолокації.',
        'en': 'Could not get location. Allow geolocation access.',
    },
    'map.geo_manual': {
        'ru': 'Разрешите геолокацию в браузере или укажите адрес вручную',
        'uk': 'Дозвольте геолокацію в браузері або вкажіть адресу вручну',
        'en': 'Allow geolocation or enter the address manually',
    },

    # ── API validation messages (taxi/serializers.py) ─────────────────────────
    'api.phone_required': {
        'ru': 'Укажите номер телефона в профиле.',
        'uk': 'Вкажіть номер телефону у профілі.',
        'en': 'Add your phone number in profile.',
    },
    'api.phone_too_long': {
        'ru': 'Телефон слишком длинный.',
        'uk': 'Телефон занадто довгий.',
        'en': 'Phone number is too long.',
    },
    'api.from_required': {
        'ru': 'Укажите адрес отправления.',
        'uk': 'Вкажіть адресу відправлення.',
        'en': 'Enter pickup address.',
    },
    'api.to_required': {
        'ru': 'Укажите адрес назначения.',
        'uk': 'Вкажіть адресу призначення.',
        'en': 'Enter destination address.',
    },
    'api.card_not_yours': {
        'ru': 'Эта карта не принадлежит вам.',
        'uk': 'Ця картка не належить вам.',
        'en': 'This card does not belong to you.',
    },
    'api.active_order': {
        'ru': 'У вас уже есть активный заказ. Дождитесь завершения или отмените его.',
        'uk': 'У вас уже є активне замовлення. Дочекайтеся завершення або скасуйте його.',
        'en': 'You already have an active order. Wait for it to finish or cancel it.',
    },
    'api.card_required': {
        'ru': 'Выберите карту для оплаты.',
        'uk': 'Оберіть картку для оплати.',
        'en': 'Select a card for payment.',
    },
    'api.status_transition': {
        'ru': 'Нельзя перейти из «{from}» в этот статус.',
        'uk': 'Неможливо перейти з «{from}» у цей статус.',
        'en': 'Cannot transition from «{from}» to this status.',
    },
    'api.driver_required': {
        'ru': 'Укажите имя водителя при принятии заказа.',
        'uk': 'Вкажіть ім\'я водія під час прийняття замовлення.',
        'en': 'Enter driver name when accepting the order.',
    },
    'api.status_invalid': {
        'ru': 'Недопустимый статус.',
        'uk': 'Недопустимий статус.',
        'en': 'Invalid status.',
    },
    'api.action_required': {
        'ru': 'Укажите действие или оценку.',
        'uk': 'Вкажіть дію або оцінку.',
        'en': 'Specify an action or rating.',
    },
    'api.one_action': {
        'ru': 'Отправьте только одно действие за раз.',
        'uk': 'Надішліть лише одну дію за раз.',
        'en': 'Send only one action at a time.',
    },
    'api.rating_done_only': {
        'ru': 'Оценить можно только завершённую поездку.',
        'uk': 'Оцінити можна лише завершену поїздку.',
        'en': 'You can only rate a completed ride.',
    },
    'api.rating_already': {
        'ru': 'Вы уже оценили эту поездку.',
        'uk': 'Ви вже оцінили цю поїздку.',
        'en': 'You have already rated this ride.',
    },
    'api.board_arrived_only': {
        'ru': 'Подтвердить посадку можно только когда такси на месте.',
        'uk': 'Підтвердити посадку можна лише коли таксі на місці.',
        'en': 'You can confirm boarding only when the taxi has arrived.',
    },
    'api.complete_on_way_only': {
        'ru': 'Завершить поездку можно только в пути к пункту назначения.',
        'uk': 'Завершити поїздку можна лише в дорозі до пункту призначення.',
        'en': 'You can complete the ride only while heading to destination.',
    },
    'api.no_access': {'ru': 'Нет доступа.', 'uk': 'Немає доступу.', 'en': 'Access denied.'},

    # ── Flash messages & view errors (accounts/views.py) ────────────────────────
    'msg.register.phone_required': {
        'ru': 'Укажите номер телефона',
        'uk': 'Вкажіть номер телефону',
        'en': 'Enter a phone number',
    },
    'msg.register.phone_too_long': {
        'ru': 'Слишком длинный номер телефона',
        'uk': 'Занадто довгий номер телефону',
        'en': 'Phone number is too long',
    },
    'msg.register.email_exists': {
        'ru': 'Пользователь с таким email уже существует',
        'uk': 'Користувач з таким email уже існує',
        'en': 'A user with this email already exists',
    },
    'msg.login.invalid': {
        'ru': 'Неверный email или пароль',
        'uk': 'Невірний email або пароль',
        'en': 'Invalid email or password',
    },
    'msg.login.dispatcher_info': {
        'ru': 'Вы вошли как диспетчер. Чтобы заказать такси — войдите здесь отдельно.',
        'uk': 'Ви увійшли як диспетчер. Щоб замовити таксі — увійдіть тут окремо.',
        'en': 'You are signed in as a dispatcher. To book a ride — sign in here separately.',
    },
    'msg.dispatcher.passenger_info': {
        'ru': 'Вы вошли как пассажир. Для диспетчерской — войдите здесь отдельно.',
        'uk': 'Ви увійшли як пасажир. Для диспетчерської — увійдіть тут окремо.',
        'en': 'You are signed in as a passenger. For dispatch — sign in here separately.',
    },
    'msg.dispatcher.no_access': {
        'ru': 'У этого аккаунта нет доступа к диспетчерской. Нужна галочка «Диспетчер» в админке.',
        'uk': 'У цього акаунта немає доступу до диспетчерської. Потрібна позначка «Диспетчер» в адмінці.',
        'en': 'This account has no dispatch access. Enable "Dispatcher" in admin.',
    },
    'msg.card.full_number': {
        'ru': 'Введите полный номер карты',
        'uk': 'Введіть повний номер картки',
        'en': 'Enter the full card number',
    },
    'msg.card.expiry': {
        'ru': 'Укажите срок действия (ММ/ГГ)',
        'uk': 'Вкажіть термін дії (ММ/РР)',
        'en': 'Enter expiry (MM/YY)',
    },
    'msg.card.month': {
        'ru': 'Неверный месяц',
        'uk': 'Невірний місяць',
        'en': 'Invalid month',
    },
    'msg.card.cvv': {
        'ru': 'Введите CVV (3 цифры)',
        'uk': 'Введіть CVV (3 цифри)',
        'en': 'Enter CVV (3 digits)',
    },
    'msg.card.saved': {'ru': 'Карта сохранена', 'uk': 'Картку збережено', 'en': 'Card saved'},
    'msg.card.not_found': {'ru': 'Карта не найдена', 'uk': 'Картку не знайдено', 'en': 'Card not found'},
    'msg.card.brand_invalid': {
        'ru': 'Неверный тип карты',
        'uk': 'Невірний тип картки',
        'en': 'Invalid card type',
    },
    'msg.card.updated': {'ru': 'Карта обновлена', 'uk': 'Картку оновлено', 'en': 'Card updated'},
    'msg.card.deleted': {'ru': 'Карта удалена', 'uk': 'Картку видалено', 'en': 'Card deleted'},
    'msg.card.default_updated': {
        'ru': 'Карта по умолчанию обновлена',
        'uk': 'Картку за замовчуванням оновлено',
        'en': 'Default card updated',
    },
    'msg.profile.required': {
        'ru': 'Имя и email обязательны',
        'uk': "Ім'я та email обов'язкові",
        'en': 'First name and email are required',
    },
    'msg.profile.phone_required': {
        'ru': 'Телефон обязателен для заказа такси',
        'uk': "Телефон обов'язковий для замовлення таксі",
        'en': 'Phone is required to book a ride',
    },
    'msg.profile.phone_too_long': {
        'ru': 'Номер телефона слишком длинный',
        'uk': 'Номер телефону занадто довгий',
        'en': 'Phone number is too long',
    },
    'msg.profile.email_taken': {
        'ru': 'Этот email уже занят',
        'uk': 'Цей email уже зайнятий',
        'en': 'This email is already taken',
    },
    'msg.profile.saved': {'ru': 'Профиль сохранён', 'uk': 'Профіль збережено', 'en': 'Profile saved'},
    'msg.password.wrong_current': {
        'ru': 'Неверный текущий пароль',
        'uk': 'Невірний поточний пароль',
        'en': 'Incorrect current password',
    },
    'msg.password.empty': {
        'ru': 'Введите новый пароль',
        'uk': 'Введіть новий пароль',
        'en': 'Enter a new password',
    },
    'msg.password.mismatch': {
        'ru': 'Пароли не совпадают',
        'uk': 'Паролі не збігаються',
        'en': 'Passwords do not match',
    },
    'msg.password.updated': {'ru': 'Пароль обновлён', 'uk': 'Пароль оновлено', 'en': 'Password updated'},
}


def translate(key: str, lang: str = 'ru') -> str:
    if lang not in LANGUAGE_CODES:
        lang = 'ru'
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get('ru', key)


def resolve_language(request) -> str:
    lang = request.session.get('language')
    if not lang and getattr(request, 'user', None) and request.user.is_authenticated:
        lang = getattr(request.user, 'preferred_language', None)
    if lang not in LANGUAGE_CODES:
        lang = 'ru'
    return lang


def js_translations(lang: str) -> dict:
    return {key.replace('.', '_'): translate(key, lang) for key in TRANSLATIONS}
