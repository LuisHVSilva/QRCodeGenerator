def input_check(field, field_name):
    if field is None or (isinstance(field, str) and not field):
        raise ValueError(f"O {field_name} não pode ser nulo ou vazio.")
    if isinstance(field, int) and field == 0:
        raise ValueError(f"O {field_name} não pode ser igual a zero.")
    return field
