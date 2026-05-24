def valid_id(value):
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    try:
        val = int(value)
    except (ValueError, TypeError):
        return None

    if val <= 0:
        return None

    return val


def valid_user(data):
    if not isinstance(data, dict):
        return False, "payload_must_be_object"

    required = ["name", "email", "major"]
    for f in required:
        v = data.get(f)
        if v is None:
            return False, f"missing:{f}"
        if isinstance(v, str) and v.strip() == "":
            return False, f"empty:{f}"

    email = data.get("email")
    if not isinstance(email, str) or "@" not in email or "." not in email.split("@")[-1]:
        return False, "invalid:email"

    role = data.get("role")
    allowed = ["student", "teacher", "librarian", "admin"]
    if role not in allowed and role is not None:
        return False, "invalid:role"

    score = data.get("score")
    if score is not None:
        try:
            s = int(score)
            if s < 0:
                return False, "invalid:score"
        except (ValueError, TypeError):
            return False, "invalid:score"

    major = data.get("major")
    if major is not None and not isinstance(major, str):
        return False, "invalid:major"

    return True, None


def valid_user_update(data):
    if not isinstance(data, dict):
        return False, "payload_must_be_object"

    allowed = ["name", "email", "role", "major", "score"]
    if not any(k in data for k in allowed):
        return False, "no_updatable_fields"

    if "name" in data:
        if data["name"] is None:
            return False, "null:name"
        if not isinstance(data["name"], str):
            return False, "invalid_type:name"
        if data["name"].strip() == "":
            return False, "empty:name"

    if "email" in data:
        if data["email"] is None:
            return False, "null:email"
        if not isinstance(data["email"], str):
            return False, "invalid_type:email"
        if data["email"].strip() == "":
            return False, "empty:email"
        if "@" not in data["email"] or "." not in data["email"].split("@")[-1]:
            return False, "invalid_format:email"

    if "role" in data:
        if data["role"] is None:
            return False, "null:role"
        if not isinstance(data["role"], str):
            return False, "invalid_type:role"
        if data["role"].strip() == "":
            return False, "empty:role"
        allowed_roles = ["student", "teacher", "librarian", "admin"]
        if data["role"] not in allowed_roles:
            return False, "invalid_value:role"

    if "score" in data:
        if data["score"] is None:
            return False, "null:score"
        try:
            s = int(data["score"])
        except (ValueError, TypeError):
            return False, "invalid_type:score"
        if s < 0:
            return False, "invalid_value:score"

    if "major" in data:
        if data.get("major") is None:
            return False, "null:major"
        if not isinstance(data.get("major"), str):
            return False, "invalid_type:major"
        if data.get("major").strip() == "":
            return False, "empty:major"

    return True, None


def valid_login(data):
    if not isinstance(data, dict):
        return False, "payload_must_be_object"

    if data.get("username") is None:
        return False, "missing:username"
    if not isinstance(data.get("username"), str):
        return False, "invalid_type:username"
    if data.get("username").strip() == "":
        return False, "empty:username"
    if len(data.get("username").strip()) < 3:
        return False, "invalid_value:username"

    if data.get("password") is None:
        return False, "missing:password"
    if not isinstance(data.get("password"), str):
        return False, "invalid_type:password"
    if data.get("password").strip() == "":
        return False, "empty:password"

    return True, None


def valid_penalty_patch(data):
    if not isinstance(data, dict):
        return False, "payload_must_be_object"

    allowed = ["status", "severity", "notes"]
    if not any(k in data for k in allowed):
        return False, "no_updatable_fields"

    if "status" in data:
        if data.get("status") is None:
            return False, "null:status"
        if not isinstance(data.get("status"), str):
            return False, "invalid_type:status"
        if data.get("status") not in ("Active", "Resolved"):
            return False, "invalid_value:status"

    if "severity" in data:
        if data.get("severity") is None:
            return False, "null:severity"
        if not isinstance(data.get("severity"), str):
            return False, "invalid_type:severity"
        if data.get("severity").strip() == "":
            return False, "empty:severity"

    if "notes" in data:
        if data.get("notes") is None:
            return False, "null:notes"
        if not isinstance(data.get("notes"), str):
            return False, "invalid_type:notes"
        if data.get("notes").strip() == "":
            return False, "empty:notes"

    return True, None
