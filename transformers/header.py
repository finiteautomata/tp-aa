#! coding: utf-8
"""Transformers del header."""
import re
import numpy as np
from . import BaseTransformer


class ContentTypeTransformer(BaseTransformer):
    """Agrega atributos basados en content/type"""

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
