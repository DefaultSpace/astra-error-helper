import re
import random

# Hata veritabanı - Tüm yaygın Python hataları dahil
error_database = {
    "SyntaxError": {
        "responses": [
            "Merhaba dostum! Sözdizimi hatası almışsın, bir yerlerde ufak bir hata var gibi.",
            "Hey, kodunda bir sözdizimi problemi var! Endişelenme, bunu çözebiliriz."
        ],
        "solutions": [
            "Kodunu satır satır kontrol et, parantezler ve girintiler doğru mu bak.",
            "Her açılan parantezin kapandığından emin ol!"
        ],
        "details": {
            "invalid syntax": "Bu, genelde yanlış bir yazım veya eksik bir şey yüzünden çıkar.",
            "expected ':'": "Kodunda bir `:` (iki nokta üst üste) eksik gibi. Genelde `if`, `for` veya fonksiyon tanımında olur.",
            "unterminated f-string literal": "f-string’in bir tırnak işareti eksik kalmış! Mesela `f'Bu` yerine `f'Bu'` olmalı."
        },
        "example": "Örnek: `if x == 5:` (Doğru) vs `if x == 5` (Yanlış)",
        "prevention": "Kod yazarken `if`, `for` gibi yapıların sonuna `:` koymayı unutma."
    },
    "NameError": {
        "responses": [
            "Tanımlanmamış bir şey mi kullanmaya çalıştın? Hata mesajında adı geçen şeye bakalım.",
            "Hmm, bir değişkeni unutmuşsun gibi görünüyor!"
        ],
        "solutions": [
            "O ismi kodunda önce tanımladığından emin ol, mesela `x = 5`.",
            "Değişkeni kullanmadan önce bir değer atadın mı?"
        ],
        "example": "Örnek: `x = 10; print(x)` (Doğru) vs `print(x)` (Yanlış)",
        "prevention": "Değişkenleri kullanmadan önce mutlaka tanımla."
    },
    "TypeError": {
        "responses": [
            "Veri tipleri arasında bir uyumsuzluk var gibi, neyi karıştırdık acaba?",
            "Oops, tipler uyuşmuyor gibi! Bir string ile sayıyı mı topladın?"
        ],
        "solutions": [
            "Değişken tiplerini kontrol et, gerekirse `int()` veya `str()` kullan.",
            "Tipini öğrenmek için `type(değişken)` yazabilirsin."
        ],
        "example": "Örnek: `x = '5'; print(int(x) + 3)` (Doğru) vs `print(x + 3)` (Yanlış)",
        "prevention": "İşlem yapmadan önce veri tiplerini uyumlu hale getir."
    },
    "ValueError": {
        "responses": [
            "Hmm, yanlış bir değer girmişsin gibi görünüyor!",
            "ValueError dediyse, verdiğin değer beklenenden farklı olabilir."
        ],
        "solutions": [
            "Girdiğin değeri kontrol et, mesela bir sayı beklenirken string mi verdin?",
            "Doğru formatta veri kullandığından emin ol!"
        ],
        "example": "Örnek: `x = int('123')` (Doğru) vs `x = int('abc')` (Yanlış)",
        "prevention": "Dönüşüm yapmadan önce girdinin geçerli olduğunu doğrula."
    },
    "IndexError": {
        "responses": [
            "Liste veya dizide sınırı aşmışsın gibi görünüyor!",
            "Hey, yanlış bir indeks mi kullandın acaba?"
        ],
        "solutions": [
            "Listenin uzunluğunu kontrol et, `len(liste)` ile bakabilirsin.",
            "İndeksin geçerli olduğundan emin ol!"
        ],
        "example": "Örnek: `liste = [1, 2]; print(liste[1])` (Doğru) vs `print(liste[2])` (Yanlış)",
        "prevention": "İndeks kullanmadan önce listenin boyutunu kontrol et."
    },
    "KeyError": {
        "responses": [
            "Hmm, sözlükte olmayan bir anahtar mı aradın?",
            "Anahtar hatası almışsın, bakalım neyi kaçırmışız!"
        ],
        "solutions": [
            "Sözlükteki anahtarları kontrol et, `dict.keys()` ile görebilirsin.",
            "Doğru anahtarı kullandığından emin ol!"
        ],
        "example": "Örnek: `d = {'a': 1}; print(d['a'])` (Doğru) vs `print(d['b'])` (Yanlış)",
        "prevention": "Sözlükten bir şey almadan önce anahtarın varlığını kontrol et."
    },
    "AttributeError": {
        "responses": [
            "Bir nesneye yanlış bir şey mi sormaya çalıştın?",
            "Hmm, böyle bir özellik veya yöntem yok gibi görünüyor!"
        ],
        "solutions": [
            "Nesnenin özelliklerini kontrol et, `dir(nesne)` ile neler var bakabilirsin.",
            "Doğru yöntemi veya özelliği kullandığından emin ol!"
        ],
        "example": "Örnek: `s = 'hello'; print(s.upper())` (Doğru) vs `print(s.uppper())` (Yanlış)",
        "prevention": "Metot veya özellik adlarını yazmadan önce kontrol et."
    },
    "ZeroDivisionError": {
        "responses": [
            "Oops, sıfıra bölmeye mi çalıştın?",
            "Bir sayıyı sıfıra bölmek pek iyi fikir değil gibi!"
        ],
        "solutions": [
            "Bölme yapmadan önce bölenin sıfır olmadığını kontrol et.",
            "Bir `if` koşulu ile sıfırı engelleyebilirsin."
        ],
        "example": "Örnek: `if b != 0: print(a / b)` (Doğru) vs `print(a / 0)` (Yanlış)",
        "prevention": "Bölme işlemlerinde bölenin sıfır olup olmadığını kontrol et."
    },
    "ImportError": {
        "responses": [
            "Bir modülü mü bulamıyorum acaba?",
            "Hmm, bu modül ya da isim kodunda eksik gibi!"
        ],
        "solutions": [
            "Modülün yüklü olduğundan emin ol, `pip install modül_adı` ile kurabilirsin.",
            "Doğru modül adını veya import yolunu kontrol et!"
        ],
        "example": "Örnek: `import math; print(math.pi)` (Doğru) vs `import maths` (Yanlış)",
        "prevention": "Modül adlarını ve kurulumlarını önceden doğrula."
    },
    "FileNotFoundError": {
        "responses": [
            "Dosyayı bulamadım, yanlış yerde mi arıyoruz?",
            "Hmm, böyle bir dosya yok gibi görünüyor!"
        ],
        "solutions": [
            "Dosya yolunu kontrol et, doğru yazdığından emin ol.",
            "Dosyanın varlığını `os.path.exists()` ile test edebilirsin."
        ],
        "example": "Örnek: `open('dosya.txt')` (Dosya varsa doğru) vs `open('yanlis.txt')` (Yanlış)",
        "prevention": "Dosya işlemlerinden önce dosyanın varlığını doğrula."
    },
    "ModuleNotFoundError": {
        "responses": [
            "Bu modül sistemde yok gibi, yükledin mi?",
            "Hmm, modül adını mı yanlış yazdın acaba?"
        ],
        "solutions": [
            "Modülü yüklemek için `pip install modül_adı` komutunu çalıştır.",
            "Modül adını doğru yazdığından emin ol."
        ],
        "example": "Örnek: `import numpy` (Doğru) vs `import numppy` (Yanlış)",
        "prevention": "Modül adlarını yazmadan önce kontrol et ve kurulum yap."
    },
    "UnboundLocalError": {
        "responses": [
            "Bir değişkeni tanımlamadan mı kullandın?",
            "Hmm, yerel bir değişkenle ilgili bir karışıklık var gibi!"
        ],
        "solutions": [
            "Değişkeni fonksiyon içinde tanımladığından emin ol.",
            "Global değişken kullanıyorsan `global` anahtarını ekle."
        ],
        "example": "Örnek: `def f(): x = 5; print(x)` (Doğru) vs `def f(): print(x); x = 5` (Yanlış)",
        "prevention": "Fonksiyonlarda değişkenleri kullanmadan önce tanımla."
    },
    "IndentationError": {
        "responses": [
            "Girintilerle mi oynadın, bir hata var gibi!",
            "Kodunun hizalaması biraz karışmış sanki."
        ],
        "solutions": [
            "Kod bloklarının girintisini kontrol et, hepsi aynı hizada olmalı.",
            "Boşluk mu yoksa tab mı kullanıyorsun, tutarlı ol!"
        ],
        "example": "Örnek: `if True:\n    print('ok')` (Doğru) vs `if True:\nprint('ok')` (Yanlış)",
        "prevention": "Kod yazarken girintileri tutarlı tut."
    },
    "OverflowError": {
        "responses": [
            "Sayılar biraz fazla büyüdü galiba, taşma hatası aldık!",
            "Hmm, bu hesaplama Python’un sınırlarını zorlamış gibi."
        ],
        "solutions": [
            "Daha küçük sayılarla çalışmayı dene veya büyük sayılar için kütüphane kullan.",
            "Hesaplamayı basitleştirebilir misin bir bakalım."
        ],
        "example": "Örnek: `2 ** 1000` (Doğru) vs `2 ** 10000` (Çok büyük, OverflowError)",
        "prevention": "Büyük matematiksel işlemlerde sınırları kontrol et."
    },
    "MemoryError": {
        "responses": [
            "Bilgisayarın belleği bu işe yetmedi gibi görünüyor!",
            "Oops, çok fazla veriyle mi uğraşıyorsun?"
        ],
        "solutions": [
            "Veri yapını küçültmeyi dene, mesela daha az elemanla çalış.",
            "Büyük veriler için `numpy` gibi optimize kütüphaneler kullanabilirsin."
        ],
        "example": "Örnek: `liste = [0] * 1000` (Doğru) vs `liste = [0] * 10**10` (Bellek yetmez)",
        "prevention": "Büyük veri yapıları oluşturmadan önce sistem kapasiteni kontrol et."
    },
    "RuntimeError": {
        "responses": [
            "Bir şeyler ters gitti, ama tam olarak neyi bulamadım!",
            "Hmm, genel bir çalışma zamanı hatası almışsın."
        ],
        "solutions": [
            "Hata mesajındaki detaylara bak, neyi işaret ediyor kontrol et.",
            "Kodunun akışını adım adım izlemeyi dene."
        ],
        "example": "Örnek: Genel bir hata, spesifik bir durum olmadan tanımlı değil.",
        "prevention": "Kodunda olası hataları öngörmek için testler yaz."
    },
    "RecursionError": {
        "responses": [
            "Fonksiyon kendini çok mu çağırdı acaba?",
            "Sonsuz bir döngüye mi girdik, ne dersin?"
        ],
        "solutions": [
            "Rekürsiyonu bir çıkış koşuluyla sınırla.",
            "Döngü (`for` veya `while`) kullanmayı düşünebilirsin."
        ],
        "example": "Örnek: `def f(n): if n <= 0: return 0; return f(n-1)` (Doğru) vs `def f(): f()` (Yanlış)",
        "prevention": "Rekürsif fonksiyonlarda temel durumu (base case) ekle."
    },
    "NotImplementedError": {
        "responses": [
            "Bir şey mi eksik kaldı, uygulanmamış bir şey mi var?",
            "Hmm, bu kısım henüz yazılmamış gibi görünüyor!"
        ],
        "solutions": [
            "Eksik metodu veya fonksiyonu tanımla.",
            "Soyut bir sınıf kullanıyorsan, gerekli metotları implement et."
        ],
        "example": "Örnek: `def metod(): return 'Tamamlandı'` (Doğru) vs `def metod(): raise NotImplementedError` (Eksik)",
        "prevention": "Kodunda eksik bırakılan yerleri tamamla."
    }
}

def astra():
    print("Merhaba yazılımcı dostum! Ben Astra, kodunda bir hata mı var? Endişelenme, birlikte çözeriz!")
    print("Hata mesajını tek seferde kopyala-yapıştır yapabilirsin, ben satır satır analiz ederim!")
    awaiting_code = False
    awaiting_feedback = False
    last_error = None
    
    while True:
        print("Sen: ", end="")
        user_input = ""
        while True:
            line = input()
            if not line:  # Boş satır girildiğinde girişi bitir
                break
            user_input += line + "\n"
        user_input = user_input.strip()
        
        if not user_input:
            print("Astra: Bir şey yazmadın gibi görünüyor. Hata mesajını girip bana gösterebilir misin?")
            continue
        
        if user_input.lower() == 'çıkış':
            print("Astra: Görüşürüz, kodlamada bol şans! Yine beklerim!")
            break
        
        if awaiting_feedback:
            if user_input.lower() in ['evet', 'e']:
                print("Astra: Harika, işine yaradıysa ne mutlu bana! Başka bir hata varsa beklerim!")
            elif user_input.lower() in ['hayır', 'h']:
                print("Astra: Hmm, üzgünüm, o zaman başka bir çözüm önerisi için daha fazla detay verebilir misin?")
            else:
                print("Astra: 'Evet' veya 'Hayır' yazarsan daha iyi anlarım, ne dersin?")
            awaiting_feedback = False
            continue
        
        if awaiting_code:
            response, changes = analyze_code(user_input, last_error)
            print(f"Astra: {response}")
            if changes:
                print(f"Astra: [Neyi değiştirdim?] {changes}")
            print("Astra: Bu çözüm işine yaradı mı? (Evet/Hayır)")
            awaiting_feedback = True
            continue
        
        response, needs_code, error_type, changes = analyze_input(user_input)
        print(f"Astra: {response}")
        if changes:
            print(f"Astra: [Neyi değiştirdim?] {changes}")
        print("Astra: Bu çözüm işine yaradı mı? (Evet/Hayır)")
        awaiting_feedback = True
        awaiting_code = needs_code
        last_error = error_type if needs_code else None

def analyze_input(user_input):
    user_input_lower = user_input.lower()
    
    if "hata" in user_input_lower and not any(e.lower() in user_input_lower for e in error_database):
        return "Hmm, hata mesajını anladım. Lütfen hatanın tam detaylarını paylaş, hemen bakalım!", True, None, None
    
    for error_type, data in error_database.items():
        if error_type.lower() in user_input_lower:
            response = random.choice(data["responses"])
            solution = random.choice(data["solutions"])
            code_snippet = extract_code_snippet(user_input)
            for detail, explanation in data.get("details", {}).items():
                if detail in user_input_lower and code_snippet:
                    fixed_code, changes = fix_code(code_snippet, error_type, detail)
                    return (
                        f"{response} Şöyle bir durum var: {explanation} "
                        f"Kodunda şunu görüyorum: `{code_snippet}`. "
                        f"Kodun şu şekilde olmalı:\n    {fixed_code}\n"
                        f"Hata, {explanation.lower()} İşte bir örnek: {data['example']}. "
                        f"Bunu nasıl önlersin? {data['prevention']} Harika gidiyorsun!"
                    ), False, error_type, changes
            if code_snippet:
                fixed_code, changes = fix_code(code_snippet, error_type, None)
                return (
                    f"{response} Kodunda şunu görüyorum: `{code_snippet}`. "
                    f"Çözüm: {solution} İşte düzeltilmiş hali:\n    {fixed_code}\n"
                    f"İşte bir örnek: {data['example']}. Bunu nasıl önlersin? {data['prevention']} Harika gidiyorsun!"
                ), False, error_type, changes
            return f"{response} Çözüm: {solution} Hata aldığın satırı paylaşır mısın?", True, error_type, None
    
    return "Bu ne bir hata mesajı ne de tanıdığım bir şey gibi görünüyor. Bir hata mesajı yazmayı dene, mesela 'SyntaxError: invalid syntax'. Ne dersin?", False, None, None

def extract_code_snippet(user_input):
    lines = user_input.split("\n")
    for i, line in enumerate(lines):
        if line.strip() and not ("file" in line.lower() or "traceback" in line.lower() or any(e.lower() in line.lower() for e in error_database)):
            if i + 1 < len(lines) and "~~" in lines[i + 1]:
                return line.strip()
            return line.strip()
    return None

def fix_code(code_snippet, error_type, detail):
    code_snippet_lower = code_snippet.lower()
    changes = None
    
    if error_type == "SyntaxError":
        if "if" in code_snippet_lower and ":" not in code_snippet_lower and detail == "expected ':'":
            fixed_code = f"{code_snippet.strip()}:"
            changes = "Kodunun sonuna `:` (iki nokta üst üste) ekledim, çünkü `if` ifadeleri bunu gerektirir."
            return fixed_code, changes
        elif "f'" in code_snippet_lower and "'" not in code_snippet_lower[2:]:
            fixed_code = f"{code_snippet.strip()}'"
            changes = "f-string’in sonuna eksik olan `'` tırnak işaretini ekledim."
            return fixed_code, changes
        elif "(" in code_snippet_lower and ")" not in code_snippet_lower:
            fixed_code = f"{code_snippet.strip()})"
            changes = "Açılan parantezi kapatmak için sonuna `)` ekledim."
            return fixed_code, changes
    elif error_type == "NameError":
        variable_match = re.search(r"name '(\w+)' is not defined", user_input_lower)
        variable = variable_match.group(1) if variable_match else code_snippet.split()[-1]
        fixed_code = f"{variable} = bir_değer  # Önce bunu ekle\n{code_snippet.strip()}"
        changes = f"`{variable}` değişkenini tanımlamak için kodun üstüne bir atama satırı ekledim."
        return fixed_code, changes
    elif error_type == "IndexError":
        fixed_code = f"# Liste uzunluğunu kontrol et\nif len(liste) > {code_snippet.split('[')[-1].split(']')[0]}:\n    {code_snippet.strip()}"
        changes = "İndeks hatasını önlemek için liste uzunluğunu kontrol eden bir `if` koşulu ekledim."
        return fixed_code, changes
    elif error_type == "KeyError":
        key = re.search(r"'(\w+)'", user_input_lower).group(1) if re.search(r"'(\w+)'", user_input_lower) else "anahtar"
        fixed_code = f"# Anahtarın varlığını kontrol et\nif '{key}' in dict:\n    {code_snippet.strip()}"
        changes = f"`{key}` anahtarının sözlükte olup olmadığını kontrol eden bir `if` koşulu ekledim."
        return fixed_code, changes
    elif error_type == "AttributeError":
        attribute = re.search(r"'(\w+)' object has no attribute '(\w+)'", user_input_lower)
        if attribute:
            fixed_code = f"# Doğru metodu kontrol et\n{code_snippet.replace(attribute.group(2), 'doğru_metot')}"
            changes = f"Hatalı `{attribute.group(2)}` metodunu `doğru_metot` ile değiştirdim (gerçek metodu kontrol et)."
        else:
            fixed_code = code_snippet
            changes = "Doğru metodu bulamadım, nesnenin metodlarını kontrol et."
        return fixed_code, changes
    elif error_type == "ZeroDivisionError":
        fixed_code = f"# Sıfıra bölmeyi kontrol et\nif bölen != 0:\n    {code_snippet.strip()}"
        changes = "Sıfıra bölmeyi önlemek için bir `if` koşulu ekledim."
        return fixed_code, changes
    elif error_type == "ImportError" or error_type == "ModuleNotFoundError":
        module_match = re.search(r"no module named '(\w+)'", user_input_lower)
        module = module_match.group(1) if module_match else "modül"
        fixed_code = f"# Modülü doğru şekilde yükle\npip install {module}\nimport {module}\n{code_snippet.strip()}"
        changes = f"`{module}` modülünü yüklemek için bir `pip install` komutu ve doğru `import` satırı ekledim."
        return fixed_code, changes
    elif error_type == "FileNotFoundError":
        file_match = re.search(r"\[Errno 2\] No such file or directory: '(.+)'", user_input_lower)
        file_name = file_match.group(1) if file_match else "dosya"
        fixed_code = f"# Dosyanın varlığını kontrol et\nimport os\nif os.path.exists('{file_name}'):\n    {code_snippet.strip()}"
        changes = f"`{file_name}` dosyasının varlığını kontrol etmek için bir `if` koşulu ekledim."
        return fixed_code, changes
    elif error_type == "UnboundLocalError":
        variable_match = re.search(r"local variable '(\w+)' referenced before assignment", user_input_lower)
        variable = variable_match.group(1) if variable_match else "değişken"
        fixed_code = f"{variable} = None  # Önce tanımla\n{code_snippet.strip()}"
        changes = f"`{variable}` değişkenini kullanmadan önce tanımladım."
        return fixed_code, changes
    elif error_type == "IndentationError":
        fixed_code = f"# Doğru girinti kullan\nif True:\n    {code_snippet.strip()}"
        changes = "Kodunun girintisini düzelttim, Python’da bloklar hizalı olmalı."
        return fixed_code, changes
    elif error_type == "OverflowError":
        fixed_code = f"# Sayıyı küçült\nsmaller_value = 100\n{code_snippet.replace('10000', 'smaller_value')}"
        changes = "Büyük sayıyı daha küçük bir değerle değiştirdim."
        return fixed_code, changes
    elif error_type == "MemoryError":
        fixed_code = f"# Daha az veri kullan\nliste = [0] * 1000\n# Eski kod: {code_snippet}"
        changes = "Bellek kullanımını azaltmak için daha küçük bir veri yapısı önerdim."
        return fixed_code, changes
    elif error_type == "RecursionError":
        fixed_code = f"# Çıkış koşulu ekle\ndef f(n):\n    if n <= 0:\n        return 0\n    return f(n-1)\n# Eski kod: {code_snippet}"
        changes = "Rekürsiyonu durdurmak için bir çıkış koşulu ekledim."
        return fixed_code, changes
    elif error_type == "NotImplementedError":
        fixed_code = f"# Metodu uygula\ndef metod():\n    return 'Tamamlandı'\n# Eski kod: {code_snippet}"
        changes = "Eksik metodu basit bir şekilde tanımladım."
        return fixed_code, changes
    elif error_type == "RuntimeError":
        fixed_code = code_snippet
        changes = "Bu genel bir hata, daha fazla detay verirsen düzeltebilirim."
        return fixed_code, changes
    
    return code_snippet, None

def analyze_code(code_snippet, error_type):
    fixed_code, changes = fix_code(code_snippet, error_type, None)
    data = error_database.get(error_type, {})
    response = (
        f"Koduna baktım: `{code_snippet}`. "
        f"Çözüm olarak şunu öneriyorum:\n    {fixed_code}\n"
        f"İşte bir örnek: {data.get('example', 'Spesifik bir örnek yok.')}. "
        f"Bunu nasıl önlersin? {data.get('prevention', 'Genel bir ipucu yok.')}"
    )
    return response, changes

if __name__ == "__main__":
    astra()