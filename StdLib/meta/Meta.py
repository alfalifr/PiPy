#from meta.MetaInspectable import MetaInspectable


META_ARGS_NAME = "meta_args"
META_KWARGS_NAME = "meta_kwargs"
INSPECTABLE_PROP_NAME = "__meta_inspectable__"
INSPECTABLE_META_PROP_NAME = "__meta_meta_inspectable__"
INSPECTABLE_META_RETENTION_PROP_NAME = "__meta_retention__"
INSPECTABLE_META_TARGET_PROP_NAME = "__meta_target__"
CLASS_INSPECTABLE_MARK = "__has_ispectable__"


def target(meta) -> int:
    try: return meta.__dict__[INSPECTABLE_META_TARGET_PROP_NAME]
    except AttributeError: raise TypeError(f"""Param "meta" harus berupa MetaInspectable.""")
