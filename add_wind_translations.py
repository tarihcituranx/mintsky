import os
import json

locales_dir = "/home/turan/Belgeler/mintsky/mintsky/locales"
locales = [f for f in os.listdir(locales_dir) if f.endswith(".json")]

wind_translations = {
    "Kuzey": {"tr": "Kuzey", "en": "North", "de": "Nord", "fr": "Nord", "ar": "شمال", "fa": "شمال", "zh": "北", "az": "Şimal"},
    "Kuzey Kuzeydoğu": {"tr": "Kuzey Kuzeydoğu", "en": "North Northeast", "de": "Nord Nordost", "fr": "Nord Nord-Est", "ar": "شمال شمال شرق", "fa": "شمال شمال شرق", "zh": "北东北", "az": "Şimal Şimal-şərq"},
    "Kuzeydoğu": {"tr": "Kuzeydoğu", "en": "Northeast", "de": "Nordost", "fr": "Nord-Est", "ar": "شمال شرق", "fa": "شمال شرق", "zh": "东北", "az": "Şimal-şərq"},
    "Doğu Kuzeydoğu": {"tr": "Doğu Kuzeydoğu", "en": "East Northeast", "de": "Ost Nordost", "fr": "Est Nord-Est", "ar": "شرق شمال شرق", "fa": "شرق شمال شرق", "zh": "东东北", "az": "Şərq Şimal-şərq"},
    "Doğu": {"tr": "Doğu", "en": "East", "de": "Ost", "fr": "Est", "ar": "شرق", "fa": "شرق", "zh": "东", "az": "Şərq"},
    "Doğu Güneydoğu": {"tr": "Doğu Güneydoğu", "en": "East Southeast", "de": "Ost Südost", "fr": "Est Sud-Est", "ar": "شرق جنوب شرق", "fa": "شرق جنوب شرق", "zh": "东东南", "az": "Şərq Cənub-şərq"},
    "Güneydoğu": {"tr": "Güneydoğu", "en": "Southeast", "de": "Südost", "fr": "Sud-Est", "ar": "جنوب شرق", "fa": "جنوب شرق", "zh": "东南", "az": "Cənub-şərq"},
    "Güney Güneydoğu": {"tr": "Güney Güneydoğu", "en": "South Southeast", "de": "Süd Südost", "fr": "Sud Sud-Est", "ar": "جنوب جنوب شرق", "fa": "جنوب جنوب شرق", "zh": "南东南", "az": "Cənub Cənub-şərq"},
    "Güney": {"tr": "Güney", "en": "South", "de": "Süd", "fr": "Sud", "ar": "جنوب", "fa": "جنوب", "zh": "南", "az": "Cənub"},
    "Güney Güneybatı": {"tr": "Güney Güneybatı", "en": "South Southwest", "de": "Süd Südwest", "fr": "Sud Sud-Ouest", "ar": "جنوب جنوب غرب", "fa": "جنوب جنوب غرب", "zh": "南西南", "az": "Cənub Cənub-qərb"},
    "Güneybatı": {"tr": "Güneybatı", "en": "Southwest", "de": "Südwest", "fr": "Sud-Ouest", "ar": "جنوب غرب", "fa": "جنوب غرب", "zh": "西南", "az": "Cənub-qərb"},
    "Batı Güneybatı": {"tr": "Batı Güneybatı", "en": "West Southwest", "de": "West Südwest", "fr": "Ouest Sud-Ouest", "ar": "غرب جنوب غرب", "fa": "غرب جنوب غرب", "zh": "西西南", "az": "Qərb Cənub-qərb"},
    "Batı": {"tr": "Batı", "en": "West", "de": "West", "fr": "Ouest", "ar": "غرب", "fa": "غرب", "zh": "西", "az": "Qərb"},
    "Batı Kuzeybatı": {"tr": "Batı Kuzeybatı", "en": "West Northwest", "de": "West Nordwest", "fr": "Ouest Nord-Ouest", "ar": "غرب شمال غرب", "fa": "غرب شمال غرب", "zh": "西西北", "az": "Qərb Şimal-qərb"},
    "Kuzeybatı": {"tr": "Kuzeybatı", "en": "Northwest", "de": "Nordwest", "fr": "Nord-Ouest", "ar": "شمال غرب", "fa": "شمال غرب", "zh": "西北", "az": "Şimal-qərb"},
    "Kuzey Kuzeybatı": {"tr": "Kuzey Kuzeybatı", "en": "North Northwest", "de": "Nord Nordwest", "fr": "Nord Nord-Ouest", "ar": "شمال شمال غرب", "fa": "شمال شمال غرب", "zh": "北西北", "az": "Şimal Şimal-qərb"}
}

for loc in locales:
    lang = loc.replace(".json", "")
    path = os.path.join(locales_dir, loc)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for key, trans_dict in wind_translations.items():
        if key not in data:
            data[key] = trans_dict.get(lang, trans_dict["en"])
            
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Wind translations added.")

# Update utils.py yon() function
utils_path = "/home/turan/Belgeler/mintsky/mintsky/utils.py"
with open(utils_path, "r", encoding="utf-8") as f:
    code = f.read()

old_yon = """def yon(derece):
    if derece is None or derece == -9999 or not isinstance(derece, (int, float)):
        return ""
    return YONLER[round(derece/22.5)%16] if derece >= 0 else \"\""""

new_yon = """def yon(derece):
    if derece is None or derece == -9999 or not isinstance(derece, (int, float)):
        return ""
    if derece >= 0:
        val = YONLER[round(derece/22.5)%16]
        try:
            return _(val)
        except NameError:
            import builtins
            if hasattr(builtins, '_'):
                return builtins._(val)
            return val
    return \"\""""

code = code.replace(old_yon, new_yon)
with open(utils_path, "w", encoding="utf-8") as f:
    f.write(code)

print("utils.py yon() patched for i18n.")
