from .i18n_messages import MESSAGES


def i18n_labels(request):
    lang = request.session.get("lang", "en")
    if lang not in MESSAGES:
        lang = "en"
    return {"L": MESSAGES[lang], "UI_LANG": lang}
