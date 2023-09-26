import secrets


def staff_id_generator():
    secret = secrets.token_hex(2)
    return f"S{secret}"


day_map = {
    1: "Monday",
    2: "Tuesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}
