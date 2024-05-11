def send_channel_message(group_name: str, content: dict) -> None:
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {
        "type": "group.message",
        "content": content
    })


def file_from_request(context, field):
    files_request = context['request'].FILES
    if field in files_request:
        file = files_request.get(field)
        if file:
            return file.read()
    return None


def coalesce(source, target, as_string: bool = False):
    if source == '':
        source = None
    if source is not None:
        return "'{}'".format(source) if as_string else source
    else:
        return target


def choice_text(choice: tuple, key: str):
    result = [item[1] for item in choice if item[0] == key]
    if len(result):
        return str(result[0])


def as_boolean(value):
    try:
        if isinstance(value, str):
            value = value.lower()

        return {
            '1': True,
            '0': False,
            'true': True,
            'false': False,
            True: True,
            False: False,
        }.get(value, None)
    except Exception:
        return None
