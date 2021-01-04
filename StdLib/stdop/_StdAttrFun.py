import inspect
import logging


def copyMember(fromObj, toObj, predicate = None):
    for name, member in inspect.getmembers(fromObj, predicate):
        #print(f"name= {name} member= {member}")
        try: setattr(toObj, name, member)
        except:
            toObjStr = "<toObj>"
            try:
                try: toObjStr = toObj.__class__
                except: toObjStr = toObj.__str__()
            except: pass
            try: logging.warning(f"copyMember() ({fromObj} -> {toObjStr}): Tidak dapat men-copy member: \"{name} : {member}\".")
            except: pass
