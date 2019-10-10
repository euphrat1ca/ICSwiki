

class NumberBasic():

    def __add__(self, *args, **kwargs):
        try:
            return self.internal_data.__add__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __mul__(self, *args, **kwargs):
        try:
            return self.internal_data.__mul__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __matmul__(self, *args, **kwargs):
        try:
            return self.internal_data.__matmul__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __truediv__(self, *args, **kwargs):
        try:
            return self.internal_data.__truediv__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __floordiv__(self, *args, **kwargs):
        try:
            return self.internal_data.__floordiv__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __mod__(self, *args, **kwargs):
        try:
            return self.internal_data.__mod__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __divmod__(self, *args, **kwargs):
        try:
            return self.internal_data.__divmod__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __pow__(self, *args, **kwargs):
        try:
            return self.internal_data.__pow__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __lshift__(self, *args, **kwargs):
        try:
            return self.internal_data.__lshift__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rshift__(self, *args, **kwargs):
        try:
            return self.internal_data.__rshift__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __and__(self, *args, **kwargs):
        try:
            return self.internal_data.__and__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __xor__(self, *args, **kwargs):
        try:
            return self.internal_data.__xor__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __or__(self, *args, **kwargs):
        try:
            return self.internal_data.__or__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __iadd__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__add__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __isub__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__sub__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __imul__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__mul__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __imatmul__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__matmul__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __itruediv__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__truediv__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __ifloordiv__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__floordiv__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __imod__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__mod__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __ipow__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__pow__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __ilshift__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__lshift__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __irshift__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__rshift__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __iand__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__and__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __ixor__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__xor__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

    def __ior__(self, *args, **kwargs):
        try:
            self.internal_data = self.internal_data.__or__(*args, **kwargs)
            return self
        except:
            raise NotImplementedError

class NumberRight():

    def __radd__(self, *args, **kwargs):
        try:
            return self.internal_data.__radd__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rsub__(self, *args, **kwargs):
        try:
            return self.internal_data.__rsub__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rmul__(self, *args, **kwargs):
        try:
            return self.internal_data.__rmul__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rmatmul__(self, *args, **kwargs):
        try:
            return self.internal_data.__rmatmul__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rtruediv__(self, *args, **kwargs):
        try:
            return self.internal_data.__rtruediv__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rfloordiv__(self, *args, **kwargs):
        try:
            return self.internal_data.__rfloordiv__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rmod__(self, *args, **kwargs):
        try:
            return self.internal_data.__rmod__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rdivmod__(self, *args, **kwargs):
        try:
            return self.internal_data.__rdivmod__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rpow__(self, *args, **kwargs):
        try:
            return self.internal_data.__rpow__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rlshift__(self, *args, **kwargs):
        try:
            return self.internal_data.__rlshift__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rrshift__(self, *args, **kwargs):
        try:
            return self.internal_data.__rrshift__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rand__(self, *args, **kwargs):
        try:
            return self.internal_data.__rand__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __rxor__(self, *args, **kwargs):
        try:
            return self.internal_data.__rxor__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __ror__(self, *args, **kwargs):
        try:
            return self.internal_data.__ror__(*args, **kwargs)
        except:
            raise NotImplementedError

class NumberMag():

    def __neg__(self, *args, **kwargs):
        try:
            return self.internal_data.__neg__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __pos__(self, *args, **kwargs):
        try:
            return self.internal_data.__pos__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __abs__(self, *args, **kwargs):
        try:
            return self.internal_data.__abs__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __invert__(self, *args, **kwargs):
        try:
            return self.internal_data.__invert__(*args, **kwargs)
        except:
            raise NotImplementedError

class NumberComplex():
    def __complex__(self, *args, **kwargs):
        try:
            return self.internal_data.__complex__(*args, **kwargs)
        except:
            raise NotImplementedError

class NumberInt():
    def __int__(self, *args, **kwargs):
        try:
            return self.internal_data.__int__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __index__(self, *args, **kwargs):
        try:
            return self.internal_data.__index__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __hash__(self):
        return self.internal_data.__hash__()

class NumberFloat():
    def __float__(self, *args, **kwargs):
        try:
            return self.internal_data.__float__(*args, **kwargs)
        except:
            raise NotImplementedError

class NumberRound():
    def __round__(self, *args, **kwargs):
        try:
            return self.internal_data.__round__(*args, **kwargs)
        except:
            raise NotImplementedError

class NumberIndex():
    def __index__(self, *args, **kwargs):
        try:
            return self.internal_data.__index__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __hash__(self):
        return self.internal_data.__hash__()

class NumberComp():
    def __lt__(self, *args, **kwargs):
        try:
            return self.internal_data.__lt__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __le__(self, *args, **kwargs):
        try:
            return self.internal_data.__le__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __eq__(self, *args, **kwargs):
        try:
            return self.internal_data.__eq__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __ne__(self, *args, **kwargs):
        try:
            return self.internal_data.__ne__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __gt__(self, *args, **kwargs):
        try:
            return self.internal_data.__gt__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __ge__(self, *args, **kwargs):
        try:
            return self.internal_data.__ge__(*args, **kwargs)
        except:
            raise NotImplementedError

    def __bool__(self):
        try:
            return self.internal_data.__bool__()
        except:
            raise NotImplementedError





