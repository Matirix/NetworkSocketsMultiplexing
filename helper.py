def ip_and_port_validator(message, isPort):
    if not message:
        raise ValueError("Missing Arguments: usage -ip <ip> -port <port>")
        return False
    if isPort:
        if message < 1 or message > 65535:
            raise ValueError("Invalid Port Number: Must be a number within range 1-65535")
            return False
        return True
    sections = message.split('.')
    if len(sections) != 4:
        raise ValueError("Invalid Address: Must be in the following format xxx.xxx.xxx.xxx")
        return False
    for section in sections:
        if not section.isdigit() and section < 0 and section > 255:
            raise ValueError("Invalid Address: Must be all numbers")
            return False
    return True
