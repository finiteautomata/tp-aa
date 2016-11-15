#! coding: utf-8
"""Transformers del header."""
import re
import random
import dateutil
import numpy as np
from . import BaseTransformer


class ContentTypeTransformer(BaseTransformer):
    """Agrega atributos basados en content/type."""

    def transform(self, mails):
        """Agrego todas las columnas relacionadas a content type."""
        content_type = [m.get_content_type() for m in mails]

        types = [
            'multipart/mixed', 'text/html', 'multipart/alternative',
            'text/plain', 'multipart/related', 'multipart/report',
            'text/plain charset="us-ascii"', 'text/html charset=iso-8859-1',
            'application/vnd.ms-excel', 'message/rfc822', 'text/enriched',
            'text/richtext', 'image/pjpeg', 'application/msword',
            'application/octet-stream']

        new_columns = []

        for ctype in types:
            new_columns.append([ctype in t for t in content_type])

        return np.array(new_columns).transpose()


class DateTransformer(BaseTransformer):
    """Agrega atributos basados en la fecha del mail."""

    def transform(self, mails):
        """Agrega atributos de fecha."""
        def parse_date(parsed_mail):
            try:
                date = parsed_mail.get('Date') or parsed_mail.get('date')
                return dateutil.parser.parse(date, fuzzy_with_tokens=True)[0]
            except:
                return None

        dates = [parse_date(m) for m in mails]

        hours = map(lambda t: t.hour if t else random.choice(range(23)), dates)
        hour_between_7_and_20 = map(lambda h: h >= 7 and h <= 21, hours)

        # df['day_of_month'] = dates.apply(
        #     lambda d: d.day if d else random.choice(range(29))
        # )

        # df['weekday'] = dates.apply(
        #     lambda d: d.weekday() if d else random.choice(range(6))
        # )

        # df['is_weekend'] = df.weekday >= 5

        # df['year'] = dates.apply(
        #     lambda d: d.year if d else random.choice(range(1990, 2005))
        # )

        return np.array([hours, hour_between_7_and_20]).transpose()


class ParticipantsTransformer(BaseTransformer):
    """Agrega atributos del header."""

    def transform(self, mails):
        u"""Aplico transformación."""
        receivers = [p.get_all("To") or p.get_all("to") or [] for p in mails]
        sender = [p.get_all("From") or p.get_all("from") or [] for p in mails]

        def join_mails(t):
            return ";".join(t)

        def is_ascii(s):
            try:
                s.encode('ascii')
                return True
            except UnicodeDecodeError:
                return False

        to_text = map(join_mails, receivers)
        from_text = map(join_mails, sender)

        no_receivers = [len(re.findall(r'<.*>', t)) for t in to_text]
        from_non_ascii = [not is_ascii(from_list) for from_list in from_text]

        return np.array([no_receivers, from_non_ascii]).transpose()
