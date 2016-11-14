"""Transformers del header."""
import email
import re
from . import BaseTransformer


class AddHeaderAttributesTransformer(BaseTransformer):
    """Agrega atributos del header."""

    def transform(self, df):
        u"""Aplico transformación."""
        parser = email.parser.Parser()

        parsed_emails = df['text'].apply(
            lambda t: parser.parsestr(t.encode('utf-8')))

        self.add_content_type_columns(df, parsed_emails)

        receivers = parsed_emails.apply(
            lambda p: p.get_all("To") or p.get_all("to") or [])
        sender = parsed_emails.apply(
            lambda p: p.get_all("From") or p.get_all("from") or [])

        def join_mails(t):
            return ";".join(t)

        def is_ascii(s):
            try:
                s.encode('ascii')
                return True
            except UnicodeDecodeError:
                return False

        to_text = receivers.apply(join_mails)
        from_text = df['from'] = sender.apply(join_mails)

        df['number_of_receivers'] = to_text.apply(
            lambda t: len(re.findall(r'<.*>', t))
        )

        df['from_non_ascii'] = from_text.apply(
            lambda from_list: not is_ascii(from_list)
        )

        return df

    def add_content_type_columns(self, df, parsed_emails):
        """Agrego todas las columnas relacionadas a content type."""
        content_type = parsed_emails.apply(
            lambda t: t.get_content_type())

        types = [
            'multipart/mixed', 'text/html', 'multipart/alternative',
            'text/plain', 'multipart/related', 'multipart/report',
            'text/plain charset="us-ascii"', 'text/html charset=iso-8859-1',
            'application/vnd.ms-excel', 'message/rfc822', 'text/enriched',
            'text/richtext', 'image/pjpeg', 'application/msword',
            'application/octet-stream']

        for ctype in types:
            df[ctype] = content_type.apply(
                lambda t: ctype in t)
