import inspect
import sys
from typing import List, Dict, Any, Optional, Callable

from exception.IllegalAccessExc import IllegalAccessExc
from foundation.wrapper.Wrapper import Wrapper
from log.logs import prind
from meta.Annotation import Annotation
from meta.metameta.Target import Target
from reflex.BoundedFun import boundedFun
from reflex.Reflex import callerClassName, callerClass, isSubclassOf, qualName, callerFile
from val.generic import T


@Target(Target.FUNCTION, Target.CLASS)  # Sementara untuk fungsi
class Private(Annotation):
    _bound = None

    def _checkScope(this):
        prind(f"this._bound={this._bound} callerClassName(2, False)={callerClassName(2, False)} this.content={this.content}")
        #currentCallerIndex = 2
        currentCaller = callerClass(2, False)

        prind(f"Private._checkScope(). AWAL currentCaller = {currentCaller} isinstance(currentCaller, Wrapper) = {isinstance(currentCaller, Wrapper)}")

        #if not currentCaller:  # Jika currentCaller `None`, kemungkinan yang memanggil adalah modul __main__. Oleh karena itu, kurangi kedalaman stack.
            #currentCaller = callerClass(1, False)
        if isinstance(currentCaller, Wrapper):  # Jika [currentCaller] merupakan instance `Wrapper`, maka unpack content-nya.
            currentCaller = currentCaller.content
        elif isinstance(currentCaller, type) and isSubclassOf(currentCaller, Wrapper):  # Jika merupakan kelas dan merupakan turunan dari `Wrapper`, maka tambah ke dalaman stack karena stack bertambah karena kehadiran Wrapper.
            currentCaller = callerClass(3, False)
            if isinstance(currentCaller, Wrapper):  # Jika [currentCaller] merupakan instance `Wrapper`, maka unpack content-nya.
                currentCaller = currentCaller.content

        #iis = contentStr(inspect.stack(6), sep='\n')
        #prind(f"Private._checkScope inspect.stack(6)={iis} \ncurrentCaller={currentCaller} currentCaller3={currentCaller3}")

        currentCallerName = qualName(currentCaller) if currentCaller else callerFile(2)

        prind(f"Private._checkScope(). AKHIR currentCaller = {currentCaller} this._bound = {this._bound} currentCallerName = {currentCallerName}")

        if this._bound != currentCallerName:
            locType = "kelas" if this._isInClass else "file"
            raise IllegalAccessExc(f"Property `{this._propName[1:]}` private dan tidak boleh diakses dari luar {locType} `{this._bound}` (dari {'kelas '+currentCaller if currentCaller else 'file '+currentCallerName})")  #{currentCallerName}

    def __init__(this, content: Optional[T] = None) -> None:
        super().__init__(content)
        callerName = callerClassName(1, False)
        this._bound = callerName if callerName else callerFile(1)
        if not callerName:
            this.__set_name__(None, content.__name__)
        this._isInClass = callerName is not None
        #print(f"__init__ this._bound={this._bound}")
        this._propContent = content

    def __set_name__(this, owner: Optional[any], name: str):
        this._propName = "_" + name

    def __get__(this, obj, objType: type = None):
        this._checkScope()
        try: return getattr(obj, this._propName)
        except AttributeError:
            savedContent = boundedFun(obj, this._propContent) \
                if isinstance(this._propContent, Callable) \
                else this._propContent
            this.__set__(obj, savedContent)
            return savedContent

    def __set__(this, obj, value):
        this._checkScope()
        return setattr(obj, this._propName, value)

    def __call__(this, inspectedUnit=None, *args, **kwargs):
        this._checkScope()
        return super().__call__(inspectedUnit, *args, **kwargs)

    """
    def __getattribute__(this, obj, *args, **kwargs): # real signature unknown
        print(f"Private.__getattribute__().obj={obj}")
        return getattr(obj, this._propContent)

    def __setattr__(this, obj, value): # real signature unknown
        return setattr(obj, this._propContent, value)
    """

    def isImplementationValid(
        this,
        inspectedCls: type,
        supers: List[type],
        immediateSubclasses: List[type],
        inspectedUnit: Dict[str, Any]
    ) -> bool:
        return True  # Karena @Private hanya digunakan saat runtime di luar konteks kelas.

    """
    def __getattr__(this=None, *var):
        print(f"var={var}")
        setattr()
        return "this.prop" if this else 10
    """
