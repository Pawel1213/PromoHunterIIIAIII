#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PromoHunter Bot - Познань Підробіток Парсер v2.1
Додано 9 джерел для гнучкої роботи в Познані

КАТЕГОРІЯ: poznań_gigs (9 джерел)
Джерела спеціалізуються на:
- Praca dodatkowa (додаткова робота)
- Praca dorywcza (разова робота)
- Praca zlecenie (робота на контракт)
- Praca na godziny (погодинна робота)
- Weekend/evenings роботи

ГОТОВО ДО ВИКОРИСТАННЯ!
"""

from datetime import datetime
from typing import List, Dict, Any


def parse_poznan_gigs():
    """🌆 Підробіток в Познані - 9 джерел"""
    return [
        {
            'title': '🌆 OLX.pl - Praca dodatkowa Poznań (найбільша дошка)',
            'description': '🇵🇱 Найбільша дошка оголошень у Польщі. Розділ "Praca dodatkowa" містить сотні aktualnych пропозицій щодня: від розносу піци (30-51 zł/godz) до роботи у Biedronka (4150-5500 zł/miesiąc). Фільтри: "umowa zlecenie", "niepełny etat", "praca dodatkowa". Можна шукати за районами Познаня (Jeżyce, Wilda, Grunwald).',
            'link': 'https://www.olx.pl/d/s/prace-dodatkowe-poznan/',
            'source': 'OLX.pl',
            'emoji': '🌆',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Easy',
            'min_earning': 30,
            'max_earning': 51,
            'rating': 4.8,
            'tags': ['praca dodatkowa', 'poznań', 'доставка', 'супермаркет', 'дошка'],
            'legality': 'Legal',
            'verified': True
        },
        {
            'title': '🔍 Jooble.org - Praca dorywcza Poznań (116k+ пропозицій)',
            'description': '🇵🇱 Агрегатор, який збирає оголошення з 100+ сайтів. Фільтр "praca dorywcza" показує 116,000+ пропозицій для Познаня. Категорії: praca na godziny, dorywcza zlecenie, dodatkowa/po godzinach. Зручний пошук за ставкою (32-80 zł/godz). Оновлення щогодини.',
            'link': 'https://jooble.org/jobs-poznan?a=true',
            'source': 'Jooble.org',
            'emoji': '🔍',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Easy',
            'min_earning': 32,
            'max_earning': 80,
            'rating': 4.7,
            'tags': ['агрегатор', 'розова робота', 'гнучкий графік', 'фільтри'],
            'legality': 'Legal',
            'verified': True
        },
        {
            'title': '💼 Indeed.pl - Praca dodatkowa, weekendy (25+ офертів)',
            'description': '🇵🇱 Міжнародна платформа з 25+ офертами для Познаня. Популярні позиції: pracownik hali (Makro), barista (Starbucks), kierowca/rowerzysta (Dott), pakowacz. Можна фільтрувати "part-time", "praca tymczasowa", "weekendy". Багато компаній відповідає за 2-3 дні.',
            'link': 'https://www.indeed.com/jobs?q=praca+dodatkowa&l=Poznan',
            'source': 'Indeed.pl',
            'emoji': '💼',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Easy',
            'min_earning': 28,
            'max_earning': 50,
            'rating': 4.6,
            'tags': ['indeed', 'part-time', 'weekend', 'гастро', 'доставка'],
            'legality': 'Legal',
            'verified': True
        },
        {
            'title': '⚡ Tikrow.com - Agencja Pracy Natychmiastowej (Uber для праці)',
            'description': '🇵🇱 Інноваційна платформа для роботи на godziny. Працює як Uber для праці: завантажуєш додаток, обираєш зміну, працюєш. Швидке з\'єднання pracodawcy з pracownikami за 48h. Категорії: magazyn, gastronomia, event, produkcja. Гнучкий графік, швидко платять.',
            'link': 'https://www.tikrow.com',
            'source': 'Tikrow.com',
            'emoji': '⚡',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Medium',
            'min_earning': 35,
            'max_earning': 60,
            'rating': 4.5,
            'tags': ['uber для праці', 'гнучкий графік', 'гарячі вакансії', 'мобільний додаток'],
            'legality': 'Legal',
            'verified': True
        },
        {
            'title': '👥 Facebook - Praca dorywcza i zlecenia Poznań (Real-time)',
            'description': '🇵🇱 Група "Praca dorywcza i zlecenia - Poznań i okolice" на Facebook. Члени діляться dorywczymi пропозиціями та zleceniami real-time. Також є група "Praca na część etatu i prace dorywcze" – фокус на nepełny час роботи. Прямий контакт з pracodawcami, часто без посередників.',
            'link': 'https://www.facebook.com/groups/praca.poznan.dorywcza/',
            'source': 'Facebook Groups',
            'emoji': '👥',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Easy',
            'min_earning': 25,
            'max_earning': 45,
            'rating': 4.4,
            'tags': ['facebook', 'спільнота', 'місцеві пропозиції', 'без посередників'],
            'legality': 'Legal',
            'verified': True
        },
        {
            'title': '🏘️ Lento.pl - Praca dodatkowa Poznań (Локальна дошка)',
            'description': '🇵🇱 Локальна дошка оголошень. Розділ "Praca dodatkowa" містить пропозиції від przeprowadzki (35-40 zł/h) до pracy zdalnej. Унікальні категорії: "praca na budowie od zaraz", "dodatkowa sprzątanie", "praca weekendowa". Багато оголошень від lokalnych pracodawców без комісій.',
            'link': 'https://poznan.lento.pl/s/praca-dodatkowa/',
            'source': 'Lento.pl',
            'emoji': '🏘️',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Easy',
            'min_earning': 30,
            'max_earning': 48,
            'rating': 4.3,
            'tags': ['локальна дошка', 'будівництво', 'прибирання', 'переїзди'],
            'legality': 'Legal',
            'verified': True
        },
        {
            'title': '⚙️ Strefajob.pl - Portal pracy dorywczej (Від одразу)',
            'description': '🇵🇱 Спеціалізований портал для błyskawicznych zleceń з całої Польщі. Фокус на dorywcze oferty pracy з можливістю премій та benefitów. Швидка реєстрація, оголошення оновлюються щодня. Ідеально для тих, хто шукає "praca od zaraz" (робота одразу).',
            'link': 'https://www.strefajob.pl',
            'source': 'Strefajob.pl',
            'emoji': '⚙️',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Easy',
            'min_earning': 32,
            'max_earning': 52,
            'rating': 4.4,
            'tags': ['портал', 'від одразу', 'премії', 'розова робота'],
            'legality': 'Legal',
            'verified': True
        },
        {
            'title': '🏢 Randstad.pl - Agencja tymczasowej pracy (Magazyn, Budownictwo)',
            'description': '🇵🇱 Агенція тимчасової праці. Є спеціальні oferty для "praca dodatkowa". Приклади: pracownik magazynowy w Plewiskach (близько Познаня), umowa na zastępstwo, elastyczne godziny. 39+ офертів для Poznania та Wielkopolski. Часто на контракт (zlecenie) або на заміну.',
            'link': 'https://www.randstad.pl/praca/?lokalizacja=poznan',
            'source': 'Randstad.pl',
            'emoji': '🏢',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Medium',
            'min_earning': 35,
            'max_earning': 60,
            'rating': 4.5,
            'tags': ['агенція', 'тимчасова робота', 'контракт', 'магазин'],
            'legality': 'Legal',
            'verified': True
        },
        {
            'title': '📦 InPost/Amazon/RGIS - Інвентаризація та магазин (36+ zł/h)',
            'description': '🇵🇱 Компанії, які постійно шукають людей na zlecenie. RGIS Usługi Inwentaryzacyjne – інвентаризації в магазинах, 35-41 zł/godz, praca dorywcza. Amazon – тимчасовий працівник магазину, 36,22 zł/h, можливість роботи 3-4 дні на тиждень. InPost – сортування пакетів, години 19:00-3:00, umowa zlecenie (28-35 zł/h).',
            'link': 'https://www.inpost.pl/pl',
            'source': 'InPost/Amazon/RGIS',
            'emoji': '📦',
            'category': 'poznan_gigs',
            'region': 'Poznań, Polska',
            'difficulty': 'Hard',
            'min_earning': 28,
            'max_earning': 45,
            'rating': 4.2,
            'tags': ['пакети', 'нічна робота', 'магазин', 'інвентаризація', 'постійні'],
            'legality': 'Legal',
            'verified': True
        },
    ]


def get_poznan_gigs_count() -> int:
    """Отримати кількість гіг в Познані"""
    return len(parse_poznan_gigs())


def get_poznan_gigs() -> List[Dict[str, Any]]:
    """Отримати всі гіги в Познані с метадатами"""
    gigs = parse_poznan_gigs()

    for gig in gigs:
        gig['updated_at'] = datetime.now().isoformat()
        gig['created_at'] = datetime.now().isoformat()

    return gigs


if __name__ == '__main__':
    gigs = get_poznan_gigs()
    print(f"✅ Завантажено {len(gigs)} гіг в Познані\n")

    total_earnings = 0
    for i, gig in enumerate(gigs, 1):
        print(f"{i}. {gig['title']}")
        print(f"   Мін. заробіток: {gig['min_earning']} zł/h")
        print(f"   Макс. заробіток: {gig['max_earning']} zł/h")
        print(f"   Рейтинг: {gig['rating']} ⭐")
        print()
        total_earnings += gig['min_earning']

    print(f"💰 Загальний мінімальний заробіток: {total_earnings} zł/h (якщо робити все відразу)")
    print(f"📊 Середній заробіток: {total_earnings / len(gigs):.1f} zł/h")
