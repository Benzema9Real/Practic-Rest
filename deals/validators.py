from django.core.exceptions import ValidationError


def validate_pdf_file(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError('Допустим только формат PDF.')


def validate_file_size(file):
    limit_mb = 20
    if file.size > limit_mb * 1024 * 1024:
        raise ValidationError(f'Размер файла не должен превышать {limit_mb} МБ.')


def validate_non_negative(value):
    if value < 0:
        raise ValidationError('Стоимость не может быть отрицательной.')
