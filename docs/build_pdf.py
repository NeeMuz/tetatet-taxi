"""PDF-документация Tetatet — презентационный дизайн, 2 скриншота на страницу."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
SCREENSHOTS = DOCS / 'screenshots'
OUTPUT = DOCS / 'Tetatet_Project_Description.pdf'

FONT_DIR = Path(r'C:\Windows\Fonts')
pdfmetrics.registerFont(TTFont('Arial', str(FONT_DIR / 'arial.ttf')))
pdfmetrics.registerFont(TTFont('Arial-Bold', str(FONT_DIR / 'arialbd.ttf')))
pdfmetrics.registerFont(TTFont('Arial-Italic', str(FONT_DIR / 'ariali.ttf')))

# Единая палитра
C_BG = colors.HexColor('#080808')
C_SURFACE = colors.HexColor('#121212')
C_SURFACE2 = colors.HexColor('#1a1a1a')
C_BORDER = colors.HexColor('#2a2a2a')
C_BORDER_LT = colors.HexColor('#3a3a3a')
C_TEXT = colors.HexColor('#f5f5f5')
C_MUTED = colors.HexColor('#8a8a8a')
C_ACCENT = colors.HexColor('#4da3ff')
C_ACCENT_DIM = colors.HexColor('#1a3a5c')
C_WHITE = colors.white

PAGE_W, PAGE_H = A4
MARGIN = 1.45 * cm
CONTENT_W = PAGE_W - 2 * MARGIN
TOP_CHROME = 1.45 * cm
BOTTOM_CHROME = 1.35 * cm
HEADER_BAR_H = 0.95 * cm
HEADER_GAP = 0.25 * cm
TOP_MARGIN = TOP_CHROME + 0.55 * cm + HEADER_BAR_H + HEADER_GAP
FRAME_H = PAGE_H - TOP_MARGIN - BOTTOM_CHROME
CONTENT_PAD_X = 0.14 * cm
SHOT_PAD_TOP = 0.12 * cm
SHOT_GAP = 0.24 * cm


def build_styles():
    return {
        'cover_sub': ParagraphStyle(
            'cover_sub', fontName='Arial', fontSize=11, leading=14,
            textColor=colors.HexColor('#b0b0b0'), alignment=TA_CENTER,
        ),
        'section': ParagraphStyle(
            'section', fontName='Arial-Bold', fontSize=8.2, leading=10,
            textColor=C_ACCENT, spaceBefore=0, spaceAfter=1,
        ),
        'body': ParagraphStyle(
            'body', fontName='Arial', fontSize=7.6, leading=9.5,
            textColor=colors.HexColor('#cccccc'), alignment=TA_JUSTIFY, spaceAfter=1,
        ),
        'bullet': ParagraphStyle(
            'bullet', fontName='Arial', fontSize=7.4, leading=9.2,
            textColor=colors.HexColor('#bdbdbd'), alignment=TA_LEFT,
            leftIndent=8, bulletIndent=0, spaceAfter=0.5,
        ),
        'cell': ParagraphStyle(
            'cell', fontName='Arial', fontSize=7.2, leading=9,
            textColor=colors.HexColor('#dedede'),
        ),
        'cell_head': ParagraphStyle(
            'cell_head', fontName='Arial-Bold', fontSize=7.2, leading=9,
            textColor=C_WHITE,
        ),
        'shot_num': ParagraphStyle(
            'shot_num', fontName='Arial-Bold', fontSize=9, leading=11,
            textColor=C_ACCENT, alignment=TA_LEFT,
        ),
        'shot_h': ParagraphStyle(
            'shot_h', fontName='Arial-Bold', fontSize=11.5, leading=13,
            textColor=C_TEXT, alignment=TA_LEFT, spaceAfter=0,
        ),
        'shot_desc': ParagraphStyle(
            'shot_desc', fontName='Arial', fontSize=7.8, leading=9.5,
            textColor=C_MUTED, alignment=TA_LEFT, spaceAfter=0,
        ),
        'caption': ParagraphStyle(
            'caption', fontName='Arial-Italic', fontSize=7, leading=8,
            textColor=colors.HexColor('#666666'), alignment=TA_CENTER,
        ),
        'page_title': ParagraphStyle(
            'page_title', fontName='Arial-Bold', fontSize=10, leading=12,
            textColor=C_TEXT, alignment=TA_LEFT,
        ),
    }


ST = build_styles()


def _draw_paragraph(canvas, text, style, x, y_top, width, max_height=999):
    para = Paragraph(text, style)
    _, h = para.wrap(width, max_height)
    para.drawOn(canvas, x, y_top - h)
    return h


def paint_page_background(canvas):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    canvas.setStrokeColor(colors.HexColor('#111111'))
    canvas.setLineWidth(0.25)
    step = 1.2 * cm
    y = 0
    while y < PAGE_H:
        canvas.line(0, y, PAGE_W, y)
        y += step
    x = 0
    while x < PAGE_W:
        canvas.line(x, 0, x, PAGE_H)
        x += step

    canvas.setFillColor(C_ACCENT)
    canvas.rect(0, PAGE_H - 3 * mm, PAGE_W, 3 * mm, fill=1, stroke=0)
    canvas.restoreState()


def paint_content_chrome(canvas, title: str, subtitle: str = ''):
    paint_page_background(canvas)
    canvas.saveState()

    header_y = PAGE_H - TOP_MARGIN + HEADER_GAP
    canvas.setFillColor(C_SURFACE)
    canvas.roundRect(MARGIN, header_y, CONTENT_W, HEADER_BAR_H, 5, fill=1, stroke=0)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.4)
    canvas.roundRect(MARGIN, header_y, CONTENT_W, HEADER_BAR_H, 5, fill=0, stroke=1)

    canvas.setFillColor(C_ACCENT)
    canvas.roundRect(MARGIN + 0.22 * cm, header_y + 0.17 * cm, 0.28 * cm, 0.6 * cm, 2, fill=1, stroke=0)

    canvas.setFont('Arial-Bold', 9.5)
    canvas.setFillColor(C_TEXT)
    canvas.drawString(MARGIN + 0.65 * cm, header_y + 0.47 * cm, title)

    if subtitle:
        canvas.setFont('Arial', 7.5)
        canvas.setFillColor(C_MUTED)
        canvas.drawRightString(PAGE_W - MARGIN - 0.2 * cm, header_y + 0.47 * cm, subtitle)

    canvas.setFont('Arial-Bold', 7)
    canvas.setFillColor(C_MUTED)
    canvas.drawString(MARGIN, 1.05 * cm, 'TETATET')
    canvas.drawRightString(PAGE_W - MARGIN, 1.05 * cm, f'стр. {canvas.getPageNumber()}')

    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.35)
    canvas.line(MARGIN, 1.35 * cm, PAGE_W - MARGIN, 1.35 * cm)
    canvas.restoreState()


def draw_cover(canvas, doc):
    paint_page_background(canvas)
    canvas.saveState()

    inset = 1.1 * cm
    canvas.setStrokeColor(C_BORDER_LT)
    canvas.setLineWidth(0.6)
    canvas.roundRect(inset, inset, PAGE_W - 2 * inset, PAGE_H - 2 * inset, 14, fill=0, stroke=1)

    canvas.setStrokeColor(C_ACCENT)
    canvas.setLineWidth(1.8)
    canvas.line(inset + 1.2 * cm, PAGE_H - inset - 1.0 * cm, PAGE_W - inset - 1.2 * cm, PAGE_H - inset - 1.0 * cm)

    cx = PAGE_W / 2

    # Вертикальная раскладка сверху вниз — без наложений
    badge_h = 0.62 * cm
    badge_w = 5.8 * cm
    badge_y = PAGE_H / 2 + 2.8 * cm
    canvas.setFillColor(C_ACCENT_DIM)
    canvas.roundRect(cx - badge_w / 2, badge_y, badge_w, badge_h, 8, fill=1, stroke=0)
    canvas.setFont('Arial-Bold', 8)
    canvas.setFillColor(C_ACCENT)
    badge = 'ПРЕЗЕНТАЦИЯ ПРОЕКТА'
    bw = pdfmetrics.stringWidth(badge, 'Arial-Bold', 8)
    canvas.drawString(cx - bw / 2, badge_y + 0.2 * cm, badge)

    title = 'TETATET'
    title_size = 62
    canvas.setFillColor(C_WHITE)
    canvas.setFont('Arial-Bold', title_size)
    tw = pdfmetrics.stringWidth(title, 'Arial-Bold', title_size)
    title_y = PAGE_H / 2 + 0.55 * cm
    canvas.drawString(cx - tw / 2, title_y, title)

    line_y = PAGE_H / 2 - 0.35 * cm
    canvas.setStrokeColor(C_ACCENT)
    canvas.setLineWidth(2.5)
    canvas.line(cx - 3.0 * cm, line_y, cx + 3.0 * cm, line_y)

    canvas.setFont('Arial', 15)
    canvas.setFillColor(colors.HexColor('#e0e0e0'))
    sub = 'Веб-сервис заказа такси'
    sw = pdfmetrics.stringWidth(sub, 'Arial', 15)
    canvas.drawString(cx - sw / 2, PAGE_H / 2 - 0.95 * cm, sub)

    canvas.setFont('Arial', 9.5)
    canvas.setFillColor(C_MUTED)
    desc = 'MVP с картой, диспетчерской и обновлениями в реальном времени'
    dw = pdfmetrics.stringWidth(desc, 'Arial', 9.5)
    canvas.drawString(cx - dw / 2, PAGE_H / 2 - 1.55 * cm, desc)

    pill_y = PAGE_H / 2 - 2.55 * cm
    pills = ['Заказ поездки', 'Диспетчерская', 'WebSocket', 'REST + GraphQL']
    pill_gap = 0.32 * cm
    total_w = sum(pdfmetrics.stringWidth(p, 'Arial', 7.5) + 1.0 * cm for p in pills) + pill_gap * (len(pills) - 1)
    px = cx - total_w / 2
    for pill in pills:
        pw = pdfmetrics.stringWidth(pill, 'Arial', 7.5) + 1.0 * cm
        canvas.setFillColor(C_SURFACE2)
        canvas.setStrokeColor(C_BORDER)
        canvas.setLineWidth(0.35)
        canvas.roundRect(px, pill_y, pw, 0.52 * cm, 6, fill=1, stroke=1)
        canvas.setFont('Arial', 7.5)
        canvas.setFillColor(colors.HexColor('#c8c8c8'))
        canvas.drawString(px + 0.5 * cm, pill_y + 0.16 * cm, pill)
        px += pw + pill_gap

    card_w = CONTENT_W * 0.72
    card_h = 2.0 * cm
    card_x = (PAGE_W - card_w) / 2
    card_y = inset + 1.55 * cm
    canvas.setFillColor(C_SURFACE)
    canvas.roundRect(card_x, card_y, card_w, card_h, 10, fill=1, stroke=0)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.roundRect(card_x, card_y, card_w, card_h, 10, fill=0, stroke=1)

    stats = [
        ('Django 6', 'Backend'),
        ('8 экранов', 'Интерфейс'),
        ('5 статусов', 'Заказы'),
        ('3 тарифа', 'Ценообразование'),
    ]
    col_w = card_w / 4
    for i, (val, lbl) in enumerate(stats):
        sx = card_x + col_w * i + col_w / 2
        canvas.setFont('Arial-Bold', 10.5)
        canvas.setFillColor(C_WHITE)
        vw = pdfmetrics.stringWidth(val, 'Arial-Bold', 10.5)
        canvas.drawString(sx - vw / 2, card_y + 1.2 * cm, val)
        canvas.setFont('Arial', 7.5)
        canvas.setFillColor(C_MUTED)
        lw = pdfmetrics.stringWidth(lbl, 'Arial', 7.5)
        canvas.drawString(sx - lw / 2, card_y + 0.5 * cm, lbl)
        if i < 3:
            canvas.setStrokeColor(C_BORDER)
            canvas.setLineWidth(0.3)
            canvas.line(card_x + col_w * (i + 1), card_y + 0.35 * cm, card_x + col_w * (i + 1), card_y + card_h - 0.35 * cm)

    canvas.setFont('Arial', 8.5)
    canvas.setFillColor(colors.HexColor('#707070'))
    meta = 'Документация · Июнь 2026'
    mw = pdfmetrics.stringWidth(meta, 'Arial', 8.5)
    canvas.drawString(cx - mw / 2, inset + 0.65 * cm, meta)

    canvas.restoreState()


def draw_about_page(canvas, doc):
    paint_content_chrome(canvas, 'О проекте', 'Обзор системы')


def draw_screens_page(canvas, doc):
    pair = max(1, canvas.getPageNumber() - 2)
    first = pair * 2 - 1
    second = pair * 2
    paint_content_chrome(canvas, 'Интерфейс приложения', f'Рис. {first}–{second}')


def _draw_mini_table(canvas, x, y_top, width, rows, col_fracs, row_h=0.46 * cm):
    col_widths = [width * f for f in col_fracs]
    height = row_h * len(rows)

    canvas.saveState()
    canvas.setFillColor(C_SURFACE2)
    canvas.roundRect(x, y_top - height, width, height, 4, fill=1, stroke=0)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.3)
    canvas.roundRect(x, y_top - height, width, height, 4, fill=0, stroke=1)

    cy = y_top
    for ri, row in enumerate(rows):
        cy -= row_h
        if ri == 0:
            canvas.setFillColor(C_ACCENT_DIM)
            canvas.rect(x + 0.5, cy, width - 1, row_h, fill=1, stroke=0)

        cx = x + 0.12 * cm
        for ci, cell in enumerate(row):
            style = ST['cell_head'] if ri == 0 else ST['cell']
            _draw_paragraph(canvas, cell, style, cx, cy + row_h - 0.1 * cm, col_widths[ci] - 0.22 * cm, row_h - 0.08 * cm)
            cx += col_widths[ci]
            if ci < len(row) - 1:
                canvas.setStrokeColor(C_BORDER)
                canvas.setLineWidth(0.2)
                canvas.line(cx - 0.06 * cm, cy, cx - 0.06 * cm, cy + row_h)

        if ri > 0:
            canvas.setStrokeColor(colors.HexColor('#1e1e1e'))
            canvas.line(x + 0.15 * cm, cy, x + width - 0.15 * cm, cy)

    canvas.restoreState()
    return height


def _draw_fact_card(canvas, x, y, w, h, value, label):
    canvas.saveState()
    canvas.setFillColor(C_SURFACE2)
    canvas.roundRect(x, y, w, h, 5, fill=1, stroke=0)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.35)
    canvas.roundRect(x, y, w, h, 5, fill=0, stroke=1)

    canvas.setFont('Arial-Bold', 11)
    canvas.setFillColor(C_ACCENT)
    vw = pdfmetrics.stringWidth(value, 'Arial-Bold', 11)
    canvas.drawString(x + (w - vw) / 2, y + h - 0.52 * cm, value)

    label_style = ParagraphStyle(
        'fact_lbl', fontName='Arial', fontSize=6.5, leading=8,
        textColor=C_MUTED, alignment=TA_CENTER,
    )
    _draw_paragraph(canvas, label, label_style, x + 0.08 * cm, y + 0.42 * cm, w - 0.16 * cm, 0.38 * cm)
    canvas.restoreState()


class AboutPage(Flowable):
    """Вторая страница — описание проекта с фиксированной сеткой без наложений."""

    BOTTOM_RESERVE = 1.05 * cm

    def __init__(self):
        Flowable.__init__(self)
        self.width = CONTENT_W
        self.height = FRAME_H

    def wrap(self, availWidth, availHeight):
        self.width = min(availWidth, CONTENT_W)
        self.height = availHeight
        return self.width, self.height

    def split(self, availWidth, availHeight):
        return []

    def _draw_footer(self, c, w):
        footer_h = 0.8 * cm
        c.saveState()
        c.setFillColor(C_ACCENT_DIM)
        c.roundRect(0, 0, w, footer_h, 5, fill=1, stroke=0)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.3)
        c.roundRect(0, 0, w, footer_h, 5, fill=0, stroke=1)
        c.restoreState()
        _draw_paragraph(
            c,
            'Далее — <b>8 экранов</b> приложения: по <b>два скриншота</b> на странице.',
            ST['body'], 0.18 * cm, footer_h - 0.12 * cm, w - 0.36 * cm,
        )

    def draw(self):
        c = self.canv
        w = self.width
        gap = 0.42 * cm
        col_w = (w - gap) / 2
        lx, rx = 0, col_w + gap
        content_bottom = self.BOTTOM_RESERVE

        y = self.height
        y -= _draw_paragraph(
            c,
            '<b>Tetatet</b> — MVP сервиса такси: заказ на карте, диспетчерская панель, '
            'обновления статусов через WebSocket.',
            ST['body'], 0, y, w,
        ) + 0.22 * cm

        cards_h = 1.28 * cm
        card_w = (w - 3 * 0.25 * cm) / 4
        cards_top = y
        for i, (val, lbl) in enumerate([
            ('3 роли', 'Пассажир · Диспетчер · Админ'),
            ('5 статусов', 'new → accepted → on_way → done'),
            ('3 тарифа', 'Эконом · Комфорт · Бизнес'),
            ('2 API', 'REST и GraphQL'),
        ]):
            _draw_fact_card(c, i * (card_w + 0.25 * cm), cards_top - cards_h, card_w, cards_h, val, lbl)
        y = cards_top - cards_h - 0.35 * cm

        # Фиксированные высоты строк сетки
        row1_h = 3.35 * cm
        row2_h = 3.05 * cm
        row3_h = y - content_bottom - row1_h - row2_h - 0.2 * cm
        if row3_h < 2.5 * cm:
            row1_h = 3.1 * cm
            row2_h = 2.85 * cm
            row3_h = y - content_bottom - row1_h - row2_h - 0.2 * cm

        def draw_block(x, top, title, lines):
            _draw_paragraph(c, title, ST['section'], x, top, col_w)
            cur = top - 0.38 * cm
            for line in lines:
                cur -= _draw_paragraph(c, f'• {line}', ST['bullet'], x, cur, col_w) + 0.06 * cm

        row1_top = y
        draw_block(lx, row1_top, 'Назначение', [
            'Полный цикл такси-сервиса в браузере',
            'Лендинг, профиль и история поездок',
            'Диспетчерская с live-обновлениями',
            'Админка Django для управления',
        ])
        draw_block(rx, row1_top, 'Сценарий заказа', [
            'Регистрация и вход в аккаунт',
            'Адреса через Nominatim, маршрут OSRM',
            'Расчёт цены в USD, выбор тарифа',
            'Отправка заказа и трекинг статуса',
        ])

        row2_top = row1_top - row1_h
        _draw_paragraph(c, 'Роли пользователей', ST['section'], lx, row2_top, col_w)
        _draw_mini_table(c, lx, row2_top - 0.38 * cm, col_w, [
            ['Роль', 'Доступ'],
            ['Пассажир', 'Заказ, профиль, история'],
            ['Диспетчер', '/dispatcher/, статусы'],
            ['Админ', 'Полный /admin/'],
        ], [0.3, 0.7])

        _draw_paragraph(c, 'Статусы и тарифы', ST['section'], rx, row2_top, col_w)
        _draw_mini_table(c, rx, row2_top - 0.38 * cm, col_w, [
            ['Параметр', 'Значение'],
            ['Статусы', 'new · accepted · on_way · done'],
            ['Отмена', 'cancelled на любом этапе'],
            ['Цена', '$3.50 + $1.25/км × тариф'],
            ['Тарифы', 'Эконом 1.0 · Комфорт 1.4 · Бизнес 1.85'],
        ], [0.34, 0.66])

        row3_top = row2_top - row2_h
        _draw_paragraph(c, 'Технологический стек', ST['section'], lx, row3_top, col_w)
        _draw_mini_table(c, lx, row3_top - 0.38 * cm, col_w, [
            ['Слой', 'Решение'],
            ['Backend', 'Django 6, DRF, Graphene'],
            ['Realtime', 'Channels, Daphne, WebSocket'],
            ['Карты', 'Leaflet, OSRM, Nominatim'],
            ['Деплой', 'Railway, PostgreSQL, WhiteNoise'],
        ], [0.3, 0.7], row_h=0.44 * cm)

        _draw_paragraph(c, 'API и модули', ST['section'], rx, row3_top, col_w)
        api_top = row3_top - 0.38 * cm
        api_h = _draw_mini_table(c, rx, api_top, col_w, [
            ['Тип', 'Адрес'],
            ['POST', '/api/taxi/orders/'],
            ['PATCH', '/api/taxi/orders/&lt;id&gt;/'],
            ['WS', '/ws/orders/'],
            ['GQL', '/graphql/'],
        ], [0.2, 0.8], row_h=0.4 * cm)
        _draw_mini_table(c, rx, api_top - api_h - 0.12 * cm, col_w, [
            ['Модуль', 'Назначение'],
            ['accounts/', 'Авторизация, профиль'],
            ['taxi/', 'Заказы, API, WebSocket'],
            ['static/', 'CSS, JavaScript'],
        ], [0.34, 0.66], row_h=0.4 * cm)

        self._draw_footer(c, w)


def _draw_image_panel(canvas, filename, x, y, width, height):
    path = SCREENSHOTS / filename
    canvas.saveState()
    canvas.setFillColor(C_SURFACE)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.roundRect(x, y, width, height, 6, fill=1, stroke=1)

    inner = 0.18 * cm
    ix, iy = x + inner, y + inner
    iw, ih = width - 2 * inner, height - 2 * inner

    if not path.exists():
        canvas.setFillColor(C_MUTED)
        canvas.setFont('Arial', 8)
        canvas.drawCentredString(x + width / 2, y + height / 2, f'Нет: {filename}')
        canvas.restoreState()
        return

    reader = ImageReader(str(path))
    img_w, img_h = reader.getSize()
    ratio = min(iw / img_w, ih / img_h)
    draw_w = img_w * ratio
    draw_h = img_h * ratio
    canvas.drawImage(
        reader,
        ix + (iw - draw_w) / 2,
        iy + (ih - draw_h) / 2,
        draw_w, draw_h,
        preserveAspectRatio=True, mask='auto',
    )
    canvas.restoreState()


class ScreenshotPairPage(Flowable):
    """Страница 3+: ровно два скриншота, единый стиль панелей."""

    def __init__(self, items, page_index: int):
        Flowable.__init__(self)
        self.items = items[:2]
        self.page_index = page_index
        self.width = CONTENT_W
        self.height = FRAME_H

    def wrap(self, availWidth, availHeight):
        self.width = min(availWidth, CONTENT_W)
        self.height = availHeight
        self.pad_x = CONTENT_PAD_X
        self.panel_w = self.width - 2 * self.pad_x
        self.half_h = (availHeight - SHOT_PAD_TOP - SHOT_GAP) / 2
        self.header_h = 1.5 * cm
        self.caption_h = 0.4 * cm
        self.img_h = self.half_h - self.header_h - self.caption_h
        return self.width, self.height

    def split(self, availWidth, availHeight):
        return []

    def _draw_shot(self, idx, title, desc, filename, caption, panel_bottom):
        c = self.canv
        px = self.pad_x
        pw = self.panel_w
        top = panel_bottom + self.half_h

        c.saveState()
        c.setFillColor(C_SURFACE2)
        c.roundRect(px, panel_bottom, pw, self.half_h, 7, fill=1, stroke=0)
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.4)
        c.roundRect(px, panel_bottom, pw, self.half_h, 7, fill=0, stroke=1)

        badge = f'{idx:02d}'
        c.setFillColor(C_ACCENT)
        c.roundRect(px + 0.2 * cm, top - 0.56 * cm, 0.58 * cm, 0.4 * cm, 4, fill=1, stroke=0)
        c.setFont('Arial-Bold', 7.5)
        c.setFillColor(C_WHITE)
        bw = pdfmetrics.stringWidth(badge, 'Arial-Bold', 7.5)
        c.drawString(px + 0.2 * cm + (0.58 * cm - bw) / 2, top - 0.44 * cm, badge)
        c.restoreState()

        text_x = px + 0.92 * cm
        text_w = pw - 1.05 * cm
        _draw_paragraph(c, title, ST['shot_h'], text_x, top - 0.22 * cm, text_w)
        _draw_paragraph(c, desc, ST['shot_desc'], text_x, top - 0.7 * cm, text_w)

        img_pad = 0.16 * cm
        img_y = panel_bottom + self.caption_h + 0.1 * cm
        _draw_image_panel(c, filename, px + img_pad, img_y, pw - 2 * img_pad, self.img_h - 0.08 * cm)
        _draw_paragraph(c, caption, ST['caption'], px, panel_bottom + 0.32 * cm, pw)

    def draw(self):
        bottoms = [self.half_h + SHOT_GAP + SHOT_PAD_TOP, 0]
        for i, (title, desc, filename, caption) in enumerate(self.items):
            if i == 1:
                divider_y = self.half_h + SHOT_GAP / 2 + SHOT_PAD_TOP / 2
                self.canv.saveState()
                self.canv.setStrokeColor(C_BORDER_LT)
                self.canv.setLineWidth(0.5)
                self.canv.line(
                    self.pad_x + 0.3 * cm, divider_y,
                    self.width - self.pad_x - 0.3 * cm, divider_y,
                )
                self.canv.restoreState()
            num = (self.page_index - 1) * 2 + i + 1
            self._draw_shot(num, title, desc, filename, caption, bottoms[i])


def build_pdf():
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_CHROME,
    )
    doc.addPageTemplates([
        PageTemplate(
            id='cover',
            frames=[Frame(MARGIN, MARGIN, CONTENT_W, PAGE_H - 2 * MARGIN, id='cover')],
            onPage=draw_cover,
        ),
        PageTemplate(
            id='about',
            frames=[Frame(MARGIN, BOTTOM_CHROME, CONTENT_W, FRAME_H, id='about')],
            onPage=draw_about_page,
        ),
        PageTemplate(
            id='screens',
            frames=[Frame(MARGIN, BOTTOM_CHROME, CONTENT_W, FRAME_H, id='screens')],
            onPage=draw_screens_page,
        ),
    ])

    screens = [
        ('01-landing.png', 'Главная страница', 'Лендинг сервиса: описание, карта и вход в систему', 'Рис. 1 — Главная'),
        ('02-order.png', 'Заказ поездки', 'Форма адресов, интерактивная карта и выбор тарифа', 'Рис. 2 — Заказ'),
        ('03-order-route.png', 'Маршрут и расчёт', 'Построенный маршрут, расстояние, время и стоимость', 'Рис. 3 — Маршрут'),
        ('04-profile.png', 'Профиль пользователя', 'Имя, телефон, email и загрузка аватара', 'Рис. 4 — Профиль'),
        ('05-history.png', 'История поездок', 'Список всех заказов с датами, маршрутами и статусами', 'Рис. 5 — История'),
        ('06-tracking.png', 'Отслеживание заказа', 'Активная поездка и карта с live-обновлением статуса', 'Рис. 6 — Трекинг'),
        ('07-dispatcher-login.png', 'Вход диспетчера', 'Отдельная авторизация для оператора диспетчерской', 'Рис. 7 — Вход'),
        ('08-dispatcher-panel.png', 'Диспетчерская панель', 'Канбан-доска: новые, принятые, в пути, завершённые', 'Рис. 8 — Диспетчер'),
    ]

    story = [
        Spacer(1, 1),
        NextPageTemplate('about'),
        PageBreak(),
        AboutPage(),
        NextPageTemplate('screens'),
        PageBreak(),
    ]

    for i in range(0, len(screens), 2):
        pair = [(t, d, f, c) for f, t, d, c in screens[i:i + 2]]
        story.append(ScreenshotPairPage(pair, page_index=i // 2 + 1))
        if i + 2 < len(screens):
            story.append(PageBreak())

    doc.build(story)
    print(f'PDF: {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    build_pdf()
