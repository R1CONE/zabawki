import ctypes
# 1. Tworzymy strukturę danych w pamięci (tak jak w plikach DLL)
class GraPamięć(ctypes.Structure):
    _fields_ = [
        ("jakies_dane", ctypes.c_byte * 64),  # 64 bajty innych danych (tworzą odstęp/offset)
        ("moja_zmienna", ctypes.c_int),       # Liczba całkowita (4 bajty), np. HP = 100
        ("flaga_aktywna", ctypes.c_bool)      # Wartość bool (True/False)
    ]
# 2. Alokujemy (tworzymy) tę strukturę w pamięci RAM
instancja = GraPamięć()
instancja.moja_zmienna = 100
instancja.flaga_aktywna = True
# 3. Pobieramy adres bazowy, pod którym system umieścił ten obiekt
base_address = ctypes.addressof(instancja)
# 4. Sprawdzamy offsety (przesunięcia bajtowe) zdefiniowane w strukturze:
# 'jakies_dane' zajmują 64 bajty, więc 'moja_zmienna' zaczyna się dokładnie po 64 bajtach
offset_zmienna = GraPamięć.moja_zmienna.offset    # Wynik: 64 bajty (0x40)
offset_flaga = GraPamięć.flaga_aktywna.offset      # Wynik: 68 bajtów (0x44)
# 5. Obliczamy rzeczywiste adresy w RAM
real_address_zmienna = base_address + offset_zmienna
real_address_flaga = base_address + offset_flaga
print(f"Adres bazowy obiektu:    {hex(base_address)}")
print(f"Offset dla moja_zmienna: {offset_zmienna} bajtów ({hex(offset_zmienna)})")
print(f"Rzeczywisty adres w RAM: {hex(real_address_zmienna)}")
print("-" * 40)
# 6. Odczytujemy wartość bezpośrednio z wyliczonego adresu w pamięci RAM
odczytany_int = ctypes.c_int.from_address(real_address_zmienna).value
odczytany_bool = ctypes.c_bool.from_address(real_address_flaga).value
print(f"Odczytano spod adresu moja_zmienna: {odczytany_int}")
print(f"Odczytano spod adresu flaga_aktywna: {odczytany_bool}")
