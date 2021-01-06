from abc import abstractmethod
from typing import Generic

from collection.iterator.Iterator import Iterator, iteratorOf
from val.generic import In, Out
from collection.List import List


class NestedIterator(Generic[In, Out], Iterator[Out]):
    @abstractmethod
    def getOutputIterator(this, nowInput: In): pass
    @abstractmethod
    def getInputIterator(this, nowOutput: Out): pass

#TODO
class NestedIteratorImpl(NestedIterator[In, Out]):
    _startInputIterator: Iterator[In] = None
    _start: In = None

    _activeOutputLines: List[Iterator[Out]]
    _activeInputLines: List[Iterator[In]]
    _activeOutputIterator: Iterator[Out] = None
    _activeInputIterator: Iterator[In] = None
    _hasInited: bool
    _nextState: int = -1  # -1 blum diketahui, 0 tidak ada lagi iterasi, 1 lanjut.
    _nowOutput: Out = None

    def _getNextInputIterator(this, out: Out) -> bool:
        inItr = this.getInputIterator(out)
        if inItr is not None and inItr.hasNext():
            this.addInputIterator(inItr)
            return True
        else: return False

    def _addInputIterator(this, inItr: Iterator[In]):
        this._activeInputLines.append(inItr)
        this._activeInputIterator = inItr

    def _getNextOutputIterator(this, inn: Out) -> bool:
        outItr = this.getOutputIterator(inn)
        if outItr is not None and outItr.hasNext():
            this.addOutputIterator(outItr)
            return True
        else: return False

    def _addOutputIterator(this, outItr: Iterator[Out]):
        this._activeOutputLines.append(outItr)
        this._activeOutputIterator = outItr


    def _getOutputFromInput(this) -> bool:
        while this._hasNextInput() and not this._getNextOutputIterator(this._activeInputIterator.next()): pass
        return this._hasNextOutput()

    def _hasNextInput(this) -> bool:
        if this._activeInputIterator is not None:
            while this._activeInputIterator.hasNext() and this._activeInputLines.size > 1:
                this._changeLastActiveInputIterator(this._activeInputIterator)
        else: return False
        return this._activeInputIterator.hasNext()

    def _changeLastActiveInputIterator(this, currentActiveInputIterator: Iterator[In]):
        this._activeInputLines.remove(currentActiveInputIterator)
        this._activeInputIterator = this._activeInputLines.last

    def _hasNextOutput(this) -> bool:
        if this._activeOutputIterator is not None:
            while this._activeOutputIterator.hasNext() and this._activeOutputLines.size > 1:
                this._changeLastActiveOutputIterator(this._activeOutputIterator)
        else: return False
        return this._activeOutputIterator.hasNext()

    def _changeLastActiveOutputIterator(this, currentActiveOutputIterator: Iterator[Out]):
        this._activeOutputLines.remove(currentActiveOutputIterator)
        this._activeOutputIterator = this._activeOutputLines.last

    def _initActiveIterator(this) -> bool:
        itr = this._startInputIterator
        if itr is None:
            if this._start is not None:
                itr = iteratorOf(this._start)

        this._startInputIterator = itr

        if itr.hasNext():
            this._addInputIterator(itr)

            if not this._hasNextOutput():
                return this._getOutputFromInput()
            else: return True
        else: return False
