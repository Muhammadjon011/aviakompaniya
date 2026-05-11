# ============================================================
#   AVIAKOMPANIYA BOSHQARUV TIZIMI — 10 ta sinf
# ============================================================

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random


# ============================================================
# 1. SHAXS (asosiy abstrakt sinf)
# ============================================================
class Shaxs(ABC):
    def __init__(self, ism: str, yosh: int, passport: str):
        self.ism = ism
        self.yosh = yosh
        self.passport = passport

    @abstractmethod
    def rol(self) -> str:
        pass

    def __str__(self):
        return f"{self.ism} ({self.yosh} yosh) — {self.rol()}"


# ============================================================
# 2. YO'LOVCHI
# ============================================================
class Yolovchi(Shaxs):
    def __init__(self, ism: str, yosh: int, passport: str, millat: str):
        super().__init__(ism, yosh, passport)
        self.millat = millat
        self._pul = 0.0
        self._chipta_tarixi: list["Chipta"] = []
        self._mil_lar = 0  # bonus millar

    def rol(self) -> str:
        return "Yo'lovchi"

    def pul_qoshish(self, miqdor: float):
        self._pul += miqdor

    def tolov_qilish(self, miqdor: float) -> bool:
        if self._pul >= miqdor:
            self._pul -= miqdor
            print(f"{self.ism} ${miqdor:.0f} to'ladi. Qoldiq: ${self._pul:.0f}")
            return True
        print(f"{self.ism}da yetarli pul yo'q! Kerak: ${miqdor:.0f}, Bor: ${self._pul:.0f}")
        return False

    def mil_qoshish(self, mil: int):
        self._mil_lar += mil
        print(f"{self.ism}ga {mil} mil qo'shildi. Jami: {self._mil_lar} mil")

    def profil(self):
        print(f"\n{self.ism} profili:")
        print(f"  Passport : {self.passport}")
        print(f"  Millat   : {self.millat}")
        print(f"  Balans   : ${self._pul:.0f}")
        print(f"  Millar   : {self._mil_lar}")
        print(f"  Safarlar : {len(self._chipta_tarixi)} ta")


# ============================================================
# 3. PILOT
# ============================================================
class Pilot(Shaxs):
    def __init__(self, ism: str, yosh: int, passport: str,
                 litsenziya: str, tajriba_yil: int):
        super().__init__(ism, yosh, passport)
        self.litsenziya = litsenziya
        self.tajriba_yil = tajriba_yil
        self._uchgan_soat = 0
        self._oylik = 5000 + tajriba_yil * 200

    def rol(self) -> str:
        return "Pilot"

    def uchish(self, soat: float):
        self._uchgan_soat += soat
        bonus = soat * 50
        self._oylik += bonus
        print(f"Pilot {self.ism} {soat} soat uchdi. Bonus: ${bonus:.0f}")

    def statistika(self):
        print(f"\nPilot {self.ism}:")
        print(f"  Litsenziya    : {self.litsenziya}")
        print(f"  Tajriba       : {self.tajriba_yil} yil")
        print(f"  Uchgan soat   : {self._uchgan_soat} soat")
        print(f"  Maosh         : ${self._oylik:.0f}")


# ============================================================
# 4. STYUARDESSA
# ============================================================
class Styuardessa(Shaxs):
    def __init__(self, ism: str, yosh: int, passport: str,
                 tillar: list[str], oylik: float):
        super().__init__(ism, yosh, passport)
        self.tillar = tillar
        self.oylik = oylik
        self._xizmat_soni = 0

    def rol(self) -> str:
        return "Styuardessa"

    def xush_kelibsiz(self, yolovchi: Yolovchi):
        til = random.choice(self.tillar)
        salom = {"uz": "Xush kelibsiz!", "en": "Welcome!", "ru": "Добро пожаловать!"}
        print(f"{self.ism}: '{salom.get(til, 'Salom!')}' — {yolovchi.ism}ga")
        self._xizmat_soni += 1

    def taom_tarqatish(self, salon: "Salon"):
        print(f"{self.ism} {salon.nomi}da taom tarqatmoqda...")
        for o in salon._o_rindiqlar.values():
            if o:
                print(f"  → {o.ism}ga taom berildi")
        self._xizmat_soni += 1


# ============================================================
# 5. SAMOLYOT
# ============================================================
class Samolyot:
    def __init__(self, model: str, raqam: str,
                 sig_im: int, diapazon_km: int):
        self.model = model
        self.raqam = raqam
        self.sig_im = sig_im
        self.diapazon_km = diapazon_km
        self._uchgan_soat = 0
        self._holat = "tayyor"  # tayyor / uchmoqda / texnik

    def texnik_tekshirish(self):
        self._holat = "texnik"
        print(f"{self.raqam} texnik tekshiruvda...")
        self._holat = "tayyor"
        print(f"{self.raqam} tayyor.")

    def uchish_boshlash(self, reys: "Reys"):
        if self._holat != "tayyor":
            print(f"{self.raqam} hozir uchishga tayyor emas!")
            return False
        self._holat = "uchmoqda"
        print(f"{self.raqam} ({self.model}) uchdi → {reys.manzil}")
        return True

    def qonish(self):
        self._holat = "tayyor"
        print(f"{self.raqam} qo'ndi.")

    def __str__(self):
        return f"{self.model} | {self.raqam} | {self.sig_im} o'rin | {self._holat}"


# ============================================================
# 6. SALON
# ============================================================
class Salon:
    def __init__(self, nomi: str, sinf: str, joy_soni: int, narx_koef: float):
        self.nomi = nomi
        self.sinf = sinf
        self.joy_soni = joy_soni
        self.narx_koef = narx_koef
        self._o_rindiqlar: dict[str, Yolovchi | None] = {
            f"{sinf[0]}{i+1}": None for i in range(joy_soni)
        }

    def joy_bor_mi(self) -> bool:
        return any(v is None for v in self._o_rindiqlar.values())

    def joy_olish(self, yolovchi: Yolovchi) -> str | None:
        for joy, egasi in self._o_rindiqlar.items():
            if egasi is None:
                self._o_rindiqlar[joy] = yolovchi
                print(f"{yolovchi.ism} → {self.nomi} | Joy: {joy}")
                return joy
        print(f"{self.nomi} to'liq!")
        return None

    def holat(self):
        band = sum(1 for v in self._o_rindiqlar.values() if v)
        print(f"\n{self.nomi} ({self.sinf}): {band}/{self.joy_soni} band")
        for joy, egasi in self._o_rindiqlar.items():
            ism = egasi.ism if egasi else "bo'sh"
            print(f"  {joy}: {ism}")


# ============================================================
# 7. CHIPTA
# ============================================================
class Chipta:
    _hisoblagich = 1000

    def __init__(self, yolovchi: Yolovchi, reys: "Reys",
                 salon: Salon, joy: str):
        Chipta._hisoblagich += 1
        self.raqam = f"UZ{Chipta._hisoblagich}"
        self.yolovchi = yolovchi
        self.reys = reys
        self.salon = salon
        self.joy = joy
        self.narx = reys.asosiy_narx * salon.narx_koef
        self.sana = datetime.now().strftime("%d.%m.%Y %H:%M")
        self._bekor = False

    def chop_etish(self):
        print(f"\n{'─'*40}")
        print(f"  AVIACHIP TA #{self.raqam}")
        print(f"{'─'*40}")
        print(f"  Yo'lovchi : {self.yolovchi.ism}")
        print(f"  Reys      : {self.reys.raqam}")
        print(f"  Yo'nalish : {self.reys.manba} → {self.reys.manzil}")
        print(f"  Sana      : {self.reys.vaqt}")
        print(f"  Sinf      : {self.salon.sinf}")
        print(f"  Joy       : {self.joy}")
        print(f"  Narx      : ${self.narx:.0f}")
        print(f"{'─'*40}")

    def bekor_qilish(self):
        if self._bekor:
            print("Chipta allaqachon bekor qilingan!")
            return
        self._bekor = True
        qaytarish = self.narx * 0.8
        self.yolovchi._pul += qaytarish
        self.salon._o_rindiqlar[self.joy] = None
        print(f"{self.raqam} chipta bekor qilindi. "
              f"${qaytarish:.0f} qaytarildi.")

    def __str__(self):
        holat = "bekor" if self._bekor else "faol"
        return f"Chipta {self.raqam} | {self.reys.raqam} | {self.joy} | [{holat}]"


# ============================================================
# 8. REYS
# ============================================================
class Reys:
    def __init__(self, raqam: str, manba: str, manzil: str,
                 vaqt: str, davomiylik_soat: float, asosiy_narx: float):
        self.raqam = raqam
        self.manba = manba
        self.manzil = manzil
        self.vaqt = vaqt
        self.davomiylik_soat = davomiylik_soat
        self.asosiy_narx = asosiy_narx
        self.samolyot: Samolyot | None = None
        self.pilot: Pilot | None = None
        self.salonlar: list[Salon] = []
        self._holat = "rejalashtirilgan"

    def samolyot_biriktirish(self, samolyot: Samolyot):
        self.samolyot = samolyot
        print(f"{self.raqam} reysiga {samolyot.raqam} biriktirildi.")

    def pilot_biriktirish(self, pilot: Pilot):
        self.pilot = pilot
        print(f"{self.raqam} reysiga Pilot {pilot.ism} biriktirildi.")

    def salon_qoshish(self, salon: Salon):
        self.salonlar.append(salon)

    def uchish(self):
        if not self.samolyot or not self.pilot:
            print("Samolyot yoki pilot biriktirilmagan!")
            return
        if self.samolyot.uchish_boshlash(self):
            self._holat = "uchmoqda"
            self.pilot.uchish(self.davomiylik_soat)
            print(f"\nReys {self.raqam}: {self.manba} → {self.manzil}")
            print(f"  Davomiyligi: {self.davomiylik_soat} soat")

    def qonish(self):
        if self.samolyot:
            self.samolyot.qonish()
        self._holat = "yetib keldi"
        print(f"Reys {self.raqam} {self.manzil}ga yetib keldi!")

    def holat(self):
        band = sum(
            sum(1 for v in s._o_rindiqlar.values() if v)
            for s in self.salonlar
        )
        jami = sum(s.joy_soni for s in self.salonlar)
        print(f"\nReys {self.raqam}: {self.manba} → {self.manzil}")
        print(f"  Vaqt      : {self.vaqt}")
        print(f"  Holat     : {self._holat}")
        print(f"  To'lganlik: {band}/{jami} o'rin")
        print(f"  Narx      : ${self.asosiy_narx:.0f} dan")

    def __str__(self):
        return f"Reys {self.raqam}: {self.manba} → {self.manzil} | {self.vaqt}"


# ============================================================
# 9. AEROPORT
# ============================================================
class Aeroport:
    def __init__(self, nomi: str, shahar: str, kod: str):
        self.nomi = nomi
        self.shahar = shahar
        self.kod = kod
        self._reyslar: list[Reys] = []
        self._yo_lovchilar: list[Yolovchi] = []

    def reys_qoshish(self, reys: Reys):
        self._reyslar.append(reys)

    def yo_lovchi_royxat(self, yolovchi: Yolovchi):
        self._yo_lovchilar.append(yolovchi)

    def jadval(self):
        print(f"\n{self.nomi} ({self.kod}) — Reyslar jadvali:")
        print(f"{'─'*50}")
        for r in self._reyslar:
            print(f"  {r.raqam:8} | {r.manba:12} → {r.manzil:12} | {r.vaqt} | {r._holat}")

    def statistika(self):
        print(f"\n{self.nomi} statistikasi:")
        print(f"  Reyslar      : {len(self._reyslar)} ta")
        print(f"  Yo'lovchilar : {len(self._yo_lovchilar)} ta")


# ============================================================
# 10. AVIAKOMPANIYA (hamma narsani birlashtiradi)
# ============================================================
class Aviakompaniya:
    def __init__(self, nomi: str, kod: str):
        self.nomi = nomi
        self.kod = kod
        self.samolyotlar: list[Samolyot] = []
        self.pilotlar: list[Pilot] = []
        self.styuardessalar: list[Styuardessa] = []
        self.reyslar: list[Reys] = []
        self.aeroport: Aeroport | None = None
        self._jami_daromad = 0.0

    def samolyot_qoshish(self, samolyot: Samolyot):
        self.samolyotlar.append(samolyot)
        print(f"Samolyot qo'shildi: {samolyot}")

    def pilot_qoshish(self, pilot: Pilot):
        self.pilotlar.append(pilot)
        print(f"Pilot qo'shildi: {pilot.ism}")

    def styuardessa_qoshish(self, styuardessa: Styuardessa):
        self.styuardessalar.append(styuardessa)
        print(f"Styuardessa qo'shildi: {styuardessa.ism}")

    def reys_qoshish(self, reys: Reys):
        self.reyslar.append(reys)
        if self.aeroport:
            self.aeroport.reys_qoshish(reys)

    def aeroport_biriktirish(self, aeroport: Aeroport):
        self.aeroport = aeroport
        print(f"{self.nomi} → {aeroport.nomi}ga biriktirildi.")

    def chipta_sotish(self, yolovchi: Yolovchi,
                      reys: Reys, sinf: str = "Econom") -> Chipta | None:
        salon = next((s for s in reys.salonlar
                      if s.sinf == sinf and s.joy_bor_mi()), None)
        if not salon:
            print(f"{sinf} sinfida joy yo'q!")
            return None
        joy = salon.joy_olish(yolovchi)
        if not joy:
            return None
        chipta = Chipta(yolovchi, reys, salon, joy)
        if yolovchi.tolov_qilish(chipta.narx):
            yolovchi._chipta_tarixi.append(chipta)
            self._jami_daromad += chipta.narx
            mil = int(chipta.narx * 0.1)
            yolovchi.mil_qoshish(mil)
            if self.aeroport:
                self.aeroport.yo_lovchi_royxat(yolovchi)
            return chipta
        else:
            salon._o_rindiqlar[joy] = None
            return None

    def statistika(self):
        print(f"\n{'='*45}")
        print(f"  {self.nomi} ({self.kod})")
        print(f"{'='*45}")
        print(f"  Samolyotlar    : {len(self.samolyotlar)} ta")
        print(f"  Pilotlar       : {len(self.pilotlar)} ta")
        print(f"  Styuardessalar : {len(self.styuardessalar)} ta")
        print(f"  Reyslar        : {len(self.reyslar)} ta")
        print(f"  Jami daromad   : ${self._jami_daromad:,.0f}")


# ============================================================
# ISHLATISH
# ============================================================
if __name__ == "__main__":

    # --- Aviakompaniya ---
    uzairways = Aviakompaniya("Uzbekistan Airways", "HY")

    # --- Aeroport ---
    tashkent_airport = Aeroport("Islom Karimov nomidagi xalqaro aeroport",
                                "Toshkent", "TAS")
    uzairways.aeroport_biriktirish(tashkent_airport)

    # --- Samolyotlar ---
    print("\n--- SAMOLYOTLAR ---")
    s1 = Samolyot("Boeing 787",  "HY-001", 280, 14000)
    s2 = Samolyot("Airbus A320", "HY-002", 180, 6000)
    s3 = Samolyot("Boeing 737",  "HY-003", 160, 5000)

    uzairways.samolyot_qoshish(s1)
    uzairways.samolyot_qoshish(s2)
    uzairways.samolyot_qoshish(s3)

    # --- Pilotlar ---
    print("\n--- PILOTLAR ---")
    p1 = Pilot("Alisher Nazarov",  45, "AA1234567", "ATPL", 20)
    p2 = Pilot("Bobur Rahimov",    38, "BB7654321", "ATPL", 12)

    uzairways.pilot_qoshish(p1)
    uzairways.pilot_qoshish(p2)

    # --- Styuardessalar ---
    print("\n--- STYUARDESSALAR ---")
    st1 = Styuardessa("Nilufar Karimova",  27, "CC1111111", ["uz","en","ru"], 1200)
    st2 = Styuardessa("Malika Yusupova",   25, "DD2222222", ["uz","en"],      1100)

    uzairways.styuardessa_qoshish(st1)
    uzairways.styuardessa_qoshish(st2)

    # --- Reyslar ---
    print("\n--- REYSLAR ---")
    r1 = Reys("HY101", "Toshkent", "Dubay",   "10:00", 4.5, 350)
    r2 = Reys("HY202", "Toshkent", "Moskva",  "14:00", 3.5, 280)
    r3 = Reys("HY303", "Toshkent", "Istanbul","18:00", 5.0, 420)

    # Salonlar
    for reys, samolyot in [(r1, s1), (r2, s2), (r3, s3)]:
        biznes = Salon("Biznes sinfi", "Biznes", 20,  2.5)
        econom  = Salon("Econom sinfi",  "Econom", 140, 1.0)
        reys.salon_qoshish(biznes)
        reys.salon_qoshish(econom)
        reys.samolyot_biriktirish(samolyot)

    r1.pilot_biriktirish(p1)
    r2.pilot_biriktirish(p2)
    r3.pilot_biriktirish(p1)

    uzairways.reys_qoshish(r1)
    uzairways.reys_qoshish(r2)
    uzairways.reys_qoshish(r3)

    # --- Yo'lovchilar ---
    print("\n--- YO'LOVCHILAR ---")
    y1 = Yolovchi("Jasur Toshev",    30, "EE3333333", "O'zbekiston")
    y2 = Yolovchi("Shahnoza Mirova", 25, "FF4444444", "O'zbekiston")
    y3 = Yolovchi("Otabek Ergashev", 42, "GG5555555", "O'zbekiston")
    y4 = Yolovchi("Dildora Holiqova",35, "HH6666666", "O'zbekiston")

    y1.pul_qoshish(2000)
    y2.pul_qoshish(1500)
    y3.pul_qoshish(3000)
    y4.pul_qoshish(1000)

    # --- Chipta sotish ---
    print("\n--- CHIPTA SOTISH ---")
    c1 = uzairways.chipta_sotish(y1, r1, "Biznes")
    c2 = uzairways.chipta_sotish(y2, r1, "Econom")
    c3 = uzairways.chipta_sotish(y3, r2, "Biznes")
    c4 = uzairways.chipta_sotish(y4, r2, "Econom")
    c5 = uzairways.chipta_sotish(y1, r3, "Econom")

    # --- Chiptalarni chop etish ---
    print("\n--- CHIPTALAR ---")
    if c1: c1.chop_etish()
    if c3: c3.chop_etish()

    # --- Chipta bekor qilish ---
    print("\n--- CHIPTA BEKOR QILISH ---")
    if c4: c4.bekor_qilish()

    # --- Styuardessa xizmati ---
    print("\n--- STYUARDESSA XIZMATI ---")
    st1.xush_kelibsiz(y1)
    st1.xush_kelibsiz(y2)
    st2.taom_tarqatish(r1.salonlar[1])

    # --- Texnik tekshiruv ---
    print("\n--- TEXNIK TEKSHIRUV ---")
    s3.texnik_tekshirish()

    # --- Reyslar uchishi ---
    print("\n--- UCHISH ---")
    r1.uchish()
    r1.qonish()
    r2.uchish()
    r2.qonish()

    # --- Salon holati ---
    print("\n--- SALON HOLATI ---")
    r1.salonlar[0].holat()
    r1.salonlar[1].holat()

    # --- Reys holati ---
    print("\n--- REYSLAR HOLATI ---")
    for r in [r1, r2, r3]:
        r.holat()

    # --- Aeroport jadvali ---
    print("\n--- AEROPORT JADVALI ---")
    tashkent_airport.jadval()
    tashkent_airport.statistika()

    # --- Pilot statistikasi ---
    print("\n--- PILOT STATISTIKASI ---")
    p1.statistika()
    p2.statistika()

    # --- Yo'lovchi profili ---
    print("\n--- YO'LOVCHI PROFILI ---")
    y1.profil()
    y3.profil()

    # --- Aviakompaniya statistikasi ---
    uzairways.statistika()