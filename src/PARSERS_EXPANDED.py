#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PromoHunter Bot - PARSERS_EXPANDED v2.1 (FINAL - FIXED)
49 джерел (36 базових + 13 сірих ниш)
Категорії: Заробіток, Бонуси, Скрипти, Пропозиції, Сірі ніші (СНД, Європа, США), Легальні маркети

ГОТОВО ДО ВИКОРИСТАННЯ! ✅
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class LegalityStatus(Enum):
    LEGAL = "Legal"
    GREY = "Grey"
    BLACK = "Black"

# ==================== КАТЕГОРІЯ 1: ЗАРОБІТОК (9) ====================

def parse_earnings() -> List[Dict[str, Any]]:
    """💰 Основні способи заробітку"""
    return [
        {
            'title': '💳 Fiverr - Фрилансові послуги від $5',
            'description': 'Глобальна платформа для фрилансерів. Виконуй завдання від $5. Комісія Fiverr 20%. Середній заробіток $500+/місяць для досвідчених.',
            'link': 'https://www.fiverr.com',
            'source': 'Fiverr',
            'emoji': '💳',
            'category': 'earnings',
            'difficulty': 'Easy',
            'min_earning': 5,
            'max_earning': 500,
            'rating': 4.7,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['фриланс', 'глобально', 'від $5'],
        },
        {
            'title': '🎯 Upwork - Біржа фрилансерів',
            'description': 'Найбільша біржа фрилансерів. Проекти від $5 до $10000+. Комісія 5-20%. Середній заробіток $300-1000/місяць.',
            'link': 'https://www.upwork.com',
            'source': 'Upwork',
            'emoji': '🎯',
            'category': 'earnings',
            'difficulty': 'Easy',
            'min_earning': 5,
            'max_earning': 10000,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['фриланс', 'проекти', 'глобально'],
        },
        {
            'title': '🎁 Swagbucks - Мікротаски та опитування',
            'description': 'Додаток для заробітку на опитуваннях, відео, покупках. Заробіток $1-50/місяць. Виведення через PayPal.',
            'link': 'https://www.swagbucks.com',
            'source': 'Swagbucks',
            'emoji': '🎁',
            'category': 'earnings',
            'difficulty': 'Very Easy',
            'min_earning': 1,
            'max_earning': 50,
            'rating': 4.3,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['опитування', 'мікротаски', 'легко'],
        },
        {
            'title': '👕 Vinted - Продаж одягу',
            'description': 'Маркетплейс для продажу речей. Комісія 5-10%. Заробіток €5-100+ за річ.',
            'link': 'https://www.vinted.com',
            'source': 'Vinted',
            'emoji': '👕',
            'category': 'earnings',
            'difficulty': 'Easy',
            'min_earning': 5,
            'max_earning': 100,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['маркетплейс', 'речі', 'європа'],
        },
        {
            'title': '🔧 TaskRabbit - Місцеві послуги',
            'description': 'Платформа для надання місцевих послуг (збірка меблів, прибирання тощо). Заробіток $15-60/год.',
            'link': 'https://www.taskrabbit.com',
            'source': 'TaskRabbit',
            'emoji': '🔧',
            'category': 'earnings',
            'difficulty': 'Medium',
            'min_earning': 15,
            'max_earning': 60,
            'rating': 4.4,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['місцеві', 'послуги', 'збірка'],
        },
        {
            'title': '🛍️ Etsy - Handmade маркетплейс',
            'description': 'Платформа для продажу хендмейду та цифрових товарів. Комісія 6.5%. Заробіток $10-1000+/місяць.',
            'link': 'https://www.etsy.com',
            'source': 'Etsy',
            'emoji': '🛍️',
            'category': 'earnings',
            'difficulty': 'Medium',
            'min_earning': 10,
            'max_earning': 1000,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['handmade', 'маркетплейс', 'цифрові'],
        },
        {
            'title': '📦 Amazon FBA - Продаж через Amazon',
            'description': 'Продавай товари через Amazon. Amazon займається доставкою. Заробіток змінний, залежить від товару.',
            'link': 'https://sellercentral.amazon.com',
            'source': 'Amazon FBA',
            'emoji': '📦',
            'category': 'earnings',
            'difficulty': 'Hard',
            'min_earning': 100,
            'max_earning': 10000,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['amazon', 'fba', 'товари'],
        },
        {
            'title': '👗 Depop - Мобільний маркетплейс',
            'description': 'Додаток для продажу речей. Комісія 10%. Молода аудиторія. Заробіток €5-100+ за річ.',
            'link': 'https://www.depop.com',
            'source': 'Depop',
            'emoji': '👗',
            'category': 'earnings',
            'difficulty': 'Easy',
            'min_earning': 5,
            'max_earning': 100,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['мобільне', 'маркетплейс', 'речі'],
        },
        {
            'title': '💸 InboxDollars - Опитування та відео',
            'description': 'Заробляй на опитуваннях, відео, іграх. Заробіток $1-50/місяць. Виведення через Check або PayPal.',
            'link': 'https://www.inboxdollars.com',
            'source': 'InboxDollars',
            'emoji': '💸',
            'category': 'earnings',
            'difficulty': 'Very Easy',
            'min_earning': 1,
            'max_earning': 50,
            'rating': 4.2,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['опитування', 'відео', 'ігри'],
        },
    ]

# ==================== КАТЕГОРІЯ 2: БОНУСИ (9) ====================

def parse_bonuses() -> List[Dict[str, Any]]:
    """🎰 Казино бонуси та промо"""
    return [
        {
            'title': '🎲 1xBet - €130 бонус для новачків',
            'description': 'Букмекерська контора. Приветствельний бонус €130. Вимога відіграшу 5x. Безліч видів спорту та ігор.',
            'link': 'https://1xbet.com',
            'source': '1xBet',
            'emoji': '🎲',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 130,
            'rating': 4.8,
            'legality': LegalityStatus.GREY.value,
            'verified': True,
            'tags': ['казино', 'бонус', 'спорт'],
            'warning': '⚠️ Перевір законність у твоїй країні'
        },
        {
            'title': '🃏 BetOnline - €250 бонус',
            'description': 'Букмекер. Бонус €250. Відіграш 3x. Прямі виплати на крипто.',
            'link': 'https://betonline.ag',
            'source': 'BetOnline',
            'emoji': '🃏',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 250,
            'rating': 4.6,
            'legality': LegalityStatus.GREY.value,
            'verified': True,
            'tags': ['букмекер', 'крипто', 'бонус'],
        },
        {
            'title': '🎪 Slots of Vegas - €2500 бонус',
            'description': 'Казино. Величезний привітальний пакет €2500. Вимога відіграшу 40x. Багато слотів.',
            'link': 'https://slotsvegasx.com',
            'source': 'Slots of Vegas',
            'emoji': '🎪',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 2500,
            'rating': 4.4,
            'legality': LegalityStatus.GREY.value,
            'verified': True,
            'tags': ['казино', 'слоти', 'великий бонус'],
        },
        {
            'title': '🎯 Super Slots - 300 Free Spins',
            'description': 'Казино. 300 фрі-спінів при реєстрації. Низька вимога відіграшу.',
            'link': 'https://superslots.ag',
            'source': 'Super Slots',
            'emoji': '🎯',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 500,
            'rating': 4.5,
            'legality': LegalityStatus.GREY.value,
            'verified': True,
            'tags': ['фрі-спіни', 'слоти', 'казино'],
        },
        {
            'title': '💎 Slots.lv - 200% бонус',
            'description': 'Казино. Бонус 200% на перший депозит. Багато популярних слотів.',
            'link': 'https://slots.lv',
            'source': 'Slots.lv',
            'emoji': '💎',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 1000,
            'rating': 4.5,
            'legality': LegalityStatus.GREY.value,
            'verified': True,
            'tags': ['казино', 'відсоток бонусу', 'слоти'],
        },
        {
            'title': '⭐ OddsChecker - £2200+ бонуси',
            'description': 'Агрегатор букмекерів. Порівняння коефіцієнтів. Кешбек та бонуси від різних букмекерів. До £2200+.',
            'link': 'https://oddschecker.com',
            'source': 'OddsChecker',
            'emoji': '⭐',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 2200,
            'rating': 4.8,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['букмекер', 'кешбек', 'порівняння'],
        },
        {
            'title': '🎁 FreeBets - 10-100 фрі-бетів',
            'description': 'Портал фрі-бетів. Збирає кращі пропозиції букмекерів. 10-100 фрі-бетів щодня.',
            'link': 'https://freebets.com',
            'source': 'FreeBets',
            'emoji': '🎁',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 500,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['фрі-бети', 'бонуси', 'букмекер'],
        },
        {
            'title': '🏆 TalkSport - Спортивні бонуси',
            'description': 'Британський спортивний сайт. Бонуси букмекерів. Безплатні прогнози.',
            'link': 'https://talksport.com/betting',
            'source': 'TalkSport',
            'emoji': '🏆',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 200,
            'rating': 4.3,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['спорт', 'букмекер', 'прогнози'],
        },
        {
            'title': '👑 CasinoRewards - VIP програма',
            'description': 'Мережа казино (Bet365, Bwin, PokerStars). VIP програма. Кешбек, бонуси, турніри.',
            'link': 'https://casinorewards.com',
            'source': 'CasinoRewards',
            'emoji': '👑',
            'category': 'bonuses',
            'min_earning': 0,
            'max_earning': 1000,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['vip', 'кешбек', 'казино'],
        },
    ]

# ==================== КАТЕГОРІЯ 3: СКРИПТИ (9) ====================

def parse_scripts_and_tools() -> List[Dict[str, Any]]:
    """🛠️ Скрипти, софт та інструменти"""
    return [
        {
            'title': '⭐ GitHub - Open Source скрипти',
            'description': 'Репозиторій відкритого коду. Мільйони безплатних проектів. Скрипти, фреймворки, бібліотеки.',
            'link': 'https://github.com',
            'source': 'GitHub',
            'emoji': '⭐',
            'category': 'scripts',
            'difficulty': 'Medium',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.9,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['open source', 'код', 'безплатно'],
        },
        {
            'title': '💻 Codester - Готові скрипти',
            'description': 'Маркетплейс готових скриптів. PHP, JavaScript, Python та ін. Ціна $5-100. Ліцензовані скрипти.',
            'link': 'https://codester.com',
            'source': 'Codester',
            'emoji': '💻',
            'category': 'scripts',
            'difficulty': 'Easy',
            'min_earning': 0,
            'max_earning': 100,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['скрипти', 'готові', 'дешево'],
        },
        {
            'title': '🎯 CodeCanyon - Envato скрипти',
            'description': 'Маркетплейс Envato. Професійні скрипти, плагіни, компоненти. Ціна $5-500.',
            'link': 'https://codecanyon.net',
            'source': 'CodeCanyon',
            'emoji': '🎯',
            'category': 'scripts',
            'difficulty': 'Easy',
            'min_earning': 0,
            'max_earning': 500,
            'rating': 4.7,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['envato', 'преміум', 'скрипти'],
        },
        {
            'title': '❓ Stack Overflow - Q&A код',
            'description': 'Форум програмістів. Відповіді на питання про код. Готові розв\'язання та снипети.',
            'link': 'https://stackoverflow.com',
            'source': 'Stack Overflow',
            'emoji': '❓',
            'category': 'scripts',
            'difficulty': 'Medium',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.8,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['q&a', 'код', 'безплатно'],
        },
        {
            'title': '📝 Dev.to - Статті про код',
            'description': 'Комьюніті розробників. Статті, туторіали, готові розв\'язання. Безплатно.',
            'link': 'https://dev.to',
            'source': 'Dev.to',
            'emoji': '📝',
            'category': 'scripts',
            'difficulty': 'Easy',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['статті', 'туторіали', 'безплатно'],
        },
        {
            'title': '🎬 Celtx - Софт для сценаристів',
            'description': 'SaaS для написання сценаріїв. Шаблони, форматування, хмарне сховище.',
            'link': 'https://celtx.com',
            'source': 'Celtx',
            'emoji': '🎬',
            'category': 'scripts',
            'difficulty': 'Easy',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.4,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['saas', 'сценарії', 'хмара'],
        },
        {
            'title': '🚀 Product Hunt - Нові додатки',
            'description': 'Агрегатор нових додатків та інструментів. Рейтинг, відгуки. Кожен день нові проекти.',
            'link': 'https://producthunt.com',
            'source': 'Product Hunt',
            'emoji': '🚀',
            'category': 'scripts',
            'difficulty': 'Very Easy',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['нове', 'додатки', 'інструменти'],
        },
        {
            'title': '👥 Reddit - Комьюніті розробників',
            'description': 'Форум Reddit. r/learnprogramming, r/coding та ін. Обговорення, поради, готові розв\'язання.',
            'link': 'https://reddit.com',
            'source': 'Reddit',
            'emoji': '👥',
            'category': 'scripts',
            'difficulty': 'Easy',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['форум', 'комьюніті', 'обговорення'],
        },
        {
            'title': '📚 Udemy - Курси по коду',
            'description': 'Платформа онлайн-курсів. Курси програмування. Ціна $10-200. Пожиттєвий доступ.',
            'link': 'https://udemy.com',
            'source': 'Udemy',
            'emoji': '📚',
            'category': 'scripts',
            'difficulty': 'Easy',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['курси', 'навчання', 'код'],
        },
    ]

# ==================== КАТЕГОРІЯ 4: НОВІ ПРОПОЗИЦІЇ (9) ====================

def parse_new_proposals() -> List[Dict[str, Any]]:
    """💡 Нові пропозиції та приховані самородки"""
    return [
        {
            'title': '🌍 Reddit r/beermoneyglobal - Мікротаски',
            'description': 'Комьюніті 500K+ юзерів. Обговорення способів заробітку. Оновлення щодня.',
            'link': 'https://reddit.com/r/beermoneyglobal',
            'source': 'Reddit',
            'emoji': '🌍',
            'category': 'proposals',
            'difficulty': 'Very Easy',
            'min_earning': 1,
            'max_earning': 100,
            'rating': 4.4,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['reddit', 'комьюніті', 'мікро'],
        },
        {
            'title': '👥 Facebook Groups - Локальні групи',
            'description': 'Групи по заробіткам. "Make Money Online", "Side Hustle" та ін. Тисячі активних учасників.',
            'link': 'https://facebook.com',
            'source': 'Facebook',
            'emoji': '👥',
            'category': 'proposals',
            'difficulty': 'Very Easy',
            'min_earning': 1,
            'max_earning': 500,
            'rating': 4.3,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['facebook', 'групи', 'локально'],
        },
        {
            'title': '❓ Quora - Q&A та спонсорство',
            'description': 'Q&A платформа. Заробляй на питаннях через Quora Partner Program. $100-1000/місяць.',
            'link': 'https://quora.com',
            'source': 'Quora',
            'emoji': '❓',
            'category': 'proposals',
            'difficulty': 'Medium',
            'min_earning': 0,
            'max_earning': 1000,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['q&a', 'спонсорство', 'контент'],
        },
        {
            'title': '📱 Telegram - Боти та канали',
            'description': 'Telegram канали по заробіткам. Боти для автоматизації. Мільйони груп з актуальною інформацією.',
            'link': 'https://t.me',
            'source': 'Telegram',
            'emoji': '📱',
            'category': 'proposals',
            'difficulty': 'Very Easy',
            'min_earning': 0,
            'max_earning': 1000,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['telegram', 'боти', 'канали'],
        },
        {
            'title': '🔗 LinkedIn Groups - Професіонали',
            'description': 'Професійні групи. Мережеві можливості. Пошук клієнтів та партнерів.',
            'link': 'https://linkedin.com',
            'source': 'LinkedIn',
            'emoji': '🔗',
            'category': 'proposals',
            'difficulty': 'Medium',
            'min_earning': 100,
            'max_earning': 10000,
            'rating': 4.7,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['linkedin', 'професіонали', 'клієнти'],
        },
        {
            'title': '🛡️ BountyHub - Bug Bounty програми',
            'description': 'Платформа для баг-охоти. Великі компанії платять за пошук уразливостей. $100-5000+ за баг.',
            'link': 'https://bountyhub.io',
            'source': 'BountyHub',
            'emoji': '🛡️',
            'category': 'proposals',
            'difficulty': 'Hard',
            'min_earning': 100,
            'max_earning': 5000,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['security', 'bug bounty', 'високо'],
        },
        {
            'title': '💼 FL.ru - Фриланс для СНД',
            'description': 'Російськомовна біржа фрилансерів. Проекти від 100 руб до безмежності. Комісія 10%.',
            'link': 'https://fl.ru',
            'source': 'FL.ru',
            'emoji': '💼',
            'category': 'proposals',
            'difficulty': 'Easy',
            'min_earning': 10,
            'max_earning': 1000,
            'rating': 4.4,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['фриланс', 'снд', 'проекти'],
        },
        {
            'title': '🤖 Amazon Turk - Механічний турк',
            'description': 'Amazon MTurk. Мікротаски. $0.01-50 за завдання. Вимагає VPN + US адреса.',
            'link': 'https://mturk.com',
            'source': 'Amazon Turk',
            'emoji': '🤖',
            'category': 'proposals',
            'difficulty': 'Very Easy',
            'min_earning': 1,
            'max_earning': 100,
            'rating': 4.3,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['amazon', 'мікро', 'турк'],
        },
        {
            'title': '📰 Side Hustle - Збірка ідей',
            'description': 'Сайт зі зібраними ідеями для заробітку. Статті, гайди, оновлення. Безплатно.',
            'link': 'https://sidehustlestack.co',
            'source': 'Side Hustle',
            'emoji': '📰',
            'category': 'proposals',
            'difficulty': 'Very Easy',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['ідеї', 'гайди', 'натхнення'],
        },
    ]

# ==================== КАТЕГОРІЯ 5: СІРІ НІШІ - СНД (3) ====================

def parse_grey_niche_cis() -> List[Dict[str, Any]]:
    """🕷️ Сірі ніші - СНД форуми ⚠️"""
    return [
        {
            'title': '⚠️ XSS.is - Форум кібербезпеки (ЧОРНИЙ)',
            'description': '🛑 ФОРУМ НАВЧАЛЬНИЙ. Обговорення взломів, 0-day, RCE. Адміністратор Phaust заарештований 2024. Форум переживає відновлення.',
            'link': 'https://xss.is',
            'source': 'XSS.is',
            'emoji': '⚠️',
            'category': 'grey_niche_cis',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 100000,
            'rating': 3.2,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['хак', 'взлом', 'illegal'],
            'warning': '🛑 НЕЗАКОННО! СБУ, ФБР, Europol моніторять! Вимагає Tor, VPN, PGP!'
        },
        {
            'title': '⚠️ Exploit.in - Форум уразливостей (ЧОРНИЙ)',
            'description': '🛑 ФОРУМ НАВЧАЛЬНИЙ. 0-day, експлойти, RCE. Активен з 2006. Вимагає репутації для доступу.',
            'link': 'https://exploit.in',
            'source': 'Exploit.in',
            'emoji': '⚠️',
            'category': 'grey_niche_cis',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 50000,
            'rating': 3.4,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['експлойт', 'взлом', 'illegal'],
            'warning': '🛑 НЕЗАКОННО! Тільки Tor + VPN + PGP!'
        },
        {
            'title': '⚠️ Duty Free - RaaS & DDoS (ЧОРНИЙ)',
            'description': '🛑 ФОРУМ ПОСЛУГ. Послуги DDoS, бот-нет, фіш. Ціни $50-5000. Активен на Tor та clearnet.',
            'link': 'https://dutyfree.onion',
            'source': 'Duty Free',
            'emoji': '⚠️',
            'category': 'grey_niche_cis',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 100000,
            'rating': 2.8,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['ddos', 'raas', 'illegal'],
            'warning': '🛑 НЕЗАКОННО! ФБР відстежує рублі та крипто!'
        },
    ]

# ==================== КАТЕГОРІЯ 6: СІРІ НІШІ - ЄВРОПА (6) ====================

def parse_grey_niche_europe() -> List[Dict[str, Any]]:
    """🌐 Сірі ніші - Європейські форуми ⚠️"""
    return [
        {
            'title': '⚠️ Cracked.sh - Credentials & Malware (СІРИЙ)',
            'description': '🛑 ФОРУМ ЗАКРИТИЙ 01/2025. Тільки клони та архіви. Було: бази даних вкрадених аккаунтів, малвер, інструменти. Вимагала входу через Tor.',
            'link': 'https://cracked.io (закритий)',
            'source': 'Cracked.sh',
            'emoji': '⚠️',
            'category': 'grey_niche_europe',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 50000,
            'rating': 2.5,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['credentials', 'malware', 'закритий'],
            'warning': '🛑 ЗАКРИТИЙ! Europol закрив 01/2025'
        },
        {
            'title': '⚠️ Nulled.io - Hacking Tools (СІРИЙ)',
            'description': '🛑 ФОРУМ ЗАКРИТИЙ 01/2025. Тільки клони. Було: готові фіш-кіти, сплити, інструменти для взлому. Ціни $1-1000.',
            'link': 'https://nulled.to (клон)',
            'source': 'Nulled.io',
            'emoji': '⚠️',
            'category': 'grey_niche_europe',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 100000,
            'rating': 2.3,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['phishing', 'tools', 'закритий'],
            'warning': '🛑 ЗАКРИТИЙ! Europol закрив головний форум'
        },
        {
            'title': '⚠️ LeakBase - Data Leaks (СІРИЙ)',
            'description': '🛑 АКТИВЕН. База вкрадених даних. Пошук по Email, Паролі, PII. Є Tor версія. Ціни від €0.01 до €100 за доступ.',
            'link': 'https://leakbase.io',
            'source': 'LeakBase',
            'emoji': '⚠️',
            'category': 'grey_niche_europe',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 1000,
            'rating': 3.1,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['leaks', 'дані', 'пошук'],
            'warning': '🛑 НЕЗАКОННО! Володіння вкраденими даними - злочин!'
        },
        {
            'title': '⚠️ DarkForums - Leaks & Malware (СІРИЙ)',
            'description': '🛑 АКТИВЕН. Аналог XSS для Європи. Утечки даних, малвер, обговорення. Зростання 600% в 04-06/2025.',
            'link': 'https://darkforums.ru (Tor)',
            'source': 'DarkForums',
            'emoji': '⚠️',
            'category': 'grey_niche_europe',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 50000,
            'rating': 2.9,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['leaks', 'malware', 'торгівля'],
            'warning': '🛑 АКТИВНО МОНІТОРИТЬСЯ! Зростання 600% юзерів!'
        },
        {
            'title': '⚠️ Dread - Darknet News (СІРИЙ)',
            'description': '🛑 АКТИВЕН. Reddit для даркнета. Новини, обговорення, утечки. ТІЛЬКИ TOR. 100K+ юзерів.',
            'link': 'https://dread.onion',
            'source': 'Dread',
            'emoji': '⚠️',
            'category': 'grey_niche_europe',
            'difficulty': 'Medium',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 3.3,
            'legality': LegalityStatus.GREY.value,
            'verified': False,
            'tags': ['darknet', 'новини', 'tor-only'],
            'warning': '⚠️ Перегляд інформаційний, але купівля чого-небудь - злочин'
        },
        {
            'title': '⚠️ Sinister.ly - Cracking Services (СІРИЙ)',
            'description': '🛑 АКТИВЕН. Послуги крекінгу, фіш, соціальна інженерія. Менш відомий ніж Black Market, але активний.',
            'link': 'https://sinister.ly (Tor)',
            'source': 'Sinister.ly',
            'emoji': '⚠️',
            'category': 'grey_niche_europe',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 100000,
            'rating': 2.7,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['cracking', 'phishing', 'se'],
            'warning': '🛑 НЕЗАКОННО! 5-10 років тюрми!'
        },
    ]

# ==================== КАТЕГОРІЯ 7: СІРІ НІШІ - США (3) ====================

def parse_grey_niche_usa() -> List[Dict[str, Any]]:
    """🔗 Сірі ніші - Американські форуми ⚠️"""
    return [
        {
            'title': '⚠️ BreachForums - Databases (ЧОРНИЙ)',
            'description': '🛑 ВІДНОВЛЕНИЙ після закриття ФБР 05/2024. Було закрито, тепер новий форум. 290K юзерів. Утечки баз даних, аккаунтів, PII.',
            'link': 'https://breachforums.com',
            'source': 'BreachForums',
            'emoji': '⚠️',
            'category': 'grey_niche_usa',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 100000,
            'rating': 2.6,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['databases', 'breaches', 'usa'],
            'warning': '🛑 ФБР ЛОВ! Закривали раніше, можуть закрити знову!'
        },
        {
            'title': '⚠️ BlackHatWorld - SEO Gray Hat (СІРИЙ)',
            'description': '🛑 АКТИВЕН. SEO форум, але багато gray-hat контенту. Спам-техніки, чорний SEO, фіш. 200K+ юзерів.',
            'link': 'https://blackhatworld.com',
            'source': 'BlackHatWorld',
            'emoji': '⚠️',
            'category': 'grey_niche_usa',
            'difficulty': 'Hard',
            'min_earning': 0,
            'max_earning': 10000,
            'rating': 3.4,
            'legality': LegalityStatus.GREY.value,
            'verified': False,
            'tags': ['seo', 'gray-hat', 'spam'],
            'warning': '⚠️ Частина контенту може бути незаконна'
        },
        {
            'title': '⚠️ OGUsers - Account Trading (ЧОРНИЙ)',
            'description': '🛑 АКТИВЕН. Торгівля аккаунтами, SIM-swapping, взломи. 17+ великих взломів. Спеціалізація: Instagram, Twitter, Email.',
            'link': 'https://ogusers.com',
            'source': 'OGUsers',
            'emoji': '⚠️',
            'category': 'grey_niche_usa',
            'difficulty': 'Very Hard',
            'min_earning': 0,
            'max_earning': 100000,
            'rating': 2.4,
            'legality': LegalityStatus.BLACK.value,
            'verified': False,
            'tags': ['accounts', 'sim-swap', 'взломи'],
            'warning': '🛑 НЕЗАКОННО! 10-15 років тюрми за SIM-swap!'
        },
    ]

# ==================== КАТЕГОРІЯ 8: ЛЕГАЛЬНІ МАРКЕТПЛЕЙСИ (4) ====================

def parse_legal_marketplaces() -> List[Dict[str, Any]]:
    """⚖️ Легальні маркетплейси"""
    return [
        {
            'title': '💜 CPA.rip - СНД Арбітраж оферів',
            'description': 'Російськомовна CPA мережа. Тисячі офер. Заробіток $10-10000+/місяць. Вимагає досвіду в арбітражі.',
            'link': 'https://cpa.rip',
            'source': 'CPA.rip',
            'emoji': '💜',
            'category': 'legal_marketplaces',
            'difficulty': 'Hard',
            'min_earning': 10,
            'max_earning': 10000,
            'rating': 4.3,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['cpa', 'арбітраж', 'снд'],
        },
        {
            'title': '🎨 CodeCanyon - Envato Scripts',
            'description': 'Маркетплейс готових скриптів. PHP, JS, Python та ін. Ціна $1-500. Пожиттєва ліцензія.',
            'link': 'https://codecanyon.net',
            'source': 'CodeCanyon',
            'emoji': '🎨',
            'category': 'legal_marketplaces',
            'difficulty': 'Easy',
            'min_earning': 0,
            'max_earning': 500,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['scripts', 'envato', 'код'],
        },
        {
            'title': '🎁 AppSumo - Lifetime Deals',
            'description': 'Маркетплейс знижок на програмне забезпечення. Lifetime deals, знижки 50-90%. Економія $100-10000+.',
            'link': 'https://appsumo.com',
            'source': 'AppSumo',
            'emoji': '🎁',
            'category': 'legal_marketplaces',
            'difficulty': 'Very Easy',
            'min_earning': 0,
            'max_earning': 0,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['знижки', 'software', 'deals'],
        },
        {
            'title': '🇺🇦 Useme/Freelancehunt - UA Фриланс',
            'description': 'Українські фриланс-біржі. Проекти від 100 грн до безмежності. Комісія 10-20%.',
            'link': 'https://useme.com.ua',
            'source': 'Useme',
            'emoji': '🇺🇦',
            'category': 'legal_marketplaces',
            'difficulty': 'Easy',
            'min_earning': 50,
            'max_earning': 5000,
            'rating': 4.4,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['фриланс', 'україна', 'проекти'],
        },
    ]

# ==================== КАТЕГОРІЯ 9: ПОЗНАНЬ ГІГИ (9) ====================

def parse_poznan_gigs() -> List[Dict[str, Any]]:
    """🇵🇱 Роботи в Познані"""
    return [
        {
            'title': '🌆 OLX.pl - Praca dodatkowa Poznań',
            'description': '🇵🇱 Найбільша дошка оголошень Польщі. Роботи від 30-51 zł/год.',
            'link': 'https://www.olx.pl/d/s/prace-dodatkowe-poznan/',
            'source': 'OLX.pl',
            'emoji': '🌆',
            'category': 'poznan_gigs',
            'difficulty': 'Easy',
            'min_earning': 30,
            'max_earning': 51,
            'rating': 4.8,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['praca dodatkowa', 'poznań', 'доставка']
        },
        {
            'title': '🔍 Jooble.org - 116K+ пропозицій',
            'description': '🇵🇱 Агрегатор вакансій. 116K+ пропозицій для Познаня. 32-80 zł/год.',
            'link': 'https://jooble.org/jobs-poznan?a=true',
            'source': 'Jooble.org',
            'emoji': '🔍',
            'category': 'poznan_gigs',
            'difficulty': 'Easy',
            'min_earning': 32,
            'max_earning': 80,
            'rating': 4.7,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['агрегатор', 'позиції', 'гнучкий']
        },
        {
            'title': '💼 Indeed.pl - 25+ офертів',
            'description': '🇵🇱 Міжнародна платформа. Barista, kierowca, pakowacz. 28-50 zł/год.',
            'link': 'https://www.indeed.com/jobs?q=praca+dodatkowa&l=Poznan',
            'source': 'Indeed.pl',
            'emoji': '💼',
            'category': 'poznan_gigs',
            'difficulty': 'Easy',
            'min_earning': 28,
            'max_earning': 50,
            'rating': 4.6,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['indeed', 'part-time', 'weekend']
        },
        {
            'title': '⚡ Tikrow.com - Uber для праці',
            'description': '🇵🇱 Інноваційна платформа. Uber-стиль для роботи. 35-60 zł/год.',
            'link': 'https://www.tikrow.com',
            'source': 'Tikrow.com',
            'emoji': '⚡',
            'category': 'poznan_gigs',
            'difficulty': 'Medium',
            'min_earning': 35,
            'max_earning': 60,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['uber для праці', 'гнучкий', 'мобільний']
        },
        {
            'title': '👥 Facebook Groups - Real-time',
            'description': '🇵🇱 Група "Praca dorywcza Poznań". Прямий контакт з роботодавцями. 25-45 zł/год.',
            'link': 'https://www.facebook.com/groups/praca.poznan.dorywcza/',
            'source': 'Facebook',
            'emoji': '👥',
            'category': 'poznan_gigs',
            'difficulty': 'Easy',
            'min_earning': 25,
            'max_earning': 45,
            'rating': 4.4,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['facebook', 'спільнота', 'місцеві']
        },
        {
            'title': '🏘️ Lento.pl - Локальна дошка',
            'description': '🇵🇱 Локальна дошка Познаня. Будівництво, прибирання. 30-48 zł/год.',
            'link': 'https://poznan.lento.pl/s/praca-dodatkowa/',
            'source': 'Lento.pl',
            'emoji': '🏘️',
            'category': 'poznan_gigs',
            'difficulty': 'Easy',
            'min_earning': 30,
            'max_earning': 48,
            'rating': 4.3,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['локальна', 'будівництво', 'прибирання']
        },
        {
            'title': '⚙️ Strefajob.pl - От одразу',
            'description': '🇵🇱 Спеціалізований портал. Робота одразу. Премії та бонуси. 32-52 zł/год.',
            'link': 'https://www.strefajob.pl',
            'source': 'Strefajob.pl',
            'emoji': '⚙️',
            'category': 'poznan_gigs',
            'difficulty': 'Easy',
            'min_earning': 32,
            'max_earning': 52,
            'rating': 4.4,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['від одразу', 'премії', 'розова']
        },
        {
            'title': '🏢 Randstad.pl - Агенція',
            'description': '🇵🇱 Агенція тимчасової праці. Магазин, логістика. 35-60 zł/год.',
            'link': 'https://www.randstad.pl/praca/?lokalizacja=poznan',
            'source': 'Randstad.pl',
            'emoji': '🏢',
            'category': 'poznan_gigs',
            'difficulty': 'Medium',
            'min_earning': 35,
            'max_earning': 60,
            'rating': 4.5,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['агенція', 'контракт', 'магазин']
        },
        {
            'title': '📦 InPost/Amazon/RGIS',
            'description': '🇵🇱 Великі компанії. Інвентаризація, логістика. 28-45 zł/год.',
            'link': 'https://www.inpost.pl/pl',
            'source': 'InPost/Amazon/RGIS',
            'emoji': '📦',
            'category': 'poznan_gigs',
            'difficulty': 'Hard',
            'min_earning': 28,
            'max_earning': 45,
            'rating': 4.2,
            'legality': LegalityStatus.LEGAL.value,
            'verified': True,
            'tags': ['пакети', 'логістика', 'постійні']
        },
    ]

# ==================== ГОЛОВНА ФУНКЦІЯ ====================

def get_all_opportunities() -> List[Dict[str, Any]]:
    """Отримати ВСІ 58 можливостей"""
    opportunities = [
        *parse_earnings(),           # 9
        *parse_bonuses(),            # 9
        *parse_scripts_and_tools(),  # 9
        *parse_new_proposals(),      # 9
        *parse_grey_niche_cis(),     # 3
        *parse_grey_niche_europe(),  # 6
        *parse_grey_niche_usa(),     # 3
        *parse_legal_marketplaces(), # 4
        *parse_poznan_gigs(),        # 9
    ]  # ИТОГО: 58
    
    for opp in opportunities:
        opp['updated_at'] = datetime.now().isoformat()
        opp['created_at'] = datetime.now().isoformat()
    
    return opportunities


def get_opportunities_by_category(category: str) -> List[Dict[str, Any]]:
    """Отримати можливості за категорією"""
    all_opps = get_all_opportunities()
    return [opp for opp in all_opps if opp.get('category') == category]


if __name__ == '__main__':
    opps = get_all_opportunities()
    print(f"✅ Всього можливостей: {len(opps)}")
    print()
    
    # Статистика по категоріях
    categories = {}
    for opp in opps:
        cat = opp.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("📊 Розподіл по категоріях:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    print(f"\n🎉 ВСЬОГО: {len(opps)} можливостей!")
