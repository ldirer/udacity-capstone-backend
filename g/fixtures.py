from g import db
from g.models import Language
from g.translator import populate_languages, fetch_translation


def languages():
    populate_languages(db)


def words():
    """Populate the db with basic words for some languages.
    Note this requires that the languages are in the db.
    """
    language_shortlist = ["French", "Spanish", "German", "Romanian"]
    phrases = ['I eat', 'I have a question', 'blue', 'I like chocolate',
               'You like chocolate', 'You only eat chocolate']

    for i, phrase in enumerate(phrases, start=1):
        print("Processing phrase %i" % i)
        for lang_name in language_shortlist:
            lang = Language.query.filter_by(name=lang_name).first()
            print("Processing phrase %i, language=%s" % (i, lang.name))
            word = fetch_translation(phrase, lang)
            db.session.add(word)
    db.session.commit()
