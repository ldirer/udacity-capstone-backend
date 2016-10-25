"""
A module to store methods that will query the microsoft (bing) api to translate words/phrases and
add the results to the db.
"""
from flask_sqlalchemy import SQLAlchemy

from g.config import microsoft_translator
from g.models import Language, Word
from g.translate import Translator, MICROSOFT_SHORT_TO_FULL_LANGUAGE_STRING

translator = Translator(microsoft_translator['CLIENT_ID'],
                        microsoft_translator['CLIENT_SECRET'])


def fetch_translation(phrase: str, language: Language) -> Word:
    translated = translator.translate(phrase, to_lang=language.microsoft_name,
                                      from_lang="en")

    # Caching mechanism. Pbbly wont work if/when the word table gets big.
    existing = Word.query.filter_by(language_id=language._id,
                                    word=phrase).first()
    if existing is not None:
        return existing

    word = Word()
    # Not printing, raises errors (ascii encoding) when run in docker.
    # print("ALRIGHT. ASKING FOR PHRASE={}, IN LANGUAGE={}, GOT: {}".format(phrase, language.name, translated))
    word.language_id = language._id
    word.word = phrase
    word.translation = translated
    return word


def populate_languages(db: SQLAlchemy):
    """
    populate the database with microsoft-supported languages.
    """
    resp = translator.get_languages()

    for short in resp:
        lang = Language()
        lang.microsoft_name = short
        try:
            lang.name = MICROSOFT_SHORT_TO_FULL_LANGUAGE_STRING[short]
        except KeyError:
            # Maybe microsoft added a new language. Like Fijian.
            continue

        # That's pbbly not 100% accurate and some short names contain hyphens
        # This wont work with android resource naming but eh.
        lang.icon_name = short
        db.session.add(lang)

    db.session.commit()


if __name__ == '__main__':
    pass
